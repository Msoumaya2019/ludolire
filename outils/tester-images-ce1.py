"""Éprouve les contrôles du corpus d'images du CE1 en les faisant ÉCHOUER.

Un contrôle qu'on n'a jamais vu échouer ne prouve rien. C'est la leçon de cette
tranche, et elle a coûté cher deux fois : un contrôle d'atteignabilité des
graphies qui cherchait chaque graphie dans la découpe d'une sonde construite
autour d'elle — il ne pouvait pas échouer, et il accusait deux graphies saines ;
et une section du harnais du décodeur qui ne regardait ni la découpe ni la
lecture, si bien que retirer une garde ne changeait rien à ce qu'elle voyait.

On présente donc au contrôle QUINZE corpus faux, un défaut à la fois, et on exige
que chacun soit vu — et vu POUR LA BONNE RAISON, c'est-à-dire que le message
attendu apparaisse. Un défaut vu par un autre contrôle que celui qui le vise est
un défaut vu par accident, et l'accident ne se reproduit pas.

Usage :
    python tester-images-ce1.py
"""

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VI = charger_module("verifier_images", ICI / "verifier-images.py")
GI = VI.GI


def item(corpus, mot):
    return next(i for i in corpus["items"] if i["mot"] == mot)


def refus(corpus, mot):
    return next(n for n in corpus["non_illustrables"] if n["mot"] == mot)


# ---------------------------------------------------------------------------
# Les corpus faux. Chacun porte UN défaut, et le message attendu dit lequel.
# ---------------------------------------------------------------------------

def decoupe_fausse(c):
    item(c, "foin")["decoupe"] = ["f", "o", "i", "n"]


def emploi_menti(c):
    item(c, "foin")["employable_par"]["present_dans_la_serie"] = True


def emploi_muet(c):
    item(c, "foin")["employable_par"]["ce_qu_il_faudrait"] = ""


def rang_faux(c):
    item(c, "parfum")["rang"] = 12


def besoin_qui_ne_repond_pas(c):
    item(c, "parfum")["besoin"] = "B04"


def besoin_inconnu(c):
    item(c, "foin")["besoin"] = "B99"


def exercice_inconnu(c):
    item(c, "foin")["employable_par"]["exercice"] = "E99"


def mot_deja_illustre(c):
    item(c, "foin")["mot"] = "lune"


def objet_duplique(c):
    item(c, "parfum")["objet"] = item(c, "foin")["objet"]


def objet_vide(c):
    item(c, "foin")["objet"] = "   "


def interdit_non_liste(c):
    item(c, "foin")["interdit"] = "aucun animal"


def risque_sans_parade(c):
    item(c, "foin")["risque"][0].pop("parade")


def risque_sans_objet(c):
    r = item(c, "foin")["risque"][0]
    r["avec"] = None
    r.pop("hors_banque", None)


def motif_hors_liste(c):
    refus(c, "coin")["motif"] = "trop dur à dessiner"


def raison_vide(c):
    refus(c, "point")["raison"] = ""


def refus_retire(c):
    c["non_illustrables"] = [n for n in c["non_illustrables"] if n["mot"] != "coin"]


def mot_a_la_fois(c):
    item(c, "foin")["mot"] = "coin"


def illustration_retiree(c):
    c["items"] = [i for i in c["items"] if i["mot"] != "foin"]


def reponse_retiree(c):
    c.pop("reponse_aux_besoins", None)


def reponse_mentie(c):
    c["reponse_aux_besoins"]["B04"]["illustrables"] = []


def reponse_sans_raison(c):
    c["reponse_aux_besoins"]["B04"]["illustrables"] = []
    c["reponse_aux_besoins"]["B04"]["raison_si_aucun"] = ""


def motif_jamais_employe(c):
    for n in c["non_illustrables"]:
        if n["motif"] == "jour":
            n["motif"] = "abstrait"


def cadrage_reference_absente(c):
    c["cadrage_de_reference"] = "images-mars.json"


CAS = [
    ("découpe déclarée ≠ découpe réelle", decoupe_fausse, "découpe déclarée"),
    ("le corpus ment sur son emploi", emploi_menti, "present_dans_la_serie"),
    ("l'emploi n'est pas dit", emploi_muet, "ce_qu_il_faudrait"),
    ("rang déclaré ≠ rang de l'unité", rang_faux, "rang déclaré"),
    ("le besoin ne répond pas au même exercice", besoin_qui_ne_repond_pas,
     "ne répond pas au même besoin"),
    ("besoin inconnu de la banque", besoin_inconnu, "absent de la banque"),
    ("exercice inconnu de la banque", exercice_inconnu, "absent de la banque"),
    ("mot déjà illustré dans la tranche GS", mot_deja_illustre,
     "déjà illustré dans la tranche GS"),
    ("deux mots, un seul objet", objet_duplique, "reçoivent le même objet"),
    ("aucun objet décrit", objet_vide, "aucun objet décrit"),
    ("`interdit` n'est pas une liste", interdit_non_liste, "doit être une liste"),
    ("risque sans parade", risque_sans_parade, "sans `parade`"),
    ("risque sans mot ni hors_banque", risque_sans_objet, "sans `hors_banque`"),
    ("motif hors de la liste fermée", motif_hors_liste, "hors de la liste fermée"),
    ("refus sans raison", raison_vide, "refus sans raison"),
    ("mot affiché ni illustré ni déclaré", refus_retire,
     "ni illustré ni déclaré non illustrable"),
    ("mot illustré ET déclaré non illustrable", mot_a_la_fois,
     "à la fois illustré et déclaré"),
    ("mot illustré disparu du corpus", illustration_retiree, "les deux sources ont divergé"),
    ("la réponse aux besoins est absente", reponse_retiree, "`reponse_aux_besoins` absent"),
    ("la réponse aux besoins est mentie", reponse_mentie, "les deux sources ont divergé"),
    ("un besoin sans réponse ni raison", reponse_sans_raison, "besoin tu"),
    ("motif déclaré et jamais employé", motif_jamais_employe, "jamais employés"),
    ("cadrage de référence absent", cadrage_reference_absente, "fichier absent"),
]


def main():
    corpus = VI.charger("images-ce1.json")
    echecs = 0

    # Le témoin. Sans lui, tout ce qui suit pourrait être vert parce que le
    # contrôle refuse TOUT — un contrôle qui refuse tout voit tous les défauts.
    _, _, _, erreurs = VI.controler_ce1(corpus)
    etat = "OK " if not erreurs else "ÉCHEC"
    if erreurs:
        echecs += 1
    print(f"  {etat} corpus réel                        attendu 0 problème   obtenu {len(erreurs)}")
    for e in erreurs:
        print(f"        → {e}")

    print()
    for etiquette, mutation, attendu in CAS:
        faux = copy.deepcopy(corpus)
        mutation(faux)
        _, _, _, erreurs = VI.controler_ce1(faux)
        vus = [e for e in erreurs if attendu in e]
        ok = bool(vus)
        if not ok:
            echecs += 1
        print(f"  {'OK ' if ok else 'ÉCHEC'} {etiquette:44s} "
              f"{len(erreurs):>2} problème(s)   attendu « {attendu} »")
        if not ok:
            for e in erreurs:
                print(f"        → {e}")
            if not erreurs:
                print("        → le contrôle n'a RIEN vu")

    # --- le contrôle des fichiers, sur un dossier temporaire -------------------
    print()
    items = corpus["items"]
    temporaire = Path(tempfile.mkdtemp(prefix="ludolire-images-"))
    try:
        for i in items:
            shutil.copy(VI.IMAGES_CE1 / f"ill_{VI.slug(i['mot'])}.svg", temporaire)
        _, erreurs = VI.controler_fichiers(items, temporaire, GI.DESSINS_CE1)
        ok = not erreurs
        if not ok:
            echecs += 1
        print(f"  {'OK ' if ok else 'ÉCHEC'} copie conforme des 3 SVG".ljust(50)
              + f"attendu 0 problème   obtenu {len(erreurs)}")

        # Un mot écrit dans l'image donne la réponse à qui sait lire.
        cible = temporaire / "ill_foin.svg"
        cible.write_bytes(
            cible.read_bytes().replace(
                b"</g></svg>", b"<text x='10' y='10'>foin</text></g></svg>"
            )
        )
        _, erreurs = VI.controler_fichiers(items, temporaire, GI.DESSINS_CE1)
        vus = [e for e in erreurs if "rien à lire" in e]
        ok = bool(vus)
        if not ok:
            echecs += 1
        print(f"  {'OK ' if ok else 'ÉCHEC'} un mot écrit dans l'image".ljust(50)
              + f"attendu « rien à lire »   obtenu {len(erreurs)} problème(s)")

        # Une couleur hors palette : la série cesse d'être homogène.
        cible.write_bytes(
            (VI.IMAGES_CE1 / "ill_foin.svg").read_bytes().replace(b"#F2C24C", b"#123456")
        )
        _, erreurs = VI.controler_fichiers(items, temporaire, GI.DESSINS_CE1)
        vus = [e for e in erreurs if "hors palette" in e]
        ok = bool(vus)
        if not ok:
            echecs += 1
        print(f"  {'OK ' if ok else 'ÉCHEC'} une couleur hors palette".ljust(50)
              + f"attendu « hors palette »   obtenu {len(erreurs)} problème(s)")

        # Un fichier absent : un mot sans image est un exercice impossible.
        cible.unlink()
        _, erreurs = VI.controler_fichiers(items, temporaire, GI.DESSINS_CE1)
        vus = [e for e in erreurs if "fichier absent" in e]
        ok = bool(vus)
        if not ok:
            echecs += 1
        print(f"  {'OK ' if ok else 'ÉCHEC'} un SVG absent".ljust(50)
              + f"attendu « fichier absent »   obtenu {len(erreurs)} problème(s)")
    finally:
        shutil.rmtree(temporaire, ignore_errors=True)

    print()
    total = 1 + len(CAS) + 4
    if echecs:
        print(f"{echecs} essai(s) en échec sur {total}.")
        return 1
    print(f"{len(CAS)} corpus faux et 4 fichiers faux : {total} essais, tous vus — "
          f"le contrôle du corpus du CE1 a des dents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
