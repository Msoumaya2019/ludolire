"""Éprouve le contrôle des images de récit en le faisant ÉCHOUER.

Un contrôle qu'on n'a jamais vu échouer ne prouve rien. Cette tranche en a déjà
donné deux preuves : un contrôle d'atteignabilité des graphies qui cherchait
chaque graphie dans une sonde construite autour d'elle — il ne pouvait pas
échouer ; et une section du harnais du décodeur qui ne regardait ni la découpe ni
la lecture, si bien que retirer une garde ne changeait rien à ce qu'elle voyait.

On présente donc au contrôle un corpus faux à la fois, et on exige que chaque
défaut soit vu — et vu POUR LA BONNE RAISON, c'est-à-dire que le message attendu
apparaisse. Un défaut vu par un autre contrôle que celui qui le vise est un
défaut vu par accident, et l'accident ne se reproduit pas.

Ce que ce harnais ne peut pas éprouver, et il faut le dire :

  - les contrôles qui lisent la BANQUE et non le corpus — la mécanique d'un
    exercice, le nombre d'images que sa série annonce — ne se falsifient pas en
    modifiant le corpus. Deux d'entre eux se falsifient par effet de bord (le
    texte, l'unité), et c'est pourquoi ceux-là sont dans la liste ;
  - la garde contre une chaîne de références qui BOUCLE n'est pas atteignable
    depuis le corpus : `resoudre_cadrage` relit les fichiers référencés sur le
    disque, donc muter la référence en mémoire ne change que le premier saut, et
    la chaîne repart sur la vraie. La garde reste — un fichier mal édité la
    déclenche — mais elle n'est pas éprouvée ici, et c'est écrit plutôt que tu.
    Ce qui EST éprouvé, c'est qu'une chaîne qui s'arrête sans cadrage est
    refusée.

Usage :
    python tester-images-recit.py
"""

import copy
import importlib.util
import re
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

BANQUE = VI.charger("exercices-ce1.json")
AUTRE_MECANIQUE = next(
    e["id"] for e in BANQUE["exercices"] if e["mecanique"] != "ordonner_recit"
)


def recit(c, exercice):
    return next(r for r in c["recits"] if r["exercice"] == exercice)


def etape(c, exercice, ident):
    return next(e for e in recit(c, exercice)["etapes"] if e["id"] == ident)


def toutes_les_etapes(c):
    return [e for r in c["recits"] for e in r["etapes"]]


# ---------------------------------------------------------------------------
# Les corpus faux. Chacun porte UN défaut, et le message attendu dit lequel.
# ---------------------------------------------------------------------------

def ordre_inverse(c):
    """Deux étapes échangent leur numéro, la liste reste dans l'ordre du texte."""
    etape(c, "E19", "e19_1")["ordre"] = 2
    etape(c, "E19", "e19_2")["ordre"] = 1


def ordre_du_texte_inverse(c):
    """Les deux premières étapes échangent leur ligne : l'ordre dessiné n'est plus celui du texte."""
    a, b = etape(c, "E19", "e19_1"), etape(c, "E19", "e19_2")
    a["ligne_citee"], b["ligne_citee"] = b["ligne_citee"], a["ligne_citee"]


def ligne_inventee(c):
    etape(c, "E19", "e19_3")["ligne_citee"] = "Le soir, l'éléphant a fermé la porte."


def ligne_d_un_autre_texte(c):
    etape(c, "E19", "e19_1")["ligne_citee"] = "Le chat est un bon compagnon."


def repere_hors_liste(c):
    etape(c, "E19", "e19_4")["repere"] = "la couleur du ciel"


def repere_duplique(c):
    etape(c, "E45", "e45_3")["repere"] = "le geste du corps"


def repere_jamais_employe(c):
    for e in toutes_les_etapes(c):
        if e["repere"] == "le décor":
            e["repere"] = "le cadre"


def exercice_inconnu(c):
    recit(c, "E19")["exercice"] = "E99"


def mecanique_autre(c):
    recit(c, "E19")["exercice"] = AUTRE_MECANIQUE


def texte_qui_n_est_pas_le_sien(c):
    r = recit(c, "E19")
    r["texte"], r["rang"] = "T17-rang33", 33


def unite_fausse(c):
    recit(c, "E45")["unite"] = 36


def nombre_d_etapes_faux(c):
    recit(c, "E19")["etapes"].pop()


def image_ne_dit_rien(c):
    recit(c, "E19")["ce_que_l_image_ne_dit_pas"] = "   "


def moment_vide(c):
    etape(c, "E19", "e19_1")["moment"] = ""


def objet_vide(c):
    etape(c, "E19", "e19_1")["objet"] = "   "


def objet_duplique(c):
    etape(c, "E45", "e45_4")["objet"] = etape(c, "E19", "e19_1")["objet"]


def identifiant_duplique(c):
    etape(c, "E19", "e19_2")["id"] = "e19_1"


def identifiant_pas_un_fichier(c):
    etape(c, "E19", "e19_1")["id"] = "e19-1"


def pas_de_dessin(c):
    etape(c, "E19", "e19_1")["id"] = "e19_5"


def risque_avec_inconnu(c):
    etape(c, "E19", "e19_1")["risque"][0]["avec"] = "e45_1"


def crainte_non_reciproque(c):
    e = etape(c, "E19", "e19_2")
    e["risque"] = [r for r in e["risque"] if r["avec"] != "e19_1"]


def risque_sans_parade(c):
    etape(c, "E45", "e45_1")["risque"][0].pop("parade")


def se_craint_elle_meme(c):
    etape(c, "E19", "e19_4")["risque"] = [
        {"avec": "e19_4", "pourquoi": "un", "parade": "deux"}
    ]


def exercice_sans_images_tu(c):
    c["exercices_sans_images"] = [
        d for d in c["exercices_sans_images"] if d["exercice"] != "E51"
    ]


def exercice_couvert_declare_sans_images(c):
    c["exercices_sans_images"].append({"exercice": "E19", "raison": "parce que"})


def declaration_sans_raison(c):
    next(d for d in c["exercices_sans_images"] if d["exercice"] == "E39")["raison"] = ""


def reperes_vides(c):
    c["reperes"] = []


def interdits_vides(c):
    c["interdits"] = []


def regles_vides(c):
    c["regles_du_recit"]["ce_qu_elle_ne_doit_pas_faire"] = []


def figures_non_dites(c):
    c["regles_du_recit"]["comment_les_figures_sont_prises"] = ""


def cadrage_reference_absente(c):
    c["cadrage_de_reference"] = "images-mars.json"


def chaine_sans_cadrage(c):
    c["cadrage_de_reference"] = "mots-gs.json"


CAS = [
    ("deux étapes échangent leur numéro", ordre_inverse, "les ordres déclarés sont"),
    ("l'ordre dessiné n'est pas celui du texte", ordre_du_texte_inverse,
     "l'ordre dessiné n'est pas celui du texte"),
    ("une ligne qui n'est pas dans le texte", ligne_inventee,
     "ne se trouve pas littéralement"),
    ("une ligne prise dans un autre texte", ligne_d_un_autre_texte,
     "ne se trouve pas littéralement"),
    ("repère hors de la liste fermée", repere_hors_liste, "hors de la liste fermée"),
    ("deux étapes, un seul repère", repere_duplique, "deux repères identiques"),
    ("un repère déclaré et jamais employé", repere_jamais_employe, "jamais employés"),
    ("exercice inconnu de la banque", exercice_inconnu, "absent de la banque"),
    ("une autre mécanique que la remise en ordre", mecanique_autre, "la banque le déclare"),
    ("les images d'un autre texte", texte_qui_n_est_pas_le_sien,
     "les images ne montrent pas le texte de l'exercice"),
    ("unité déclarée ≠ unité de la banque", unite_fausse, "déclarée par le récit"),
    ("le récit a une étape de moins que la série", nombre_d_etapes_faux,
     "la série annonce 4 images"),
    ("ce que l'image ne dit pas est tu", image_ne_dit_rien, "est vide"),
    ("aucun moment décrit", moment_vide, "aucun moment décrit"),
    ("aucun objet décrit", objet_vide, "aucun objet décrit"),
    ("deux étapes, un seul objet", objet_duplique, "reçoivent le même objet"),
    ("deux étapes, un seul identifiant", identifiant_duplique,
     "deux étapes portent le même identifiant"),
    ("un identifiant qui n'est pas un nom de fichier", identifiant_pas_un_fichier,
     "doit être un nom de fichier"),
    ("aucune fonction de dessin pour une étape", pas_de_dessin,
     "aucune fonction de dessin"),
    ("une crainte déclarée avec une autre série", risque_avec_inconnu,
     "qui n'est pas une étape de"),
    ("une crainte qui n'est pas réciproque", crainte_non_reciproque,
     "ne craint pas"),
    ("un risque sans parade", risque_sans_parade, "sans `parade`"),
    ("une étape qui se craint elle-même", se_craint_elle_meme, "se craint elle-même"),
    ("un exercice sans images tu", exercice_sans_images_tu,
     "se DÉCLARE dans `exercices_sans_images`"),
    ("un exercice couvert déclaré sans images", exercice_couvert_declare_sans_images,
     "la déclaration contredit la progression"),
    ("une déclaration sans raison", declaration_sans_raison, "sans raison"),
    ("aucun repère déclaré", reperes_vides, "liste vide"),
    ("aucun interdit déclaré", interdits_vides, "liste vide"),
    ("une règle du récit vidée", regles_vides, "la règle n'est pas dite"),
    ("les figures réemployées non dites", figures_non_dites,
     "comment_les_figures_sont_prises"),
    ("cadrage de référence absent", cadrage_reference_absente, "fichier absent"),
    ("une chaîne de référence sans cadrage", chaine_sans_cadrage,
     "ni cadrage, ni référence"),
]


def main():
    corpus = VI.charger("images-recit-ce1.json")
    echecs = 0

    # Le témoin. Sans lui, tout ce qui suit pourrait être vert parce que le
    # contrôle refuse TOUT — un contrôle qui refuse tout voit tous les défauts.
    _, _, erreurs = VI.controler_recit(corpus)
    if erreurs:
        echecs += 1
    print(f"  {'OK ' if not erreurs else 'ÉCHEC'} corpus réel".ljust(50)
          + f"attendu 0 problème   obtenu {len(erreurs)}")
    for e in erreurs:
        print(f"        → {e}")

    print()
    for etiquette, mutation, attendu in CAS:
        faux = copy.deepcopy(corpus)
        mutation(faux)
        _, _, erreurs = VI.controler_recit(faux)
        vus = [e for e in erreurs if attendu in e]
        ok = bool(vus)
        if not ok:
            echecs += 1
        print(f"  {'OK ' if ok else 'ÉCHEC'} {etiquette:48s} "
              f"{len(erreurs):>2} problème(s)   attendu « {attendu} »")
        if not ok:
            for e in erreurs:
                print(f"        → {e}")
            if not erreurs:
                print("        → le contrôle n'a RIEN vu")

    # --- le contrôle des fichiers, sur un dossier temporaire -------------------
    print()
    etapes = toutes_les_etapes(corpus)
    cle = etiquette = lambda i: i["id"]
    temporaire = Path(tempfile.mkdtemp(prefix="ludolire-recit-"))
    try:
        for e in etapes:
            shutil.copy(VI.IMAGES_RECIT / f"ill_{e['id']}.svg", temporaire)

        def problemes():
            _, f = VI.controler_fichiers(etapes, temporaire, GI.DESSINS_RECIT,
                                         cle=cle, etiquette=etiquette)
            return f + VI.controler_composition(etapes, temporaire, cle=cle,
                                                etiquette=etiquette)

        erreurs = problemes()
        ok = not erreurs
        if not ok:
            echecs += 1
        print(f"  {'OK ' if ok else 'ÉCHEC'} copie conforme des 8 SVG".ljust(50)
              + f"attendu 0 problème   obtenu {len(erreurs)}")
        for e in erreurs:
            print(f"        → {e}")

        cible = temporaire / "ill_e19_1.svg"
        conforme = cible.read_bytes()

        cible.write_bytes(conforme.replace(
            b"</g></svg>", b"<text x='10' y='10'>papa</text></g></svg>"
        ))
        vus = [e for e in problemes() if "rien à lire" in e]
        echecs += not vus
        print(f"  {'OK ' if vus else 'ÉCHEC'} un mot écrit dans l'image".ljust(50)
              + "attendu « rien à lire »")

        # La couleur est prise dans le fichier lui-même plutôt qu'écrite en dur :
        # viser une teinte que le dessin n'emploie pas ferait un remplacement qui
        # ne remplace rien, et l'essai serait vert pour la mauvaise raison.
        premiere = re.search(rb"#[0-9A-Fa-f]{6}", conforme)
        cible.write_bytes(conforme.replace(premiere.group(0), b"#123456", 1))
        vus = [e for e in problemes() if "hors palette" in e]
        echecs += not vus
        print(f"  {'OK ' if vus else 'ÉCHEC'} une couleur hors palette".ljust(50)
              + "attendu « hors palette »")

        # L'échelle change, l'épaisseur ne suit pas : c'est le défaut que le
        # contrôle de composition existe pour voir, et il ne se voit pas dans le
        # code — les deux nombres sont là, c'est leur produit qui est faux.
        cible.write_bytes(
            re.sub(rb"scale\([\d.]+ [\d.]+\)", b"scale(0.2500 0.2500)", conforme, count=1)
        )
        vus = [e for e in problemes() if "le trait rend" in e]
        echecs += not vus
        print(f"  {'OK ' if vus else 'ÉCHEC'} l'échelle change sans l'épaisseur".ljust(50)
              + "attendu « le trait rend »")

        cible.write_bytes(conforme)
        (temporaire / "ill_e19_2.svg").write_bytes(conforme)
        vus = [e for e in problemes() if "même fichier à l'octet" in e]
        echecs += not vus
        print(f"  {'OK ' if vus else 'ÉCHEC'} deux images identiques".ljust(50)
              + "attendu « même fichier à l'octet »")

        (temporaire / "ill_e19_2.svg").write_bytes(
            (VI.IMAGES_RECIT / "ill_e19_2.svg").read_bytes()
        )
        cible.unlink()
        vus = [e for e in problemes() if "fichier absent" in e]
        echecs += not vus
        print(f"  {'OK ' if vus else 'ÉCHEC'} un SVG absent".ljust(50)
              + "attendu « fichier absent »")
    finally:
        shutil.rmtree(temporaire, ignore_errors=True)

    print()
    total = 1 + len(CAS) + 6
    if echecs:
        print(f"{echecs} essai(s) en échec sur {total}.")
        return 1
    print(f"{len(CAS)} corpus faux et 6 fichiers faux : {total} essais, tous vus — "
          f"le contrôle des images de récit a des dents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
