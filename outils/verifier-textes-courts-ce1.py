"""Contrôle les textes courts du CE1 — le corpus que les exercices citent.

Un texte court n'est pas un texte du palier. Il fait de deux à six lignes de 34
signes, il est porté par un exercice, et il ne se relit pas seul. Mais il doit
être un TEXTE — avec un rang, un type et un titre — sans quoi il n'existe que
dans le corps d'un exercice, où rien ne le voit.

CE QUI EST REFUSÉ ICI, ET POURQUOI

  - un texte illisible au rang qu'il déclare. La règle du palier vaut aussi pour
    un texte court : un texte qu'on ne peut pas encore lire n'est pas un texte.
  - une longueur hors de deux à six lignes de 34 signes.
  - un type inconnu. C'est le type qui rend vérifiable la réponse d'un exercice
    qui demande de distinguer un récit d'un documentaire : sans lui, la clé de
    réponse ne se compare à rien.
  - un titre égal à celui d'un texte du palier, ou qui le CONTIENT. Un enfant qui
    a lu « Le vent » au rang 3 et rencontre un autre « Le vent » ne peut pas
    savoir de quel texte on parle — et c'est exactement la confusion que l'unité
    16 demande de lever.
  - une phrase qui est DÉJÀ une ligne d'un texte du palier, ou qui est déjà dans
    un autre texte court. Deux copies d'un même texte divergent : c'est mesuré,
    pas supposé — cinq phrases des textes courts étaient des lignes des textes du
    palier, et deux exercices partageaient trois phrases sans que rien ne le dise.
  - deux textes courts qui partagent une phrase.

CE QUI N'EST PAS VÉRIFIÉ, et il faut le dire : l'intérêt du texte, et le fait que
son type déclaré soit le bon. Le contrôle lit le type, il ne juge pas le texte.
Le fait qu'un texte soit EMPLOYÉ par un exercice se contrôle de l'autre côté, par
`verifier-exercices.py --ce1`, qui lit la banque.

Usage :
    python verifier-textes-courts-ce1.py
"""

import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
COURTS = RACINE / "contenu" / "textes-courts-ce1"
TEXTES = RACINE / "contenu" / "textes-ce1"

# Le type d'un texte court, liste FERMÉE. Un type libre ne se comparerait à rien.
TYPES = ("recit", "informatif", "prescriptif")

MIN_LIGNES = 2
MAX_LIGNES = 6

CLEF = re.compile(r"^#\s*([a-z_]+)\s*:\s*(.*)$")


def charger_module(nom):
    spec = importlib.util.spec_from_file_location(nom.replace(".py", "").replace("-", "_"),
                                                  ICI / nom)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VC = charger_module("verifier-textes-ce1.py")


def normaliser(texte):
    """Minuscules, sans accent, sans ponctuation — pour comparer des titres et
    des phrases. La ponctuation est retirée : « L'air qui va » et « l air qui va »
    sont le même titre, et une virgule ne fait pas deux textes."""
    t = unicodedata.normalize("NFD", texte.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def analyser(contenu):
    """Rend (meta, titre, lignes écrites).

    Le titre se déclare de deux façons, et le contrôle accepte les deux : par une
    ligne `# titre: ...` (les textes courts, qui portent d'autres métadonnées), ou
    par une ligne `# ...` nue (les textes du palier, qui n'ont qu'un titre).
    """
    meta, titre, lignes = {}, None, []
    for brute in contenu.splitlines():
        ligne = brute.strip()
        if not ligne:
            continue
        if ligne.startswith("#"):
            m = CLEF.match(ligne)
            if m:
                meta[m.group(1)] = m.group(2).strip()
            elif titre is None:
                titre = ligne.lstrip("#").strip()
            continue
        lignes.append(ligne)
    titre = meta.pop("titre", None) or titre
    return meta, titre, lignes


def lire_paliers():
    """Les textes du palier : leurs titres, et toutes leurs phrases."""
    titres, phrases = {}, {}
    for chemin in sorted(TEXTES.glob("*.txt")):
        contenu = chemin.read_text(encoding="utf-8")
        _, titre, lignes = analyser(contenu)
        if titre:
            titres.setdefault(normaliser(titre), []).append(chemin.stem)
        for ligne in lignes:
            phrases.setdefault(normaliser(ligne), []).append(chemin.stem)
    return titres, phrases


def lire_courts():
    textes = {}
    for chemin in sorted(COURTS.glob("*.txt")):
        contenu = chemin.read_text(encoding="utf-8")
        meta, titre, lignes = analyser(contenu)
        textes[chemin.stem] = {"chemin": chemin, "meta": meta, "titre": titre,
                               "lignes": lignes, "contenu": contenu}
    return textes


def controler_court(nom, t, cp, ce1):
    """Un texte court tient debout seul : rang, type, titre, longueur, lisibilité."""
    erreurs, limites = [], []
    meta = t["meta"]

    rang = meta.get("rang")
    if rang is None or not rang.isdigit():
        erreurs.append(f"{nom} : aucun rang déclaré (`# rang: N`)")
        rang = None
    else:
        rang = int(rang)

    type_ = meta.get("type")
    if not type_:
        erreurs.append(f"{nom} : aucun type déclaré (`# type: ...`) — sans lui la "
                       f"clé de réponse d'un exercice de distinction ne se compare à rien")
    elif type_ not in TYPES:
        erreurs.append(f"{nom} : type « {type_} » inconnu — la liste est fermée : {list(TYPES)}")

    if not t["titre"]:
        erreurs.append(f"{nom} : aucun titre (`# titre: ...`)")

    if not t["lignes"]:
        erreurs.append(f"{nom} : le fichier ne contient aucun texte")

    lignes_pliees = VC.lignes_du_texte(t["contenu"])
    if not MIN_LIGNES <= len(lignes_pliees) <= MAX_LIGNES:
        erreurs.append(
            f"{nom} : {len(lignes_pliees)} lignes de {VC.LARGEUR_LIGNE} signes — un texte "
            f"court va de {MIN_LIGNES} à {MAX_LIGNES} lignes"
        )

    if rang is not None:
        autorisees = VC.cgp_autorisees(cp, ce1, rang)
        ecartes = VC.mots_ecartes(cp, ce1, rang)
        prononcees = VC.exceptions_prononcees(ce1)
        sans_son = VC.lettres_sans_son(ce1)
        ent_nasal = VC.mots_en_ent_nasal(ce1)
        declarees = VC.correspondances_declarees(ce1)
        for mot in sorted({m.lower() for m in VC._vt.extraire_mots(t["contenu"])}):
            if mot in ecartes:
                continue
            problemes, inconnus = VC.controler_mot(mot, rang, autorisees, prononcees,
                                                   sans_son, ent_nasal, declarees)
            for _, g, raison in problemes:
                erreurs.append(f"{nom} : « {mot} » illisible au rang {rang} ({raison})")
            for _, g, raison in inconnus:
                # Une découpe non classée n'est pas une faute : le décodeur dit
                # où il s'arrête, et c'est ici qu'on le rapporte.
                limites.append(f"{nom} : « {mot} » au rang {rang} — {raison}")
    return rang, type_, erreurs, limites


def main():
    cp, ce1, _ = VC.charger_tables()
    titres_paliers, phrases_paliers = lire_paliers()
    courts = lire_courts()

    erreurs, limites = [], []

    if not courts:
        print(f"Aucun texte court dans {COURTS} — le corpus est vide.")
        return 1

    titres_courts, phrases_courts = {}, {}
    for nom, t in courts.items():
        rang, type_, e, l = controler_court(nom, t, cp, ce1)
        erreurs += e
        limites += l
        t["rang"], t["type"] = rang, type_

        if t["titre"]:
            cle = normaliser(t["titre"])
            titres_courts.setdefault(cle, []).append(nom)
            for cle_palier, noms in titres_paliers.items():
                if cle == cle_palier or cle_palier in cle:
                    erreurs.append(
                        f"{nom} : le titre « {t['titre']} » reprend celui d'un texte du "
                        f"palier ({', '.join(noms)}) — deux textes du même nom ne se "
                        f"distinguent pas"
                    )
        for ligne in t["lignes"]:
            cle = normaliser(ligne)
            phrases_courts.setdefault(cle, []).append(nom)
            if cle in phrases_paliers:
                erreurs.append(
                    f"{nom} : « {ligne} » est déjà une ligne de "
                    f"{', '.join(phrases_paliers[cle])} — un texte court ne recopie pas un "
                    f"texte du palier"
                )

    for cle, noms in sorted(phrases_courts.items()):
        if len(set(noms)) > 1:
            erreurs.append(
                f"{', '.join(sorted(set(noms)))} : la phrase « {cle} » est dans deux textes "
                f"courts — deux copies d'un même texte divergent"
            )
    for cle, noms in sorted(titres_courts.items()):
        if len(set(noms)) > 1:
            erreurs.append(f"{', '.join(sorted(set(noms)))} : deux textes courts portent le titre « {cle} »")

    print(f"Textes courts       : {len(courts)} dans contenu/textes-courts-ce1")
    for nom, t in sorted(courts.items()):
        pliees = len(VC.lignes_du_texte(t["contenu"]))
        rang = "?" if t["rang"] is None else str(t["rang"])
        print(f"  {nom:16s} rang {rang:>2}  {t['type'] or '?':11s} "
              f"{pliees} lignes  « {t['titre']} »")
    print(f"Types déclarés      : {sorted({t['type'] for t in courts.values() if t['type']})}")

    if limites:
        print(f"\nOÙ LE CONTRÔLE S'ARRÊTE — {len(limites)} segment(s) non classé(s) :")
        for l in limites:
            print(f"  {l}")

    if erreurs:
        print(f"\nNON CONFORME — {len(erreurs)} problème(s) :")
        for e in erreurs:
            print(f"  {e}")
        return 1
    print("\nRésultat : conforme")
    return 0


if __name__ == "__main__":
    sys.exit(main())
