"""Éprouve les contrôles de la banque d'exercices du CE1 en les faisant échouer.

Les mutations portent sur une COPIE EN MÉMOIRE de la banque : les vrais fichiers
ne sont jamais touchés. Chaque cas porte le message qu'il doit déclencher, et le
banc refuse un cas qui échoue pour une autre raison — ou qui ne fait rien échouer
du tout.

Un témoin est joué d'abord, sur la banque réelle : sans lui, un contrôle qui
refuserait tout passerait le banc.

CE QUE CE BANC NE PEUT PAS PROUVER : la qualité pédagogique d'un exercice, et le
fait qu'un intrus soit plausible. Le contrôle des intrus ne voit que la forme.
"""

import copy
import importlib.util
import pathlib
import sys

RACINE = pathlib.Path(r"C:\Users\mchik\WorkBuddy AI\2026-09-21-15-03-17")
ICI = RACINE / "outils"


def charger_module(nom, cle=None):
    spec = importlib.util.spec_from_file_location(cle or nom.replace(".py", "").replace("-", "_"),
                                                  ICI / nom)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VE = charger_module("verifier-exercices.py")
VE_CTX = VE.contexte_ce1()


def messages(d):
    """Toutes les erreurs que la banque déclenche, dans une copie de contexte."""
    ctx = dict(VE_CTX)
    ctx["limites"] = []
    ids, _, mec_emp, cons_emp, e_ex = VE.controler_exercices(d, ctx)
    _, _, e_bes = VE.controler_besoins(d, ctx["unites"], ctx)
    e_usage = VE.controler_usage(d, ctx, mec_emp, cons_emp)
    return e_ex + e_bes + e_usage + ctx["limites"]


def exercice(d, ident):
    for e in d["exercices"]:
        if e["id"] == ident:
            return e
    raise SystemExit(f"exercice {ident} absent de la banque")


CAS = []


def cas(nom, attendu):
    def enveloppe(f):
        CAS.append((nom, attendu, f))
        return f
    return enveloppe


@cas("distinguer_type_bonne_inverse", "la question demande un texte « recit »")
def _(d):
    q = exercice(d, "E21")["questions"][0]
    q["bonne"], q["intrus"] = "L'air qui va", ["L'agneau de la reine", "Ni l'un ni l'autre"]


@cas("distinguer_type_intrus_du_meme_type", "est déclaré « recit » comme la bonne réponse")
def _(d):
    exercice(d, "E21")["questions"][0]["intrus"] = ["L'air qui va", "Le téléphone de papa"]


@cas("distinguer_type_bonne_pas_un_texte", "n'est le titre d'aucun texte court")
def _(d):
    exercice(d, "E21")["questions"][0]["bonne"] = "Le chat"


@cas("distinguer_type_question_sans_direction", "le contrôle ne peut pas conclure")
def _(d):
    exercice(d, "E21")["questions"][0]["question"] = "Touche le bon texte."


@cas("texte_court_inexistant", "n'existe pas dans contenu/textes-courts-ce1")
def _(d):
    exercice(d, "E21")["textes_courts"] = ["C01-rang16", "C99-rang01"]


@cas("texte_court_au_dela_du_rang", "au-delà de l'unité 16")
def _(d):
    exercice(d, "E21")["textes_courts"] = ["C01-rang16", "C03-rang27"]


@cas("texte_court_cite_deux_fois", "un texte court est cité deux fois")
def _(d):
    exercice(d, "E21")["textes_courts"] = ["C01-rang16", "C01-rang16"]


@cas("phrase_preuve_absente_des_textes_cites", "ne se trouve pas littéralement")
def _(d):
    exercice(d, "E21")["questions"][0]["phrase_preuve"] = "La reine a un agneau gris."


@cas("texte_court_cite_par_aucun_exercice", "cité par aucun exercice")
def _(d):
    e = exercice(d, "E55")
    e["textes_courts"] = [c for c in e["textes_courts"] if c != "C05-rang41"]


@cas("besoin_consolide_mais_orphelin", "consolidé mais déclaré par aucun exercice")
def _(d):
    d["besoins"] = list(d["besoins"]) + [{
        "id": "B16", "unite": 16,
        "manque": "un manque remis à la main",
        "detail": "ce besoin n'est déclaré par aucun exercice", "bloque": False,
    }]


# ---------------------------------------------------------------------------
# LES CAS RETROUVÉS. La banque avait été falsifiée une première fois, à la main,
# et cette falsification avait trouvé un vrai défaut : le contrôle d'usage lisait
# les déclarations dans le fichier d'origine au lieu de la banque qu'on lui
# passait, si bien qu'une mécanique AJOUTÉE lui échappait. Mais elle n'avait
# laissé aucun banc : rien ne pouvait la rejouer, et une falsification qu'on ne
# peut pas rejouer ne protège que le jour où elle a été faite. Les cas ci-dessous
# sont ceux qu'elle avait trouvés, écrits ici pour qu'ils le restent.
# ---------------------------------------------------------------------------

@cas("mecanique_declaree_jamais_employee", "déclarée et employée par aucun exercice")
def _(d):
    d["mecaniques"] = list(d["mecaniques"]) + [{
        "id": "mecanique_fantome",
        "libelle": "Une mécanique écrite et jamais employée",
        "ce_que_l_enfant_fait": "rien, aucun exercice ne l'emploie",
        "ce_que_l_application_fait": "rien non plus",
        "verdict": "app",
    }]


@cas("consigne_declaree_jamais_employee", "déclarée et employée par aucun exercice")
def _(d):
    d["consignes"] = list(d["consignes"]) + [{
        "id": "consigne_fantome", "texte": "Cette consigne ne sert à rien.",
        "picto": "aucun", "besoin_id": "B01a",
    }]


@cas("question_illisible_a_l_unite", "illisible à l'unité 16")
def _(d):
    exercice(d, "E21")["questions"][0]["question"] = "Fais attention."


@cas("texte_adosse_au_dela_de_l_unite", "au-delà de l'unité 5")
def _(d):
    exercice(d, "E10")["texte"] = "T17-rang33"


@cas("bonne_reponse_parmi_les_intrus", "la bonne réponse est aussi un intrus")
def _(d):
    q = exercice(d, "E21")["questions"][0]
    q["intrus"] = [q["bonne"], "L'air qui va"]


@cas("question_sans_mauvaise_reponse", "sans mauvaise réponse ne mesure rien")
def _(d):
    exercice(d, "E21")["questions"][0]["intrus"] = []


@cas("champ_de_question_manquant", "champ(s) manquant(s) ['phrase_preuve']")
def _(d):
    del exercice(d, "E21")["questions"][0]["phrase_preuve"]


@cas("pseudo_mot_qui_ne_se_resout_pas", "ne se résout pas")
def _(d):
    exercice(d, "E42")["pseudo_mots"] = ["pm01", "pm02", "pm03", "pm04", "pm99"]


@cas("aucun_pseudo_mot_complexe", "n'est complexe")
def _(d):
    exercice(d, "E42")["pseudo_mots"] = ["pm01", "pm02", "pm03", "pm04"]


@cas("graphie_inconnue_de_la_table", "n'est déclarée par aucune unité de cgp-ce1")
def _(d):
    exercice(d, "E04")["graphies"] = ["ai", "ei", "è", "ê", "xx"]


def main():
    d_reelle = VE_CTX["banque"]
    restes = messages(d_reelle)
    if restes:
        print("TÉMOIN ROUGE — la banque réelle déclenche des erreurs :")
        for m in restes:
            print(f"  {m}")
        return 1
    print("Témoin : la banque réelle passe les contrôles")

    rates, vus = [], []
    for nom, attendu, mutation in CAS:
        d = copy.deepcopy(d_reelle)
        mutation(d)
        sortie = messages(d)
        if not sortie:
            rates.append((nom, attendu, "le contrôle n'a RIEN vu"))
        elif not any(attendu in m for m in sortie):
            rates.append((nom, attendu, "\n".join(sortie)))
        else:
            vus.append(nom)

    if rates:
        print(f"\n{len(rates)} cas raté(s) :")
        for nom, attendu, sortie in rates:
            print(f"\n--- {nom} : attendu « {attendu} »")
            print(sortie[:1200])
        return 1

    print(f"{len(vus)} banques fausses et 1 témoin : {len(vus) + 1} essais, tous vus — "
          f"les contrôles de la banque ont des dents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
