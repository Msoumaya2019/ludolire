"""Fabrique le contenu que l'application embarque, à partir des corpus du projet.

POURQUOI CE GÉNÉRATEUR EXISTE
-----------------------------
L'application ne peut pas lire `outils/*.json` : ces fichiers sont hors de son
paquet, et Metro ne regroupe que ce qu'on lui demande d'importer. Elle a donc
besoin d'un fichier à elle.

Ce fichier n'est PAS une seconde source. Les corpus restent la source unique :
ce script les lit, les met en forme pour l'écran, et écrit un seul fichier. Le
jour où un texte ou un mot change, on relance ce script — et l'empreinte qu'il
inscrit change avec le contenu, ce qui rend la version du paquet vérifiable.

CE QUI EST EMBARQUÉ, ET RIEN DE PLUS
------------------------------------
  - les progressions GS et CE1, pour la liste de ce qu'on apprend ;
  - les textes de lecture, avec leur titre, leur rang et leur corps ;
  - le jeu des syllabes, avec la découpe de chaque mot ;
  - les correspondances du CP, qui n'ont ni progression ni texte à ce jour ;
  - les exercices que l'application sait rendre, c'est-à-dire ceux dont la
    mécanique reçoit une forme dans `outils/formes-exercices.json`.

CE QUI N'EST PAS EMBARQUÉ, ET C'EST DÉCLARÉ
-------------------------------------------
L'audio. Aucun son n'est enregistré à ce jour, donc rien n'est embarqué, et
l'application le dit plutôt que de faire semblant. Les exercices de la banque
qui reposent sur la voix ne sont donc pas jouables — c'est écrit dans le
document de livraison, pas caché.

Et les exercices que l'application ne sait pas encore rendre : ils sont
COMPTÉS, groupés par mécanique avec la raison que la table porte, et le
fichier embarqué les reprend pour que l'écran puisse les montrer. Un
générateur qui écarte en silence annonce un nombre et en livre un autre.

Usage :
    python outils/generer-contenu-app.py
"""

import hashlib
import io
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
OUTILS = RACINE / "outils"
CONTENU = RACINE / "contenu"
CIBLE = RACINE / "assets" / "contenu-app.json"

VERSION = "0.1.0"

# Les en-têtes d'un fichier de texte : `# rang: 3`, `# type: recit`,
# `# titre: Le chat`, ou simplement `# Le chat` pour le titre.
ENTETE = re.compile(r"^(rang|type|titre)\s*:\s*(.+)$")


def charger(nom):
    return json.loads((OUTILS / nom).read_text(encoding="utf-8"))


def lire_texte(chemin):
    """Un fichier de texte : ses en-têtes, puis son corps.

    Le format est celui que les documents du projet emploient déjà — les lignes
    qui commencent par `#` portent les métadonnées, les autres sont le texte.
    Un `#` qui n'est pas « clef: valeur » est le titre, parce que c'est ainsi
    que les textes de la GS sont écrits.
    """
    titre, rang, genre, corps = None, None, None, []
    for brute in chemin.read_text(encoding="utf-8").splitlines():
        ligne = brute.strip()
        if not ligne:
            continue
        if ligne.startswith("#"):
            entete = ligne.lstrip("#").strip()
            trouve = ENTETE.match(entete)
            if trouve:
                cle, valeur = trouve.group(1), trouve.group(2).strip()
                if cle == "rang":
                    rang = int(valeur)
                elif cle == "type":
                    genre = valeur
                else:
                    titre = valeur
            elif entete:
                titre = entete
        else:
            corps.append(ligne)
    return {
        "id": chemin.stem,
        "titre": titre or chemin.stem,
        "rang": rang,
        "genre": genre,
        "lignes": corps,
    }


def textes(dossier):
    d = CONTENU / dossier
    if not d.is_dir():
        return []
    return [lire_texte(f) for f in sorted(d.glob("*.txt"))]


def mots_decoupes():
    """La découpe de chaque mot du jeu, prise dans les DEUX banques.

    Les deux, et non celle de la GS seule : la banque du jeu porte deux rendus —
    `oral` (items J, tranche GS) et `ecrit` (items K, tranche CP) — et huit des
    douze items écrits tirent leur mot de `mots-cp.json`. Le contrôle du corpus
    fusionne déjà les deux banques ; suivre la seule déclaration de la banque
    ferait tomber ces huit items sans un mot d'explication.
    """
    decoupe = {m["mot"]: m["syllabes"] for m in charger("mots-gs.json")["mots"]}
    decoupe.update({m["mot"]: m["syllabes"] for m in charger("mots-cp.json")["mots"]})
    return decoupe


def jeu_syllabes():
    """Le jeu des syllabes, prêt à jouer : le mot découpé, le trou, les cartes.

    La bonne réponse n'est PAS recopiée dans le contenu embarqué : elle se
    déduit de la découpe et du rang du trou. Une réponse recopiée à côté de la
    question finit par diverger de la question ; ici, il n'y a rien à faire
    diverger.

    UN ITEM QUI NE SE RÉSOUT PAS FAIT ÉCHOUER LA FABRICATION. C'est la leçon du
    défaut corrigé dans la banque le même jour : un générateur qui écarte en
    silence ce qu'il ne sait pas lire annonce 42 items et en livre 34, sans une
    erreur. Un refus bruyant vaut mieux qu'un compte faux.
    """
    decoupe = mots_decoupes()
    items, refus = [], []
    for item in charger("jeu-syllabes.json")["items"]:
        mot = item["mot"]
        syllabes = decoupe.get(mot)
        if not syllabes:
            refus.append(f"{item['id']} : « {mot} » n'est dans aucune des deux banques de mots")
            continue
        trou = item["trou"]
        if not 0 <= trou < len(syllabes):
            refus.append(
                f"{item['id']} : le trou {trou} est hors de la découpe de « {mot} » "
                f"({len(syllabes)} syllabes)"
            )
            continue
        cartes = [syllabes[trou]] + [i["syllabe"] for i in item.get("intruses", [])]
        items.append({
            "id": item["id"],
            "mot": mot,
            "syllabes": syllabes,
            "trou": trou,
            "cartes": cartes,
            "rendu": item.get("rendu"),
            "sert": item.get("sert"),
        })
    if refus:
        raise SystemExit(
            "REFUS — le jeu des syllabes ne se fabrique pas :\n  "
            + "\n  ".join(refus)
        )
    return items


def unites(nom):
    """La liste de ce qu'on apprend, allégée pour l'écran."""
    if not (OUTILS / nom).exists():
        return []
    vues = []
    for u in charger(nom)["unites"]:
        vues.append({
            "rang": u["rang"],
            "periode": u.get("periode"),
            "domaine": u.get("domaine"),
            "objectif": u.get("objectif"),
            "action": u.get("action"),
        })
    return vues


def correspondances():
    """Les correspondances du CP : la lettre, son son, ses graphies."""
    return [
        {
            "rang": u["rang"],
            "semaine": u.get("semaine"),
            "phoneme": u.get("phoneme"),
            "graphies": u.get("graphies", []),
        }
        for u in charger("cgp-cp.json")["unites"]
    ]


def formes_declarees():
    """La table des formes, lue telle quelle.

    Elle dit quelle mécanique l'application rend, et pourquoi elle ne rend pas
    les autres. Le générateur ne décide rien : il applique la table, et il
    refuse si un exercice emploie une mécanique que la table ignore.
    """
    return charger("formes-exercices.json")


def consignes_ce1():
    """Le texte écrit de chaque consigne du CE1.

    Ce texte est aussi le script de l'enregistrement à faire. Tant qu'aucun son
    n'existe, c'est lui qui s'affiche : l'enfant du CE1 lit, donc la consigne
    peut être écrite là où celle de la GS doit être dite.
    """
    return {c["id"]: c for c in charger("exercices-ce1.json").get("consignes", [])}


def exercices():
    """Les exercices que l'application sait rendre, et le compte des autres.

    RIEN NE TOMBE EN SILENCE. C'est la leçon du jour où un générateur annonçait
    42 items et en livrait 34 sans une erreur. On n'embarque donc pas seulement
    ce qu'on sait rendre : on compte aussi ce qu'on écarte, groupé par mécanique
    avec la raison que la table porte, pour que l'écran puisse le MONTRER au lieu
    de laisser croire que ces exercices n'existent pas.
    """
    table = formes_declarees()
    par_forme = {f["id"]: f for f in table["formes"]}
    par_mecanique = {(m["niveau"], m["id"]): m for m in table["mecaniques"]}
    exceptions = {
        (x["niveau"], x["exercice"]): x["raison"]
        for x in table.get("exceptions", [])
    }
    consignes = consignes_ce1()

    resultat = {}
    for niveau, nom in (("gs", "exercices-gs.json"),
                        ("cp", "exercices-cp.json"),
                        ("ce1", "exercices-ce1.json")):
        # Le CP n'a pas encore de banque d'exercices. Ce n'est pas un oubli
        # de lecture : c'est un fichier qui n'existe pas, et l'écran du CP
        # n'annonce donc aucun exercice. Un niveau sans banque se dit vide,
        # il ne se devine pas.
        if not (OUTILS / nom).exists():
            resultat[niveau] = {"embarques": [], "non_rendus": [], "exceptions": []}
            continue
        banque = charger(nom)
        embarques, non_rendus, refuses = [], {}, []
        for e in banque["exercices"]:
            if e["verdict"] != "app":
                continue
            mid = e["mecanique"]
            declaration = par_mecanique.get((niveau, mid))
            if declaration is None:
                raise SystemExit(
                    f"REFUS — {niveau}/{e['id']} emploie la mécanique « {mid} », "
                    "absente de outils/formes-exercices.json. Lancez "
                    "outils/verifier-formes.py."
                )
            forme_id = declaration["forme"]
            if not forme_id or not par_forme[forme_id]["embarque_les_exercices"]:
                entree = non_rendus.setdefault(
                    mid,
                    {
                        "mecanique": mid,
                        "nombre": 0,
                        "pourquoi": declaration["pourquoi"] or "rendue par un autre écran",
                    },
                )
                entree["nombre"] += 1
                continue
            if (niveau, e["id"]) in exceptions:
                refuses.append(
                    {"exercice": e["id"], "raison": exceptions[(niveau, e["id"])]}
                )
                continue
            consigne = consignes.get(e.get("consigne") or "")
            embarques.append({
                "id": e["id"],
                "unite": e["unite"],
                "mecanique": mid,
                "titre": e["titre"],
                "consigne": consigne.get("texte") if consigne else None,
                "geste": e["geste"],
                "duree_s": e["duree_s"],
                "entraine": e["entraine"],
                "texte": e.get("texte"),
                "questions": [
                    {
                        "question": q["question"],
                        "bonne": q["bonne"],
                        "intrus": list(q.get("intrus") or []),
                        "phrase_preuve": q.get("phrase_preuve"),
                    }
                    for q in e.get("questions") or []
                ],
            })
        resultat[niveau] = {
            "embarques": embarques,
            "non_rendus": [non_rendus[k] for k in sorted(non_rendus)],
            "exceptions": refuses,
        }
    return resultat


def construire():
    ex = exercices()
    d = {
        "meta": {
            "titre": "Ludo'Lire",
            "sous_titre": "Apprendre à lire en jouant",
            "etablissement": "Écoles maternelle et élémentaire Frères Lumières — Montmagny",
            "version": VERSION,
            "role": "Contenu embarqué dans l'application, fabriqué par outils/generer-contenu-app.py.",
            "source": "Les corpus de outils/ et les textes de contenu/ restent la source unique.",
            "audio": "Aucun son n'est enregistré à ce jour. Les activités qui reposent sur la voix ne sont pas encore jouables, et l'application le dit.",
        },
        "niveaux": [
            {
                "id": "gs",
                "nom": "Grande section",
                "court": "GS",
                "sous_titre": "Écouter, jouer avec les syllabes, entrer dans l'écrit",
                "couleur": "#2E9E6B",
                "textes": textes("textes"),
                "jeu_syllabes": jeu_syllabes(),
                "unites": unites("progression-gs.json"),
                "correspondances": [],
                "exercices": ex["gs"]["embarques"],
                "exercices_non_rendus": ex["gs"]["non_rendus"],
                "exercices_exceptions": ex["gs"]["exceptions"],
            },
            {
                "id": "cp",
                "nom": "Cours préparatoire",
                "court": "CP",
                "sous_titre": "Les sons et leurs lettres, une par une",
                "couleur": "#D9822B",
                "textes": [],
                "jeu_syllabes": [],
                "unites": [],
                "correspondances": correspondances(),
                "exercices": ex["cp"]["embarques"],
                "exercices_non_rendus": ex["cp"]["non_rendus"],
                "exercices_exceptions": ex["cp"]["exceptions"],
            },
            {
                "id": "ce1",
                "nom": "Cours élémentaire 1re année",
                "court": "CE1",
                "sous_titre": "Décoder, comprendre, lire tout seul",
                "couleur": "#2554D6",
                "textes": textes("textes-ce1") + textes("textes-courts-ce1"),
                "jeu_syllabes": [],
                "unites": unites("progression-ce1.json"),
                "correspondances": [],
                "exercices": ex["ce1"]["embarques"],
                "exercices_non_rendus": ex["ce1"]["non_rendus"],
                "exercices_exceptions": ex["ce1"]["exceptions"],
            },
        ],
    }
    return d


def empreinte(d):
    """L'empreinte du contenu, inscrite dans le contenu lui-même.

    Elle porte sur tout SAUF elle-même — sinon elle ne pourrait pas se calculer.
    Le flux de compilation la cherche dans le paquet livré : c'est ainsi qu'on
    sait que l'application embarque bien ce contenu-là, et pas un autre.
    """
    nu = json.loads(json.dumps(d))
    nu["meta"].pop("empreinte", None)
    canonique = json.dumps(nu, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonique.encode("utf-8")).hexdigest()[:16]


def main():
    d = construire()
    d["meta"]["empreinte"] = empreinte(d)

    CIBLE.parent.mkdir(parents=True, exist_ok=True)
    # Écriture en OCTETS : `Path.write_text` traduirait « \n » en « \r\n » sous
    # Windows, et le fichier ne serait plus identique d'une machine à l'autre.
    octets = json.dumps(d, ensure_ascii=False, indent=2).encode("utf-8")
    CIBLE.write_bytes(octets + b"\n")

    print(f"{CIBLE.relative_to(RACINE)}")
    print(f"  empreinte            {d['meta']['empreinte']}")
    print(f"  taille               {len(octets) + 1} octets")
    for n in d["niveaux"]:
        print(f"  {n['court']:3} {n['nom']:34} "
              f"{len(n['textes']):3} textes  {len(n['jeu_syllabes']):3} items  "
              f"{len(n['unites']):3} unités  {len(n['correspondances']):3} correspondances  "
              f"{len(n['exercices']):3} exercices rendus  "
              f"{len(n['exercices_non_rendus']):3} mécaniques déclarées non rendues")
    return 0


if __name__ == "__main__":
    sys.exit(main())
