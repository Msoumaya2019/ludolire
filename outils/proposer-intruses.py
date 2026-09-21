"""Dérive les intruses du jeu de syllabes, et fige la banque.

Deux modes :

    python proposer-intruses.py            # imprime les candidats, n'écrit rien
    python proposer-intruses.py --figer    # réécrit les items de jeu-syllabes.json

Pourquoi ce détour. La banque a d'abord été écrite à la main, avec **une seule
intruse** par item : l'enfant avait une chance sur deux de tomber juste sans
rien discriminer. Passer à deux intruses demande, pour chaque mot, de trouver un
trou dont la syllabe cachée admette deux voisines — et cette recherche est un
calcul, pas un jugement. La faire à la main est précisément ce qui avait produit
la banque à une intruse.

Ce qui reste un jugement, et n'est donc pas calculé : le choix du trou gardé
quand plusieurs conviennent (on garde celui déjà écrit, pour que le changement
soit petit et relisible) et le contenu de `sert`, qui dit quelle unité de la
progression l'item sert. Ces deux valeurs sont donc **lues dans la banque
existante** et préservées.

Règles de voisinage appliquées :

  - une intruse CONSONANTIQUE partage la voyelle (et la coda) de la syllabe
    cachée, et n'en diffère que par la consonne d'attaque, prise dans une paire
    de consonnes proches ;
  - une intruse VOCALIQUE partage l'attaque et la coda, et n'en diffère que par
    la voyelle, prise dans une paire de voyelles proches ;
  - la paire `c`/`g` ne vaut que devant a, o, u (où `c` vaut /k/) ; `c`/`s` et
    `c`/`z` ne valent que devant e, i (où `c` vaut /s/) ; `g`/`j` devant e, i.
    C'est pourquoi la paire s'écrit en LETTRES : `c` n'est pas `k`.

Ce que ce script ne sait pas faire, et qu'il faut savoir : décider si le mot
reconstitué est un mot FRANÇAIS. `lune` avec l'intruse `ru` donne « rune », qui
existe. Le contrôle ne le voit pas. C'est le retour sonore qui le corrige —
l'enfant entend « rune » et non « lune » — mais c'est une limite à énoncer.
"""

import importlib.util
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent

# --- Le matériel phonologique -------------------------------------------------

# Attaques de deux lettres d'abord : la découpe est gloutonne.
ATTAQUES = [
    "ch", "ph", "gn",
    "pl", "bl", "cl", "fl", "gl", "cr", "br", "dr", "tr", "pr", "fr", "gr", "vr", "qu",
] + list("bcdfghjklmnpqrstvwxz")

VOYELLES = [
    "eau", "oeu", "ain", "ein", "oin", "ou", "on", "an", "in", "ei", "ai", "au",
    "eu", "oi", "ui",
] + list("aàâeéèêiîïoôuûùy")

# (membre A, membre B, voyelles pour lesquelles la paire vaut — None = toutes)
PAIRES_CONS = [
    ("p", "b", None), ("p", "m", None), ("b", "m", None), ("m", "n", None),
    ("f", "v", None), ("t", "d", None), ("t", "n", None), ("d", "n", None),
    ("s", "z", None), ("l", "n", None), ("l", "r", None),
    ("ch", "j", None), ("ch", "s", None), ("j", "z", None),
    ("c", "g", "aou"), ("g", "c", "aou"),
    ("c", "s", "ei"), ("s", "c", "ei"),
    ("c", "z", "ei"), ("z", "c", "ei"),
    ("g", "j", "ei"), ("j", "g", "ei"),
]

PAIRES_VOY = [
    ("a", "è"), ("a", "o"), ("i", "u"), ("o", "ou"),
    ("on", "an"), ("in", "an"), ("é", "è"), ("e", "é"), ("e", "è"),
]


def decouper(syllabe):
    """(attaque, voyelle, coda) — découpe gloutonne, voyelle la plus longue."""
    attaque = ""
    for a in sorted(ATTAQUES, key=len, reverse=True):
        if syllabe.startswith(a):
            attaque = a
            break
    reste = syllabe[len(attaque):]
    voyelle = ""
    for v in sorted(VOYELLES, key=len, reverse=True):
        if reste.startswith(v):
            voyelle = v
            break
    return attaque, voyelle, reste[len(voyelle):]


def _sans_doublon(candidats):
    """`a/è` et `è/a` désignent la même paire : on garde la première vue."""
    vus, sortie = set(), []
    for syllabe, paire in candidats:
        if syllabe in vus:
            continue
        vus.add(syllabe)
        sortie.append((syllabe, paire))
    return sortie


def voisines(syllabe, interdites):
    """(intruses consonantiques, intruses vocaliques) de `syllabe`."""
    attaque, voyelle, coda = decouper(syllabe)
    if not voyelle:
        return [], []

    premiere = voyelle[0]
    par_consonne, par_voyelle = [], []

    for a, b, condition in PAIRES_CONS:
        if condition is not None and premiere not in condition:
            continue
        if attaque == a:
            candidat = b + voyelle + coda
        elif attaque == b:
            candidat = a + voyelle + coda
        else:
            continue
        if candidat != syllabe and candidat not in interdites:
            par_consonne.append((candidat, f"{a}/{b}"))

    for a, b in PAIRES_VOY:
        if voyelle == a:
            candidat = attaque + b + coda
        elif voyelle == b:
            candidat = attaque + a + coda
        else:
            continue
        if candidat != syllabe and candidat not in interdites:
            par_voyelle.append((candidat, f"{a}/{b}"))

    return _sans_doublon(par_consonne), _sans_doublon(par_voyelle)


# --- Le choix, qui est une règle et non un goût -------------------------------

def candidates(syllabes, trou, accepte=None):
    """Les voisines du trou, séparées par sorte, restreintes par `accepte`.

    Deux raisons de refuser un candidat, et deux seulement.

    Le rendu ÉCRIT : au CP, une carte est une syllabe que l'enfant doit
    DÉCHIFFRER. Une intruse dont un graphème n'est pas encore enseigné au rang de
    l'item ne serait pas une carte difficile, ce serait une carte illisible — et
    l'item ne mesurerait plus rien. Les premières intruses dérivées ont fait
    exactement cette faute : `lama` au rang 10 recevait `pa` et `ba`, alors que ni
    `p` ni `b` ne sont enseignés à ce rang.

    La COLLISION : si le mot reconstitué est un mot français que l'enfant connaît
    déjà, il peut le tenir pour juste — la faute ne se voit plus. `poisson` avec
    l'intruse `bois` donne `boisson`. Ces mots sont listés dans
    `collisions-fr.json`, qui est incomplet par construction.
    """
    cons, voy = voisines(syllabes[trou], set(syllabes))
    if accepte is not None:
        cons = [(s, p) for s, p in cons if accepte(trou, s)]
        voy = [(s, p) for s, p in voy if accepte(trou, s)]
    return cons, voy


def choisir_trou(syllabes, trou_existant, accepte=None):
    """Le trou gardé : celui qui donne le plus de voisines consonantiques.

    La carte consonantique est la carte qui compte : c'est la consonne proche qui
    fait trébucher un lecteur débutant. On préfère donc un trou à deux voisines
    consonantiques plutôt qu'un trou à une consonantique et une vocalique. À
    égalité, on garde le trou déjà écrit — pour que la relecture du changement
    reste courte — et sinon le plus à droite, faute de mieux.
    """
    classables = []
    for i in range(len(syllabes)):
        cons, voy = candidates(syllabes, i, accepte)
        if len(cons) + len(voy) >= 2:
            classables.append((i, len(cons)))
    if not classables:
        return None
    return max(
        classables,
        key=lambda c: (c[1], 1 if c[0] == trou_existant else 0, c[0]),
    )[0]


def choisir_intruses(cons, voy):
    """Deux intruses : les consonantiques d'abord, les vocaliques en complément.

    La carte consonantique est celle qui compte — c'est la consonne proche qui
    fait trébucher un lecteur débutant. La vocalique est un complément, et non un
    équivalent : elle est plus facile à écarter. On la prend donc seulement
    quand la syllabe n'offre pas deux voisines consonantiques.
    """
    retenues = []
    for sorte, liste in (("consonne", cons), ("voyelle", voy)):
        for syllabe, paire in liste:
            if len(retenues) == 2:
                break
            if any(r["syllabe"] == syllabe for r in retenues):
                continue
            retenues.append({"syllabe": syllabe, "paire": paire, "sorte": sorte})
    return retenues


def reconstruire(syllabes, trou, intruse):
    """Le mot que donnerait l'intruse placée dans le trou."""
    return "".join(syllabes[:trou] + [intruse] + syllabes[trou + 1:])


def figer():
    spec = importlib.util.spec_from_file_location("verifier_textes", ICI / "verifier-textes.py")
    vt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vt)
    cgp = vt.charger()

    interdits = {
        c["mot"] for c in json.loads((ICI / "collisions-fr.json").read_text(encoding="utf-8"))["interdits"]
    }

    gs = json.loads((ICI / "mots-gs.json").read_text(encoding="utf-8"))["mots"]
    cp = json.loads((ICI / "mots-cp.json").read_text(encoding="utf-8"))["mots"]
    decoupes = {m["mot"]: m["syllabes"] for m in gs}
    decoupes.update({m["mot"]: m["syllabes"] for m in cp})

    chemin = ICI / "jeu-syllabes.json"
    banque = json.loads(chemin.read_text(encoding="utf-8"))

    changements, impossibles = [], []
    nouveaux = []
    for item in banque["items"]:
        mot = item["mot"]
        syllabes = decoupes[mot]
        rang_du_mot = item.get("rang")

        def accepte(trou, intruse, mot=mot, syllabes=syllabes, rang=None, autorisees=None):
            if reconstruire(syllabes, trou, intruse) in interdits:
                return False
            if rang is None:
                return True
            problemes, inconnus = vt.controler_mot(intruse, cgp, rang, autorisees)
            return not (problemes or inconnus)

        # Le rang d'un ITEM n'est pas celui de son mot : c'est celui de sa carte la
        # plus tardive. `poisson` se déchiffre au rang 21, mais aucune de ses deux
        # voisines n'y est déchiffrable — `an` n'arrive qu'au rang 22. Déclarer
        # l'item au rang 22 est la seule issue honnête : le mot reste déchiffrable,
        # les cartes aussi, et l'item ne mesure plus autre chose que ce qu'il croit.
        trou, cons, voy = None, [], []
        if rang_du_mot is None:
            trou = choisir_trou(syllabes, item.get("trou"), accepte)
            if trou is not None:
                cons, voy = candidates(syllabes, trou, accepte)
        else:
            for rang in range(rang_du_mot, rang_du_mot + 5):
                autorisees = vt.cgp_autorisees(cgp, rang)

                def accepte(trou, intruse, syllabes=syllabes, rang=rang, autorisees=autorisees):
                    if reconstruire(syllabes, trou, intruse) in interdits:
                        return False
                    problemes, inconnus = vt.controler_mot(intruse, cgp, rang, autorisees)
                    return not (problemes or inconnus)

                trou = choisir_trou(syllabes, item.get("trou"), accepte)
                if trou is None:
                    continue
                cons, voy = candidates(syllabes, trou, accepte)
                if len(cons) + len(voy) >= 2:
                    break

        if trou is None or len(cons) + len(voy) < 2:
            impossibles.append(f"{item['id']} {mot} : aucun trou à deux voisines")
            continue
        intruses = choisir_intruses(cons, voy)
        if len(intruses) != 2:
            impossibles.append(f"{item['id']} {mot} (trou {trou}) : {len(intruses)} intruse")
            continue

        neuf = dict(item)
        avant = ([i["syllabe"] for i in item["intruses"]], item.get("trou"), rang_du_mot)
        apres = ([i["syllabe"] for i in intruses], trou, rang if rang_du_mot is not None else None)
        if avant != apres:
            changements.append(f"{item['id']:4s} {mot:12s} trou {avant[1]} -> {trou} ; {avant[0]} -> {apres[0]}")
        neuf["trou"] = trou
        neuf["intruses"] = intruses
        if rang_du_mot is not None:
            neuf["rang"] = rang
        nouveaux.append(neuf)

    if impossibles:
        print("Aucun trou à deux voisines pour :")
        for m in impossibles:
            print(f"  {m}")
        print("\nRien n'a été écrit.")
        return 1

    if "--figer" not in sys.argv:
        print(f"{len(nouveaux)} items dérivés, {len(changements)} changeraient :\n")
        for c in changements:
            print(f"  {c}")
        print("\nRelancer avec --figer pour écrire.")
        return 0

    banque["items"] = nouveaux
    banque["meta"]["version"] = "0.2.0"
    banque["mecanique"]["deroulement"][2] = (
        "En bas, les cartes : la bonne syllabe et deux intruses."
    )
    banque["mecanique"]["regle_des_intruses"] = (
        "DEUX intruses par item, toutes deux VOISINES de la syllabe cachée, et chacune "
        "d'une des deux sortes. CONSONANTIQUE : elle partage la voyelle et la coda, et "
        "n'en diffère que par la consonne d'attaque, prise dans une paire de consonnes "
        "proches (m/n, p/b, p/m, b/m, f/v, t/d, t/n, d/n, s/z, l/n, l/r, ch/j, ch/s, j/z, "
        "c/g devant a-o-u, c/s et c/z devant e-i, g/j devant e-i). VOCALIQUE : elle "
        "partage l'attaque et la coda, et n'en diffère que par la voyelle, prise dans une "
        "paire de voyelles proches (a/è, a/o, i/u, o/ou, on/an, in/an, é/è, e/é, e/è). La "
        "paire est écrite en LETTRES — `c/g` pour le couple de sons /k/ et /g/ — parce que "
        "c'est la lettre que la carte porte et que le contrôle compare. Une intruse "
        "LOINTAINE, qui ne partage ni la voyelle ni la consonne, est interdite : elle "
        "s'écarte d'emblée et n'ajoute aucune difficulté. La banque est dérivée puis figée "
        "par outils/proposer-intruses.py ; le choix du trou gardé et le champ `sert` "
        "restent des décisions d'auteur, préservées à chaque dérivation."
    )
    banque["mecanique"]["pourquoi_deux_intruses"] = (
        "Une seule intruse laisse une chance sur deux de tomber juste sans rien "
        "discriminer — ce n'est pas un exercice, c'est un pile ou face. À deux intruses, "
        "la chance tombe à une sur trois, et surtout chaque mauvaise carte est une "
        "voisine : il faut entendre la différence, pas éliminer le bruit."
    )
    chemin.write_bytes(
        (json.dumps(banque, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )
    print(f"{len(nouveaux)} items écrits dans {chemin.name} — {len(changements)} modifiés.")
    return 0


def proposer(filtres):
    gs = json.loads((ICI / "mots-gs.json").read_text(encoding="utf-8"))["mots"]
    cp = json.loads((ICI / "mots-cp.json").read_text(encoding="utf-8"))["mots"]

    for banque, nom in ((gs, "GS"), (cp, "CP")):
        print(f"\n{'=' * 70}\nBanque {nom}\n{'=' * 70}")
        for m in banque:
            mot, syl = m["mot"], m["syllabes"]
            if filtres and mot not in filtres:
                continue
            if len(syl) < 2:
                print(f"\n{mot:12s} — monosyllabe, hors jeu (un seul trou possible)")
                continue
            print(f"\n{mot:12s} {'-'.join(syl)}")
            for t, cachee in enumerate(syl):
                c, v = voisines(cachee, set(syl))
                total = len(c) + len(v)
                note = ""
                if total < 2:
                    note = "  <-- insuffisant"
                elif not c:
                    note = "  <-- aucune consonantique"
                print(f"   trou {t} « {cachee} » : {total} candidate(s){note}")
                if c:
                    print(f"      consonnes  : " + ", ".join(f"{s} ({p})" for s, p in c))
                if v:
                    print(f"      voyelles   : " + ", ".join(f"{s} ({p})" for s, p in v))
    return 0


if __name__ == "__main__":
    if "--figer" in sys.argv:
        sys.exit(figer())
    sys.exit(proposer({a for a in sys.argv[1:] if not a.startswith("--")}))
