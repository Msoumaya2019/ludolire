"""Contrôle la table des formes d'exercice.

CE QUE CE CONTRÔLE EMPÊCHE
--------------------------
`outils/formes-exercices.json` dit, pour chaque mécanique des deux banques,
quelle interaction l'application emploie — ou pourquoi elle n'en emploie
aucune. C'est une décision, et une décision qui n'est pas contrôlée dérive :

  - UNE MÉCANIQUE ABSENTE DE LA TABLE. L'exercice existe, il est déclaré
    jouable, et l'application ne le rend pas. Personne ne l'a décidé : on l'a
    oublié. C'est le défaut que la table existe pour rendre impossible.

  - UNE FORME NULLE SANS RAISON. « Pas rendu » sans motif est indistinguable
    d'un oubli. La table refuse le silence.

  - UNE FORME QUI EXIGE CE QUE L'EXERCICE NE PORTE PAS. Une forme
    `carte_a_choisir` reçoit ses cartes de `questions` ; un exercice qui n'en
    porte pas ne peut pas la recevoir. Sans ce contrôle, la fabrication
    produirait un écran vide au lieu d'une erreur. Un tel exercice doit être
    DÉCLARÉ en exception, avec sa raison.

  - UNE EXCEPTION PÉRIMÉE, OU MAL NOMMÉE. Une exception qui ne sert plus est un
    mensonge qui dort. Le contrôle regarde donc dans les DEUX SENS : tout
    exercice qui a besoin d'une exception doit en avoir une, et toute exception
    doit être nécessaire. Et il faut dire DE QUEL GENRE elle est, parce que les
    deux n'obéissent pas au même critère : un `champs_manquants` est un trou
    dans la donnée, et se mesure ; une `forme_inadaptee` est un jugement sur ce
    que la forme sait montrer, et ne se mesure pas. Une exception de jugement
    n'est acceptée que si l'exercice porte VRAIMENT tout ce que la forme exige —
    sinon elle masquerait un trou de donnée sous un mot plus flatteur.

  - UNE ROUTE QUI N'EXISTE PAS. Une forme dit par quel écran elle est rendue.
    Si le fichier n'est pas dans `app/`, la forme ne sera rendue nulle part.

  - UN EXERCICE DÉCLARÉ HORS APP QUI SERAIT EMBARQUÉ. La banque dit qu'il n'est
    pas jouable ; l'embarquer contredirait sa propre déclaration.

CE QUI N'EST PAS VÉRIFIÉ, et il faut le dire : le choix de la forme. Qu'une
mécanique de compréhension se rende par un choix de carte plutôt que par une
autre interaction est un JUGEMENT, et ce contrôle ne le juge pas — il vérifie
seulement que la décision est écrite, complète, et tenue.

Usage :
    python outils/verifier-formes.py
"""

import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent

TABLE = ICI / "formes-exercices.json"
APP = RACINE / "app"

# `banques` est indexe par NIVEAU — gs, ce1 — et non par nom de fichier.
BANQUES = {
    "gs": "exercices-gs.json",
    "ce1": "exercices-ce1.json",
}

# Les clés attendues, et elles sont CLOSES : une clé qui n'y figure pas est
# refusée, pour qu'une faute de frappe se voie au lieu de dormir dans le
# fichier.
CLES_TABLE = {"meta", "formes", "exceptions", "mecaniques"}

CLES_FORME = {"id", "libelle", "ce_que_l_enfant_fait", "ce_que_l_application_fait",
              "exige", "embarque_les_exercices", "rendu_par"}
CLES_FORME_FACULTATIVES = {"remarque"}

CLES_MECANIQUE = {"niveau", "id", "forme", "pourquoi"}
CLES_EXCEPTION = {"niveau", "exercice", "parce_que", "raison"}

# LES DEUX GENRES D'EXCEPTION, et pourquoi il faut les distinguer.
#
#   - `champs_manquants` : la forme exige un champ que l'exercice ne porte pas.
#     C'est un TROU DANS LA DONNÉE, et il se mesure.
#   - `forme_inadaptee` : l'exercice porte tout ce que la forme exige, mais la
#     forme ne sait pas montrer ce que l'exercice juge. C'est un JUGEMENT, et il
#     ne se mesure pas — il s'écrit.
#
# Sans cette distinction, le contrôle n'avait qu'un critère — « la forme exige
# ce qui manque » — et il refusait une exception de jugement comme « périmée »
# alors qu'elle était exacte. Mesuré sur E21 et E55, dont les cartes sont des
# titres que l'écran ne montre jamais, et qui portent pourtant leurs questions.
PARCE_QUE = {"champs_manquants", "forme_inadaptee"}


def charger(chemin):
    return json.loads(chemin.read_text(encoding="utf-8"))


def routes_de_l_application(dossier):
    """Les routes qui existent, lues sur le disque et non supposées."""
    if not dossier.is_dir():
        return set()
    return {f.stem for f in dossier.glob("*.tsx") if f.name != "_layout.tsx"}


def controler(table, banques):
    erreurs = []
    verifications = 0

    def verifier(condition, message):
        nonlocal verifications
        verifications += 1
        if not condition:
            erreurs.append(message)

    # --- 1. La structure de la table ----------------------------------------
    verifier(
        set(table) == CLES_TABLE,
        f"la table doit porter exactement {sorted(CLES_TABLE)}, elle porte {sorted(table)}",
    )

    formes = {}
    for f in table.get("formes", []):
        cles = set(f)
        verifier(
            CLES_FORME <= cles <= (CLES_FORME | CLES_FORME_FACULTATIVES),
            f"forme « {f.get('id')} » : clés {sorted(cles)} — attendu {sorted(CLES_FORME)} "
            f"plus, au plus, {sorted(CLES_FORME_FACULTATIVES)}",
        )
        verifier(bool(f.get("id")), "une forme sans identifiant")
        if f.get("id"):
            verifier(f["id"] not in formes, f"forme « {f['id']} » déclarée deux fois")
            formes[f["id"]] = f

    routes = routes_de_l_application(APP)

    # La route d'une forme se verifie UNE FOIS, et non une fois par mecanique
    # qui l'emploie : neuf fois le meme message, personne ne le lit.
    for forme in formes.values():
        # UNE FORME INCOMPLETE EST DEJA REFUSEE, et on ne la lit pas plus loin.
        #
        # Mesure, et c'est le banc qui l'a trouvee : privee de sa cle « exige »,
        # une forme faisait lever au controle un `KeyError` au lieu de rapporter
        # le defaut. Un controle qui plante ne rapporte rien — il remplace un
        # message lisible par une trace d'appels, et c'est le pire des deux.
        if not CLES_FORME <= set(forme):
            continue
        verifier(
            forme["rendu_par"].startswith("/"),
            f"forme « {forme['id']} » : rendu_par « {forme['rendu_par']} » n'est pas un chemin",
        )
        verifier(
            forme["rendu_par"].lstrip("/") in routes,
            f"forme « {forme['id']} » dit être rendue par « {forme['rendu_par']} », "
            f"qu'aucun fichier de {APP.name}/ ne porte",
        )

    # --- 2. Chaque mécanique du catalogue est déclarée ----------------------
    declarees = {}
    for m in table.get("mecaniques", []):
        verifier(set(m) == CLES_MECANIQUE,
                 f"mécanique {m.get('niveau')}/{m.get('id')} : clés {sorted(m)}")
        cle = (m.get("niveau"), m.get("id"))
        verifier(cle not in declarees, f"mécanique {cle[0]}/{cle[1]} déclarée deux fois")
        declarees[cle] = m
        verifier(m.get("niveau") in BANQUES,
                 f"mécanique {cle[1]} : niveau « {m.get('niveau')} » inconnu")

    # --- 3. Les exceptions déclarées ----------------------------------------
    exceptions = {}
    for x in table.get("exceptions", []):
        verifier(set(x) == CLES_EXCEPTION,
                 f"exception {x.get('niveau')}/{x.get('exercice')} : clés {sorted(x)}")
        verifier(bool(x.get("raison")),
                 f"exception {x.get('niveau')}/{x.get('exercice')} : sans raison")
        cle = (x.get("niveau"), x.get("exercice"))
        verifier(cle not in exceptions, f"exception {cle[0]}/{cle[1]} déclarée deux fois")
        exceptions[cle] = x

    for niveau in BANQUES:
        b = banques[niveau]
        catalogue = {m["id"] for m in b["mecaniques"]}
        identifiants = {e["id"] for e in b["exercices"]}

        for mid in sorted(catalogue):
            verifier(
                (niveau, mid) in declarees,
                f"{niveau}/{mid} est au catalogue de la banque et absent de la table : "
                "une mécanique qu'on oublie est une mécanique que personne n'a décidé "
                "de ne pas rendre",
            )

        for e in b["exercices"]:
            if e["verdict"] != "app" or e["mecanique"] is None:
                continue
            verifier(
                (niveau, e["mecanique"]) in declarees,
                f"{niveau}/{e['id']} déclare la mécanique « {e['mecanique']} », "
                "absente de la table",
            )

        for cle in exceptions:
            if cle[0] != niveau:
                continue
            verifier(
                cle[1] in identifiants,
                f"exception {niveau}/{cle[1]} : cet exercice n'existe pas dans la banque",
            )

    # --- 4. Chaque forme nommée existe, et tient ses exigences --------------
    besoin_d_exception = set()

    for (niveau, mid), m in declarees.items():
        # Un niveau inconnu est deja refuse plus haut. Continuer ferait planter
        # le controle sur `banques[niveau]` — deuxieme voie de plantage trouvee
        # par le banc, apres la forme incomplete.
        if niveau not in BANQUES:
            continue
        forme_id = m.get("forme")
        if forme_id is None:
            verifier(
                bool(m.get("pourquoi")),
                f"{niveau}/{mid} : forme nulle sans raison. « Pas rendu » sans motif "
                "est indistinguable d'un oubli",
            )
            continue

        verifier(
            not m.get("pourquoi"),
            f"{niveau}/{mid} : une raison est donnée alors que la forme est « {forme_id} »",
        )
        verifier(forme_id in formes, f"{niveau}/{mid} : forme « {forme_id} » inconnue")
        if forme_id not in formes:
            continue
        forme = formes[forme_id]
        # Meme garde-fou que ci-dessus : une forme incomplete est deja refusee,
        # et lire ses exigences ferait planter le controle sur une cle absente.
        if not CLES_FORME <= set(forme):
            continue

        for e in banques[niveau]["exercices"]:
            if e["mecanique"] != mid:
                continue
            if e["verdict"] != "app":
                # Une forme qui n'embarque pas les exercices ne dit rien d'eux :
                # c'est le cas de `mot_a_trou`, rendue depuis la banque du jeu.
                if forme["embarque_les_exercices"]:
                    verifier(
                        False,
                        f"{niveau}/{e['id']} est déclaré hors app et sa mécanique "
                        f"« {mid} » est embarquée : embarquer un exercice qu'on dit "
                        "injouable contredit sa propre déclaration",
                    )
                continue

            # L'exigence ne porte que sur les exercices que la forme reçoit.
            if not forme["embarque_les_exercices"]:
                continue

            manquants = [champ for champ in forme["exige"] if not e.get(champ)]
            if manquants:
                besoin_d_exception.add((niveau, e["id"]))
                verifier(
                    (niveau, e["id"]) in exceptions,
                    f"{niveau}/{e['id']} : la forme « {forme_id} » exige "
                    f"{manquants}, que l'exercice ne porte pas — l'écran serait vide. "
                    "Déclarez-le en exception, avec sa raison",
                )

    # --- 5. Une exception doit être nécessaire, ET DU BON GENRE -------------
    for cle, x in exceptions.items():
        genre = x.get("parce_que")
        verifier(
            genre in PARCE_QUE,
            f"exception {cle[0]}/{cle[1]} : « parce_que » vaut « {genre} », "
            f"attendu l'un de {sorted(PARCE_QUE)}",
        )
        if genre == "champs_manquants":
            verifier(
                cle in besoin_d_exception,
                f"exception {cle[0]}/{cle[1]} : déclarée « champs_manquants », mais "
                "l'exercice porte ce que sa forme exige — une exception périmée est "
                "un mensonge qui dort",
            )
        elif genre == "forme_inadaptee":
            verifier(
                cle not in besoin_d_exception,
                f"exception {cle[0]}/{cle[1]} : déclarée « forme_inadaptee », mais il "
                "manque à l'exercice ce que sa forme exige — c'est un trou dans la "
                "donnée, et il doit être déclaré « champs_manquants »",
            )

    # --- 6. Le compte tombe ------------------------------------------------
    total = embarques = 0
    for niveau in BANQUES:
        for e in banques[niveau]["exercices"]:
            if e["verdict"] != "app":
                continue
            total += 1
            m = declarees.get((niveau, e["mecanique"]))
            if not (m and m.get("forme")):
                continue
            # Le compte ne lit une forme que si elle est nommee, connue ET
            # complete. Compter est la derniere chose que fait le controle : il
            # ne doit pas etre l'endroit ou il plante sur une table deja refusee.
            f = formes.get(m["forme"])
            if not (f and CLES_FORME <= set(f)):
                continue
            if f["embarque_les_exercices"] and (niveau, e["id"]) not in exceptions:
                embarques += 1

    return verifications, erreurs, total, embarques, len(exceptions)


def main():
    table = charger(TABLE)
    banques = {niveau: charger(ICI / nom) for niveau, nom in BANQUES.items()}

    verifications, erreurs, total, embarques, nb_exceptions = controler(table, banques)

    print("Contrôle des formes d'exercice")
    print(f"  formes déclarées       {len(table['formes'])} "
          f"({', '.join(f['id'] for f in table['formes'])})")
    print(f"  mécaniques déclarées   {len(table['mecaniques'])}")
    print(f"  exercices jouables     {total}")
    print(f"  embarqués              {embarques}")
    print(f"  exceptions déclarées   {nb_exceptions}")
    print(f"  non rendus             {total - embarques - nb_exceptions}, chacun avec sa raison")
    print(f"  vérifications          {verifications}")

    if erreurs:
        print(f"\nNON CONFORME — {len(erreurs)} défaut(s) :")
        for e in erreurs:
            print(f"  {e}")
        return 1

    print("\nRésultat : conforme")
    return 0


if __name__ == "__main__":
    sys.exit(main())
