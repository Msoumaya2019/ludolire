"""Contrôle des textes du CE1, et de la table de CGP qui les rend déchiffrables.

Deux choses sont contrôlées ici, et il faut dire pourquoi elles le sont ensemble :

  1. LA TABLE `outils/cgp-ce1.json`. Un rang qui n'existe pas dans la progression,
     une répartition d'unités qui ne tombe pas juste, une CGP nouvelle annoncée
     dans un domaine autre que « Identifier les mots » : ces défauts ne se voient
     pas en lisant la table, et ils rendent le contrôle des textes faux — on
     vérifierait contre un ensemble de CGP que personne n'enseigne.

  2. LES TEXTES. Un texte du CE1 n'emploie que des graphèmes déjà couverts : les
     trente CGP du CP, puis les CGP du CE1 jusqu'au rang de l'unité, plus les
     mots-outils mémorisés et les mots irréguliers déclarés.

CE QUI CHANGE PAR RAPPORT AU CP, et c'est la raison d'être du fichier. Trois
règles du CP tombent au CE1, chacune à un rang précis :

  - la terminaison -ent, INTERDITE dans toute la tranche CP, devient lisible au
    rang 27. Le programme en donne l'exemple « ils chantent » ;
  - les consonnes doubles, admises au CP pour ss et ll seulement, deviennent
    générales au rang 28 ;
  - les lettres finales muettes, admises au CP pour e, s, t, d, x, s'étendent aux
    muettes LEXICALES au rang 26 — « le lait », « le loup ».

CE QUI EST PARTAGÉ AVEC LE CP, ET POURQUOI. La SEGMENTATION ne se réécrit pas :
`decouper` et `valide` sont importés de `verifier-textes.py`. La découpe d'un mot
en graphèmes est la même règle dans les deux tranches, et deux implémentations
divergeraient — c'est le défaut que ces contrôles existent pour attraper. Ce qui
est propre au CE1 est le SEUIL de chaque règle, pas la règle.

CE QUE CE CONTRÔLE NE FAIT PAS, et il faut le dire :
  - il ne juge pas le sens du texte, ni sa qualité littéraire ;
  - il ne vérifie pas que la phrase-preuve d'une question de compréhension existe
    réellement dans le texte — cela appartient au contrôle des exercices ;
  - il ne connaît pas l'intérêt du texte, qui est le seul point qui décide qu'un
    enfant revienne le lendemain.

CE QU'IL FAIT DEPUIS QUE LA LARGEUR DE LIGNE EST FIXÉE : il compte les lignes. Le
programme fixe la longueur en LIGNES — « une quinzaine de lignes » — et une ligne
n'a de sens qu'avec la largeur de ligne de l'application. Cette largeur est
maintenant déclarée dans ce fichier (`LARGEUR_LIGNE`), le texte est plié à cette
largeur, et le compte de lignes est contrôlé. Sans cette décision, « une quinzaine
de lignes » n'était vérifiable par rien, et un texte de quinze PHRASES passait
pour un texte de quinze lignes — il en fait vingt.

Usage :
    python verifier-textes-ce1.py --table
    python verifier-textes-ce1.py --rang 27 contenu/textes-ce1/T05-rang27.txt
    python verifier-textes-ce1.py --rang 27 --mots contenu/textes-ce1/T05-rang27.txt
    python verifier-textes-ce1.py --tous

Sortie : 0 si tout est conforme, 1 sinon. Le script dit toujours où il s'arrête :
tout segment qu'il ne sait pas classer est signalé, jamais ignoré.
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
TEXTES = RACINE / "contenu" / "textes-ce1"

# La découpe est importée, pas réécrite : deux découpes divergeraient.
_spec = importlib.util.spec_from_file_location("vt", ICI / "verifier-textes.py")
_vt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_vt)


def charger(nom):
    return json.loads((ICI / nom).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Les seuils du CE1. Le CP refuse -ent partout ; le CE1 l'ouvre au rang 27.
# ---------------------------------------------------------------------------
RANG_MUETTES_LEXICALES = 26
RANG_MORPHEMES_MUETS = 27
RANG_CONSONNES_DOUBLES = 28

# LA LARGEUR DE LIGNE, ET POURQUOI ELLE EST ICI.
#
# Le programme du CE1 fixe la longueur d'un texte en LIGNES — « une quinzaine de
# lignes » — et pas en mots. Une ligne n'a de sens qu'avec la largeur de ligne de
# l'application : tant qu'elle n'est pas fixée, « une quinzaine de lignes » n'est
# vérifiable par aucune machine, et le contrôle ne pouvait que rapporter un
# nombre de mots, en disant qu'il ne savait pas conclure.
#
# La largeur est donc fixée ICI, à 34 signes espaces comprises, et c'est désormais
# ce que « une ligne » veut dire dans Ludo'Lire. Le chiffre n'est pas choisi pour
# arranger les textes : un enfant qui apprend à lire a un empan de lecture court,
# et au-delà d'une trentaine de signes le retour à la ligne devient une source
# d'erreur — l'œil saute la ligne ou revient au début de la même. Trente-quatre
# signes est le haut de cette fourchette, et il vaut pour le téléphone, qui est
# le support le plus contraint.
#
# Conséquence directe, et elle se vérifie : une ligne de Ludo'Lire porte quatre à
# cinq mots courants, donc « une quinzaine de lignes » vaut une soixantaine à une
# quatre-vingtaine de mots. Un texte qui écrit quinze PHRASES fait vingt lignes et
# dépasse le palier — c'est le piège que ce compteur a fait apparaître.
LARGEUR_LIGNE = 34

# Le palier de la tranche : six lignes au premier texte, une quinzaine au
# dernier. La borne haute tolère la ligne de plus qu'un « quinzaine ».
MIN_LIGNES = 6
MAX_LIGNES = 16

# LES GRAPHIES DU CE1 SONT DÉRIVÉES DE LA TABLE, PAS ÉCRITES ICI.
#
# Une première version tenait dans ce fichier une liste `GRAPHEMES_CE1` et une
# table `CE1_VERS_IDENTIFIANT`, à côté de `outils/cgp-ce1.json` qui déclare les
# mêmes graphies. Deux listes de la même chose : elles ont divergé, et la
# divergence ne se voyait nulle part.
#
# La table déclarait pour l'unité 18 les graphies « ail, eil, euil, ouille » ;
# le code en découpait quatre autres, dont « aille » et « eille », qu'il ne
# savait ensuite rattacher à aucune CGP. Tout mot contenant « aille » ou
# « eille » — « oreille », « taille », « bataille », « abeille » — était donc
# refusé comme « graphème non enseigné » ; et « feuille », découpé
# `f | euil | l | e`, était lu /fœjl/ : accepté, et de travers.
#
# Rien ne le voyait. Aucun des dix-huit textes de la tranche ne contient ces
# graphies, donc le contrôle des textes était vert — le refus n'est apparu qu'en
# écrivant la banque d'exercices de l'unité 18, c'est-à-dire en demandant au
# décodeur un mot qu'aucun texte ne lui avait encore demandé.
#
# La liste est donc dérivée de la table. Ajouter une graphie se fait dans le
# JSON, à l'unité qui l'enseigne, et le code suit. Ce que la dérivation n'a pas
# su faire est RAPPORTÉ par `controler_table`, jamais tu.
#
# c et g ne sont pas des graphies comme les autres : leur valeur dépend de la
# lettre qui suit, et `resoudre_ce1` les traite à part. Les dériver ici les
# ferait résoudre par la table, donc toujours de la même façon, et « café »
# deviendrait « c-doux ». Cette liste dit lesquelles sont dans ce cas.
GRAPHEMES_POSITIONNELS = {"c", "g"}

# Nasales : elles ne le sont pas devant une voyelle ni devant n. « une » n'est pas
# « un » + « e », c'est /yn/ — sans cette règle, le mot passerait au rang 13 en
# étant lu de travers, ce qui est le sens d'erreur le plus dangereux.
#
# « um » est du même cas que « un », et c'est ce qui a été oublié : la table
# déclarait « on/om », « an/am », « in/im », « ain/ein » — la nasale devant p ou b
# s'écrit avec un m — mais l'unité 13 ne déclarait que « un ». « parfum » était
# donc refusé (« m » final qu'aucune règle ne couvre), et « humble », découpé
# `h | u | m | b | l | e`, était lu /ymbl/ : accepté, et de travers. Le garde-fou
# qui suit ne s'appliquait qu'aux graphies listées ici : déclarer « um » dans la
# table sans l'ajouter ici l'aurait rendu nasal partout, « humide » compris.
NASALES_CE1 = {"oin", "un", "um", "en", "em"}


def graphemes_et_identifiants(ce1):
    """Rend (liste ordonnée des graphies, graphie -> identifiant, erreurs).

    L'ordre de la liste est celui de la table : par rang d'unité, puis par ordre
    de déclaration dans l'unité. `decouper_ce1` la retrie ensuite par longueur,
    et c'est cette liste qui tranche une égalité de longueur — l'ordre est donc
    une donnée, et il est déclaré là où sont les graphies.

    Le t de « tion » vaut /s/ contre sa valeur habituelle : c'est bien une
    correspondance, pas une lettre, et c'est l'identifiant de la table qui le dit.
    """
    liste, table, erreurs = [], {}, []
    for u in ce1["unites"]:
        cgp = u.get("cgp") or []
        graphies = u.get("graphies", [])
        if len(cgp) != 1:
            erreurs.append(
                f"cgp-ce1 unité {u['rang']} : {len(cgp)} identifiant(s) de CGP pour "
                f"{len(graphies)} graphie(s) — la dérivation suppose une seule CGP par "
                f"unité, et ne peut pas décider laquelle rattacher à quelle graphie"
            )
            continue
        for g in graphies:
            if g in GRAPHEMES_POSITIONNELS:
                continue
            if g in table:
                erreurs.append(
                    f"cgp-ce1 : la graphie « {g} » est déclarée deux fois — une graphie "
                    f"qui a deux unités n'a pas d'ordre de découpe"
                )
                continue
            table[g] = cgp[0]
            liste.append(g)
    return liste, table, erreurs


GRAPHEMES_CE1, CE1_VERS_IDENTIFIANT, ERREURS_DERIVATION = graphemes_et_identifiants(
    charger("cgp-ce1.json")
)

# Valeurs positionnelles : c et g valent autre chose selon la lettre qui suit.
# Le CP connaît c-dur et g-dur ; c-doux et g-doux sont des CGP du CE1.
C_DEVANT_DOUX = "eiéèê"


def charger_tables():
    return charger("cgp-cp.json"), charger("cgp-ce1.json"), charger("progression-ce1.json")


def cgp_autorisees(cp, ce1, rang):
    """Les CGP disponibles à ce rang : tout le CP, plus le CE1 jusqu'au rang.

    Le CP entier, et pas seulement ses premiers rangs : au CE1, les trente
    correspondances du CP sont acquises. Les redéclarer ici serait deux listes de
    la même chose, et deux listes de la même chose divergent.
    """
    autorisees = set()
    for u in cp["unites"]:
        autorisees.update(u["cgp"])
    for u in ce1["unites"]:
        if u["rang"] <= rang:
            autorisees.update(u["cgp"])
    return autorisees


def mots_ecartes(cp, ce1, rang):
    """Les mots que le contrôle ne déchiffre pas : ils sont mémorisés.

    DEUX LISTES, ET C'EST VOULU. Celle du CP dit ce qui est mémorisé EN CP — et,
    est, elle, elles. Celle du CE1 dit ce qui est mémorisé EN PLUS, et elle est
    longue : trente-quatre mots-outils dont les correspondances arrivent plus
    tard — le en à l'unité 3, le è à l'unité 2, le c doux à l'unité 19, les
    consonnes doubles à l'unité 28. Un enfant de CE1 lit ces mots d'un seul
    regard dès le premier jour, et un texte de la période 1 ne peut pas s'en
    passer.

    Une première version refusait que le CE1 déclare ses propres mots-outils, au
    motif que « deux listes de la même chose divergent ». L'intention était
    bonne, l'invariant était faux : les deux listes ne disent pas la même chose.
    Ce qu'il faut refuser, c'est qu'un mot soit déclaré des deux côtés — une
    double déclaration — et c'est ce que vérifie `controler_table`.
    """
    ecartes = {}
    for m in cp["mots_outils_memorises"]:
        if m["rang"] <= rang:
            ecartes[m["mot"]] = "mot-outil mémorisé au CP"
    for m in ce1.get("mots_outils_memorises", []):
        if m["rang"] <= rang:
            ecartes[m["mot"]] = "mot-outil mémorisé au CE1"
    for m in ce1["mots_irreguliers_memorises"]:
        if m["rang"] <= rang:
            ecartes[m["mot"]] = "mot irrégulier déclaré au CE1"
    return ecartes


def lettres_sans_son(ce1):
    """Les lettres qui ne s'entendent pas, déclarées dans la table.

    La mécanique est ici, la déclaration est dans le JSON : ajouter une lettre
    sans son est une décision, pas un ajustement de code. Un h qui n'est ni dans
    ch ni dans ph est toujours muet — « homme », « huit », « heure » — et le
    contrôle ne pouvait pas lire ces mots avant que la règle soit déclarée.

    La lettre est lue dans le champ `lettres`, et non devinée dans la phrase
    `regle` : une première version la cherchait par expression régulière dans le
    texte français, ce qui aurait fait de la prose une source de vérité.
    """
    lettres = set()
    for regle in ce1.get("strands", {}).get("lettres_sans_son", []):
        for lettre in regle.get("lettres", []):
            lettres.add(lettre)
    return lettres


def correspondances_declarees(ce1):
    """Lettre -> identifiants de CGP qu'elle met en jeu, déclarés dans la table.

    Une lettre qu'aucune unité n'enseigne et dont le contrôle a pourtant besoin.
    Le x entre deux voyelles en est le cas : il vaut /ks/, donc les deux
    correspondances que l'enfant connaît déjà depuis le CP — c et s. Sans cette
    déclaration, « texte » était inclaffable, et « texte » est le mot autour
    duquel tourne toute la compréhension du CE1.
    """
    table = {}
    for regle in ce1.get("strands", {}).get("correspondances_declarees", []):
        for lettre in regle.get("lettres", []):
            table[lettre] = regle.get("identifiants", [])
    return table


def mots_en_ent_nasal(ce1):
    """Les mots en -ent dont le en est NASAL — « vent », « dent », « argent ».

    Tous les autres mots en -ent sont lus avec la terminaison muette, qui est le
    cas de loin le plus fréquent dans un récit. La liste est la limite du pari.
    """
    strand = ce1.get("strands", {}).get("muettes_lexicales", [])
    mots = set()
    for regle in strand:
        for mot in regle.get("mots_en_ent_nasal", []):
            mots.add(mot)
    return mots


def exceptions_prononcees(ce1):
    """Les mots dont la consonne finale SE PRONONCE, contre la règle.

    DEUX FAMILLES, ET DEUX ENDROITS, parce que ce ne sont pas deux fois la même
    chose : la règle du r final est une règle de POSITION (`muettes_de_position`,
    elle vaut à tout rang), les autres sont des exceptions à la muette lexicale
    du rang 26 (`muettes_lexicales`). Le contrôle lit les deux : une déclaration
    rangée dans une famille que personne ne lit n'existe pas, et c'est ainsi
    qu'un mot déclaré se met à être refusé sans que rien ne le signale.
    """
    mots = set()
    for famille in ("muettes_de_position", "muettes_lexicales"):
        for regle in ce1.get("strands", {}).get(famille, []):
            for e in regle.get("exceptions_prononcees", []):
                mots.add(e["mot"])
    return mots


def valide_ce1(g, mot, i):
    """Le contexte d'un graphème nasal, étendu aux nasales du CE1."""
    if g in NASALES_CE1:
        suivant = mot[i + len(g)] if i + len(g) < len(mot) else None
        if suivant is None:
            return True
        if suivant in _vt.VOYELLES or suivant == "n":
            return False
        return True
    return _vt.valide(g, mot, i)


def decouper_ce1(mot):
    """Découpe un mot avec les graphèmes du CP ET ceux du CE1, du plus long au plus court.

    L'ORDRE EST DÉCLARÉ, ET IL EST FIXE. Une première version faisait
    `sorted(set(GP) | set(CE1), key=len, reverse=True)` : `sorted` est stable,
    mais l'ordre des éléments de même longueur venait d'un `set`, donc du hachage
    des chaînes — qui est randomisé d'un processus à l'autre. « pomme » pouvait
    être découpé `p | o | mm | e` dans une exécution et `p | om | m | e` dans la
    suivante, et le contrôle répondait alors deux choses différentes au même
    texte. Une découpe qui n'est pas reproductible ne prouve rien : on ne sait
    pas ce qu'on a éprouvé.

    La liste ci-dessous donne donc la priorité à la main : les graphèmes du CE1
    d'abord (ils sont les plus spécifiques), puis ceux du CP dans l'ordre où le
    contrôle du CP les déclare — de sorte qu'une longueur égale se tranche par
    la position dans cette liste, et non par le hachage.
    """
    graphemes = sorted(GRAPHEMES_CE1 + _vt.GRAPHEMES, key=len, reverse=True)
    morceaux = []
    i = 0
    while i < len(mot):
        for g in graphemes:
            if mot.startswith(g, i) and valide_ce1(g, mot, i):
                morceaux.append((g, i, i + len(g)))
                i += len(g)
                break
        else:
            morceaux.append((mot[i], i, i + 1))
            i += 1
    return morceaux


def resoudre_ce1(mot, morceaux, index, autorisees):
    """Rend (identifiant, drapeaux) ou (None, raisons)."""
    g, debut, fin = morceaux[index]
    suivant = mot[fin] if fin < len(mot) else ""
    precedent = mot[debut - 1] if debut > 0 else ""
    drapeaux = []

    # Les graphèmes du CE1 d'abord : « oin » avant « oi », « tion » avant « on ».
    if g in CE1_VERS_IDENTIFIANT:
        if g == "y":
            # y vaut /j/ au contact d'une voyelle, /i/ ailleurs : « yeux » et
            # « crayon » contre « stylo ». La règle se lit sur le voisinage.
            if precedent in _vt.VOYELLES or suivant in _vt.VOYELLES:
                return "ill", ["position:y"]
            return "i", ["position:y"]
        return CE1_VERS_IDENTIFIANT[g], drapeaux

    # La valeur positionnelle de c, qui n'est pas au CP.
    #
    # `suivant and` N'EST PAS UNE PRÉCAUTION DE STYLE, et son absence était un
    # défaut. Quand le c est la DERNIÈRE lettre du mot, `suivant` vaut la chaîne
    # vide — et en Python, `"" in "eiéèê"` est VRAI, parce que la chaîne vide est
    # sous-chaîne de toute chaîne. Tout mot terminé par un c était donc résolu
    # « c-doux », c'est-à-dire /s/ : « sac » refusé avant le rang 19, « bloc » et
    # « sec » refusés avant le rang 19, et — le sens d'erreur le plus dangereux —
    # les mots qui passaient quand même, lus de travers.
    #
    # Un c final vaut toujours /k/ en français : sac, lac, parc, avec, sec, bloc.
    # La règle du c final n'est pas une exception, c'est le cas « aucune lettre
    # ne suit », et il n'appartient pas à la liste des voyelles douces.
    if g == "c":
        if suivant and suivant in C_DEVANT_DOUX:
            return "c-doux", drapeaux
        return "c-dur", drapeaux

    # idem pour g, et le e de « ge » ne se prononce pas.
    if g == "g":
        if suivant and suivant in C_DEVANT_DOUX:
            return "g-doux", drapeaux
        return "g-dur", drapeaux
    if g == "ge":
        return "j", ["graphie:ge"]

    # Un q seul ne se rencontre qu'en finale — « cinq », « coq » — et il vaut /k/.
    # Le CP ne le connaît que par le digramme qu, ce qui laissait « cinq »
    # inclaffable : le contrôle répondait « graphème non enseigné » sur un mot de
    # tous les jours, et un refus qui porte à côté finit par être ignoré.
    if g == "q":
        return "c-dur", ["graphie:q-seul"]

    # Tout le reste appartient au CP.
    return _vt.resoudre(mot, morceaux, index, None, 0)


CONSONNES_FINALES = set("bcdfgjklmnpqrstvwxz")


def indices_muets_ce1(mot, morceaux, rang, finale_prononcee, ent_nasal):
    """Rend (indices muets, indices indécidables).

    QUATRE RÈGLES, ET TROIS D'ENTRE ELLES ONT ÉTÉ CORRIGÉES APRÈS AVOIR ÉTÉ FAUSSES.

    1. LA CONSONNE DEVANT UN e FINAL SE PRONONCE. C'est l'attaque de la dernière
       syllabe : « livre », « arbre », « père », « heure », « vitre ». Une
       première version la rangeait dans la queue muette, et lisait « heure »
       /œ/, « livre » /liv/. La queue s'arrête donc au e final et ne va pas
       au-delà.

    2. UNE CONSONNE FINALE EST MUETTE À PARTIR DU RANG 26 — « loup », « tabac »,
       « fusil ». Avant, le contrôle ne sait pas et le DIT : il la range parmi
       les indécidables. Une version antérieure la laissait passer dans le
       décodeur ordinaire, qui la lisait prononcée : « loup » était ACCEPTÉ au
       rang 25 en étant lu /lup/. Un mot juste, lu de travers, accepté en
       silence — le sens d'erreur le plus dangereux.

    3. LA TERMINAISON -ent EST UNE MARQUE GRAMMATICALE MUETTE à partir du rang
       27, et elle ressemble exactement à une nasale suivie d'un t : « ils
       chantent » contre « le vent ». La découpe ne peut pas les distinguer :
       les mots où le en EST nasal sont donc déclarés un par un dans
       `mots_en_ent_nasal`, et tous les autres sont lus avec la terminaison
       muette. La liste est la limite de la règle.

    4. LE r FINAL SUIT UNE RÈGLE DE POSITION, et elle vaut à TOUT RANG. Un r
       final est muet après un e — « chanter », « aimer », « premier » — et
       prononcé après toute autre voyelle — « partir », « fleur », « voir ». La
       règle est déclarée dans `strands.muettes_de_position`, avec la petite
       liste des mots en -er qui font exception (« mer », « hiver »).

       UNE VERSION ANTÉRIEURE N'IMPLÉMENTAIT PAS LA MOITIÉ « MUETTE » DE CETTE
       RÈGLE : le r après un e tombait dans la queue des muettes lexicales, donc
       dans la barrière du rang 26. « chanter » au rang 1 était alors rapporté
       comme « consonne finale qu'aucune règle ne couvre » — un refus qui portait
       à côté, puisque la règle était écrite dans la même table. Le harnais ne
       l'avait pas vu parce qu'il ne testait « chanter » qu'au rang 26, où la
       barrière de rang masque exactement ce défaut.

    5. QUELQUES MOTS ONT UNE FINALE PRONONCÉE — « avec », « sac », « cinq ».
       Ils sont déclarés dans `strands.muettes_lexicales.exceptions_prononcees`,
       et le contrôle les y lit plutôt que de deviner.
    """
    muets, indecidables = set(), set()
    if not morceaux:
        return muets, indecidables

    # 3. La terminaison -ent, quand c'est une marque grammaticale muette.
    if mot.endswith("ent") and rang >= RANG_MORPHEMES_MUETS and mot not in ent_nasal:
        debut_ent = len(mot) - 3
        for i, (g, debut, fin) in enumerate(morceaux):
            if debut >= debut_ent:
                muets.add(i)
        return muets, indecidables

    i = len(morceaux) - 1

    # 1a. Les marques du pluriel, s et x, quand elles sont la dernière lettre —
    # et pas quand elles sont la seule : le s de « s'il » n'est pas un pluriel.
    if i >= 0 and morceaux[i][0] in ("s", "x") and morceaux[i][1] > 0:
        muets.add(i)
        i -= 1

    # 1b. Le e final muet — seulement s'il y a une voyelle avant lui, sinon
    # « de » serait analysé sans voyelle.
    e_muet = False
    if i >= 0 and morceaux[i][0] == "e" and any(c in _vt.VOYELLES for c in mot[:morceaux[i][1]]):
        muets.add(i)
        i -= 1
        e_muet = True

    # 2. La consonne devant un e muet est prononcée : la queue s'arrête là.
    if e_muet:
        return muets, indecidables

    # 4. Sinon, la consonne finale peut être muette.
    #
    # LA RÈGLE NE VAUT QUE POUR UNE CONSONNE QUI N'EST PAS LA PREMIÈRE LETTRE DU
    # MOT. Une consonne en tête est une ATTAQUE : elle se prononce toujours, et
    # un mot ne peut pas être entièrement muet. Sans cette condition, les formes
    # élidées étaient refusées : `l'agneau`, `n'est`, `j'aime`, `d'un` — la
    # découpe jette l'apostrophe, et `l`, `n`, `j`, `d` arrivaient au contrôle
    # comme des mots d'une lettre dont la consonne finale serait muette. Le
    # refus portait à côté : ce n'est pas une consonne finale, c'est la seule
    # lettre du mot.
    if (i >= 0 and len(morceaux[i][0]) == 1 and morceaux[i][0] in CONSONNES_FINALES
            and morceaux[i][1] > 0):
        g, debut, fin = morceaux[i]
        if finale_prononcee:
            return muets, indecidables

        # LE r FINAL A UNE RÈGLE, et elle n'est pas « muet par défaut ». Un r
        # final est MUET après un e — « chanter », « aimer », « premier »,
        # « escalier » — et PRONONCÉ après toute autre voyelle — « partir »,
        # « voir », « trésor », « cœur », « sœur », « peur », « fleur », « mur »,
        # « bonjour ». Sans cette règle, la liste des exceptions grossissait à
        # chaque texte écrit : fleur, peur, cœur, trésor, sœur, pêcheur… y
        # entraient un par un, alors qu'aucun n'est une exception.
        #
        # C'est une règle de POSITION, pas une muette lexicale : elle ne dépend
        # donc PAS du rang. La version antérieure ne coupait que le cas
        # « prononcé » et laissait le cas « muet » tomber dans la barrière du
        # rang 26, ce qui faisait rapporter « chanter » au rang 1 comme une
        # consonne qu'aucune règle ne couvre.
        #
        # Ce qui RESTE exceptionnel, c'est le petit nombre de mots en -er dont le
        # r se prononce — « mer », « fer », « cher », « hiver », « hier »,
        # « super ». Ceux-là sont déclarés.
        if g == "r" and debut > 0:
            if mot[debut - 1] != "e":
                return muets, indecidables
            muets.add(i)
            return muets, indecidables

        if g in _vt.MUETTES_FINALES or rang >= RANG_MUETTES_LEXICALES:
            muets.add(i)
        else:
            indecidables.add(i)
    return muets, indecidables


def controler_mot(mot, rang, autorisees, exceptions_prononcees=(), muettes_declarees=(),
                  ent_nasal=(), declarees=None):
    """Rend (problemes, inconnus) pour un mot."""
    problemes, inconnus = [], []
    declarees = declarees or {}

    # La terminaison -ent : refusée au CP, ouverte au rang 27 du CE1 — SAUF pour
    # les mots dont le en est NASAL. « dent » et « vent » ne portent pas une
    # marque grammaticale, et ils sont lisibles dès que le en est enseigné, à
    # l'unité 3. Une version antérieure refusait « dent » au rang 3 : le refus
    # portait à côté, et un refus qui porte à côté finit par être ignoré.
    if _vt.TERMINAISON_ENT.search(mot) and rang < RANG_MORPHEMES_MUETS and mot not in ent_nasal:
        problemes.append(
            (mot, "-ent", f"terminaison -ent admise à partir du rang {RANG_MORPHEMES_MUETS}")
        )
        return problemes, inconnus

    morceaux = decouper_ce1(mot)

    # LE PLURIEL NE CHANGE PAS LA CONSONNE. « les mers » se lit comme « mer »,
    # « les hivers » comme « hiver ». Sans cet essai, le pluriel d'un mot déclaré
    # était lu de travers : accepté, mais avec un r muet au lieu d'un r prononcé
    # — le sens d'erreur le plus dangereux, puisqu'il ne se voit pas.
    finale_prononcee = mot in exceptions_prononcees or (
        mot.endswith("s") and mot[:-1] in exceptions_prononcees
    )

    muets, indecidables = indices_muets_ce1(
        mot, morceaux, rang, finale_prononcee, ent_nasal
    )

    for i, (g, debut, fin) in enumerate(morceaux):
        if i in muets:
            continue
        if g in muettes_declarees:
            # Une lettre sans son, déclarée dans la table. Elle est traversée
            # comme une lettre muette, et non résolue : c'est une lettre qu'on ne
            # prononce pas, pas une correspondance.
            continue
        if g in declarees:
            # Une correspondance déclarée : la lettre met en jeu des
            # correspondances que l'enfant connaît déjà.
            manquantes = [i for i in declarees[g] if i not in autorisees]
            if manquantes:
                problemes.append(
                    (mot, g, f"« {g} » met en jeu {manquantes}, non enseigné(s) au rang {rang}")
                )
            continue
        if i in indecidables:
            inconnus.append(
                (
                    mot,
                    g,
                    f"consonne finale qu'aucune règle ne couvre avant le rang "
                    f"{RANG_MUETTES_LEXICALES} — le contrôle ne peut pas dire si elle se prononce",
                )
            )
            continue
        cgp, drapeaux = resoudre_ce1(mot, morceaux, i, autorisees)
        if cgp is None:
            inconnus.append((mot, g, "; ".join(drapeaux)))
            continue
        if cgp not in autorisees:
            problemes.append((mot, g, f"CGP '{cgp}' non enseignée au rang {rang}"))
            continue
        # Les consonnes doubles : ss et ll au CP, toutes au rang 28.
        for d in drapeaux:
            if d.startswith("double:") and d not in ("double:ss", "double:ll"):
                if rang < RANG_CONSONNES_DOUBLES:
                    problemes.append(
                        (mot, g, f"{d} admis à partir du rang {RANG_CONSONNES_DOUBLES}")
                    )
    return problemes, inconnus


MOT_DANS_EXEMPLE = re.compile(r"[A-Za-zÀ-ÿœŒ]+")


def controler_exemples(prog, cp, ce1):
    """Les mots d'un exemple doivent être lisibles AU RANG DE LEUR UNITÉ.

    Un exemple de réussite qui cite un mot que l'enfant ne peut pas encore
    déchiffrer lui apprend un mot qu'il ne peut pas lire — et le contrôle de
    déchiffrabilité ne le voit pas, puisqu'il ne regarde que les textes.

    La convention est déclarée : un exemple qui commence par « Il lit » ou
    « Il distingue » est une LISTE DE MOTS, et on contrôle ses mots. Les autres
    exemples sont des phrases de programme, qui décrivent une réussite sans
    prétendre qu'on peut la lire — on ne les contrôle pas, et c'est dit.

    Ce contrôle a trouvé deux vrais défauts : l'unité 2 donnait « neige », dont
    le g doux n'arrive qu'à l'unité 20, et l'unité 17 donnait « attention » et
    « addition », dont les consonnes doubles n'arrivent qu'à l'unité 28.
    """
    erreurs = []
    prononcees = exceptions_prononcees(ce1)
    sans_son = lettres_sans_son(ce1)
    ent_nasal = mots_en_ent_nasal(ce1)
    declarees = correspondances_declarees(ce1)
    controles = 0

    for u in prog["unites"]:
        if u.get("exemples_source") != "notre formulation":
            continue
        exemple = u.get("exemples", "")
        if not (exemple.startswith("Il lit ") or exemple.startswith("Il distingue ")):
            continue
        controles += 1
        autorisees = cgp_autorisees(cp, ce1, u["rang"])
        ecartes = mots_ecartes(cp, ce1, u["rang"])
        for mot in (m.lower() for m in MOT_DANS_EXEMPLE.findall(exemple)):
            if mot in ecartes:
                continue
            problemes, inconnus = controler_mot(
                mot, u["rang"], autorisees, prononcees, sans_son, ent_nasal, declarees
            )
            for m, g, raison in problemes + inconnus:
                erreurs.append(
                    f"CE1 unité {u['rang']} : l'exemple cite « {m} », illisible à ce rang "
                    f"({raison})"
                )
    return controles, erreurs


# ---------------------------------------------------------------------------
# La table
# ---------------------------------------------------------------------------
def controler_table(cp, ce1, prog):
    """Contrôle `cgp-ce1.json` contre la progression du CE1."""
    # Ce que la dérivation des graphies n'a pas su faire. Une graphie déclarée
    # deux fois, une unité sans identifiant de CGP : ces défauts empêchent la
    # découpe, et ils se rapportent ici au lieu de faire mourir le module.
    erreurs = list(ERREURS_DERIVATION)
    rangs_prog = {u["rang"]: u for u in prog["unites"]}
    rangs_table = [u["rang"] for u in ce1["unites"]]

    for r in rangs_table:
        if r not in rangs_prog:
            erreurs.append(f"cgp-ce1 : le rang {r} n'existe pas dans la progression du CE1")
        elif rangs_prog[r]["domaine"] != "IDM":
            erreurs.append(
                f"cgp-ce1 : l'unité {r} introduit une CGP mais son domaine est "
                f"« {rangs_prog[r]['domaine']} », et non « Identifier les mots »"
            )
    if len(set(rangs_table)) != len(rangs_table):
        erreurs.append("cgp-ce1 : un rang apparaît deux fois")

    # La répartition des unités « Identifier les mots » doit tomber juste, et
    # c'est une DONNÉE, pas une phrase : un nombre écrit dans une phrase ne se
    # contrôle pas.
    rep = ce1["meta"].get("repartition_idm")
    if not rep:
        erreurs.append("cgp-ce1 meta : `repartition_idm` absent — le compte des unités "
                       "« Identifier les mots » n'est alors vérifiable par rien")
    else:
        idm = {u["rang"] for u in prog["unites"] if u["domaine"] == "IDM"}
        groupes = {k: set(v) for k, v in rep.items()}
        union = set()
        for nom, ensemble in groupes.items():
            chevauche = union & ensemble
            if chevauche:
                erreurs.append(f"cgp-ce1 repartition_idm : {nom} recouvre {sorted(chevauche)}")
            union |= ensemble
        if union != idm:
            erreurs.append(
                f"cgp-ce1 repartition_idm : la réunion des quatre groupes n'est pas "
                f"l'ensemble des unités « Identifier les mots » — manquantes "
                f"{sorted(idm - union)}, en trop {sorted(union - idm)}"
            )
        if groupes.get("cgp_nouvelle") != set(rangs_table):
            erreurs.append(
                f"cgp-ce1 repartition_idm : `cgp_nouvelle` ({sorted(groupes.get('cgp_nouvelle', []))}) "
                f"n'est pas l'ensemble des rangs de la table ({sorted(rangs_table)})"
            )

    for cle in ("titre", "version", "date", "statut", "heritage_du_cp", "source_progression"):
        if not str(ce1.get("meta", {}).get(cle, "")).strip():
            erreurs.append(f"cgp-ce1 meta : `{cle}` absent ou vide")

    for m in ce1.get("mots_irreguliers_memorises", []):
        if m.get("rang") not in rangs_prog:
            erreurs.append(f"cgp-ce1 mot irrégulier « {m.get('mot')} » : rang {m.get('rang')} inconnu")

    # Les mots-outils du CE1 et ceux du CP ne doivent pas se recouvrir : un mot
    # déclaré des deux côtés est une double déclaration, et deux déclarations de
    # la même chose finissent par diverger.
    mots_cp = {m["mot"] for m in cp["mots_outils_memorises"]}
    mots_ce1 = {m["mot"] for m in ce1.get("mots_outils_memorises", [])}
    doubles = sorted(mots_cp & mots_ce1)
    if doubles:
        erreurs.append(
            f"cgp-ce1 : {doubles} déclaré(s) à la fois comme mot-outil du CP et du CE1 — "
            f"une double déclaration, et deux déclarations de la même chose divergent"
        )
    # Un mot-outil qui serait aussi déclaré mot irrégulier, ou l'inverse.
    irr = {m["mot"] for m in ce1["mots_irreguliers_memorises"]}
    recouvre = sorted(mots_ce1 & irr)
    if recouvre:
        erreurs.append(f"cgp-ce1 : {recouvre} déclaré(s) à la fois mot-outil et mot irrégulier")

    # LES VALEURS POSITIONNELLES DOIVENT RÉPONDRE CE QU'ELLES DÉCLARENT.
    #
    # c et g sont les deux graphies que la dérivation écarte : leur valeur dépend
    # de la lettre qui suit, et `resoudre_ce1` les traite par un chemin à part.
    # Ce chemin est donc le seul endroit du décodeur qui ne se dérive de rien —
    # et c'est celui qu'on oublie. Le contrôle éprouve les deux contextes : le
    # c de « citron » doit valoir c-doux, celui de « cartable » ne doit pas.
    #
    # Une première version de ce contrôle vérifiait que la découpe PRODUIT chaque
    # graphie déclarée, en la cherchant dans la découpe d'une sonde construite
    # autour d'elle. Ce contrôle ne pouvait pas échouer : la découpe prend
    # toujours la plus longue correspondance, et la graphie cherchée était la
    # plus longue de sa propre sonde. Un contrôle qui ne peut pas échouer ne
    # prouve rien, et il fait pire que rien : il rassure.
    declarees_partout = {g for u in ce1["unites"] for g in u.get("graphies", [])}
    for u in ce1["unites"]:
        for g in u.get("graphies", []):
            if g not in GRAPHEMES_POSITIONNELS:
                continue
            identifiant = (u.get("cgp") or [None])[0]
            for suite, doit_etre_doux in (("it", True), ("at", False)):
                sonde = g + suite
                morceaux = decouper_ce1(sonde)
                cgp, _ = resoudre_ce1(sonde, morceaux, 0, set())
                est_doux = cgp == identifiant
                if est_doux != doit_etre_doux:
                    attendu = f"« {identifiant} »" if doit_etre_doux else f"autre chose que « {identifiant} »"
                    erreurs.append(
                        f"cgp-ce1 : dans « {sonde} », la valeur positionnelle de « {g} » "
                        f"devrait être {attendu}, et le décodeur répond « {cgp} » — "
                        f"la règle est déclarée à l'unité {u['rang']}, le code ne la suit pas"
                    )
    for g in sorted(GRAPHEMES_POSITIONNELS - declarees_partout):
        erreurs.append(
            f"cgp-ce1 : « {g} » est traitée comme une valeur positionnelle par le code, "
            f"et n'est déclarée par aucune unité — la dérivation l'écarte, et la table "
            f"ne dit pas où elle s'enseigne"
        )
    return erreurs


def lignes_du_texte(texte):
    """Le texte tel que l'application le rendra : une ligne par ligne pliée.

    Les lignes d'écriture — une phrase par ligne dans le fichier — ne sont PAS
    les lignes de lecture. Le fichier met une phrase par ligne pour qu'on puisse
    la relire et la corriger ; l'application, elle, plie le texte à
    `LARGEUR_LIGNE`. Ce sont ces lignes pliées qui se comptent, parce que ce sont
    celles que l'enfant lit.

    Le pliage est glouton et coupe aux espaces : un mot ne se coupe pas. C'est la
    règle la plus simple, et la seule qu'on puisse vérifier sans connaître la
    police de l'application.
    """
    lignes = []
    for brute in texte.splitlines():
        brute = brute.strip()
        if not brute or brute.startswith("#"):
            continue
        courant = ""
        for mot in brute.split():
            if not courant:
                courant = mot
            elif len(courant) + 1 + len(mot) <= LARGEUR_LIGNE:
                courant += " " + mot
            else:
                lignes.append(courant)
                courant = mot
        if courant:
            lignes.append(courant)
    return lignes


def controler_texte(chemin, rang, cp, ce1, verbeux):
    autorisees = cgp_autorisees(cp, ce1, rang)
    ecartes = mots_ecartes(cp, ce1, rang)
    prononcees = exceptions_prononcees(ce1)
    sans_son = lettres_sans_son(ce1)
    ent_nasal = mots_en_ent_nasal(ce1)
    declarees = correspondances_declarees(ce1)
    texte = chemin.read_text(encoding="utf-8")
    mots = _vt.extraire_mots(texte)
    lignes = lignes_du_texte(texte)

    problemes, inconnus, utilises, mémorisés = [], [], set(), set()

    # LA LONGUEUR SE CONTRÔLE, maintenant que la largeur de ligne est fixée. Le
    # palier de la tranche est un texte d'une quinzaine de lignes, et un texte
    # hors de la fourchette est un texte qu'on annonce sans l'avoir écrit.
    if not MIN_LIGNES <= len(lignes) <= MAX_LIGNES:
        problemes.append(
            (
                chemin.name,
                f"{len(lignes)} lignes",
                f"la tranche va de {MIN_LIGNES} à {MAX_LIGNES} lignes de "
                f"{LARGEUR_LIGNE} signes — ce texte en fait {len(lignes)}",
            )
        )

    for mot in mots:
        if mot in ecartes:
            mémorisés.add(mot)
            if verbeux:
                print(f"  {mot:16s} {ecartes[mot]}, hors contrôle")
            continue
        utilises.add(mot)
        p, inc = controler_mot(mot, rang, autorisees, prononcees, sans_son, ent_nasal, declarees)
        problemes.extend(p)
        inconnus.extend(inc)
        if verbeux:
            seg = " | ".join(g for g, _, _ in decouper_ce1(mot))
            print(f"  {mot:16s} {seg}")

    return mots, utilises, mémorisés, problemes, inconnus, lignes


def afficher(chemin, rang, resultat):
    mots, utilises, mémorisés, problemes, inconnus, lignes = resultat
    print(f"\nFichier        : {chemin.name}")
    print(f"Rang contrôlé  : {rang}")
    print(f"Longueur       : {len(lignes)} lignes de {LARGEUR_LIGNE} signes")
    print(f"Mots           : {len(mots)} occurrences, {len(utilises)} distincts, "
          f"{len(mémorisés)} mémorisés hors contrôle")
    if problemes:
        print(f"\nNON CONFORME — {len(problemes)} problème(s) :")
        for mot, g, raison in problemes:
            print(f"  {mot:16s} « {g} »  {raison}")
    if inconnus:
        print(f"\nOÙ LE CONTRÔLE S'ARRÊTE — {len(inconnus)} segment(s) non classé(s) :")
        for mot, g, raison in inconnus:
            print(f"  {mot:16s} « {g} »  {raison}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier", nargs="?", type=Path)
    ap.add_argument("--rang", type=int)
    ap.add_argument("--mots", action="store_true")
    ap.add_argument("--table", action="store_true", help="contrôle seulement cgp-ce1.json")
    ap.add_argument("--tous", action="store_true", help="tous les textes de contenu/textes-ce1")
    args = ap.parse_args()

    cp, ce1, prog = charger_tables()
    echecs = 0

    erreurs_table = controler_table(cp, ce1, prog)
    n_exemples, erreurs_exemples = controler_exemples(prog, cp, ce1)
    print(f"Table cgp-ce1  : {len(ce1['unites'])} CGP nouvelles, "
          f"{len(ce1.get('mots_outils_memorises', []))} mots-outils et "
          f"{len(ce1['mots_irreguliers_memorises'])} mots irréguliers déclarés, "
          f"{len(ce1['strands'])} familles de règles")
    print(f"Exemples       : {n_exemples} exemples en forme de liste, contrôlés mot à mot")
    erreurs_table = erreurs_table + erreurs_exemples
    if erreurs_table:
        print(f"\nTABLE NON CONFORME — {len(erreurs_table)} problème(s) :")
        for e in erreurs_table:
            print(f"  {e}")
        echecs += 1
    else:
        print("Table cgp-ce1  : conforme")

    if args.table:
        return 1 if echecs else 0

    a_controler = []
    if args.tous:
        a_controler = sorted(TEXTES.glob("*.txt"))
        if not a_controler:
            print(f"\nAucun texte dans {TEXTES} — rien à contrôler.")
            return 1 if echecs else 0
    elif args.fichier:
        a_controler = [args.fichier]
    else:
        ap.error("il faut un fichier, ou --tous, ou --table")

    for chemin in a_controler:
        if not chemin.exists():
            print(f"\n{chemin} : absent.")
            echecs += 1
            continue
        # Le rang est déclaré dans le texte lui-même : une ligne
        # `# rang: 27`. Le redonner à la main sur la ligne de commande serait une
        # seconde source de la même vérité, et elle divergerait.
        rang = args.rang
        if rang is None:
            m = re.search(r"^#\s*rang\s*:\s*(\d+)", chemin.read_text(encoding="utf-8"), re.M)
            if not m:
                print(f"\n{chemin.name} : aucun rang déclaré (`# rang: N`) et --rang absent.")
                echecs += 1
                continue
            rang = int(m.group(1))
        resultat = controler_texte(chemin, rang, cp, ce1, args.mots)
        afficher(chemin, rang, resultat)
        if resultat[3] or resultat[4]:
            echecs += 1

    if echecs:
        print(f"\nRésultat : à corriger ({echecs})")
        return 1
    print("\nRésultat : conforme")
    return 0


if __name__ == "__main__":
    sys.exit(main())
