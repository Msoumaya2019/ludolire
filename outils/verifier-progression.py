"""Contrôle les deux tables de progression : la GS et le CE1.

Ce qui est vérifié ici ne se voit pas à l'oeil :

  - les rangs forment une suite de 1 à N, sans trou ni doublon — un trou dans une
    progression est une semaine que personne ne sait où placer ;
  - chaque unité renvoie à un domaine déclaré, et chaque domaine déclaré porte au
    moins une unité ;
  - `production` est un booléen partout : c'est le seul champ de ces tables dont
    dépend le verdict des exercices, et une valeur manquante rend le contrôle des
    inversions aveugle ;
  - à la GS, `colonne` est l'une des trois colonnes d'âge du programme — c'est
    l'attribution relevée, et elle doit être contestable item par item ;
  - au CE1, un exemple annoncé « programme » se retrouve réellement dans
    `citations_officielles` ;
  - au CE1, les quatre domaines sont ceux du programme, et non une organisation
    inventée ;
  - au CE1, un objectif qui porte un acte de parole — « donner un titre »,
    « justifier », « résumer » — est marqué `production`. C'est le contrôle qui
    garde l'axe honnête, et il n'est QUE DANS UN SENS : il attrape une
    production oubliée, pas une production inventée. Voir la note au-dessus de
    `VERBES_DE_PRODUCTION` pour sa limite, qui est réelle.

CE QUE CE CONTRÔLE NE FAIT PAS, et il faut le dire : il ne compare pas les
citations officielles au texte publié. Il ne peut pas — le PDF n'est pas dans le
dépôt. Il garantit seulement qu'un exemple marqué « programme » est couvert par
une citation présente dans le même fichier, et donc que le bloc de citations est
tenu à jour quand une unité change. La fidélité des citations au Bulletin
officiel se vérifie en les relisant contre l'Annexe 3, et c'est une relecture
humaine.

Usage :
    python verifier-progression.py
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

ICI = Path(__file__).resolve().parent

# Les trois colonnes d'âge du programme de cycle 1, relevées du tableau publié.
COLONNES = {"Avant 4 ans", "À partir de 4 ans", "À partir de 5 ans"}
PALIERS_GS = {"préparatoire", "GS"}
# Les quatre ensembles de la section « Lecture » du programme de cycle 2.
DOMAINES_CE1 = {"IDM", "LVH", "CTX", "DVL"}
SOURCES_CE1 = {"objectif", "exemple", "choix"}
EXEMPLES_SOURCE = {"programme", "notre formulation"}

CHAMPS_GS = ("rang", "periode", "domaine", "palier", "colonne", "objectif", "exemples",
             "action", "production")
CHAMPS_CE1 = ("rang", "periode", "domaine", "objectif", "exemples", "exemples_source",
              "action", "production", "source")

# Les actes de parole : ce que le programme demande de DIRE, et que l'application
# ne peut pas entendre. Un objectif qui en porte un est une production, et son
# exercice devra déclarer son `inversion`.
#
# CE CONTRÔLE N'EST APPLIQUÉ QU'AU CE1, et la raison compte : les productions de
# la GS sont pour la plupart ARTICULATOIRES — « Prononcer », « Articuler »,
# « Reproduire des sons ». Ce sont des actes de la voix, pas des actes de parole,
# et aucune liste de verbes ne les attrape. Appliquer la même liste à la GS
# demanderait de basculer dix-huit unités, ce qui serait faux. Le contrôle est
# donc lexical, et il ne porte que là où les productions sont bien des actes de
# parole. C'est une limite déclarée, pas un oubli.
#
# Il n'est aussi QUE DANS UN SENS : un verbe trouvé impose `production: true`.
# L'erreur inverse — une unité marquée de production sans l'être — n'est pas
# attrapée ici, et ne peut pas l'être par une liste de verbes. Elle l'est plus
# loin, par le contrôle des exercices : une unité de production oblige l'exercice
# qui la couvre à déclarer une `inversion`, et une inversion inventée se lit.
VERBES_DE_PRODUCTION = (
    "dire", "raconter", "restituer", "expliciter", "resumer", "justifier", "exprimer",
    "nommer", "caracteriser", "reformuler", "expliquer", "reciter", "chanter", "epeler",
    "donner un titre", "lire a voix haute", "dire le nom", "dire le son",
)


def motif_mot(verbe):
    """Le verbe comme MOT entier.

    Sans les bornes, « dire » se retrouve dans « dire**ctement** » : l'unité 29
    du CE1, « Identifier directement l'ensemble des mots courants », était
    signalée à tort. Un contrôle qui refuse à tort finit par être désactivé —
    donc les bornes sont ici, et elles ont été éprouvées sur les deux tables.
    """
    return re.compile(r"(?<![a-z])" + re.escape(verbe) + r"(?![a-z])")


def verbes_de_production(u):
    trouves = []
    for champ in ("objectif", "exemples"):
        t = normaliser(str(u.get(champ, "")))
        trouves += [v for v in VERBES_DE_PRODUCTION if motif_mot(v).search(t)]
    return sorted(set(trouves))


def charger(nom):
    return json.loads((ICI / nom).read_text(encoding="utf-8"))


def normaliser(t):
    """Casse, accents et espaces neutralisés.

    L'extraction d'un PDF perd des circonflexes — « enchainements » pour
    « enchaînements », « entraine » pour « entraîne ». Une comparaison exacte
    refuserait des citations fidèles, et un contrôle qui refuse à tort finit par
    être désactivé. La normalisation est donc déclarée ici, et elle est la même
    des deux côtés.
    """
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", t).strip().lower()


def controler_commun(nom, d, champs):
    erreurs = []
    unites = d["unites"]
    domaines = {x["id"] for x in d["domaines"]}
    erreurs += controler_meta(nom, d)

    rangs = [u.get("rang") for u in unites]
    if rangs != list(range(1, len(unites) + 1)):
        manquants = sorted(set(range(1, len(unites) + 1)) - set(rangs))
        doubles = sorted({r for r in rangs if rangs.count(r) > 1})
        if manquants:
            erreurs.append(f"{nom} : rang(s) manquant(s) {manquants}")
        if doubles:
            erreurs.append(f"{nom} : rang(s) en double {doubles}")

    periodes = sorted({u["periode"] for u in unites})
    if periodes != list(range(1, len(periodes) + 1)):
        erreurs.append(f"{nom} : les périodes ne forment pas une suite de 1 à n — {periodes}")

    portees = {}
    for u in unites:
        r = u.get("rang", "?")
        manquants = [c for c in champs if c not in u]
        if manquants:
            erreurs.append(f"{nom} unité {r} : champ(s) manquant(s) {manquants}")
            continue
        if u["domaine"] not in domaines:
            erreurs.append(f"{nom} unité {r} : domaine « {u['domaine']} » non déclaré")
        portees.setdefault(u["domaine"], []).append(r)
        for cle in ("objectif", "exemples", "action"):
            if not str(u[cle]).strip():
                erreurs.append(f"{nom} unité {r} : `{cle}` vide")
        if not isinstance(u["production"], bool):
            erreurs.append(
                f"{nom} unité {r} : `production` = {u['production']!r}, booléen attendu — "
                f"sans lui le contrôle des inversions est aveugle"
            )
    for dom in sorted(domaines - set(portees)):
        erreurs.append(f"{nom} : le domaine « {dom} » est déclaré mais ne porte aucune unité")

    # Le palier de sortie : chaque ligne doit dire si elle est vérifiable.
    palier = d.get("palier_de_sortie")
    if not palier:
        erreurs.append(f"{nom} : aucun palier de sortie")
    else:
        for p in palier:
            for cle in ("objectif", "verifiable"):
                if not str(p.get(cle, "")).strip():
                    erreurs.append(f"{nom} palier de sortie : `{cle}` absent ou vide")

    h = d.get("hors_tranche") or {}
    for cle in ("note", "contenu", "raison"):
        if not h.get(cle):
            erreurs.append(f"{nom} hors_tranche : `{cle}` absent ou vide")
    return portees, erreurs


def controler_meta(nom, d):
    erreurs = []
    for cle in ("titre", "version", "date", "statut"):
        if not str(d.get("meta", {}).get(cle, "")).strip():
            erreurs.append(f"{nom} meta : `{cle}` absent ou vide")
    return erreurs


def controler_gs(d):
    """Renvoie (portees, erreurs) — toujours les deux, sur tous les chemins.

    Les sous-contrôles lisent `palier` et `colonne` que `controler_commun` a pu
    déjà signaler comme absents. Ils y accèdent donc par `.get()` : un contrôle
    doit RAPPORTER une unité mal formée, pas mourir dessus et taire tout le
    reste du fichier.
    """
    portees, erreurs = controler_commun("GS", d, CHAMPS_GS)
    for u in d["unites"]:
        r = u.get("rang", "?")
        palier, colonne = u.get("palier"), u.get("colonne")
        if palier is None or colonne is None:
            continue
        if palier not in PALIERS_GS:
            erreurs.append(f"GS unité {r} : palier « {palier} » inconnu")
        if colonne not in COLONNES:
            erreurs.append(
                f"GS unité {r} : colonne « {colonne} » absente des trois "
                f"colonnes d'âge du programme"
            )
        # La correspondance palier / colonne n'est pas libre : le préparatoire est
        # la réunion des deux premières colonnes, le palier GS la troisième.
        attendu = "GS" if colonne == "À partir de 5 ans" else "préparatoire"
        if palier != attendu:
            erreurs.append(
                f"GS unité {r} : palier « {palier} » pour la colonne "
                f"« {colonne} » — « {attendu} » attendu"
            )
    return portees, erreurs


def controler_ce1(d):
    """Renvoie (portees, n_programme, n_citations, erreurs)."""
    portees, erreurs = controler_commun("CE1", d, CHAMPS_CE1)

    if {x["id"] for x in d["domaines"]} != DOMAINES_CE1:
        erreurs.append(
            "CE1 : les domaines ne sont pas les quatre ensembles de la section "
            f"« Lecture » du programme — {sorted(x['id'] for x in d['domaines'])}"
        )

    citations = d["meta"].get("citations_officielles")
    if not citations:
        erreurs.append("CE1 meta : `citations_officielles` absent — les exemples « programme » "
                       "ne sont alors couverts par rien")
        citations = []
    for c in citations:
        for cle in ("page", "section", "texte"):
            if not str(c.get(cle, "")).strip():
                erreurs.append(f"CE1 citation p.{c.get('page', '?')} : `{cle}` absent ou vide")
    corpus = [normaliser(c["texte"]) for c in citations]

    n_programme = 0
    for u in d["unites"]:
        r = u.get("rang", "?")
        src, ex_src = u.get("source"), u.get("exemples_source")
        if src is None or ex_src is None:
            continue
        if src not in SOURCES_CE1:
            erreurs.append(f"CE1 unité {r} : source « {src} » inconnue")
        if ex_src not in EXEMPLES_SOURCE:
            erreurs.append(f"CE1 unité {r} : `exemples_source` « {ex_src} » inconnu")
            continue
        if ex_src != "programme":
            continue
        n_programme += 1
        exemple = str(u.get("exemples", ""))
        if not any(normaliser(exemple) in c for c in corpus):
            erreurs.append(
                f"CE1 unité {r} : l'exemple est annoncé « programme » mais ne se retrouve "
                f"dans aucune citation officielle — « {exemple[:70]}… »"
            )

    # `production` commande le verdict des exercices : un objectif qui porte un
    # acte de parole et qui n'est pas marqué de production est un drapeau faux,
    # et il ne se voit pas à la lecture — la table reste pleine.
    for u in d["unites"]:
        r = u.get("rang", "?")
        if u.get("production") is None:
            continue
        trouves = verbes_de_production(u)
        if trouves and not u["production"]:
            erreurs.append(
                f"CE1 unité {r} : l'objectif ou l'exemple porte un acte de parole "
                f"({', '.join(trouves)}) mais `production` est faux — l'exercice qui "
                f"couvre cette unité ne saura pas qu'il doit déclarer une inversion"
            )

    # Le palier de la tranche doit être nommé, et nommé comme le programme le nomme.
    attendu = "lire et comprendre en autonomie un texte narratif, informatif ou prescriptif d'une quinzaine de lignes"
    paliers = " ".join(normaliser(p.get("objectif", "")) for p in d["palier_de_sortie"])
    if attendu not in paliers:
        erreurs.append("CE1 : le palier de sortie ne reprend pas la formule du programme "
                       "« … d'une quinzaine de lignes »")
    if not any(u.get("rang") == 38 for u in d["unites"]):
        erreurs.append("CE1 : l'unité 38 porte le palier de sortie et doit exister")

    return portees, n_programme, len(citations), erreurs


def main():
    gs = charger("progression-gs.json")
    ce1 = charger("progression-ce1.json")

    p_gs, e_gs = controler_gs(gs)
    p_ce1, n_prog, n_cit, e_ce1 = controler_ce1(ce1)

    print(f"GS  : {len(gs['unites'])} unités, {len(gs['domaines'])} domaines, "
          f"{sum(1 for u in gs['unites'] if u['production'])} de production, "
          f"{len(gs['palier_de_sortie'])} réussites de sortie")
    print(f"CE1 : {len(ce1['unites'])} unités, {len(ce1['domaines'])} domaines, "
          f"{sum(1 for u in ce1['unites'] if u['production'])} de production, "
          f"{len(ce1['palier_de_sortie'])} réussites de sortie")
    print(f"CE1 : {n_prog} exemples annoncés « programme », couverts par "
          f"{n_cit} citations officielles")
    prod_ce1 = [u["rang"] for u in ce1["unites"] if u.get("production")]
    print(f"CE1 unités de production ({len(prod_ce1)}) : {prod_ce1}")
    print("  chacune oblige l'exercice qui la couvre à déclarer ce que le geste "
          "reprend à la place de la production")
    print("CE1 par domaine :")
    for x in ce1["domaines"]:
        rangs = [u["rang"] for u in ce1["unites"] if u["domaine"] == x["id"]]
        print(f"  {x['id']} — {x['libelle']:52s} {len(rangs):>2} unités  {rangs}")
    print("GS par domaine :")
    for x in gs["domaines"]:
        n = sum(1 for u in gs["unites"] if u["domaine"] == x["id"])
        print(f"  {x['id']} — {x['libelle']:52s} {n:>2} unités")

    erreurs = e_gs + e_ce1
    if erreurs:
        print(f"\nNON CONFORME — {len(erreurs)} problème(s) :")
        for e in erreurs:
            print(f"  {e}")
        return 1
    print("\nRésultat : conforme")
    return 0


if __name__ == "__main__":
    sys.exit(main())
