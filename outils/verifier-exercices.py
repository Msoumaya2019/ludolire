"""Contrôle la banque d'exercices d'une tranche : GS ou CE1.

Ce qui est vérifié ici ne se voit pas à l'oeil :

  - toutes les unités de la progression sont servies par au moins un exercice —
    une unité sans exercice est un objectif qu'on annonce et qu'on n'entraîne pas ;
  - un exercice déclaré « app » n'emploie pas une mécanique que l'application ne
    sait pas juger : sans quoi on annonce un verdict qu'on ne peut pas rendre ;
  - les mots, phonèmes et lettres cités existent réellement, et les affiches sont
    des mots effectivement illustrés ;
  - l'accord entre les besoins déclarés et la liste consolidée est vérifié DANS
    LES DEUX SENS. Un besoin déclaré sans entrée consolidée est un manque qu'on
    ne retrouve nulle part ; une entrée sans déclarant est une entrée périmée.
    N'écrire qu'un sens est exactement la façon dont on oublie la moitié.

CE QUI CHANGE D'UNE TRANCHE À L'AUTRE, et pourquoi le même fichier les contrôle :

  - LA CONSIGNE. À la GS, les consignes viennent d'un corpus audio enregistré
    (`corpus-gs.json`) ; au CE1, elles sont déclarées par la banque elle-même,
    avec le texte qui sert de script d'enregistrement. Contrôler les deux avec le
    même code oblige à dire lequel des deux on contrôle — et c'est ce que fait
    `source_consignes`.
  - LE MATÉRIEL MOT. À la GS, un mot est valide s'il est dans `mots-gs.json`. Au
    CE1, un mot est valide s'il est DÉCHIFFRABLE au rang de son unité, et c'est le
    décodeur du CE1 qui le dit. La règle n'est plus la même, l'exigence si.
  - CE QUE L'ENFANT LIT. Un exercice du CE1 fait lire des questions et des
    réponses : elles sont contrôlées mot à mot comme la série. Une option qu'on ne
    peut pas lire est une option qui n'existe pas.
  - LA PHRASE-PREUVE. Une question de compréhension porte la phrase du texte qui
    prouve sa réponse, et le contrôle vérifie qu'elle s'y trouve LITTÉRALEMENT.

CE QUI N'EST PAS VÉRIFIÉ, et il faut le dire : la qualité pédagogique d'un
exercice, la justesse de sa difficulté, et le fait qu'un intrus soit vraiment
plausible. Le contrôle des intrus ne voit que la forme — non vide, distinct de la
bonne réponse — et la plausibilité reste un jugement.

Usage :
    python verifier-exercices.py            # la tranche GS
    python verifier-exercices.py --ce1      # la tranche CE1
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent

# Les champs obligatoires d'un exercice. Le champ `source` et le champ
# `besoin_id` s'ajoutent aux exercices concernés. La liste est CLOSE : une clé
# qui n'y figure pas est refusée, et c'est ainsi qu'une faute de frappe
# (`ne_verifies_pas`) se voit au lieu de dormir dans le fichier.
OBLIGATOIRES = {
    "id", "unite", "mecanique", "titre", "consigne", "geste", "serie", "mots",
    "affiches", "phonemes", "lettres", "verdict", "substitution", "inversion",
    "pourquoi_hors_app", "duree_s", "entraine", "ne_verifie_pas",
}
FACULTATIFS_GS = {"source", "besoin_id"}
# Le CE1 ajoute cinq champs : le texte adossé, ses questions avec leur
# phrase-preuve, les textes courts portés par l'exercice, les pseudo-mots, et les
# graphies manipulées (multi-lettres, que le champ `lettres` ne peut pas porter).
FACULTATIFS_CE1 = FACULTATIFS_GS | {
    "texte", "questions", "textes_courts", "pseudo_mots", "graphies",
}

CHAMPS_META_GS = (
    "titre", "version", "date", "role", "source_progression", "source_consignes",
    "source_mots", "regle_de_contenu", "regle_du_geste", "ce_que_la_banque_ne_regle_pas",
    "les_deux_champs_de_production",
)
CHAMPS_META_CE1 = (
    "titre", "version", "date", "role", "source_progression", "source_textes",
    "source_mots", "regle_de_contenu", "regle_du_geste", "regle_des_distracteurs",
    "ce_que_la_banque_ne_regle_pas", "les_deux_champs_de_production",
    "le_champ_phrase_preuve", "les_consignes_du_ce1", "les_textes_courts",
    "les_illustrations_du_ce1", "les_images_de_recit",
)
CHAMPS_MECANIQUE = ("libelle", "ce_que_l_enfant_fait", "ce_que_l_application_fait")
CHAMPS_CORRECTION = ("objet", "defaut", "correction", "pourquoi_c_est_grave")
CHAMPS_BESOIN = ("id", "unite", "manque", "detail", "bloque")
CHAMPS_QUESTION = ("question", "bonne", "intrus", "phrase_preuve")
CHAMPS_CONSIGNE = ("id", "texte", "picto")

JEU = "outils/jeu-syllabes.json"
ID_EXERCICE = re.compile(r"^E\d{2}$")
ID_BESOIN = re.compile(r"^B(\d{2})[a-z]?$")
MOT = re.compile(r"[A-Za-zÀ-ÿœŒ]+")


def charger(nom):
    return json.loads((ICI / nom).read_text(encoding="utf-8"))


def charger_module(nom):
    spec = importlib.util.spec_from_file_location(nom.replace(".py", "").replace("-", "_"),
                                                  ICI / nom)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Le contexte d'une tranche
# ---------------------------------------------------------------------------
def contexte_gs():
    d = charger("exercices-gs.json")
    prog = charger("progression-gs.json")
    corpus = charger("corpus-gs.json")
    jeu = charger("jeu-syllabes.json")
    images = charger("images-gs.json")
    production, e_prog = controler_progression(prog)
    ctx = {
        "nom": "GS",
        "banque": d,
        "unites": {u["rang"] for u in prog["unites"]},
        "production": production,
        "erreurs_progression": e_prog,
        "mots": {m["mot"] for m in charger("mots-gs.json")["mots"]},
        "illustres": {i["mot"] for i in images["items"]},
        "phonemes": {p["api"] for p in corpus["phonemes"]},
        "alphabet": {l["lettre"] for l in corpus["lettres"]},
        "consignes": {c["slug"] for c in corpus["consignes"]},
        "source_consignes": "corpus-gs.json",
        "champs_meta": CHAMPS_META_GS,
        "facultatifs": FACULTATIFS_GS,
        "besoins": {b["id"] for b in d["besoins"] if "id" in b},
        "jeu_mots": {i["mot"] for i in jeu["items"]},
        "jeu_unites": set(jeu["mecanique"]["sert_les_unites"]),
        # Deux consignes distinctes, et la distinction est la règle : celle qui
        # NOMME la lettre exige un nom enregistré, celle qui fait entendre le SON
        # exige un phonème enregistré. Les confondre interdirait `é` là où il est
        # légitime, ou l'autoriserait là où il ne l'est pas.
        "consignes_a_nom": {"touche_lettre_nom", "touche_lettres_ordre", "nomme_lettre"},
        "consignes_a_son": {"touche_lettre_son"},
    }
    ctx["mecaniques"] = {m["id"]: m["verdict"] for m in d["mecaniques"]}
    return ctx


def contexte_ce1():
    d = charger("exercices-ce1.json")
    prog = charger("progression-ce1.json")
    corpus = charger("corpus-gs.json")
    images = charger("images-gs.json")
    vt = charger_module("verifier-textes.py")
    vc = charger_module("verifier-textes-ce1.py")
    cp = charger("cgp-cp.json")
    ce1 = charger("cgp-ce1.json")
    # Le corpus des textes courts est lu depuis SON dossier : c'est lui qui porte
    # le rang, le type et le titre, et la banque ne fait que le citer. Le lire
    # dans la banque serait lire une copie — et c'est la copie qui avait divergé.
    vtc = charger_module("verifier-textes-courts-ce1.py")
    # Les pseudo-mots, même principe : c'est le corpus qui porte la suite, ses
    # graphies et sa complexité, et la banque ne fait que citer un identifiant.
    # Les lire dans la banque serait lire une copie — et c'est la copie qui avait
    # divergé : les deux exercices de l'unité 35 portaient la même liste de cinq.
    vpm = charger_module("verifier-pseudo-mots.py")
    production, e_prog = controler_progression(prog)

    # Les textes de la tranche : leur rang est déclaré DANS le texte, comme pour
    # le contrôle de déchiffrabilité. Le redonner ici serait une seconde source
    # de la même vérité, et elle divergerait.
    textes = {}
    dossier = RACINE / "contenu" / "textes-ce1"
    for chemin in sorted(dossier.glob("*.txt")):
        contenu = chemin.read_text(encoding="utf-8")
        m = re.search(r"^#\s*rang\s*:\s*(\d+)", contenu, re.M)
        textes[chemin.stem] = {
            "rang": int(m.group(1)) if m else None,
            "contenu": contenu,
        }

    ctx = {
        "nom": "CE1",
        "banque": d,
        "unites": {u["rang"] for u in prog["unites"]},
        "production": production,
        "erreurs_progression": e_prog,
        "illustres": {i["mot"] for i in images["items"]},
        "phonemes": {p["api"] for p in corpus["phonemes"]},
        "alphabet": {l["lettre"] for l in corpus["lettres"]},
        "consignes": {c["id"] for c in d.get("consignes", []) if "id" in c},
        "consignes_declarees": {c["id"]: c for c in d.get("consignes", []) if "id" in c},
        "source_consignes": "la banque elle-même (le texte de la consigne est le script de l'enregistrement)",
        "champs_meta": CHAMPS_META_CE1,
        "facultatifs": FACULTATIFS_CE1,
        "besoins": {b["id"] for b in d["besoins"] if "id" in b},
        "textes": textes,
        "courts": {
            nom: {
                "rang": (int(t["meta"]["rang"])
                         if str(t["meta"].get("rang", "")).isdigit() else None),
                "type": t["meta"].get("type"),
                "titre": t["titre"],
                "contenu": t["contenu"],
            }
            for nom, t in vtc.lire_courts().items()
        },
        "normaliser": vtc.normaliser,
        "pseudo_mots": vpm.lire_corpus()[1],
        "limites": [],
        "graphies": set(vc.GRAPHEMES_CE1) | set(vc.GRAPHEMES_POSITIONNELS),
        "decouper": vc.decouper_ce1,
        "controler_mot": vc.controler_mot,
        "lignes_du_texte": vc.lignes_du_texte,
        "largeur_ligne": vc.LARGEUR_LIGNE,
        "cp": cp,
        "ce1": ce1,
        "exceptions": vc.exceptions_prononcees(ce1),
        "sans_son": vc.lettres_sans_son(ce1),
        "ent_nasal": vc.mots_en_ent_nasal(ce1),
        "declarees": vc.correspondances_declarees(ce1),
        "consignes_a_nom": set(),
        "consignes_a_son": set(),
    }
    ctx["mecaniques"] = {m["id"]: m["verdict"] for m in d["mecaniques"]}
    # Les mots mémorisés changent à chaque rang, et le contrôle les demande pour
    # chaque unité : la table est calculée une fois, pas une fois par mot.
    ctx["mots_memorises"] = {
        r: vc.mots_ecartes(cp, ce1, r) for r in sorted(ctx["unites"])
    }
    ctx["vc"] = vc
    return ctx


def mot_est_lisible(ctx, mot, rang):
    """Au CE1, un mot est valide s'il est déchiffrable au rang de son unité."""
    if mot in ctx["mots_memorises"].get(rang, {}):
        return None
    autorisees = ctx["vc"].cgp_autorisees(ctx["cp"], ctx["ce1"], rang)
    p, inc = ctx["controler_mot"](
        mot, rang, autorisees, ctx["exceptions"], ctx["sans_son"],
        ctx["ent_nasal"], ctx["declarees"]
    )
    for m, g, raison in p + inc:
        return raison
    return None


# ---------------------------------------------------------------------------
# Les contrôles
# ---------------------------------------------------------------------------
def controler_progression(prog):
    """Chaque unité dit si son objectif porte une production.

    C'est le seul champ de la progression dont dépend le verdict d'un exercice.
    S'il manque, le contrôle des inversions ne porte plus sur rien — et un
    contrôle qui ne porte sur rien est vert.
    """
    erreurs = []
    production = {}
    for u in prog["unites"]:
        if not isinstance(u.get("production"), bool):
            erreurs.append(
                f"unité {u['rang']} : `production` = {u.get('production')!r}, "
                f"booléen attendu — sans lui le contrôle des inversions est aveugle"
            )
            continue
        production[u["rang"]] = u["production"]
    if not any(production.values()):
        erreurs.append("progression : aucune unité déclarée de production — la table a perdu son axe")
    return production, erreurs


def controler_meta(d, ctx):
    erreurs = []
    meta = d.get("meta", {})
    for cle in ctx["champs_meta"]:
        if not str(meta.get(cle, "")).strip():
            erreurs.append(f"meta : le champ `{cle}` est absent ou vide")
    inconnues = sorted(set(meta) - set(ctx["champs_meta"]))
    for cle in inconnues:
        erreurs.append(f"meta : champ inattendu `{cle}`")
    return erreurs


def controler_mecaniques(d, ctx):
    """Une mécanique dit ce que l'enfant fait ET ce que l'application fait."""
    erreurs = []
    vus = set()
    for m in d["mecaniques"]:
        i = m.get("id", "?")
        if i in vus:
            erreurs.append(f"mécanique « {i} » : identifiant en double")
        vus.add(i)
        for cle in CHAMPS_MECANIQUE:
            if not str(m.get(cle, "")).strip():
                erreurs.append(f"mécanique « {i} » : `{cle}` absent ou vide")
        if m.get("verdict") not in ("app", "hors app"):
            erreurs.append(f"mécanique « {i} » : verdict « {m.get('verdict')} » inconnu")
        if m.get("verdict") == "hors app" and not str(m.get("ce_que_l_application_fait", "")).strip():
            erreurs.append(f"mécanique « {i} » : déclarée hors app sans dire ce que l'app fait")
    return vus, erreurs


def controler_consignes(d, ctx):
    """La consigne existe — dans le corpus audio à la GS, dans la banque au CE1."""
    erreurs = []
    if ctx["nom"] != "CE1":
        return erreurs
    vus = set()
    for c in d.get("consignes", []):
        manquants = [k for k in CHAMPS_CONSIGNE if not str(c.get(k, "")).strip()]
        if manquants:
            erreurs.append(f"consigne {c.get('id', '?')} : champ(s) vide(s) {manquants}")
            continue
        if c["id"] in vus:
            erreurs.append(f"consigne « {c['id']} » : identifiant en double")
        vus.add(c["id"])
        if "besoin_id" in c and c["besoin_id"] not in ctx["besoins"]:
            erreurs.append(f"consigne « {c['id']} » : besoin « {c['besoin_id']} » absent de la liste")
    return erreurs


def controler_exercices(d, ctx):
    """Chaque exercice tient debout seul, et dit vrai sur ce qu'il est."""
    erreurs = []
    vus = set()
    verdicts = {"app": 0, "hors app": 0}
    mecaniques_employees = set()
    consignes_employees = set()

    for e in d["exercices"]:
        i = e.get("id", "?")
        if i in vus:
            erreurs.append(f"{i} : identifiant en double")
        vus.add(i)
        if not ID_EXERCICE.match(str(i)):
            erreurs.append(f"{i} : identifiant non conforme (E suivi de deux chiffres attendu)")

        inconnues = set(e) - OBLIGATOIRES - ctx["facultatifs"]
        if inconnues:
            erreurs.append(f"{i} : champ(s) inattendu(s) {sorted(inconnues)}")
        manquants = OBLIGATOIRES - set(e)
        if manquants:
            erreurs.append(f"{i} : champ(s) obligatoire(s) manquant(s) {sorted(manquants)}")
            continue

        unite = e["unite"]
        if unite not in ctx["unites"]:
            erreurs.append(f"{i} : unité {unite} absente de la progression")

        for cle in ("titre", "geste", "entraine", "ne_verifie_pas"):
            if not str(e[cle]).strip():
                erreurs.append(f"{i} : `{cle}` vide")

        # Le verdict. Un exercice « app » doit pouvoir être jugé par la machine,
        # et le déclarer sans le pouvoir est la faute la plus coûteuse : elle
        # promet une vérification qui n'aura pas lieu.
        verdict = e["verdict"]
        if verdict not in verdicts:
            erreurs.append(f"{i} : verdict « {verdict} » inconnu")
        else:
            verdicts[verdict] += 1

        mec = e["mecanique"]
        if mec is None:
            if verdict != "hors app":
                erreurs.append(
                    f"{i} : déclaré « {verdict} » sans mécanique — on ne dit pas "
                    f"comment l'application le jugerait"
                )
        elif mec not in ctx["mecaniques"]:
            erreurs.append(f"{i} : mécanique « {mec} » absente de la liste")
        else:
            mecaniques_employees.add(mec)
            vm = ctx["mecaniques"][mec]
            if vm == "hors app" and verdict != "hors app":
                erreurs.append(
                    f"{i} : déclaré « {verdict} » alors que sa mécanique « {mec} » "
                    f"est déclarée hors app — le verdict promet plus que la mécanique"
                )
            if vm == "app" and verdict == "app" and not e["consigne"]:
                erreurs.append(f"{i} : mécanique « {mec} » mais aucune consigne")

        consigne = e["consigne"]
        if consigne is None:
            if verdict != "hors app":
                erreurs.append(f"{i} : déclaré « {verdict} » sans consigne")
        elif consigne not in ctx["consignes"]:
            erreurs.append(f"{i} : consigne « {consigne} » absente de {ctx['source_consignes']}")
        else:
            consignes_employees.add(consigne)

        if verdict == "hors app":
            if not str(e["pourquoi_hors_app"] or "").strip():
                erreurs.append(f"{i} : hors app sans `pourquoi_hors_app`")
            if not str(e["substitution"] or "").strip():
                erreurs.append(
                    f"{i} : hors app sans `substitution` — l'absence de jumeau "
                    f"réceptif se déclare (« aucune »), elle ne se tait pas"
                )
        else:
            for cle in ("pourquoi_hors_app", "substitution"):
                if e[cle] is not None:
                    erreurs.append(f"{i} : déclaré « {verdict} » mais `{cle}` est rempli")

        # L'unité demande-t-elle une production que la machine ne peut pas
        # entendre ? Si oui et que l'exercice est jugé par l'app, il doit dire ce
        # que le geste reprend à la place. C'est le seul endroit où la banque
        # avoue qu'un objectif du programme n'est pas atteint par l'exercice qui
        # le couvre — et le taire ferait passer un objectif non entraîné pour un
        # objectif entraîné.
        if verdict == "app" and ctx["production"].get(unite):
            if not str(e["inversion"] or "").strip():
                erreurs.append(
                    f"{i} : l'unité {unite} porte un objectif de production, et "
                    f"l'exercice est déclaré « app » sans `inversion` — on ne dit pas "
                    f"ce que le geste reprend à la place de la production"
                )
        elif verdict == "app" and not ctx["production"].get(unite):
            if str(e["inversion"] or "").strip():
                erreurs.append(
                    f"{i} : `inversion` rempli alors que l'unité {unite} ne porte "
                    f"aucun objectif de production"
                )

        duree = e["duree_s"]
        if not isinstance(duree, int) or duree < 0:
            erreurs.append(f"{i} : `duree_s` = {duree!r}, entier positif attendu")
        elif verdict == "app" and duree == 0:
            erreurs.append(f"{i} : déclaré « app » avec une durée nulle")

        serie = e["serie"]
        if verdict == "app" and not serie:
            erreurs.append(f"{i} : déclaré « app » sans contenu à jouer")

        erreurs += controler_materiel(e, i, unite, ctx)
        erreurs += controler_questions(e, i, unite, ctx)
        erreurs += controler_distinguer_type(e, i, ctx)

        if "besoin_id" in e and e["besoin_id"] not in ctx["besoins"]:
            erreurs.append(f"{i} : besoin « {e['besoin_id']} » absent de la liste consolidée")

    return vus, verdicts, mecaniques_employees, consignes_employees, erreurs


def controler_materiel(e, i, unite, ctx):
    """Le matériel. Une image ne s'affiche que si elle existe, un mot se lit."""
    erreurs = []
    for mot in e["mots"]:
        if ctx["nom"] == "GS":
            if mot not in ctx["mots"]:
                erreurs.append(f"{i} : le mot « {mot} » est absent du corpus GS")
        else:
            raison = mot_est_lisible(ctx, mot, unite)
            if raison:
                erreurs.append(
                    f"{i} : le mot « {mot} » n'est pas déchiffrable à l'unité {unite} ({raison})"
                )
    if len(set(e["mots"])) != len(e["mots"]):
        erreurs.append(f"{i} : un mot est cité deux fois")
    for mot in e["affiches"]:
        if mot not in e["mots"]:
            erreurs.append(f"{i} : l'affiche « {mot} » n'est pas dans `mots`")
        if mot not in ctx["illustres"]:
            erreurs.append(f"{i} : l'affiche « {mot} » n'est pas un mot illustré")
    for ph in e["phonemes"]:
        if ph not in ctx["phonemes"]:
            erreurs.append(f"{i} : le phonème {ph} n'est pas enregistré au corpus")
    for lettre in e["lettres"]:
        if len(lettre) != 1 or lettre != lettre.lower():
            erreurs.append(f"{i} : « {lettre} » n'est pas une lettre minuscule seule")
        elif lettre not in ctx["alphabet"] and e["consigne"] in ctx["consignes_a_nom"]:
            erreurs.append(
                f"{i} : la consigne « {e['consigne']} » nomme la lettre, or « {lettre} » "
                f"n'a pas de nom enregistré — une consigne qui nomme exige le nom"
            )
    # Une consigne qui fait entendre le son suppose qu'il y a un son à faire
    # entendre.
    if e["consigne"] in ctx["consignes_a_son"] and not e["phonemes"]:
        erreurs.append(
            f"{i} : consigne « {e['consigne']} » sans aucun phonème déclaré — "
            f"l'application n'aurait rien à faire entendre"
        )
    return erreurs


def controler_questions(e, i, unite, ctx):
    """Ce que l'enfant lit : les questions, les réponses, et la preuve."""
    erreurs = []
    if ctx["nom"] != "CE1":
        return erreurs

    # Les graphies manipulées : elles doivent être déclarées par la table, sinon
    # le décodeur ne les connaît pas et l'exercice porte sur une graphie que
    # personne n'enseigne.
    for g in e.get("graphies", []):
        if g not in ctx["graphies"]:
            erreurs.append(f"{i} : la graphie « {g} » n'est déclarée par aucune unité de cgp-ce1")

    # Le texte adossé : il doit exister, et son rang ne peut pas dépasser celui
    # de l'unité. Un texte qu'on ne peut pas encore lire ne peut pas porter une
    # question.
    texte = e.get("texte")
    if texte is not None:
        if texte not in ctx["textes"]:
            erreurs.append(f"{i} : le texte « {texte} » n'existe pas dans contenu/textes-ce1")
        else:
            rang_texte = ctx["textes"][texte]["rang"]
            if rang_texte is None:
                erreurs.append(f"{i} : le texte « {texte} » ne déclare pas son rang")
            elif rang_texte > unite:
                erreurs.append(
                    f"{i} : le texte « {texte} » est au rang {rang_texte}, au-delà de "
                    f"l'unité {unite} — l'enfant ne peut pas encore le lire"
                )

    # LES TEXTES COURTS SONT CITÉS, PAS PORTÉS. La banque nomme le fichier, et
    # c'est le corpus qui porte le rang, le type et le titre. La lisibilité et la
    # longueur se contrôlent là-bas, une fois pour toutes : les contrôler ici
    # aussi serait deux règles pour la même chose, et elles divergeraient.
    textes_courts = e.get("textes_courts", [])
    if len(set(textes_courts)) != len(textes_courts):
        erreurs.append(f"{i} : un texte court est cité deux fois")
    contenus_courts = []
    for nom in textes_courts:
        if nom not in ctx["courts"]:
            erreurs.append(
                f"{i} : le texte court « {nom} » n'existe pas dans contenu/textes-courts-ce1"
            )
            continue
        court = ctx["courts"][nom]
        contenus_courts.append(court["contenu"])
        if court["rang"] is None:
            erreurs.append(f"{i} : le texte court « {nom} » ne déclare pas son rang")
        elif court["rang"] > unite:
            erreurs.append(
                f"{i} : le texte court « {nom} » est au rang {court['rang']}, au-delà de "
                f"l'unité {unite} — l'enfant ne peut pas encore le lire"
            )

    # LES PSEUDO-MOTS SONT CITÉS, PAS PORTÉS — même règle que les textes courts.
    # La banque nomme l'identifiant ; le corpus porte la suite, ses graphies et sa
    # complexité. Ce qui se contrôle ici est ce qui dépend de l'unité, et rien
    # d'autre : que la suite existe, qu'elle soit déchiffrable au rang de l'unité,
    # et que l'exercice porte au moins une suite COMPLEXE. L'objectif de l'unité
    # 35 est de décoder des pseudo-mots COMPLEXES, et une suite faite des seules
    # correspondances du CP n'entraîne rien de ce que le CE1 ajoute. Le reste —
    # que la suite ne soit pas déjà un mot de l'application, qu'elle ne se lise
    # pas comme un mot connu — se contrôle dans le corpus, une fois pour toutes.
    pseudo_mots = e.get("pseudo_mots", [])
    if len(set(pseudo_mots)) != len(pseudo_mots):
        erreurs.append(f"{i} : un pseudo-mot est cité deux fois")
    complexes = 0
    for pid in pseudo_mots:
        entree = ctx["pseudo_mots"].get(pid)
        if entree is None:
            erreurs.append(
                f"{i} : le pseudo-mot « {pid} » ne se résout pas dans "
                f"outils/pseudo-mots-ce1.json — un identifiant qui ne se résout pas est "
                f"une suite que l'application n'aura pas à faire entendre"
            )
            continue
        if entree.get("complexite") == "complexe":
            complexes += 1
        raison = mot_est_lisible(ctx, entree["mot"], unite)
        if raison:
            erreurs.append(
                f"{i} : le pseudo-mot « {entree['mot']} » ({pid}) n'est pas déchiffrable "
                f"à l'unité {unite} ({raison})"
            )
    if pseudo_mots and complexes == 0:
        erreurs.append(
            f"{i} : aucun des {len(pseudo_mots)} pseudo-mots cités n'est complexe — "
            f"l'objectif de l'unité est de décoder des pseudo-mots complexes, et une "
            f"suite faite des seules correspondances du CP n'entraîne rien du CE1"
        )

    for k, q in enumerate(e.get("questions", [])):
        manquants = [c for c in CHAMPS_QUESTION if c not in q]
        if manquants:
            erreurs.append(f"{i} question n° {k + 1} : champ(s) manquant(s) {manquants}")
            continue
        inconnues = sorted(set(q) - set(CHAMPS_QUESTION))
        if inconnues:
            erreurs.append(f"{i} question n° {k + 1} : champ(s) inattendu(s) {inconnues}")
        if not str(q["question"]).strip() or not str(q["bonne"]).strip():
            erreurs.append(f"{i} question n° {k + 1} : `question` ou `bonne` vide")
        intrus = q["intrus"]
        if not isinstance(intrus, list) or not intrus:
            erreurs.append(
                f"{i} question n° {k + 1} : `intrus` doit être une liste non vide — "
                f"une question sans mauvaise réponse ne mesure rien"
            )
        else:
            if q["bonne"] in intrus:
                erreurs.append(f"{i} question n° {k + 1} : la bonne réponse est aussi un intrus")
            if len(set(intrus)) != len(intrus):
                erreurs.append(f"{i} question n° {k + 1} : un intrus est cité deux fois")

        # LA PHRASE-PREUVE, ET C'EST LE CONTRÔLE CENTRAL DES QUESTIONS. Une
        # question de compréhension ne vaut que si l'on peut montrer où le texte
        # le dit : la phrase est cherchée LITTÉRALEMENT, dans le texte adossé ou
        # dans l'un des textes courts portés par l'exercice.
        preuve = q["phrase_preuve"]
        sources = []
        if texte in ctx["textes"]:
            sources.append(ctx["textes"][texte]["contenu"])
        sources.extend(contenus_courts)
        if not any(preuve in s for s in sources):
            ou = texte if texte else f"les {len(textes_courts)} textes courts"
            erreurs.append(
                f"{i} question n° {k + 1} : la phrase-preuve « {preuve} » ne se trouve "
                f"pas littéralement dans {ou} — une preuve qu'on ne peut pas montrer "
                f"est une réponse qu'on ne peut pas défendre"
            )

        # Et l'enfant doit pouvoir LIRE la question et ses réponses.
        for champ in ("question", "bonne"):
            for mot in (m.lower() for m in MOT.findall(str(q[champ]))):
                raison = mot_est_lisible(ctx, mot, unite)
                if raison:
                    erreurs.append(
                        f"{i} question n° {k + 1} : `{champ}` emploie « {mot} », illisible "
                        f"à l'unité {unite} ({raison})"
                    )
        for reponse in intrus if isinstance(intrus, list) else []:
            for mot in (m.lower() for m in MOT.findall(str(reponse))):
                raison = mot_est_lisible(ctx, mot, unite)
                if raison:
                    erreurs.append(
                        f"{i} question n° {k + 1} : un intrus emploie « {mot} », illisible "
                        f"à l'unité {unite} ({raison})"
                    )
    return erreurs


def controler_distinguer_type(e, i, ctx):
    """Une question qui demande de distinguer un récit d'un documentaire a-t-elle
    la bonne réponse ?

    C'EST LE SEUL DÉFAUT DE CE MÉCANISME QUI NE SE VOIE NI DANS LE CODE NI DANS
    LES FICHIERS : une clé de réponse qui désigne le mauvais texte. Chaque image
    est conforme, chaque fichier existe, la phrase-preuve est bien dans un des
    textes — et l'exercice apprend l'inverse de ce qu'il annonce.

    Le type est déclaré par le texte court lui-même, et c'est ce qui rend la
    comparaison possible. La DIRECTION se lit dans la question : « qui raconte »
    demande un récit, « qui explique » demande un documentaire. Quand la question
    ne dit ni l'un ni l'autre, le contrôle ne conclut pas — et il le dit, plutôt
    que de laisser croire qu'il a vérifié.
    """
    if e.get("mecanique") != "distinguer_type":
        return []
    erreurs = []
    par_titre = {
        ctx["normaliser"](t["titre"]): nom
        for nom, t in ctx["courts"].items() if t["titre"]
    }
    for k, q in enumerate(e.get("questions", [])):
        question = ctx["normaliser"](str(q.get("question", "")))
        attendu = "recit" if "raconte" in question else (
            "informatif" if "explique" in question else None)
        if attendu is None:
            ctx["limites"].append(
                f"{i} question n° {k + 1} : la question ne dit ni « raconte » ni "
                f"« explique » — le contrôle ne peut pas conclure sur le type attendu"
            )
            continue
        nom = par_titre.get(ctx["normaliser"](str(q.get("bonne", ""))))
        if nom is None:
            erreurs.append(
                f"{i} question n° {k + 1} : la bonne réponse « {q.get('bonne')} » n'est le "
                f"titre d'aucun texte court — on ne peut pas vérifier qu'elle est du type "
                f"demandé"
            )
            continue
        if ctx["courts"][nom]["type"] != attendu:
            erreurs.append(
                f"{i} question n° {k + 1} : la question demande un texte « {attendu} », et la "
                f"bonne réponse « {q.get('bonne')} » est déclarée "
                f"« {ctx['courts'][nom]['type']} »"
            )
        for reponse in q.get("intrus", []):
            nom_i = par_titre.get(ctx["normaliser"](str(reponse)))
            if nom_i is None:
                continue
            if ctx["courts"][nom_i]["type"] == attendu:
                erreurs.append(
                    f"{i} question n° {k + 1} : l'intrus « {reponse} » est déclaré "
                    f"« {attendu} » comme la bonne réponse — deux textes du même type ne se "
                    f"distinguent pas"
                )
    return erreurs


def controler_usage(d, ctx, mecaniques_employees, consignes_employees):
    """Ce qui est déclaré et jamais employé est une promesse qu'on ne tient pas.

    LES DÉCLARATIONS SONT LUES DANS LA BANQUE, PAS DANS LE CONTEXTE. Une première
    version comparait l'emploi à `ctx["mecaniques"]` et `ctx["consignes"]`, deux
    ensembles construits une fois à partir du fichier. Le contrôle ne pouvait donc
    pas voir une déclaration AJOUTÉE à la banque — et c'est exactement le cas
    qu'il doit attraper : une mécanique qu'on vient d'écrire et dont on n'a pas
    encore écrit l'exercice. La falsification l'a montré : les deux fautes
    passaient inaperçues. Un contrôle qui lit sa matière ailleurs que dans ce
    qu'il contrôle ne contrôle rien.
    """
    erreurs = []
    if ctx["nom"] != "CE1":
        return erreurs
    declarees_mec = {m["id"] for m in d["mecaniques"] if "id" in m}
    for mec in sorted(declarees_mec - mecaniques_employees):
        erreurs.append(
            f"mécanique « {mec} » : déclarée et employée par aucun exercice — c'est une "
            f"promesse qu'on ne tient pas, ou un exercice qui a perdu sa mécanique"
        )
    declarees_cons = {c["id"] for c in d.get("consignes", []) if "id" in c}
    for consigne in sorted(declarees_cons - consignes_employees):
        erreurs.append(
            f"consigne « {consigne} » : déclarée et employée par aucun exercice — "
            f"c'est un enregistrement à faire pour rien"
        )
    # Et un texte court que personne ne cite est un texte écrit pour rien. Le
    # corpus est lu depuis son dossier, donc un fichier ajouté est vu au run
    # suivant — c'est la même exigence que pour les mécaniques et les consignes.
    employees_courts = set()
    for e in d["exercices"]:
        employees_courts.update(e.get("textes_courts", []))
    for nom in sorted(set(ctx["courts"]) - employees_courts):
        erreurs.append(
            f"texte court « {nom} » : déclaré dans le corpus et cité par aucun exercice — "
            f"un texte écrit pour rien"
        )
    return erreurs


def controler_couverture(d, unites):
    """Aucune unité sans exercice — et le dire unité par unité, pas en compte."""
    servies = {}
    for e in d["exercices"]:
        servies.setdefault(e["unite"], []).append(e["id"])
    erreurs = []
    for rang in sorted(unites):
        if rang not in servies:
            erreurs.append(f"unité {rang} : aucun exercice — l'objectif est annoncé, pas entraîné")
    orphelines = sorted(set(servies) - set(unites))
    for rang in orphelines:
        erreurs.append(f"unité {rang} : servie par {servies[rang]}, mais absente de la progression")
    return servies, erreurs


def controler_besoins(d, unites, ctx):
    """L'accord dans les deux sens entre besoins déclarés et besoins consolidés."""
    erreurs = []
    vus = set()
    for b in d["besoins"]:
        manquants = [c for c in CHAMPS_BESOIN if c not in b]
        if manquants:
            erreurs.append(f"besoin {b.get('id', '?')} : champ(s) manquant(s) {manquants}")
            continue
        i = b["id"]
        if i in vus:
            erreurs.append(f"besoin « {i} » : identifiant en double")
        vus.add(i)
        m = ID_BESOIN.match(i)
        if not m:
            erreurs.append(f"besoin « {i} » : identifiant non conforme (B + unité + suffixe)")
        elif int(m.group(1)) != b["unite"]:
            erreurs.append(
                f"besoin « {i} » : l'identifiant annonce l'unité {int(m.group(1))}, "
                f"le champ `unite` dit {b['unite']}"
            )
        if b["unite"] not in unites:
            erreurs.append(f"besoin « {i} » : unité {b['unite']} absente de la progression")
        for cle in ("manque", "detail"):
            if not str(b[cle]).strip():
                erreurs.append(f"besoin « {i} » : `{cle}` vide")
        if not isinstance(b["bloque"], bool):
            erreurs.append(f"besoin « {i} » : `bloque` = {b['bloque']!r}, booléen attendu")

    # Sens 1 — tout besoin déclaré a son entrée. Au CE1, une consigne DÉCLARE
    # aussi : elle porte le besoin de son enregistrement, et une consigne
    # jamais employée resterait sinon à enregistrer pour rien.
    declarees = set()
    for e in d["exercices"]:
        if "besoin_id" in e:
            declarees.add(e["besoin_id"])
    for c in d.get("consignes", []):
        if "besoin_id" in c:
            declarees.add(c["besoin_id"])

    # Sens 2 — toute entrée consolidée est déclarée par au moins un déclarant.
    for i in sorted(vus - declarees):
        erreurs.append(
            f"besoin « {i} » : consolidé mais déclaré par aucun exercice — "
            f"entrée périmée, ou exercice qui a perdu son besoin"
        )
    return vus, declarees, erreurs


def controler_corrections(d):
    erreurs = []
    for c in d["corrections"]:
        manquants = [k for k in CHAMPS_CORRECTION if not str(c.get(k, "")).strip()]
        if manquants:
            erreurs.append(
                f"correction « {str(c.get('objet', '?'))[:40]}… » : champ(s) vide(s) {manquants}"
            )
    return erreurs


def controler_jeu(d, ctx):
    """Un exercice adossé au jeu sert une unité que le jeu déclare servir."""
    erreurs = []
    for e in d["exercices"]:
        if e.get("source") != JEU:
            continue
        if e["unite"] not in ctx["jeu_unites"]:
            erreurs.append(
                f"{e['id']} : déclare servir l'unité {e['unite']} via {JEU}, "
                f"qui ne déclare servir que {sorted(ctx['jeu_unites'])}"
            )
        for mot in e["mots"]:
            if mot not in ctx["jeu_mots"]:
                erreurs.append(
                    f"{e['id']} : le mot « {mot} » n'est l'objet d'aucun item du jeu — "
                    f"l'exercice ne peut pas le montrer"
                )
    return erreurs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ce1", action="store_true", help="contrôle la tranche CE1")
    args = ap.parse_args()

    if args.ce1:
        ctx = contexte_ce1()
    else:
        ctx = contexte_gs()

    d = ctx["banque"]
    e_meta = controler_meta(d, ctx)
    mecaniques, e_mec = controler_mecaniques(d, ctx)
    e_cons = controler_consignes(d, ctx)
    ids, verdicts, mec_emp, cons_emp, e_ex = controler_exercices(d, ctx)
    servies, e_couv = controler_couverture(d, ctx["unites"])
    besoins, declarees, e_bes = controler_besoins(d, ctx["unites"], ctx)
    e_corr = controler_corrections(d)
    e_usage = controler_usage(d, ctx, mec_emp, cons_emp)
    e_jeu = controler_jeu(d, ctx) if ctx["nom"] == "GS" else []

    n = len(d["exercices"])
    n_prod = sum(1 for r, v in ctx["production"].items() if v)
    print(f"Tranche             : {ctx['nom']}")
    print(f"Exercices           : {n} ({verdicts['app']} jugés par l'app, "
          f"{verdicts['hors app']} hors app)")
    print(f"Mécaniques          : {len(mecaniques)}"
          + (f" ({len(mec_emp)} employées)" if ctx["nom"] == "CE1" else ""))
    if ctx["nom"] == "CE1":
        print(f"Consignes           : {len(ctx['consignes'])} déclarées, "
              f"{len(cons_emp)} employées")
    print(f"Unités servies      : {len(servies)} sur {len(ctx['unites'])}")
    print(f"Unités de production: {n_prod} sur {len(ctx['production'])}")
    print(f"Inversions          : {sum(1 for e in d['exercices'] if e['inversion'])}")
    print(f"Besoins             : {len(besoins)} consolidés, {len(declarees)} déclarés")
    print(f"  dont bloquants    : {sum(1 for b in d['besoins'] if b['bloque'])}")
    print(f"Corrections         : {len(d['corrections'])}")
    if ctx["nom"] == "CE1":
        textes = sorted({e["texte"] for e in d["exercices"] if e.get("texte")})
        questions = sum(len(e.get("questions", [])) for e in d["exercices"])
        cites = sorted({c for e in d["exercices"] for c in e.get("textes_courts", [])})
        pms = sorted({c for e in d["exercices"] for c in e.get("pseudo_mots", [])})
        print(f"Textes adossés      : {len(textes)} sur {len(ctx['textes'])}")
        print(f"Textes courts cités : {len(cites)} sur {len(ctx['courts'])}")
        print(f"Pseudo-mots cités   : {len(pms)} sur {len(ctx['pseudo_mots'])}")
        print(f"Questions           : {questions} avec leur phrase-preuve")
    doubles = {r: v for r, v in servies.items() if len(v) > 1}
    print(f"Unités à plusieurs exercices : {len(doubles)}")
    print(f"Durée totale des exercices   : {sum(e['duree_s'] for e in d['exercices'])} s")

    if ctx.get("limites"):
        print(f"\nOÙ LE CONTRÔLE S'ARRÊTE — {len(ctx['limites'])} cas non conclu(s) :")
        for l in ctx["limites"]:
            print(f"  {l}")

    erreurs = (ctx["erreurs_progression"] + e_meta + e_mec + e_cons + e_ex
               + e_couv + e_bes + e_corr + e_usage + e_jeu)
    if erreurs:
        print(f"\nNON CONFORME — {len(erreurs)} problème(s) :")
        for e in erreurs:
            print(f"  {e}")
        return 1
    print("\nRésultat : conforme")
    return 0


if __name__ == "__main__":
    sys.exit(main())
