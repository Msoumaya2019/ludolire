"""Éprouve le contrôle des formes d'exercice.

POURQUOI CE BANC EXISTE
-----------------------
`verifier-formes.py` garde une DÉCISION : quelle interaction rend chaque
mécanique des deux banques, et pourquoi les autres ne sont pas rendues. Un
contrôle qu'on n'a jamais vu échouer n'est pas un contrôle — c'est une fonction
qui renvoie `[]`. On fabrique donc ici une table FAUSSE par défaut que le
contrôle prétend attraper, et on exige qu'il l'attrape.

UN REFUS N'EST PROBANT QUE SI L'ON SAIT SUR QUOI IL PORTE
--------------------------------------------------------
Chaque cas porte donc un **fragment attendu** dans le message. Un défaut signalé
pour une autre raison que celle qu'on éprouve ne prouve rien : sans ce fragment,
un cas vert dirait seulement « le contrôle a refusé quelque chose ».

TROIS CAS NE FABRIQUENT AUCUN DÉFAUT, ET CE SONT LES PLUS IMPORTANTS
-------------------------------------------------------------------
  - LE TÉMOIN : la table réelle doit passer sans une seule erreur, et le
    contrôle lancé en ligne de commande doit sortir avec le code 0. Sans lui, un
    contrôle qui refuserait TOUT serait vert sur tous les autres cas.
  - L'EXCEPTION NÉCESSAIRE : un exercice à qui il manque ce que sa forme exige,
    mais qui est DÉCLARÉ en exception, doit passer. Sans ce cas, un contrôle qui
    refuserait toute exception serait vert partout ailleurs.
  - LE COMPTE : le nombre d'exercices embarqués est vérifié contre le chiffre
    que le cadrage cite. Si la table grandit légitimement, ce chiffre change, et
    ce cas le dit — c'est le seul endroit où le compte est écrit deux fois.

CE QUE CE BANC N'ÉPROUVE PAS
----------------------------
Le CHOIX des formes. Qu'une mécanique de compréhension se rende par un choix de
carte plutôt que par une autre interaction est un jugement, et aucun banc ne le
tranchera. On éprouve seulement que la décision est écrite, complète, et tenue.

Usage :
    python outils/tester-formes.py
"""

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
PYTHON = sys.executable

# `verifier-formes.py` porte un tiret : il ne s'importe pas par `import`.
_spec = importlib.util.spec_from_file_location("vf", ICI / "verifier-formes.py")
vf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vf)


def charger():
    table = json.loads((ICI / "formes-exercices.json").read_text(encoding="utf-8"))
    banques = {
        niveau: json.loads((ICI / nom).read_text(encoding="utf-8"))
        for niveau, nom in vf.BANQUES.items()
    }
    return table, banques


TABLE, BANQUES = charger()


# ---------------------------------------------------------------------------
# Les accesseurs prennent l'objet qu'on leur donne, et JAMAIS la table globale.
#
# C'est une précaution, pas un style : la première version de ce banc lisait la
# table globale, si bien qu'un cas qui mutait « sa » copie modifiait en réalité
# celle du cas suivant — et le dernier cas, celui qui attend zéro erreur, aurait
# échoué pour une raison venue d'ailleurs. Un banc dont les cas se contaminent
# mesure son propre désordre.
# ---------------------------------------------------------------------------
def forme(table, identifiant):
    for f in table["formes"]:
        if f["id"] == identifiant:
            return f
    raise AssertionError(f"la table ne porte pas de forme « {identifiant} »")


def mecanique(table, niveau, identifiant):
    for m in table["mecaniques"]:
        if m["niveau"] == niveau and m["id"] == identifiant:
            return m
    raise AssertionError(f"la table ne déclare pas {niveau}/{identifiant}")


def exercice(banques, niveau, identifiant):
    for e in banques[niveau]["exercices"]:
        if e["id"] == identifiant:
            return e
    raise AssertionError(f"la banque {niveau} ne porte pas d'exercice {identifiant}")


# Le dossier vide qui sert de décor au cas « la route n'existe nulle part ». Il
# vit hors du projet : c'est un décor de banc, pas un fichier du dépôt.
#
# Il s'appelle `app`, et ce n'est pas cosmétique : le message du contrôle nomme
# le dossier qu'il a regardé — « qu'aucun fichier de app/ ne porte ». Le banc
# cherche ce message, et un dossier nommé autrement ferait échouer le cas sur
# une différence de nom, en accusant le contrôle d'un défaut qu'il n'a pas.
VIDE = Path(tempfile.mkdtemp(prefix="ludolire-banc-")) / "app"
VIDE.mkdir()


# ---------------------------------------------------------------------------
# Les cas. Chacun MUTE une copie de la table et des banques, et dit ce que le
# contrôle doit répondre. `None` comme fragment signifie : aucune erreur.
# ---------------------------------------------------------------------------
def cas():
    defs = []

    def cas_(libelle, fragment, mutation):
        defs.append((libelle, fragment, mutation))

    # --- La structure de la table ------------------------------------------
    def cle_en_trop(t, b):
        t["note"] = "une clé que personne n'a décidée"

    cas_("une clé de table en trop", "la table doit porter exactement", cle_en_trop)

    def cle_de_forme_manquante(t, b):
        del forme(t, "carte_a_choisir")["exige"]

    cas_("une forme sans « exige »", "forme « carte_a_choisir » : clés", cle_de_forme_manquante)

    def cle_de_forme_inconnue(t, b):
        forme(t, "carte_a_choisir")["couleur"] = "bleu"

    cas_("une forme avec une clé inconnue", "forme « carte_a_choisir » : clés", cle_de_forme_inconnue)

    def forme_sans_identifiant(t, b):
        forme(t, "carte_a_choisir")["id"] = ""

    cas_("une forme sans identifiant", "une forme sans identifiant", forme_sans_identifiant)

    def forme_en_double(t, b):
        t["formes"].append(copy.deepcopy(forme(t, "carte_a_choisir")))

    cas_("une forme déclarée deux fois", "déclarée deux fois", forme_en_double)

    # --- Les routes --------------------------------------------------------
    def route_pas_un_chemin(t, b):
        forme(t, "carte_a_choisir")["rendu_par"] = "exercice"

    cas_("une route qui n'est pas un chemin", "n'est pas un chemin", route_pas_un_chemin)

    def route_absente(t, b):
        # On ne touche pas la table : on retire à `app/` son contenu. C'est le
        # seul moyen d'éprouver ce contrôle sans effacer un vrai écran.
        vf.APP = VIDE

    cas_("une route qu'aucun fichier de app/ ne porte",
        "qu'aucun fichier de app/ ne porte", route_absente)

    # --- Les mécaniques ----------------------------------------------------
    def mecanique_absente(t, b):
        t["mecaniques"] = [
            m for m in t["mecaniques"]
            if not (m["niveau"] == "ce1" and m["id"] == "choisir_resume")
        ]

    cas_("une mécanique du catalogue absente de la table", "absent de la table", mecanique_absente)

    def mecanique_en_double(t, b):
        t["mecaniques"].append(copy.deepcopy(mecanique(t, "ce1", "choisir_resume")))

    cas_("une mécanique déclarée deux fois", "déclarée deux fois", mecanique_en_double)

    def niveau_inconnu(t, b):
        mecanique(t, "ce1", "choisir_resume")["niveau"] = "cp"

    cas_("une mécanique de niveau inconnu", "niveau « cp » inconnu", niveau_inconnu)

    def forme_nulle_sans_raison(t, b):
        mecanique(t, "ce1", "lire_mot_image")["pourquoi"] = None

    cas_("une forme nulle sans raison", "forme nulle sans raison", forme_nulle_sans_raison)

    def raison_alors_que_rendue(t, b):
        mecanique(t, "ce1", "choisir_resume")["pourquoi"] = "aucune raison, puisque rendue"

    cas_("une raison donnée alors que la forme est nommée",
        "une raison est donnée alors que la forme est", raison_alors_que_rendue)

    def forme_inconnue(t, b):
        mecanique(t, "ce1", "choisir_resume")["forme"] = "inventee"

    cas_("une forme nommée qui n'existe pas", "forme « inventee » inconnue", forme_inconnue)

    def exercice_a_mecanique_absente(t, b):
        exercice(b, "ce1", "E10")["mecanique"] = "zzz"

    cas_("un exercice dont la mécanique est absente de la table",
        "déclare la mécanique « zzz »", exercice_a_mecanique_absente)

    # --- Les exceptions ----------------------------------------------------
    def exception_manquante(t, b):
        t["exceptions"] = []

    cas_("un exercice à qui sa forme demande ce qu'il n'a pas, sans exception",
        "Déclarez-le en exception", exception_manquante)

    def exception_perimee(t, b):
        # E10 porte ses `questions` : sa forme ne lui demande rien, donc une
        # exception « champs_manquants » le concernant n'est plus nécessaire.
        t["exceptions"].append({
            "niveau": "ce1", "exercice": "E10",
            "parce_que": "champs_manquants", "raison": "périmée",
        })

    cas_("une exception « champs_manquants » qui n'est plus nécessaire",
        "mais l'exercice porte ce que sa forme exige", exception_perimee)

    def exception_mal_nommee(t, b):
        # E11 n'a pas de questions : le trou est dans la DONNÉE. Le déclarer
        # « forme_inadaptee » masquerait ce trou sous un mot plus flatteur.
        for x in t["exceptions"]:
            if x["exercice"] == "E11":
                x["parce_que"] = "forme_inadaptee"

    cas_("une exception « forme_inadaptee » alors qu'il manque des champs",
        "doit être déclaré « champs_manquants »", exception_mal_nommee)

    def exception_sans_genre(t, b):
        t["exceptions"][0]["parce_que"] = "parce que"

    cas_("une exception dont le genre n'est pas reconnu",
        "attendu l'un de", exception_sans_genre)

    def exception_sur_un_fantome(t, b):
        t["exceptions"].append({
            "niveau": "ce1", "exercice": "E999",
            "parce_que": "champs_manquants", "raison": "fantôme",
        })

    cas_("une exception sur un exercice qui n'existe pas",
        "cet exercice n'existe pas dans la banque", exception_sur_un_fantome)

    def exception_sans_raison(t, b):
        t["exceptions"][0]["raison"] = ""

    cas_("une exception sans raison", "sans raison", exception_sans_raison)

    def exception_en_double(t, b):
        t["exceptions"].append(copy.deepcopy(t["exceptions"][0]))

    cas_("une exception déclarée deux fois", "déclarée deux fois", exception_en_double)

    # --- L'accord entre la banque et la table ------------------------------
    def hors_app_embarque(t, b):
        exercice(b, "ce1", "E10")["verdict"] = "hors app"

    cas_("un exercice déclaré hors app que sa forme embarquerait",
        "contredit sa propre déclaration", hors_app_embarque)

    # --- Le cas sans défaut : une exception NÉCESSAIRE doit passer ---------
    def exception_necessaire(t, b):
        # E10 perd ses questions : sa forme exige ce qu'il n'a plus. Déclaré, il
        # doit passer. C'est la seule preuve que le contrôle ne refuse pas toute
        # exception — et donc que les cas ci-dessus mesurent bien quelque chose.
        exercice(b, "ce1", "E10")["questions"] = []
        t["exceptions"].append({
            "niveau": "ce1",
            "exercice": "E10",
            "parce_que": "champs_manquants",
            "raison": "questions retirées pour éprouver le banc",
        })

    cas_("une exception nécessaire est acceptée", None, exception_necessaire)

    return defs


def main():
    echecs = 0
    total = len(cas())

    for libelle, fragment, mutation in cas():
        table = copy.deepcopy(TABLE)
        banques = copy.deepcopy(BANQUES)

        app_reel = vf.APP
        try:
            mutation(table, banques)
            _, erreurs, _, _, _ = vf.controler(table, banques)
        finally:
            vf.APP = app_reel

        if fragment is None:
            ok = not erreurs
            detail = "aucune erreur attendue" if ok else f"{len(erreurs)} erreur(s) : {erreurs[0]}"
        else:
            trouve = next((e for e in erreurs if fragment in e), None)
            ok = trouve is not None
            detail = (f"« {fragment} »" if ok
                      else f"« {fragment} » ABSENT — {erreurs or 'aucune erreur'}")

        print(f"  {'OK        ' if ok else 'ÉCHEC     '} {libelle} ({detail})")
        if not ok:
            echecs += 1

    # --- Le témoin, par la ligne de commande -------------------------------
    #
    # Les cas ci-dessus appellent `controler` directement. Celui-ci passe par le
    # programme, et vérifie donc ce que les autres ne voient pas : le code de
    # sortie. Un contrôle qui rapporte « conforme » et sort avec 1 serait vert
    # partout ailleurs.
    r = subprocess.run(
        [PYTHON, str(ICI / "verifier-formes.py")],
        capture_output=True, text=True, encoding="utf-8", cwd=RACINE,
    )
    ok = r.returncode == 0
    print(f"  {'OK        ' if ok else 'ÉCHEC     '} la table réelle, par la ligne de commande "
          f"(code {r.returncode}, attendu 0)")
    if not ok:
        print(r.stdout)
        print(r.stderr)
        echecs += 1
    total += 1

    # --- Le compte ---------------------------------------------------------
    #
    # Ces trois nombres sont ceux que le cadrage cite. Ils sont écrits ici une
    # seconde fois, et c'est délibéré : si la table grandit légitimement, ce cas
    # rougit, et il faut alors mettre le chiffre à jour — au lieu de le laisser
    # vieillir en silence dans la documentation.
    _, erreurs, jouables, embarques, nb_exceptions = vf.controler(
        copy.deepcopy(TABLE), copy.deepcopy(BANQUES)
    )
    attendus = {
        "exercices jouables": (jouables, 95),
        "embarqués": (embarques, 11),
        "exceptions": (nb_exceptions, 3),
    }
    print()
    print("  --- le compte ---")
    for nom, (obtenu, attendu) in attendus.items():
        ok = obtenu == attendu
        print(f"  {'OK        ' if ok else 'ÉCHEC     '} {nom:20s} {obtenu} "
              f"(le cadrage cite {attendu})")
        if not ok:
            echecs += 1
        total += 1

    shutil.rmtree(VIDE.parent, ignore_errors=True)

    print()
    if echecs:
        print(f"{echecs} cas en échec sur {total}.")
        return 1
    print(f"{total} cas conformes à l'attendu.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
