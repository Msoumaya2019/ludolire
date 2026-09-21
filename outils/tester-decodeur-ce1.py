"""Éprouve le décodeur du CE1 : il doit refuser avant le rang, accepter après.

Un contrôle de déchiffrabilité n'est utile que s'il a des dents. On lui présente
donc, pour chaque règle que le CE1 change, le même mot de part et d'autre du rang
où la règle s'ouvre. Si les deux réponses sont identiques, le seuil ne sert à
rien — et c'est le genre de défaut qui ne se voit pas, parce que le contrôle
répond « conforme » dans les deux cas.

CE HARNAIS A TROUVÉ DIX DÉFAUTS RÉELS, et c'est sa raison d'être :

  1. « pomme » se découpait `p | om | m | e` — le m doublé était pris pour un
     contexte nasal, et le mot était lu /pɔ̃m/. Le défaut était AUSSI dans
     `verifier-textes.py`, donc dans la tranche CP, où mm n'est pas enseigné :
     le contrôle acceptait à tort « pomme » au CP.
  2. « loup » était ACCEPTÉ au rang 25 en étant lu /lup/ : une consonne finale
     qu'aucune règle ne couvre passait dans le décodeur ordinaire, qui la lisait
     prononcée. Le sens d'erreur le plus dangereux — un mot juste, lu de travers.
  3. « heure » et « livre » étaient lus /œ/ et /liv/ : la consonne devant un e
     final muet était rangée dans la queue muette, alors qu'elle est prononcée.
  4. « chantent » était lisible dès le rang 3, lu /ʃɑ̃tɑ̃/ : la terminaison -ent
     ressemble exactement à la nasale en suivie d'un t.
  5. « cinq » était inclaffable : le q final n'était connu que par le digramme qu.
  6. « homme », « huit », « histoire » étaient inclaffables : le h muet n'était
     déclaré nulle part.
  7. « chanter » au rang 1 était rapporté comme « consonne finale qu'aucune règle
     ne couvre », alors que la règle du r final était écrite dans la même table :
     la moitié « muette » de la règle n'était pas implémentée, et la barrière du
     rang 26 l'absorbait. Le harnais ne l'avait pas vu parce qu'il ne testait
     « chanter » qu'AU RANG 26 — le seul rang où le défaut est invisible. C'est
     pourquoi il y a maintenant TROIS sections : le VERDICT (accepté / refusé),
     la LECTURE (quels graphèmes sont muets), et — ajoutée après le défaut 10,
     qui a montré que les deux premières ne suffisaient pas — la DÉCOUPE (quels
     graphèmes sont reconnus, dans quel ordre). Un mot accepté peut être lu de
     travers, et le verdict seul ne le dit pas ; deux lectures peuvent donner la
     même liste de muets tout en découpant le mot autrement, et c'est ce qui est
     arrivé au « um ».
  8. Les graphies « aille », « eille » et « euille » étaient écrites dans le code
     et rattachées à AUCUNE CGP : tout mot qui les contient — « oreille »,
     « taille », « bataille », « abeille » — était refusé comme « graphème non
     enseigné », et « feuille », découpé `f | euil | l | e`, était lu /fœjl/.
     Aucun texte de la tranche ne contient ces graphies : le contrôle des textes
     était donc vert, et le défaut n'est apparu qu'en écrivant la banque
     d'exercices de l'unité 18. Les graphies sont désormais DÉRIVÉES de
     `cgp-ce1.json`, et la table contrôle que chacune est atteignable par la
     découpe.
  9. Tout mot terminé par un c était résolu « c-doux », donc /s/. La raison est
     une ligne de Python : quand le c est la dernière lettre, la lettre suivante
     est la chaîne vide, et `"" in "eiéèê"` est VRAI — la chaîne vide est
     sous-chaîne de toute chaîne. « sac », « lac », « parc », « bloc », « sec »
     étaient refusés avant le rang 19 ; ceux qui passaient — « avec », dans les
     textes des rangs 28 et 38 — étaient lus de travers, sans que rien ne le
     dise. Trouvé en écrivant      l'exercice de l'unité 1, qui affiche « sac ».
 10. Le « um » de la nasale « un » n'était déclaré nulle part. La table déclare
     « on/om », « an/am », « in/im », « ain/ein » — une nasale devant p ou b
     s'écrit avec un m — mais l'unité 13 ne déclarait que « un ». « parfum »
     était donc REFUSÉ, son m final n'étant couvert par aucune règle avant le
     rang 26, et « humble », découpé `h | u | m | b | l | e`, était lu /ymbl/
     pour /œ̃bl/ : accepté, et de travers. Le défaut est apparu en cherchant
     l'image d'un mot porteur de la nasale — c'est-à-dire en dehors des textes,
     ce qui est le seul endroit où il pouvait se voir : aucun des dix-huit textes
     du CE1 ne contient de « um ». Trouvé en écrivant le corpus d'images.

TROIS ATTENTES DU HARNAIS ÉTAIENT FAUSSES, et elles ont été corrigées ici plutôt
que dans le code — c'est le contrôle qui avait raison :

  - `échelle` au rang 27 : attendu refusé pour cause de ll doublé. Faux : le ll
    est enseigné au CP dès le rang 14, et au CE1 tout le CP est acquis.
  - `lait` au rang 1 : attendu accepté. Faux deux fois — le t final muet est une
    règle du CP, mais le ai ne vient qu'au rang 2 du CE1.
  - `père` au rang 1 : attendu accepté. Faux : le è est une graphie de l'unité 2.

Un contrôle éprouvé par des attentes fausses ne prouve rien : il apprend à douter
de lui-même, pas à mesurer.

Usage :
    python tester-decodeur-ce1.py
"""

import importlib.util
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("vc", ICI / "verifier-textes-ce1.py")
vc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vc)

# (mot, rang, doit_être_accepté, ce qui est éprouvé)
ESSAIS = [
    # La terminaison -ent : interdite au CP, ouverte au rang 27.
    ("chantent", 26, False, "terminaison -ent avant le rang 27"),
    ("chantent", 27, True, "terminaison -ent au rang 27"),

    # Les consonnes doubles : ss et ll au CP, toutes au rang 28.
    ("pomme", 27, False, "double mm avant le rang 28"),
    ("pomme", 28, True, "double mm au rang 28"),
    ("arrive", 27, False, "double rr avant le rang 28"),
    ("arrive", 28, True, "double rr au rang 28"),
    ("échelle", 1, True, "ll doublé : acquis du CP, lisible dès le rang 1"),

    # La consonne devant un e final muet se prononce.
    ("heure", 1, True, "heure : le r devant le e final est prononcé"),
    ("livre", 1, True, "livre : le v devant le e final est prononcé"),
    ("arbre", 1, True, "arbre : le r devant le e final est prononcé"),
    ("vitre", 1, True, "vitre : le t devant le e final est prononcé"),

    # Les muettes lexicales : à partir du rang 26. « loup », et non « lait »,
    # dont le t final est déjà réglé par le CP.
    ("loup", 25, False, "p final muet avant le rang 26"),
    ("loup", 26, True, "p final muet au rang 26"),
    ("tabac", 26, True, "c final muet au rang 26"),
    ("fusil", 26, True, "l final muet au rang 26"),

    # Les finales qui se prononcent, déclarées.
    ("avec", 26, True, "avec : le c final se prononce"),
    ("sac", 26, True, "sac : le c final se prononce"),
    ("cinq", 26, True, "cinq : le q final se prononce"),
    ("sud", 26, True, "sud : le d final se prononce"),

    # Les mots en -ent dont le en est nasal, déclarés.
    ("vent", 27, True, "vent : le en est nasal, le t muet"),
    ("dent", 27, True, "dent : idem"),
    ("argent", 27, True, "argent : idem"),
    ("content", 27, True, "content : idem"),

    # Les verbes en -er : le r final est muet, et c'est le cas le plus fréquent.
    ("parler", 27, True, "parler : le r final est muet"),
    ("aimer", 27, True, "aimer : idem"),

    # Les mots irréguliers déclarés sortent du contrôle.
    ("sept", 26, True, "sept : déclaré mot irrégulier"),
    ("huit", 26, True, "huit : déclaré mot irrégulier"),
    ("monsieur", 30, True, "monsieur : déclaré mot irrégulier"),

    # Le h muet, déclaré.
    ("homme", 28, True, "homme : le h est muet, et le mm attend le rang 28"),
    ("histoire", 1, True, "histoire : le h est muet"),
    ("hiver", 26, True, "hiver : le h est muet, le r final se prononce"),
    ("huit", 26, True, "huit : le h est muet"),

    # La valeur positionnelle de c, qui n'est pas au CP.
    ("cinéma", 18, False, "c-doux avant le rang 19"),
    ("cinéma", 19, True, "c-doux au rang 19"),
    # ... et le cas « aucune lettre ne suit ». Défaut 9 : la lettre suivante est
    # alors la chaîne vide, et `"" in "eiéèê"` est vrai — le c final était lu /s/,
    # donc « sac », « lac » et « parc » étaient refusés avant le rang 19.
    ("sac", 1, True, "sac : le c final vaut /k/, et il se prononce — le mot est déclaré"),
    ("lac", 1, True, "lac : idem"),
    ("parc", 1, True, "parc : idem"),
    # DEUX ATTENTES FAUSSES ICI, corrigées comme les trois du début du fichier :
    # le contrôle a RAISON de refuser « bloc » et « sec » avant le rang 26. Leur c
    # final vaut /k/, mais rien ne dit encore s'il SE PRONONCE — « bloc » et
    # « sec » si, « tabac » non. C'est la barrière du rang 26, et elle est
    # légitime : c'est exactement le pari que le contrôle refuse de faire.
    ("bloc", 1, False, "bloc : le c final vaut /k/, mais on ne sait pas encore s'il se prononce"),
    ("sec", 1, False, "sec : idem"),
    ("tabac", 1, False, "tabac : le c final est muet — une muette lexicale, décidée au rang 26"),

    # Les CGP du CE1, une par une, juste avant et juste après leur rang.
    ("montagne", 8, False, "gn avant le rang 9"),
    ("montagne", 9, True, "gn au rang 9"),
    ("photo", 10, False, "ph avant le rang 11"),
    ("photo", 11, True, "ph au rang 11"),
    ("loin", 3, False, "oin avant le rang 4"),
    ("loin", 4, True, "oin au rang 4"),
    ("potion", 16, False, "tion avant le rang 17"),
    ("potion", 17, True, "tion au rang 17"),
    ("fauteuil", 17, False, "euil avant le rang 18"),
    ("fauteuil", 18, True, "euil au rang 18"),
    # Le l des graphies -aille, -eille, -euille ne s'entend pas. Défaut 8 : ces
    # trois graphies étaient écrites dans le code et rattachées à aucune CGP.
    ("oreille", 17, False, "eille avant le rang 18"),
    ("oreille", 18, True, "oreille : le l de eille est muet, la graphie est une CGP"),
    ("taille", 18, True, "taille : le l de aille est muet"),
    ("bataille", 18, True, "bataille : idem"),
    ("abeille", 18, True, "abeille : idem"),
    ("bouteille", 18, True, "bouteille : idem"),
    ("feuille", 18, True, "feuille : le l de euille est muet"),
    ("travaille", 18, True, "travaille : le l de aille est muet"),
    ("lundi", 12, False, "un avant le rang 13"),
    ("lundi", 13, True, "un au rang 13"),
    ("craie", 1, False, "ai avant le rang 2"),
    ("craie", 2, True, "ai au rang 2"),
    ("tempête", 2, False, "en avant le rang 3"),
    ("tempête", 3, True, "en au rang 3"),
    ("père", 1, False, "è avant le rang 2"),
    ("père", 2, True, "è au rang 2"),

    # L'unité 12 est une règle d'oreille, pas une correspondance : les deux sons
    # s'écrivent pareil. « deux » le montre — il se lit dès le rang 1. « fleur »
    # non, mais pour une autre raison : son r final n'est couvert avant le rang
    # 26, et le r final est le point fragile du modèle.
    ("deux", 1, True, "eu fermé : la graphie eu est acquise au CP"),
    ("fleur", 1, True, "fleur : le r final est déclaré prononcé, donc lisible dès le rang 1"),
    ("fleur", 26, True, "fleur : idem"),
    ("mer", 26, True, "mer : le r final est déclaré prononcé"),
    # Un mot en -er dont le r est muet, lui, n'a pas besoin d'être déclaré :
    # c'est le pari de la règle, et il est bon pour les infinitifs.
    ("chanter", 26, True, "chanter : le r final est muet par la règle"),
    # ... et la règle vaut À TOUT RANG, parce que c'est une règle de position.
    # C'est le défaut 7 : ne tester le r muet qu'au rang 26 le rendait invisible.
    ("chanter", 1, True, "chanter : la règle du r muet ne dépend pas du rang"),
    ("aimer", 2, True, "aimer : le r final est muet, et le ai arrive au rang 2"),
    ("premier", 1, True, "premier : le r de -ier est muet"),
    ("partir", 1, True, "partir : le r final se prononce après un i"),
    ("trésor", 1, True, "trésor : le r final se prononce après un o"),
    ("chers", 1, True, "chers : le r de cher se prononce, le s du pluriel est muet"),
    ("c", 1, True, "c : forme élidée de « ce », déclarée mot-outil du CE1"),

    # Les formes élidées : la découpe jette l'apostrophe, et la lettre seule
    # arrivait au contrôle comme une consonne finale. Une consonne en tête de mot
    # est une attaque — elle se prononce toujours.
    ("l", 1, True, "l : forme élidée de « le »"),
    ("n", 1, True, "n : forme élidée de « ne »"),
    ("j", 1, True, "j : forme élidée de « je »"),
    ("d", 1, True, "d : forme élidée de « de »"),
    ("s", 1, True, "s : forme élidée de « si »"),
    ("m", 1, True, "m : forme élidée de « me »"),
    ("t", 1, True, "t : forme élidée de « te »"),
    ("qu", 1, True, "qu : forme élidée de « que »"),

    # Les nasales ne le sont pas devant une voyelle ni devant un m doublé.
    ("une", 12, True, "un devant voyelle n'est pas nasal"),
    ("lune", 12, True, "lune : le u et le n ne forment pas la nasale un"),
    ("pompe", 1, True, "pompe : le om EST nasal devant p"),

    # L'acquis du CP doit rester acquis, quel que soit le rang.
    ("lama", 1, True, "CGP du CP au rang 1"),
    ("poisson", 1, True, "ss du CP au rang 1"),
    ("bateau", 1, True, "eau du CP au rang 1"),
    ("lait", 2, True, "lait : le ai au rang 2, le t final muet dès le CP"),

    # Défaut 10 — le « um » de la nasale « un ». La table déclarait « on/om »,
    # « an/am », « in/im », « ain/ein » : une nasale devant p ou b s'écrit avec
    # un m. L'unité 13 ne déclarait que « un », et « um » manquait à l'appel.
    ("parfum", 12, False, "um non enseigné avant le rang 13"),
    ("parfum", 13, True, "parfum : le um final est nasal au rang 13"),
    ("humble", 13, True, "humble : le um devant b est nasal"),
    ("album", 13, True, "album : le um final est nasal"),
    ("humide", 13, True, "humide : le um devant une voyelle n'est PAS nasal"),
    ("humer", 13, True, "humer : le um devant une voyelle n'est PAS nasal"),
]


# ---------------------------------------------------------------------------
# LA LECTURE, ET PAS SEULEMENT LE VERDICT.
#
# Un mot accepté peut être lu de travers : « loup » au rang 25 était accepté
# parce qu'il était lu /lup/. Le verdict seul ne le dit pas, et le défaut 7 est
# de la même famille — la moitié « muette » de la règle du r final n'était pas
# implémentée, et cela ne se voyait qu'en regardant QUEL graphème était muet.
#
# On éprouve donc la liste des graphèmes muets, et pas seulement la réponse.
#
# (mot, rang, graphèmes muets attendus, ce qui est éprouvé)
# ---------------------------------------------------------------------------
LECTURES = [
    ("chers", 1, ["s"], "chers : le s du pluriel est muet, le r de cher se prononce"),
    ("mer", 1, [], "mer : rien n'est muet, le r final se prononce"),
    ("mers", 1, ["s"], "mers : le pluriel suit le singulier"),
    ("hiver", 1, [], "hiver : le r final se prononce"),
    ("chanter", 1, ["r"], "chanter : seul le r final est muet"),
    ("partir", 1, [], "partir : le r final se prononce"),
    ("livre", 1, ["e"], "livre : le e final est muet, le r se prononce"),
    ("pomme", 28, ["e"], "pomme : le e final est muet, le mm se prononce"),
    ("lait", 2, ["t"], "lait : le t final est muet"),
    ("loup", 26, ["p"], "loup : le p final est muet"),
    ("chantent", 27, ["en", "t"], "chantent : la terminaison -ent est muette"),
    ("l", 1, [], "l : rien n'est muet, c'est la seule lettre du mot"),
    ("d", 1, [], "d : le d de « d'un » n'est pas muet"),
    ("s", 1, [], "s : le s de « s'il » n'est pas un pluriel"),
    # Défaut 8, vu par la lecture : « feuille » se découpait `f | euil | l | e`,
    # donc le e était muet et le l se prononçait. Il se découpe maintenant
    # `f | euille`, et rien n'est muet — le l est dans la graphie.
    ("feuille", 18, [], "feuille : le l de euille ne s'entend pas"),
    ("oreille", 18, [], "oreille : le l de eille ne s'entend pas"),
    ("taille", 18, [], "taille : le l de aille ne s'entend pas"),
    # Défaut 10, vu par la lecture : avant le correctif, « humble » se découpait
    # `h | u | m | b | l | e`, donc le m se prononçait et rien n'était nasal —
    # /ymbl/ au lieu de /œ̃bl/. Le verdict seul ne le disait pas : le mot était
    # ACCEPTÉ. C'est la raison d'être de cette section.
    ("parfum", 13, [], "parfum : rien n'est muet, le um final se prononce"),
    ("humble", 13, ["e"], "humble : seul le e final est muet, le um est nasal"),
    ("humide", 13, ["e"], "humide : le m devant i se prononce, le e final est muet"),
]


# ---------------------------------------------------------------------------
# LA DÉCOUPE, ET PAS SEULEMENT LA LECTURE.
#
# Cette section existe parce que la falsification du correctif du « um » a
# montré que les deux premières ne suffisaient pas : en retirant « um » du
# garde-fou, « humide » se découpait `h | um | i | d | e` au lieu de
# `h | u | m | i | d | e` — et AUCUN essai ne bronchait. Le verdict est le même
# (accepté), et la liste des muets est la même (`e` final). Deux découpes
# différentes, la même réponse : le contrôle ne pouvait pas voir ce qu'il était
# censé garder.
#
# C'est la leçon de la section précédente, poussée d'un cran : un contrôle ne
# prouve que ce qu'il REGARDE, et il faut le falsifier pour savoir ce qu'il
# regarde vraiment.
#
# (mot, rang, découpe attendue, ce qui est éprouvé)
# ---------------------------------------------------------------------------
DECOUPES = [
    ("parfum", 13, ["p", "a", "r", "f", "um"], "parfum : le um final est la nasale"),
    ("humble", 13, ["h", "um", "b", "l", "e"], "humble : le um devant b est la nasale"),
    ("album", 13, ["a", "l", "b", "um"], "album : le um final est la nasale"),
    ("humide", 13, ["h", "u", "m", "i", "d", "e"],
     "humide : devant une voyelle, le u et le m sont deux graphèmes"),
    ("humer", 13, ["h", "u", "m", "e", "r"],
     "humer : devant une voyelle, le u et le m sont deux graphèmes"),
    ("lundi", 13, ["l", "un", "d", "i"], "lundi : le un devant une consonne est la nasale"),
    ("lune", 13, ["l", "u", "n", "e"], "lune : devant un n, le u n'est pas nasal"),
    ("une", 13, ["u", "n", "e"], "une : le un n'est pas nasal devant un n"),
    # Ancrages : deux découpes déjà connues, pour que la section ne soit pas
    # verte par accident.
    ("pomme", 28, ["p", "o", "mm", "e"], "pomme : le mm est une graphie, pas une nasale"),
    ("important", 28, ["im", "p", "o", "r", "t", "an", "t"],
     "important : les nasales en m devant p et b"),
]


def lire(mot, rang, prononcees, ent_nasal):
    """Les graphèmes muets d'un mot, tels que le décodeur les voit."""
    finale = mot in prononcees or (mot.endswith("s") and mot[:-1] in prononcees)
    morceaux = vc.decouper_ce1(mot)
    muets, _ = vc.indices_muets_ce1(mot, morceaux, rang, finale, ent_nasal)
    return [morceaux[i][0] for i in sorted(muets)]


def decoupe(mot):
    """Les graphèmes reconnus, dans l'ordre où le décodeur les reconnaît."""
    return [g for g, _, _ in vc.decouper_ce1(mot)]


def main():
    cp, ce1, prog = vc.charger_tables()
    prononcees = vc.exceptions_prononcees(ce1)
    sans_son = vc.lettres_sans_son(ce1)
    ent_nasal = vc.mots_en_ent_nasal(ce1)

    echecs = 0
    for mot, rang, attendu_ok, quoi in ESSAIS:
        autorisees = vc.cgp_autorisees(cp, ce1, rang)
        ecartes = vc.mots_ecartes(cp, ce1, rang)
        if mot in ecartes:
            ok = True
            detail = f"mémorisé ({ecartes[mot]})"
        else:
            problemes, inconnus = vc.controler_mot(
                mot, rang, autorisees, prononcees, sans_son, ent_nasal
            )
            ok = not problemes and not inconnus
            detail = "; ".join(r for _, _, r in problemes + inconnus) or "rien à signaler"
        if ok != attendu_ok:
            echecs += 1
        verdict = "OK " if ok == attendu_ok else "ÉCHEC"
        attendu = "accepté" if attendu_ok else "refusé"
        obtenu = "accepté" if ok else "refusé"
        print(f"  {verdict} {mot:12s} rang {rang:>2}  attendu {attendu:8s} obtenu {obtenu:8s}  {quoi}")
        if ok != attendu_ok:
            print(f"        → {detail}")

    print()
    print("  --- la lecture : quels graphèmes sont muets ---")
    for mot, rang, attendu, quoi in LECTURES:
        obtenu = lire(mot, rang, prononcees, ent_nasal)
        if obtenu != attendu:
            echecs += 1
        verdict = "OK " if obtenu == attendu else "ÉCHEC"
        print(f"  {verdict} {mot:12s} rang {rang:>2}  attendu muets {str(attendu):16s} "
              f"obtenu muets {str(obtenu):16s}  {quoi}")

    print()
    print("  --- la découpe : quels graphèmes sont reconnus, dans quel ordre ---")
    for mot, rang, attendu, quoi in DECOUPES:
        obtenu = decoupe(mot)
        if obtenu != attendu:
            echecs += 1
        verdict = "OK " if obtenu == attendu else "ÉCHEC"
        print(f"  {verdict} {mot:12s} rang {rang:>2}  attendu {(' | '.join(attendu)):26s} "
              f"obtenu {(' | '.join(obtenu)):26s}  {quoi}")

    print()
    total = len(ESSAIS) + len(LECTURES) + len(DECOUPES)
    if echecs:
        print(f"{echecs} essai(s) en échec sur {total}.")
        return 1
    print(f"{len(ESSAIS)} verdicts, {len(LECTURES)} lectures et {len(DECOUPES)} découpes "
          f"concluants sur {total} essais — le décodeur refuse avant le rang, accepte après, "
          f"lit ce qu'il annonce et découpe comme il le dit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
