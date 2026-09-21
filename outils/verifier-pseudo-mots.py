"""Contrôle du corpus des pseudo-mots du CE1, et de ce que la banque en fait.

Ce qui est vérifié ici ne se voit pas à l'oeil :

  - un pseudo-mot est DÉCHIFFRABLE à l'unité de l'exercice qui le cite — c'est
    toute la question de l'exercice, et un pseudo-mot trop complexe ne se décode
    pas, il se devine ;
  - il n'est le mot d'AUCUN corpus de l'application. C'est la crainte que B35
    déclare : une suite que l'enfant a déjà lue comme un mot n'est plus un
    pseudo-mot pour lui, et l'exercice lui demande alors de décider qu'un mot
    n'en est pas un ;
  - sa lecture mécanique n'est celle d'aucun mot du lexique de l'application,
    sans quoi l'exercice fait écouter ou lire un homophone d'un mot connu ;
  - chaque graphie déclarée est réellement dans la suite, et la complexité
    déclarée est celle que la table lui donne : une déclaration que rien ne
    vérifie est une décoration, pas une déclaration ;
  - deux exercices de la MÊME unité ne citent pas le même pseudo-mot. Sans cette
    règle, le second exercice se répond de mémoire au lieu de se décoder — et
    c'est ce que faisaient E42 et E43, qui portaient la même liste de cinq ;
  - un pseudo-mot que personne ne cite est une suite écrite pour rien ;
  - et les mots réels d'un exercice « vrai mot ou pas » sont des mots que
    l'application a déjà montrés : on ne peut pas demander de reconnaître un mot
    qu'on n'a jamais lu.

LA LECTURE EST DÉRIVÉE, PAS DÉCLARÉE. Elle est calculée graphie par graphie avec
`decouper_ce1` et `resoudre_ce1` — le décodeur du projet, celui-là même qui décide
si un texte est déchiffrable — puis chaque correspondance est lue dans la table
des phonèmes. La seule lettre muette admise est le e final. Déclarer la
prononciation à la main aurait produit des valeurs que rien n'aurait pu
vérifier ; la dériver la rend vérifiable, et c'est le script de l'enregistrement.

CE QUE CE CONTRÔLE NE PEUT PAS PROUVER : qu'une suite ne soit pas un mot
français. Il n'y a pas de lexique embarqué, et la limite est déclarée plus bas
plutôt que tue.

Usage :
    python verifier-pseudo-mots.py
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent

ID = re.compile(r"^pm\d{2}$")
MOT = re.compile(r"[A-Za-zÀ-ÿœŒ]+")
EXEMPLES_DU_PROGRAMME = ("doir", "stag", "choust", "valin", "cagnou")
CHAMPS = ("id", "mot", "graphies", "complexite", "origine")
COMPLEXITES = ("simple", "complexe")
ORIGINES = ("programme", "ecrit")
MIN_LETTRES = 3
MAX_LETTRES = 9

# UNE GRAPHIE QUI CONTIENT UNE VOYELLE DOIT RENDRE UNE SYLLABE.
#
# La table du CE1 déclare `/j/` pour huit graphies — ill, y, ail, eil, euil,
# ouille, aille, eille, euille — et `/j/` est une SEMI-CONSONNE : elle ne fait
# pas une syllabe. Ce n'est donc pas la lecture de ces graphies, c'est
# l'étiquette de la classe qu'elles forment — celle des graphies du /j/ en fin
# de mot. La lecture réelle se compose : `ail` vaut /aj/, `euille` /œj/, `ill`
# /ij/. Rien dans la table ne porte cette composition.
#
# La distinction avec `qu`, `gu` et `ge` n'est pas arbitraire : ces trois-là
# contiennent une voyelle et rendent `/k/`, `/g/`, `/ʒ/`, qui sont des
# consonnes pleines — la voyelle y est muette par convention, et la lecture est
# complète. Une graphie dont le phonème est UNE SEMI-CONSONNE SEULE, alors
# qu'elle contient une voyelle, est une étiquette de classe.
#
# Conséquence, et elle est déclarée : aucune suite bâtie sur ces huit graphies
# n'a de lecture dérivable, donc aucune ne peut entrer dans ce corpus — sans
# quoi la voix enregistrerait une prononciation que rien ne fonde. Le décodeur,
# lui, n'en souffre pas : il n'a jamais besoin du phonème pour dire si un texte
# est déchiffrable.
SEMI_CONSONNES = set("jwɥ")
VOYELLES_ECRITES = set("aeiouyàâäéèêëîïôöûüùœ")


def est_etiquette_de_classe(graphie, phoneme):
    """Vrai quand le phonème déclaré ne peut pas être la lecture de la graphie."""
    if phoneme is None:
        return False
    if not any(c in VOYELLES_ECRITES for c in graphie):
        return False
    return all(c in SEMI_CONSONNES for c in phoneme.strip("/"))

# La tranche dont on lit la lecture : le dernier rang de la progression CE1. La
# table des correspondances du CE1 s'arrête au rang 20, donc tous les rangs de
# la fin de la tranche donnent le même ensemble — mais le dire ici évite d'avoir
# à le redire ailleurs.
RANG_DE_LECTURE = 42


def charger(nom):
    return json.loads((ICI / nom).read_text(encoding="utf-8"))


def charger_module(nom, cle):
    spec = importlib.util.spec_from_file_location(cle, ICI / nom)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lire_corpus():
    """Le corpus, indexé par identifiant."""
    d = charger("pseudo-mots-ce1.json")
    return d, {p["id"]: p for p in d["pseudo_mots"] if "id" in p}


def tables():
    """Les correspondances : identifiant de CGP -> phonème, rang, tranche.

    Les deux tables sont lues ENSEMBLE et c'est voulu : une graphie que le CP
    enseigne et une que le CE1 ajoute peuvent porter le même identifiant, et
    c'est la table qui dit laquelle est laquelle. Une seule source pour les trois
    lectures, donc rien à faire diverger.
    """
    phonemes, rangs, tranches, erreurs = {}, {}, {}, []
    for nom, tranche in (("cgp-cp.json", "CP"), ("cgp-ce1.json", "CE1")):
        for u in charger(nom)["unites"]:
            cgp = (u.get("cgp") or [None])[0]
            if cgp is None:
                erreurs.append(
                    f"{nom} unité {u['rang']} : aucune correspondance déclarée — "
                    f"sa lecture ne peut pas être dérivée"
                )
                continue
            if cgp in phonemes and phonemes[cgp] != u.get("phoneme"):
                erreurs.append(
                    f"« {cgp} » : deux phonèmes déclarés, {phonemes[cgp]} et "
                    f"{u.get('phoneme')} — la lecture d'une suite cesserait d'être unique"
                )
                continue
            phonemes[cgp] = u.get("phoneme")
            rangs[cgp] = u["rang"]
            tranches[cgp] = tranche
    return phonemes, rangs, tranches, erreurs


def graphies_sans_lecture():
    """Les graphies dont la table déclare une étiquette de classe, pas une lecture.

    Elles sont rapportées, et c'est tout ce que le contrôle peut en dire : la
    lecture composée n'est nulle part dans la table, donc rien ne peut la
    dériver. Un pseudo-mot bâti sur l'une d'elles est refusé plus bas, parce
    qu'il faudrait inventer sa prononciation — et une prononciation inventée est
    exactement ce que la voix enregistrerait.
    """
    vues = []
    for nom in ("cgp-cp.json", "cgp-ce1.json"):
        for u in charger(nom)["unites"]:
            for g in u.get("graphies", []):
                if est_etiquette_de_classe(g, u.get("phoneme")) and g not in vues:
                    vues.append(g)
    return sorted(vues)


def lexique():
    """Tout ce que l'application donne à lire comme mot, avec sa provenance.

    Les pseudo-mots du corpus n'y entrent pas : ils ne sont pas des mots, et les
    y mettre ferait qu'un pseudo-mot se heurterait à lui-même.
    """
    sources = {}

    def ajouter(mot, provenance):
        if not mot:
            return
        sources.setdefault(mot.lower(), set()).add(provenance)

    for nom in ("mots-gs.json", "mots-cp.json"):
        for m in charger(nom)["mots"]:
            ajouter(m["mot"], nom)
            for s in m.get("syllabes", []):
                ajouter(s, f"{nom} (syllabe)")

    for it in charger("jeu-syllabes.json")["items"]:
        ajouter(it["mot"], "jeu-syllabes")
        for intr in it.get("intruses", []):
            ajouter(intr["syllabe"], "jeu-syllabes (intruse)")

    d = charger("corpus-gs.json")
    for p in d["phonemes"]:
        ajouter(p.get("mot"), "corpus-gs (mot porteur)")
    for c in d["consignes"] + d["retours"]:
        for m in MOT.findall(c.get("texte", "")):
            ajouter(m, "corpus-gs (consigne)")

    for nom in ("images-gs.json", "images-ce1.json", "images-recit-ce1.json"):
        for it in charger(nom).get("items", []):
            if "mot" in it:
                ajouter(it["mot"], nom)

    for dossier in ("textes", "textes-ce1", "textes-courts-ce1"):
        for f in sorted((RACINE / "contenu" / dossier).glob("*.txt")):
            for m in MOT.findall(f.read_text(encoding="utf-8")):
                ajouter(m, f"texte {dossier}/{f.name}")

    for nom in ("exercices-gs.json", "exercices-ce1.json"):
        d = charger(nom)
        for e in d.get("exercices", []):
            for m in e.get("mots", []) + e.get("affiches", []):
                ajouter(m, f"{nom} {e.get('id')} (mot)")
            for s in e.get("serie", []):
                for m in MOT.findall(str(s)):
                    ajouter(m, f"{nom} {e.get('id')} (série)")
            for q in e.get("questions", []):
                for champ in ("question", "bonne"):
                    for m in MOT.findall(str(q.get(champ, ""))):
                        ajouter(m, f"{nom} {e.get('id')} (question)")
                for i in q.get("intrus", []):
                    for m in MOT.findall(str(i)):
                        ajouter(m, f"{nom} {e.get('id')} (intrus)")
        for c in d.get("consignes", []):
            for m in MOT.findall(str(c.get("texte", ""))):
                ajouter(m, f"{nom} (consigne)")

    for nom in ("progression-gs.json", "progression-ce1.json"):
        for u in charger(nom).get("unites", []):
            for champ in ("exemple", "action", "objectif", "observation"):
                for m in MOT.findall(str(u.get(champ, ""))):
                    ajouter(m, f"{nom} (exemple)")

    return sources


def lecture_mecanique(mot, vc, autorisees, phonemes, sans_son=()):
    """La lecture d'une suite de lettres, dérivée du décodeur du projet.

    LA SEULE LETTRE MUETTE EST LE e FINAL. Tout le reste est lu par sa
    correspondance — y compris une consonne finale. C'est la seule lecture qu'un
    enfant puisse produire devant un pseudo-mot : la règle des consonnes finales
    muettes s'apprend mot par mot (« loup », « tabac », « fusil »), et un
    pseudo-mot n'est dans aucun lexique. « stag » se lit donc /stag/, et non
    /sta/.

    Les lettres sans son — le h qui n'est ni dans ch ni dans ph — ne rendent
    aucun phonème. Elles sont lues dans la table, pas devinées : c'est le même
    garde-fou qui laisse passer « homme », « huit » et « heure ».

    Rend (lecture, inconnus) — les inconnus sont les graphies que le décodeur ne
    sait pas rattacher, et ils sont rapportés plutôt que tus.

    La lecture est rendue entre barres obliques, une seule fois : chaque phonème
    est déclaré avec les siennes dans la table, et les recoller telles quelles
    donnerait `/d//wa//ʁ/`.
    """
    morceaux = vc.decouper_ce1(mot)
    muets = set()
    if len(morceaux) > 1 and morceaux[-1][0] == "e":
        muets.add(len(morceaux) - 1)
    sons, inconnus = [], []
    for i, (g, _debut, _fin) in enumerate(morceaux):
        if i in muets:
            continue
        if g in sans_son:
            continue
        cgp, drapeaux = vc.resoudre_ce1(mot, morceaux, i, autorisees)
        if cgp is None:
            inconnus.append((g, " ; ".join(str(d) for d in drapeaux)))
            continue
        if cgp not in phonemes:
            inconnus.append((g, f"la correspondance « {cgp} » n'a pas de phonème déclaré"))
            continue
        if est_etiquette_de_classe(g, phonemes[cgp]):
            inconnus.append((
                g,
                f"la table déclare {phonemes[cgp]} pour « {g} », et une semi-consonne "
                f"seule ne fait pas une syllabe : c'est l'étiquette de la classe des "
                f"graphies du /j/, pas sa lecture",
            ))
            continue
        sons.append(phonemes[cgp].strip("/"))
    return "/" + "".join(sons) + "/", inconnus


def graphies_reelles(mot, vc, autorisees):
    """La découpe réelle, et pour chaque morceau sa correspondance."""
    morceaux = vc.decouper_ce1(mot)
    vues = []
    for i, (g, _debut, _fin) in enumerate(morceaux):
        cgp, _ = vc.resoudre_ce1(mot, morceaux, i, autorisees)
        vues.append((g, cgp))
    return vues


def controler(corpus=None, banque=None):
    """Contrôle le corpus, et ce que la banque en fait.

    Les deux entrées sont injectables, et c'est ce qui rend le contrôle
    falsifiable : un banc peut lui présenter un corpus faux sans toucher aux
    fichiers. Un contrôle qu'on ne peut pas faire échouer sur commande est un
    contrôle dont on ne sait rien.
    """
    d = corpus if corpus is not None else charger("pseudo-mots-ce1.json")
    index = {p["id"]: p for p in d["pseudo_mots"] if "id" in p}
    vc = charger_module("verifier-textes-ce1.py", "verifier_textes_ce1")
    cp, ce1 = charger("cgp-cp.json"), charger("cgp-ce1.json")
    phonemes, _rangs, tranches, erreurs = tables()
    autorisees = vc.cgp_autorisees(cp, ce1, RANG_DE_LECTURE)
    sans_son = vc.lettres_sans_son(ce1)
    lex = lexique()
    banque = banque if banque is not None else charger("exercices-ce1.json")
    limites = []

    # La lecture de tout le lexique, calculée une fois : c'est elle qui dit si un
    # pseudo-mot est l'homophone d'un mot connu.
    lectures = {}
    for forme in lex:
        lecture, inconnus = lecture_mecanique(forme, vc, autorisees, phonemes, sans_son)
        if not inconnus:
            lectures.setdefault(lecture, []).append(forme)

    # --- Les déclarations, une par une -------------------------------------
    lignes = []
    for p in d["pseudo_mots"]:
        i = p.get("id", "?")
        manquants = [c for c in CHAMPS if c not in p]
        if manquants:
            erreurs.append(f"{i} : champ(s) manquant(s) {manquants}")
            continue
        inconnus = sorted(set(p) - set(CHAMPS))
        if inconnus:
            erreurs.append(f"{i} : champ(s) inattendu(s) {inconnus}")
        if not ID.match(i):
            erreurs.append(f"{i} : identifiant non conforme (pm suivi de deux chiffres attendu)")
        if p["origine"] not in ORIGINES:
            erreurs.append(f"{i} : origine « {p['origine']} » hors de {list(ORIGINES)}")
        if p["complexite"] not in COMPLEXITES:
            erreurs.append(
                f"{i} : complexité « {p['complexite']} » hors de {list(COMPLEXITES)}"
            )

        mot = p["mot"]
        if mot != mot.lower() or not mot.isascii() or not mot.isalpha():
            erreurs.append(
                f"{i} : « {mot} » — une suite de lettres en minuscules ASCII est attendue "
                f"(un accent dans un pseudo-mot ferait travailler une graphie que la suite "
                f"ne montre pas)"
            )
        if not MIN_LETTRES <= len(mot) <= MAX_LETTRES:
            erreurs.append(
                f"{i} : « {mot} » fait {len(mot)} lettres, hors de "
                f"{MIN_LETTRES}–{MAX_LETTRES}"
            )

        # L'origine : les exemples du programme sont ceux du programme, et
        # réciproquement. Sans cette règle, on pourrait écrire « programme » sur
        # une suite qu'on a inventée, et le porteur du projet croirait qu'il ne
        # peut pas la changer.
        est_du_programme = mot in EXEMPLES_DU_PROGRAMME
        if (p["origine"] == "programme") != est_du_programme:
            if p["origine"] == "programme":
                erreurs.append(
                    f"{i} : « {mot} » est déclaré exemple du programme et n'en est pas un "
                    f"— les exemples cités par le texte officiel sont "
                    f"{list(EXEMPLES_DU_PROGRAMME)}"
                )
            else:
                erreurs.append(
                    f"{i} : « {mot} » est un exemple du programme et n'est pas déclaré "
                    f"comme tel — sa modification est une décision pédagogique, et elle "
                    f"doit se voir"
                )

        # --- La lecture, dérivée -------------------------------------------
        lecture, non_lus = lecture_mecanique(mot, vc, autorisees, phonemes, sans_son)
        if non_lus:
            erreurs.append(
                f"{i} : « {mot} » — la lecture ne se dérive pas : "
                + " ; ".join(f"« {g} » ({r})" for g, r in non_lus)
            )

        # --- Les graphies déclarées ----------------------------------------
        vues = graphies_reelles(mot, vc, autorisees)
        morceaux = [g for g, _ in vues]
        if not p["graphies"]:
            erreurs.append(
                f"{i} : aucune graphie déclarée — la suite ne dirait pas ce qu'elle "
                f"fait travailler"
            )
        for g in p["graphies"]:
            if g not in morceaux:
                erreurs.append(
                    f"{i} : la graphie « {g} » est déclarée et la découpe de « {mot} » "
                    f"donne {morceaux} — elle n'y est pas"
                )
                continue
            if not any(cgp for h, cgp in vues if h == g):
                erreurs.append(
                    f"{i} : la graphie « {g} » n'est rattachée à aucune correspondance "
                    f"déclarée — elle n'est enseignée par aucune unité"
                )

        # --- La complexité, vérifiée par la table --------------------------
        du_ce1 = sorted({g for g, cgp in vues if cgp and tranches.get(cgp) == "CE1"})
        attendue = "complexe" if du_ce1 else "simple"
        if p["complexite"] != attendue:
            erreurs.append(
                f"{i} : « {mot} » est déclaré {p['complexite']} et la table en fait un "
                f"pseudo-mot {attendue}"
                + (f" (graphies du CE1 : {du_ce1})" if du_ce1 else " (aucune graphie du CE1)")
            )

        # --- La crainte de B35, rendue vérifiable --------------------------
        if mot in lex:
            erreurs.append(
                f"{i} : « {mot} » est déclaré pseudo-mot et c'est déjà un mot de "
                f"l'application — {', '.join(sorted(lex[mot]))}. Un enfant qui l'a lu "
                f"là ne peut pas décider que ce n'en est pas un"
            )
        if lecture and lecture in lectures:
            voisins = [f for f in lectures[lecture] if f != mot]
            if voisins:
                erreurs.append(
                    f"{i} : « {mot} » se lit {lecture}, comme "
                    f"{', '.join(sorted(voisins)[:4])} — l'exercice ferait lire "
                    f"l'homophone d'un mot connu"
                )

        lignes.append({
            "id": i, "mot": mot, "lecture": lecture, "graphies": p["graphies"],
            "du_ce1": du_ce1, "complexite": p["complexite"], "origine": p["origine"],
        })

    # --- Les citations, et ce que la banque en fait ------------------------
    par_unite = {e["id"]: e["unite"] for e in banque["exercices"]}
    citations = {}
    for e in banque["exercices"]:
        for pid in e.get("pseudo_mots", []):
            citations.setdefault(pid, []).append(e["id"])

    for pid in sorted(index):
        if pid not in citations:
            erreurs.append(
                f"{pid} : « {index[pid]['mot']} » est déclaré et cité par aucun exercice "
                f"— une suite écrite pour rien"
            )
    for pid, exs in sorted(citations.items()):
        if pid not in index:
            erreurs.append(f"{pid} : cité par {exs}, et absent du corpus")
            continue
        if len(exs) != len(set(exs)):
            erreurs.append(f"{pid} : cité deux fois par le même exercice ({exs})")
        par_rang = {}
        for eid in set(exs):
            par_rang.setdefault(par_unite[eid], []).append(eid)
        for rang, ids in sorted(par_rang.items()):
            if len(ids) > 1:
                erreurs.append(
                    f"{pid} : « {index[pid]['mot']} » est cité par {sorted(ids)}, deux "
                    f"exercices de l'unité {rang} — le second se répond de mémoire au "
                    f"lieu de se décoder"
                )

    # --- Les mots réels, dans l'autre sens ---------------------------------
    mecaniques = {m["id"]: m["verdict"] for m in banque["mecaniques"]}
    for e in banque["exercices"]:
        if e.get("mecanique") != "lire_pseudo_mot":
            continue
        for m in e.get("mots", []):
            if m not in lex:
                erreurs.append(
                    f"{e['id']} : le mot réel « {m} » n'est dans aucun corpus de "
                    f"l'application — on ne peut pas demander de reconnaître un mot "
                    f"qu'on n'a jamais lu"
                )
            if m in {p["mot"] for p in d["pseudo_mots"]}:
                erreurs.append(
                    f"{e['id']} : « {m} » est offert comme mot réel et figure au corpus "
                    f"des pseudo-mots — la même suite ne peut pas être les deux"
                )
    if "lire_pseudo_mot" not in mecaniques:
        limites.append(
            "aucun exercice ne déclare la mécanique `lire_pseudo_mot` : les mots réels "
            "n'ont pas été éprouvés"
        )

    limites.append(
        "« ce n'est pas un mot français » n'est pas vérifié : sans lexique embarqué, le "
        "contrôle ne voit que les mots DE L'APPLICATION, et une suite qui serait un mot "
        "français absent de l'application passerait"
    )
    sans_lecture = graphies_sans_lecture()
    limites.append(
        f"{len(sans_lecture)} graphies de la table ({', '.join(sans_lecture)}) n'ont pas "
        f"de lecture dérivable : la table leur donne /j/, qui est une semi-consonne, donc "
        f"l'étiquette d'une classe et non une lecture. Aucun pseudo-mot bâti sur l'une "
        f"d'elles ne peut entrer dans ce corpus."
    )
    detail = {
        "pseudo_mots": len(d["pseudo_mots"]),
        "du programme": sum(1 for p in d["pseudo_mots"] if p.get("origine") == "programme"),
        "complexes": sum(1 for p in d["pseudo_mots"] if p.get("complexite") == "complexe"),
        "formes du lexique": len(lex),
        "lectures distinctes du lexique": len(lectures),
        "graphies sans lecture dérivable": len(sans_lecture),
        "exercices citant": len({e for exs in citations.values() for e in exs}),
    }
    return lignes, detail, erreurs, limites


def main():
    lignes, detail, erreurs, limites = controler()

    print("Le corpus des pseudo-mots du CE1")
    for k, v in detail.items():
        print(f"  {k:32s} {v:>5}")

    if lignes:
        print()
        largeur = max(len(l["mot"]) for l in lignes) + 2
        for l in lignes:
            marque = "complexe" if l["du_ce1"] else "simple  "
            print(f"  {l['id']}  {l['mot']:<{largeur}} {l['lecture']:<10} "
                  f"{marque}  {l['graphies']}")

    if erreurs:
        print(f"\nNON CONFORME — {len(erreurs)} problème(s) :")
        for e in erreurs:
            print(f"  {e}")
        return 1

    print("\nOÙ LE CONTRÔLE S'ARRÊTE")
    for l in limites:
        print(f"  - {l}")
    print("\nRésultat : conforme")
    return 0


if __name__ == "__main__":
    sys.exit(main())
