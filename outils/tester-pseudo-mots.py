"""Éprouve le contrôle des pseudo-mots, et la dérivation de la lecture.

TROIS SECTIONS, ET LA DEUXIÈME COMPTE AUTANT QUE LA PREMIÈRE.

1. LA LECTURE DÉRIVÉE, sur des mots réels dont la prononciation est connue. La
   transcription est ce qui part au script de l'enregistrement : si elle dérive
   de travers, la voix dit autre chose que ce que les lettres donnent, et
   l'exercice devient insoluble. Un contrôle qui lirait faux serait vert partout
   ailleurs.

   La section nomme aussi les mots où la lecture mécanique DIFFÈRE de la lecture
   réelle — « loup », « tas », « chanter ». Ce n'est pas un défaut : c'est la
   décision du corpus, et elle est vérifiée ici pour qu'elle reste une décision.

2. LES GRAPHIES SANS LECTURE. Neuf graphies de la table portent /j/ pour huit
   lettres : c'est une étiquette de classe. Le banc vérifie qu'une suite bâtie
   sur l'une d'elles est bien REFUSÉE — et non silencieusement lue de travers,
   ce qui était le cas avant.

3. LES CORPUS FAUX, injectés un par un sur une copie en mémoire. Chaque cas
   porte le message qu'il doit déclencher, et un cas qui échoue pour une autre
   raison est compté comme raté : un refus n'est probant que si l'on sait sur
   quoi il porte.

Un témoin est joué d'abord, sur le corpus réel : sans lui, un contrôle qui
refuserait tout passerait le banc.

CE QUE CE BANC NE PEUT PAS PROUVER : qu'une suite ne soit pas un mot français.
C'est la limite déclarée du corpus, et aucun banc ne la lèvera.

Usage :
    python tester-pseudo-mots.py
"""

import copy
import importlib.util
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent


def charger_module(nom, cle):
    spec = importlib.util.spec_from_file_location(cle, ICI / nom)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VPM = charger_module("verifier-pseudo-mots.py", "verifier_pseudo_mots")
VC = charger_module("verifier-textes-ce1.py", "verifier_textes_ce1")
CP = json.loads((ICI / "cgp-cp.json").read_text(encoding="utf-8"))
CE1 = json.loads((ICI / "cgp-ce1.json").read_text(encoding="utf-8"))
PHONEMES, _RANGS, _TRANCHES, E_TABLES = VPM.tables()
AUTORISEES = VC.cgp_autorisees(CP, CE1, VPM.RANG_DE_LECTURE)
SANS_SON = VC.lettres_sans_son(CE1)


def lecture(mot):
    return VPM.lecture_mecanique(mot, VC, AUTORISEES, PHONEMES, SANS_SON)


# ---------------------------------------------------------------------------
# 1. La lecture dérivée
# ---------------------------------------------------------------------------
# (mot, lecture attendue) — des mots réels dont la lecture tombe juste.
#
# LA TABLE DONNE UN PHONÈME PAR GRAPHIE : elle ne distingue pas le o ouvert du o
# fermé, et « école » s'y lit donc /ekol/. La transcription fixe la SUITE des
# sons et la place des muettes ; elle ne prétend pas à la qualité exacte des
# voyelles, et cette limite est écrite ici pour qu'on ne la lui fasse pas dire.
LECTURES = [
    ("lune", "/lyn/"),
    ("école", "/ekol/"),
    ("musique", "/myzik/"),
    ("poisson", "/pwasɔ̃/"),
    ("montagne", "/mɔ̃taɲ/"),
    ("cartable", "/kaʁtabl/"),
    ("parfum", "/paʁfœ̃/"),
    ("humble", "/œ̃bl/"),
    ("cagnou", "/kaɲu/"),
    ("poinche", "/pwɛ̃ʃ/"),
    ("trumpon", "/tʁœ̃pɔ̃/"),
    ("flaption", "/flapsjɔ̃/"),
]

# (mot, lecture mécanique, pourquoi elle diffère) — les mots où la lecture
# mécanique N'EST PAS la lecture réelle, et c'est voulu : une consonne finale se
# lit par sa correspondance, parce qu'un pseudo-mot n'a pas de lexique pour dire
# qu'elle est muette. Ces cas sont ici pour que la décision reste visible, et
# pour qu'on ne la prenne pas un jour pour une erreur de dérivation.
DIVERGENCES = [
    ("loup", "/lup/", "le p est muet en français"),
    ("tas", "/tas/", "le s du pluriel est muet en français"),
    ("chat", "/ʃat/", "le t est muet en français"),
    ("chanter", "/ʃɑ̃təʁ/", "la terminaison -er vaut /e/ : la morphologie n'est pas dans la table"),
    ("doir", "/dwaʁ/", "« doir » n'est pas un mot : rien ne dit que le r serait muet"),
]

# Les graphies dont la table donne une étiquette de classe : une suite qui les
# emploie n'a pas de lecture dérivable, et doit être refusée comme telle.
SANS_LECTURE = ["fille", "soleil", "feuille", "travail", "yeux"]


def section_lecture():
    rates = []
    for mot, attendue in LECTURES:
        lue, inconnus = lecture(mot)
        if inconnus:
            rates.append(f"{mot} : lecture non dérivée — {inconnus}")
        elif lue != attendue:
            rates.append(f"{mot} : lu {lue}, attendu {attendue}")
    for mot, attendue, _pourquoi in DIVERGENCES:
        lue, inconnus = lecture(mot)
        if inconnus:
            rates.append(f"{mot} : lecture non dérivée — {inconnus}")
        elif lue != attendue:
            rates.append(f"{mot} : lu {lue}, attendu {attendue} (lecture mécanique)")
    print(f"  lecture dérivée      : {len(LECTURES)} mots réels, "
          f"{len(DIVERGENCES)} divergences assumées"
          + (" — TOUS JUSTES" if not rates else " — ÉCHEC"))
    return rates


def section_sans_lecture():
    rates = []
    for mot in SANS_LECTURE:
        lue, inconnus = lecture(mot)
        if not inconnus:
            rates.append(
                f"{mot} : lu {lue} sans broncher — la table donne /j/ pour une graphie "
                f"qui contient une voyelle, et le contrôle a composé une syllabe qui "
                f"n'existe pas"
            )
        elif not any("semi-consonne" in r for _g, r in inconnus):
            rates.append(f"{mot} : refusé, mais pour une autre raison — {inconnus}")
    print(f"  graphies sans lecture: {len(SANS_LECTURE)} suites bâties sur les neuf "
          f"graphies du /j" + (" — TOUTES REFUSÉES" if not rates else " — ÉCHEC"))
    return rates


# ---------------------------------------------------------------------------
# 3. Les corpus faux
# ---------------------------------------------------------------------------
CAS = []


def cas(nom, attendu):
    def enveloppe(f):
        CAS.append((nom, attendu, f))
        return f
    return enveloppe


def entree(corpus, ident):
    for p in corpus["pseudo_mots"]:
        if p.get("id") == ident:
            return p
    raise SystemExit(f"{ident} absent du corpus")


def exercice(banque, ident):
    for e in banque["exercices"]:
        if e["id"] == ident:
            return e
    raise SystemExit(f"{ident} absent de la banque")


@cas("champ_manquant", "champ(s) manquant(s) ['graphies']")
def _(c, _b):
    del entree(c, "pm01")["graphies"]


@cas("champ_inattendu", "champ(s) inattendu(s) ['prononciation']")
def _(c, _b):
    entree(c, "pm01")["prononciation"] = "/dwaʁ/"


@cas("identifiant_non_conforme", "identifiant non conforme")
def _(c, _b):
    entree(c, "pm01")["id"] = "PM1"


@cas("mot_avec_accent", "minuscules ASCII est attendue")
def _(c, _b):
    entree(c, "pm01")["mot"] = "dóir"


@cas("mot_trop_court", "hors de 3–9")
def _(c, _b):
    entree(c, "pm01")["mot"] = "da"


@cas("origine_menteuse", "est un exemple du programme et n'est pas déclaré comme tel")
def _(c, _b):
    entree(c, "pm02")["origine"] = "ecrit"


@cas("origine_inventee", "est déclaré exemple du programme et n'en est pas un")
def _(c, _b):
    entree(c, "pm06")["origine"] = "programme"


@cas("graphie_absente_de_la_suite", "la graphie « x » est déclarée")
def _(c, _b):
    entree(c, "pm01")["graphies"] = ["oi", "x"]


@cas("graphies_vides", "aucune graphie déclarée")
def _(c, _b):
    entree(c, "pm01")["graphies"] = []


@cas("complexite_menteuse_complexe", "la table en fait un pseudo-mot complexe")
def _(c, _b):
    entree(c, "pm05")["complexite"] = "simple"


@cas("complexite_menteuse_simple", "la table en fait un pseudo-mot simple")
def _(c, _b):
    entree(c, "pm01")["complexite"] = "complexe"


@cas("mot_deja_dans_l_application", "est déjà un mot de l'application")
def _(c, _b):
    entree(c, "pm06")["mot"] = "cartable"


@cas("homophone_d_un_mot_connu", "se lit /myzik/, comme musique")
def _(c, _b):
    entree(c, "pm06")["mot"] = "musiqe"


@cas("suite_batie_sur_une_graphie_sans_lecture", "semi-consonne")
def _(c, _b):
    entree(c, "pm06")["mot"] = "brondail"


@cas("pseudo_mot_cite_par_aucun_exercice", "cité par aucun exercice")
def _(c, _b):
    e = exercice(_b, "E43")
    e["pseudo_mots"] = [p for p in e["pseudo_mots"] if p != "pm10"]


@cas("meme_pseudo_mot_dans_deux_exercices", "deux exercices de l'unité 35")
def _(c, _b):
    exercice(_b, "E43")["pseudo_mots"] = ["pm06", "pm07", "pm08", "pm09", "pm01"]


@cas("pseudo_mot_cite_deux_fois", "cité deux fois par le même exercice")
def _(c, _b):
    exercice(_b, "E42")["pseudo_mots"] = ["pm01", "pm01", "pm02", "pm03", "pm04"]


@cas("citation_qui_ne_se_resout_pas", "absent du corpus")
def _(c, _b):
    exercice(_b, "E42")["pseudo_mots"] = ["pm01", "pm02", "pm03", "pm04", "pm99"]


@cas("mot_reel_absent_du_lexique", "n'est dans aucun corpus de l'application")
def _(c, b):
    exercice(b, "E43")["mots"] = ["montagne", "soleil", "poisson", "zorglub", "musique"]


@cas("mot_reel_qui_est_un_pseudo_mot", "ne peut pas être les deux")
def _(c, b):
    exercice(b, "E43")["mots"] = ["montagne", "soleil", "poisson", "doir", "musique"]


def main():
    corpus_reel = json.loads((ICI / "pseudo-mots-ce1.json").read_text(encoding="utf-8"))
    banque_reelle = json.loads((ICI / "exercices-ce1.json").read_text(encoding="utf-8"))

    print("Contrôle des pseudo-mots du CE1 — falsification")
    print()

    if E_TABLES:
        print("TÉMOIN ROUGE — les tables de correspondance sont incohérentes :")
        for e in E_TABLES:
            print(f"  {e}")
        return 1

    rates = section_lecture() + section_sans_lecture()
    if rates:
        print()
        for r in rates:
            print(f"  {r}")
        return 1

    _, _, e_reel, _ = VPM.controler(corpus_reel, banque_reelle)
    if e_reel:
        print("\nTÉMOIN ROUGE — le corpus réel déclenche des erreurs :")
        for e in e_reel:
            print(f"  {e}")
        return 1
    print("  témoin               : le corpus réel passe les contrôles")

    rates, vus = [], []
    for nom, attendu, mutation in CAS:
        c = copy.deepcopy(corpus_reel)
        b = copy.deepcopy(banque_reelle)
        mutation(c, b)
        _, _, erreurs, _ = VPM.controler(c, b)
        if not erreurs:
            rates.append((nom, attendu, "le contrôle n'a RIEN vu"))
        elif not any(attendu in m for m in erreurs):
            rates.append((nom, attendu, "\n".join(erreurs)))
        else:
            vus.append(nom)

    if rates:
        print(f"\n{len(rates)} cas raté(s) :")
        for nom, attendu, sortie in rates:
            print(f"\n--- {nom} : attendu « {attendu} »")
            print(sortie[:1200])
        return 1

    print()
    print(f"{len(vus)} corpus faux et 1 témoin : {len(vus) + 1} essais, tous vus — "
          f"le contrôle des pseudo-mots a des dents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
