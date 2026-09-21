"""Contrôle de conformité d'un texte de lecture de Ludo'Lire.

Un texte n'est lisible par l'enfant que si chacun de ses graphèmes a déjà été
enseigné au rang considéré. Cette règle ne se contrôle pas à l'oeil : elle se
contrôle par segmentation.

Usage :
    python verifier-textes.py --rang 7 contenu/textes/T01-rang07.txt
    python verifier-textes.py --rang 7 --mots contenu/textes/T01-rang07.txt

Sortie : 0 si le texte est conforme, 1 sinon. Le script dit toujours où il
s'arrête : tout caractère qu'il ne sait pas classer est signalé, jamais ignoré.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ICI = Path(__file__).resolve().parent
DONNEES = ICI / "cgp-cp.json"

# Graphèmes candidats, du plus long au plus court. La segmentation est gloutonne.
GRAPHEMES = [
    "eau", "ain", "ein", "oin", "ill",
    "ch", "ou", "oi", "on", "om", "an", "am", "en", "em", "in", "im",
    "au", "ai", "ei", "eu", "œu", "gn", "ph", "qu", "gu",
    "ss", "ll", "mm", "nn", "pp", "tt", "rr", "bb", "dd", "ff", "cc",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ç",
]
GRAPHEMES.sort(key=len, reverse=True)

# Graphèmes dont la valeur dépend du contexte : ils sont résolus plus bas.
CONTEXTUELS = {"c", "g", "s", "qu", "gu", "ge", "cc"}

# CGP sans ambiguïté de valeur.
CGP_SIMPLE = {
    "ch": "ch", "ou": "ou", "oi": "oi",
    "on": "on", "om": "on", "an": "an", "am": "an",
    "in": "in", "im": "in", "ain": "ain", "ein": "ain",
    "eu": "eu", "œu": "eu", "au": "au", "eau": "au",
    "a": "a", "i": "i", "o": "o", "u": "u", "e": "e",
    "l": "l", "m": "m", "r": "r", "n": "n", "v": "v",
    "p": "p", "t": "t", "f": "f", "d": "d", "b": "b",
    "j": "j", "z": "s-sonore",
}

# Voyelles accentuées : même phonème, marque orthographique supplémentaire.
VOYELLES_ACCENTUEES = {
    "à": ("a", "accent"), "â": ("a", "accent"),
    "è": ("e", "accent"), "ê": ("e", "accent"), "ë": ("e", "accent"),
    "î": ("i", "accent"), "ï": ("i", "accent"),
    "ô": ("o", "accent"),
    "û": ("u", "accent"), "ù": ("u", "accent"),
    "é": ("e-aigu", None),
}

# Consonnes doublées : on retient le phonème de la lettre simple, en le signalant.
DOUBLEES = {
    "ll": ("l", "double:ll"), "mm": ("m", "double:mm"), "nn": ("n", "double:nn"),
    "pp": ("p", "double:pp"), "tt": ("t", "double:tt"), "rr": ("r", "double:rr"),
    "bb": ("b", "double:bb"), "dd": ("d", "double:dd"), "ff": ("f", "double:ff"),
}

VOYELLES = set("aeiouyàâäéèêëîïôöûüù")

NASALES_EN_N = {"an", "en", "in", "on"}
NASALES_EN_M = {"am", "em", "im", "om"}

# Lettres finales muettes, avec le rang à partir duquel la règle est admise.
MUETTES_FINALES = {"e": 3, "s": 11, "t": 12, "d": 12, "x": 12}

# Mots où une lettre muette se prononce : le contrôle ne les tranche pas seul.
MOTS_PIEGES = {"sens", "ours", "fils", "mars", "os", "sept", "dix"}

# Terminaison -ent : refusée dans toute la tranche CP.
#
# Le morphème -ent d'un verbe (« ils dorment ») n'est pas un /e/ suivi d'un /t/,
# c'est une terminaison muette ; et dans un nom (« dent », « vent ») c'est une
# nasale suivie d'un t muet. Dans les deux cas la segmentation lit de travers, et
# l'enfant de CP n'a la règle ni dans un cas ni dans l'autre. Décision du
# 21 septembre 2026 : la terminaison est interdite, sans exception.
#
# La liste blanche existe pour mémoire. Y ajouter un mot est une décision
# pédagogique, pas un ajustement technique : aucun nom en -ent n'est déchiffrable
# avant le rang 30 de toute façon.
MOTS_ENT_AUTORISES = frozenset()
TERMINAISON_ENT = re.compile(r"ent$")

PONCTUATION = set(".,;:!?…«»\"'()[]—–-’/0123456789 ")


def charger():
    with DONNEES.open(encoding="utf-8") as f:
        return json.load(f)


def cgp_autorisees(donnees, rang):
    """Identifiants de CGP enseignées jusqu'au rang demandé inclus."""
    autorisees = set()
    for u in donnees["unites"]:
        if u["rang"] <= rang:
            autorisees.update(u["cgp"])
    return autorisees


def rang_regle_muette(lettre):
    """Rang minimal auquel la règle rendant cette lettre finale muette est admise."""
    return MUETTES_FINALES.get(lettre)


def indices_muets_finaux(mot, morceaux):
    """Indices de la queue muette finale, en raisonnant sur les graphèmes.

    Une lettre finale muette peut en cacher une autre : dans « pattes », le e
    et le s sont muets tous les deux. Mais la queue s'arrête au premier
    graphème de plus d'une lettre : dans « patte », le premier t appartient au
    digramme tt et n'est pas une lettre finale muette. Le e final n'est muet
    que s'il y a une voyelle avant lui — sans quoi « de » serait analysé sans
    voyelle.

    LA QUEUE NE VA PAS JUSQU'À LA PREMIÈRE LETTRE. Une consonne en tête de mot
    est une ATTAQUE : elle se prononce toujours, et un mot ne peut pas être
    entièrement muet. Sans cette condition, les formes élidées étaient lues de
    travers — `d'un`, `s'il`, `t'` : la découpe jette l'apostrophe, et `d`, `s`,
    `t` arrivaient au contrôle comme des mots d'une lettre dont la consonne
    finale serait muette. Accepté, mais mal lu — le sens d'erreur le plus
    dangereux, et le même défaut que celui corrigé au CE1.
    """
    muets = set()
    i = len(morceaux) - 1
    while i >= 0:
        g, debut, fin = morceaux[i]
        if len(g) != 1 or g not in MUETTES_FINALES or debut == 0:
            break
        if g == "e" and not any(c in VOYELLES for c in mot[:debut]):
            break
        muets.add(i)
        i -= 1
    return muets


def valide(g, mot, i):
    """Un digramme nasal ne l'est que dans son contexte.

    « an », « en », « in », « on » sont nasaux devant une consonne autre que n,
    et ne le sont pas devant une voyelle ni devant n — sinon « liane » serait lu
    « li-ane » et « année » serait nasal. « am », « em », « im », « om » ne sont
    nasaux que devant m, p ou b : « tomate » n'est pas nasal, « pomme » l'est.

    En fin de mot, le digramme EST nasal : « son », « bon », « nom » se
    terminent par une voyelle nasale, pas par une voyelle suivie d'une nasale.
    Traiter la fin de mot comme un contexte non nasal faisait passer « son » au
    rang 20 alors que la CGP « on » n'est enseignée qu'au rang 21 — le contrôle
    acceptait à tort, ce qui est le sens d'erreur le plus dangereux.
    """
    if g in NASALES_EN_N:
        suivant = mot[i + 2] if i + 2 < len(mot) else None
        if suivant is None:
            return True
        if suivant in VOYELLES or suivant == "n":
            return False
        return True
    if g in NASALES_EN_M:
        suivant = mot[i + 2] if i + 2 < len(mot) else None
        if suivant is None:
            return True
        # Un m doublé n'est PAS un contexte nasal : dans « pomme », « homme »,
        # « somme », le digramme nasal est suivi du second m de la double, et la
        # voyelle n'est pas nasale — /pɔm/, /ɔm/, /sɔm/. Sans cette garde, la
        # découpe lisait « p | om | m | e », c'est-à-dire /pɔ̃m/, un mot qui
        # n'existe pas. C'est le sens d'erreur le plus dangereux : le contrôle
        # ACCEPTAIT à tort, et il acceptait « pomme » au CP, où mm n'est pas
        # enseigné du tout.
        #
        # La garde symétrique existe déjà pour les nasales en n (« bonne »,
        # « année ») ; celle-ci manquait, et rien ne le signalait parce que les
        # deux cas ne se ressemblent pas à la lecture.
        if suivant == "m":
            return False
        if suivant not in "mpb":
            return False
        return True
    return True


def decouper(mot):
    """Découpe un mot en graphèmes, du plus long au plus court."""
    morceaux = []
    i = 0
    while i < len(mot):
        for g in GRAPHEMES:
            if mot.startswith(g, i) and valide(g, mot, i):
                morceaux.append((g, i, i + len(g)))
                i += len(g)
                break
        else:
            morceaux.append((mot[i], i, i + 1))
            i += 1
    return morceaux


def resoudre(mot, morceaux, index, donnees, rang):
    """Rend (identifiant de CGP, drapeaux) pour un graphème, ou (None, [raison])."""
    g, debut, fin = morceaux[index]
    suivant = mot[fin] if fin < len(mot) else ""
    precedent = mot[debut - 1] if debut > 0 else ""
    drapeaux = []

    if g in VOYELLES_ACCENTUEES:
        cgp, marque = VOYELLES_ACCENTUEES[g]
        if marque:
            drapeaux.append("accent")
        return cgp, drapeaux

    if g in DOUBLEES:
        cgp, marque = DOUBLEES[g]
        drapeaux.append(marque)
        return cgp, drapeaux

    if g == "ss":
        return "s-sourd", ["double:ss"]

    if g == "c":
        if suivant in "eiéèê":
            return "c-doux", drapeaux
        return "c-dur", drapeaux

    if g == "qu":
        return "c-dur", ["graphie:qu"]

    if g == "g":
        if suivant in "eiéèê":
            return "g-doux", drapeaux
        return "g-dur", drapeaux

    if g == "gu":
        return "g-dur", ["graphie:gu"]

    if g == "ge":
        return "j", ["graphie:ge"]

    if g == "s":
        if precedent in VOYELLES and suivant in VOYELLES:
            return "s-sonore", ["contexte:entre-deux-voyelles"]
        return "s-sourd", drapeaux

    if g == "cc":
        return None, ["double consonne non tranchée par le contrôle"]

    if g in CGP_SIMPLE:
        return CGP_SIMPLE[g], drapeaux

    return None, ["graphème non enseigné dans la tranche"]


def controler_mot(mot, donnees, rang, autorisees):
    """Rend (problemes, inconnus) pour un mot."""
    problemes = []
    inconnus = []

    # La terminaison -ent est refusée avant toute analyse, et le diagnostic
    # s'arrête là pour ce mot. Les autres remarques porteraient sur une
    # segmentation que la terminaison rend fausse de toute façon, et un refus
    # n'est probant que si l'on sait sur quoi il porte.
    if TERMINAISON_ENT.search(mot) and mot not in MOTS_ENT_AUTORISES:
        problemes.append(
            (
                mot,
                "-ent",
                "terminaison -ent interdite dans la tranche CP "
                "(morphème muet, ou nasale suivie d'un t muet)",
            )
        )
        return problemes, inconnus

    morceaux = decouper(mot)
    muets = indices_muets_finaux(mot, morceaux)
    for i, (g, debut, fin) in enumerate(morceaux):
        if i in muets:
            seuil = rang_regle_muette(g)
            if seuil is None:
                inconnus.append((mot, g, "lettre finale muette sans règle déclarée"))
            elif rang < seuil:
                problemes.append((mot, g, f"lettre finale muette admise à partir du rang {seuil}"))
            continue
        cgp, drapeaux = resoudre(mot, morceaux, i, donnees, rang)
        if cgp is None:
            inconnus.append((mot, g, "; ".join(drapeaux)))
            continue
        if cgp not in autorisees:
            problemes.append((mot, g, f"CGP '{cgp}' non enseignée au rang {rang}"))
            continue
        if "accent" in drapeaux and rang < 6:
            problemes.append((mot, g, "accent admis à partir du rang 6"))
        for d in drapeaux:
            if d.startswith("double:") and rang < 14 and d not in ("double:ss",):
                problemes.append((mot, g, f"{d} admis à partir du rang 14"))
    return problemes, inconnus


def extraire_mots(texte):
    """Rend la liste des mots, apostrophes et traits d'union séparant les unités."""
    mots = []
    for ligne in texte.splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#"):
            continue
        for brut in re.split(r"[^\w\u00c0-\u017f]+", ligne, flags=re.UNICODE):
            brut = brut.strip()
            if not brut:
                continue
            brut = brut.lower()
            for partie in re.split(r"['’\-]", brut):
                if partie and any(c.isalpha() for c in partie):
                    mots.append(partie)
    return mots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier", type=Path)
    ap.add_argument("--rang", type=int, required=True)
    ap.add_argument("--mots", action="store_true", help="affiche la segmentation de chaque mot")
    args = ap.parse_args()

    donnees = charger()
    autorisees = cgp_autorisees(donnees, args.rang)
    memorises = {m["mot"] for m in donnees["mots_outils_memorises"] if m["rang"] <= args.rang}

    texte = args.fichier.read_text(encoding="utf-8")
    mots = extraire_mots(texte)

    problemes, inconnus, pieges, ecartes = [], [], [], []
    if args.mots:
        print("Segmentation :")
    for mot in mots:
        if mot in memorises:
            ecartes.append(mot)
            if args.mots:
                print(f"  {mot:14s} mot-outil mémorisé, hors contrôle")
            continue
        if mot in MOTS_PIEGES:
            pieges.append(mot)
        p, inc = controler_mot(mot, donnees, args.rang, autorisees)
        problemes.extend(p)
        inconnus.extend(inc)
        if args.mots:
            seg = " | ".join(g for g, _, _ in decouper(mot))
            print(f"  {mot:14s} {seg}")

    print(f"\nFichier        : {args.fichier}")
    print(f"Rang contrôlé  : {args.rang}")
    print(f"CGP autorisées : {len(autorisees)}")
    print(f"Mots examinés  : {len(mots)} (dont {len(ecartes)} mots-outils mémorisés)")
    print(f"Mots pièges    : {len(set(pieges))} (à vérifier à la main)")

    if problemes:
        print(f"\nNON CONFORME — {len(problemes)} problème(s) :")
        for mot, g, raison in problemes:
            print(f"  {mot:14s} « {g} »  {raison}")
    if inconnus:
        print(f"\nOÙ LE CONTRÔLE S'ARRÊTE — {len(inconnus)} segment(s) non classé(s) :")
        for mot, g, raison in inconnus:
            print(f"  {mot:14s} « {g} »  {raison}")

    if problemes or inconnus:
        print("\nRésultat : à corriger")
        return 1
    print("\nRésultat : conforme")
    return 0


if __name__ == "__main__":
    sys.exit(main())
