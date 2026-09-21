"""Éprouve le brief de dessin des illustrations.

Ce qui est vérifié ici ne se voit pas à l'oeil, et c'est exactement ce qui fait
rater une série d'images :

  - chaque mot de la banque GS a exactement un brief, et aucun mot étranger n'en
    a un — un mot sans image est un exercice impossible, pas un oubli ;
  - deux mots ne reçoivent pas le même brief : deux fois le même dessin, c'est
    deux réponses possibles pour une seule image ;
  - un risque d'ambiguïté déclaré dans un sens est déclaré dans l'autre. Si
    `dodo` craint `lit`, alors `lit` craint `dodo` : la crainte est réciproque par
    nature, et ne l'écrire qu'une fois est la façon dont on oublie la moitié ;
  - les slugs sont uniques une fois les accents retirés — sans quoi deux images
    s'écraseraient l'une l'autre sans que rien ne le signale ;
  - le cadrage technique est complet : un format manquant est une image qu'on ne
    sait pas exporter.

Au CE1 (`--ce1`), le corpus est plus court mais le contrôle est plus long, et
c'est voulu : à la GS, l'image PORTE le mot ; au CE1, elle le VÉRIFIE. Le
contrôle vérifie donc en plus :

  - que chaque mot illustré est LISIBLE au rang de l'unité qui l'affiche, ce que
    le décodeur du CE1 calcule — un mot affiché qu'on ne peut pas lire est une
    devinette, pas un exercice ;
  - que la `decoupe` déclarée est bien celle du décodeur : un changement de
    découpe change la lecture, et rien ne le signalerait ;
  - que le corpus dit la VÉRITÉ sur son emploi : `present_dans_la_serie` est
    comparé aux mots réels de l'exercice nommé ;
  - que chaque mot non illustrable porte un motif d'une liste fermée et une
    raison écrite — un refus tu se lit comme un oubli ;
  - et que TOUT mot qu'un exercice des besoins B04, B13 ou B30 affiche est soit
    illustré, ici ou dans la tranche GS, soit déclaré non illustrable. C'est le
    contrôle qui fait du corpus une RÉPONSE : un mot oublié le fait échouer.

Aux images de récit (`--recit`), la question change de nature, et le contrôle
avec elle. Une icône se vérifie seule ; une image de récit ne se vérifie que
DANS SON ORDRE :

  - chaque étape cite une ligne du texte, et cette ligne est cherchée
    LITTÉRALEMENT dans le fichier du texte — pas dans une phrase reconstruite ;
  - **l'ordre déclaré est celui du texte** : le rang de la ligne citée croît
    strictement avec l'ordre de l'étape. C'est le contrôle central, et le seul
    qui empêche de ranger quatre dessins dans un ordre que le texte ne porte pas ;
  - chaque étape s'appuie sur un repère déclaré, pris dans une liste fermée, et
    deux étapes d'un même récit n'ont pas le même — deux repères identiques, ce
    sont deux images interchangeables, donc un exercice sans réponse ;
  - chaque repère déclaré sert au moins une fois : une case qui ne sert pas est
    une case qu'on n'a pas relue ;
  - la crainte de confusion est RÉCIPROQUE : si une étape craint une autre, cette
    autre la craint aussi. Ne l'écrire qu'une fois, c'est oublier la moitié ;
  - **tout exercice de remise en ordre de la banque est couvert** par un récit, et
    réciproquement : c'est ce qui fait de ce corpus une réponse et non un
    échantillon ;
  - et le trait d'une figure réemployée rend bien 4 px, produit de l'échelle et de
    l'épaisseur écrites dans le fichier.

Usage :
    python verifier-images.py            # la tranche GS
    python verifier-images.py --ce1      # la tranche CE1
    python verifier-images.py --recit    # les images de récit du CE1
"""

import hashlib
import importlib.util
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ICI = Path(__file__).resolve().parent
IMAGES = ICI.parent / "contenu" / "images"
IMAGES_CE1 = ICI.parent / "contenu" / "images-ce1"
IMAGES_RECIT = ICI.parent / "contenu" / "images-recit-ce1"

# Clés du cadrage technique qui doivent être renseignées, sans quoi le brief
# n'est pas exécutable par quelqu'un d'autre.
CHAMPS_TECHNIQUES = [
    "format_master", "export", "taille_logique", "occupation_du_cadre",
    "epaisseur_du_contour", "palette", "poids_cible",
]

CHAMPS_LICENCE = ["pourquoi_c_est_une_contrainte_technique", "ce_qu_il_faut",
                  "ce_qu_il_ne_faut_pas", "ou_c_est_range"]


def charger(nom):
    return json.loads((ICI / nom).read_text(encoding="utf-8"))


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Le générateur est chargé UNE fois, et c'est lui qui porte la palette, le cadre,
# l'épaisseur et le slug. Recopier le slug ici était la façon la plus sûre de le
# faire diverger : les deux copies donnaient le même résultat tant que tous les
# mots étaient en a-z, et « œil » les aurait séparées — le générateur écrivant
# ill_oeil.svg pendant que le contrôle chercherait ill_il.svg.
GI = charger_module("generer_images", ICI / "generer-images.py")


def slug(mot):
    """Le nom de fichier d'un mot. Calculé par le générateur, jamais recopié."""
    return GI.slug(mot)


def resoudre_cadrage(nom, erreurs, vus=None, reste=4):
    """Le cadrage se suit DE RÉFÉRENCE EN RÉFÉRENCE jusqu'au fichier qui le porte.

    Le corpus du CE1 référence le cadrage de la GS ; celui du récit référence le
    corpus du CE1, qui ne porte pas le cadrage lui-même. Suivre la chaîne est la
    seule façon de garder la référence qui dit quelque chose — « ces images sont
    de la même série que celles-là » — sans recopier la règle. Le corpus du CE1
    n'avait qu'un saut à faire ; le récit en a deux, et c'est ce qui a fait
    apparaître que la référence est transitive.
    """
    vus = vus if vus is not None else set()
    if nom in vus:
        erreurs.append(f"cadrage de référence « {nom} » : la chaîne revient sur elle-même")
        return None
    if reste <= 0:
        erreurs.append(f"cadrage de référence « {nom} » : la chaîne ne se termine pas")
        return None
    if not (ICI / nom).exists():
        erreurs.append(f"cadrage de référence « {nom} » : fichier absent")
        return None
    d = charger(nom)
    if "cadrage" in d:
        return d["cadrage"]
    suivant = d.get("cadrage_de_reference")
    if not suivant:
        erreurs.append(
            f"cadrage de référence « {nom} » : ni cadrage, ni référence — la chaîne "
            f"s'arrête avant d'avoir atteint le cadrage"
        )
        return None
    return resoudre_cadrage(suivant, erreurs, vus | {nom}, reste - 1)


def verifier_cadrage(corpus, erreurs):
    """Le cadrage technique et la licence, atteints par référence."""
    cadrage = resoudre_cadrage(corpus["cadrage_de_reference"], erreurs)
    if cadrage is None:
        return None
    for champ in CHAMPS_TECHNIQUES:
        if not cadrage["technique"].get(champ, "").strip():
            erreurs.append(f"cadrage de référence — technique.{champ} : vide")
    for champ in CHAMPS_LICENCE:
        if not cadrage["licence"].get(champ, "").strip():
            erreurs.append(f"cadrage de référence — licence.{champ} : vide")
    return cadrage


def controler():
    mots = charger("mots-gs.json")["mots"]
    d = charger("images-gs.json")
    erreurs = []

    attendus = {m["mot"]: m for m in mots}
    items = d["items"]
    par_mot = {}
    for item in items:
        mot = item["mot"]
        if mot in par_mot:
            erreurs.append(f"{mot} : deux briefs pour le même mot")
        par_mot[mot] = item
        if mot not in attendus:
            erreurs.append(f"{mot} : brief pour un mot absent de la banque GS")
        if not item.get("objet", "").strip():
            erreurs.append(f"{mot} : aucun objet décrit — le brief n'est pas exécutable")
        if not isinstance(item.get("interdit"), list):
            erreurs.append(f"{mot} : `interdit` doit être une liste (même vide)")

    for mot in attendus:
        if mot not in par_mot:
            erreurs.append(f"{mot} : présent dans la banque GS, sans brief de dessin")

    # Deux fois le même dessin, deux réponses pour une seule image.
    vus = {}
    for item in items:
        objet = item.get("objet", "")
        if objet in vus:
            erreurs.append(
                f"{item['mot']} et {vus[objet]} reçoivent le même objet « {objet} » — "
                f"l'image ne pourrait pas dire lequel des deux mots est visé"
            )
        vus[objet] = item["mot"]

    # Les risques d'ambiguïté vont par paires.
    declare = {}
    for item in items:
        for r in item.get("risque") or []:
            avec = r.get("avec")
            if avec is None:
                if not r.get("hors_banque"):
                    erreurs.append(
                        f"{item['mot']} : risque sans mot de la banque et sans "
                        f"`hors_banque` — on ne sait pas de quelle confusion on parle"
                    )
                continue
            if avec not in attendus:
                erreurs.append(
                    f"{item['mot']} : risque déclaré avec « {avec} », absent de la banque GS"
                )
                continue
            declare.setdefault(item["mot"], set()).add(avec)
    for a, partenaires in declare.items():
        for b in partenaires:
            if a not in declare.get(b, set()):
                erreurs.append(
                    f"{a} déclare un risque avec {b}, mais {b} n'en déclare aucun avec {a} — "
                    f"la crainte est réciproque, elle doit être écrite des deux côtés"
                )

    # Les slugs : deux mots qui se réduisent au même nom de fichier s'écrasent.
    par_slug = {}
    for item in items:
        s = slug(item["mot"])
        if s in par_slug:
            erreurs.append(
                f"{item['mot']} et {par_slug[s]} donnent tous deux le slug « {s} » — "
                f"une image écraserait l'autre"
            )
        par_slug[s] = item["mot"]
        if not s.isascii() or not s:
            erreurs.append(f"{item['mot']} : slug « {s} » non conforme")

    cadrage = d["cadrage"]
    for champ in CHAMPS_TECHNIQUES:
        if not cadrage["technique"].get(champ, "").strip():
            erreurs.append(f"cadrage.technique.{champ} : vide")
    for champ in CHAMPS_LICENCE:
        if not cadrage["licence"].get(champ, "").strip():
            erreurs.append(f"cadrage.licence.{champ} : vide")
    for champ in ("regles", "nommage"):
        if not cadrage.get(champ):
            erreurs.append(f"cadrage.{champ} : vide")

    avec_risque = sum(1 for i in items if i.get("risque"))
    paires = sum(len(i["risque"]) for i in items if i.get("risque"))
    detail = {
        "mots de la banque GS": len(attendus),
        "briefs de dessin": len(items),
        "mots portant un risque d'ambiguïté": avec_risque,
        "risques déclarés": paires,
        "risques réciproques (paires)": len(declare),
        "images à produire": len(items),
    }
    return detail, items, erreurs


def controler_fichiers(items, dossier, dessins, cle=None, etiquette=None):
    """Les SVG produits obéissent au cadrage. Ce contrôle regarde le fichier.

    Ce qu'il peut établir, et c'est beaucoup : le cadre est le bon, la palette est
    fermée, aucune image ne contient de texte, aucun fichier n'est vide ni
    démesuré. Ce qu'il ne peut pas établir : qu'un dessin est RECONNAISSABLE. Un
    fichier peut être parfaitement conforme et représenter un gribouillis. Cette
    limite est énoncée dans le document plutôt que masquée.

    `cle` désigne le nom de fichier d'un item — son mot réduit en slug pour les
    icônes, son identifiant pour une étape de récit, qui est déjà un nom de
    fichier.

    Une limite à connaître : pour une scène, le contrôle du contour de 4 px est
    satisfait par le groupe extérieur, alors que chaque figure réemployée porte sa
    propre épaisseur compensée. C'est `controler_composition` qui vérifie ce
    produit-là — ici, on ne regarde que le cadre.
    """
    cle = cle or (lambda i: slug(i["mot"]))
    etiquette = etiquette or (lambda i: i["mot"])
    palette = set(GI.PALETTE)
    cote = str(GI.COTE)
    erreurs = []
    tailles = []

    for item in items:
        nom = etiquette(item)
        chemin = dossier / f"ill_{cle(item)}.svg"
        if not chemin.exists():
            erreurs.append(f"{nom} : fichier absent ({chemin.name})")
            continue

        brut = chemin.read_text(encoding="utf-8")
        tailles.append((chemin.stat().st_size, chemin.name))

        try:
            racine = ET.fromstring(brut)
        except ET.ParseError as e:
            erreurs.append(f"{nom} : SVG illisible ({e})")
            continue

        if racine.get("viewBox") != f"0 0 {cote} {cote}":
            erreurs.append(
                f"{nom} : viewBox « {racine.get('viewBox')} » au lieu de « 0 0 {cote} {cote} »"
            )

        # Rien à lire dans une image. À la GS, un mot écrit dans le dessin ne
        # serait pas lu — mais il donnerait la réponse à qui sait lire, et
        # contournerait l'exercice.
        balises = {el.tag for el in racine.iter()}
        for interdit in ("text", "tspan", "tref", "flowRoot"):
            if f"{{http://www.w3.org/2000/svg}}{interdit}" in balises:
                erreurs.append(f"{nom} : contient un élément <{interdit}> — rien à lire")

        couleurs = set(re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"', brut))
        hors = {c.upper() for c in couleurs} - palette
        if hors:
            erreurs.append(
                f"{nom} : couleurs hors palette {sorted(hors)} — la série cesse d'être homogène"
            )

        if f'stroke-width="{GI.EPAISSEUR}"' not in brut:
            erreurs.append(f"{nom} : contour de {GI.EPAISSEUR} absent")

        if chemin.stat().st_size > 12288:
            erreurs.append(
                f"{nom} : {chemin.stat().st_size} octets, au-delà des 12 ko du cadrage"
            )

        # Le dessin doit exister dans le générateur : un fichier écrit à la main
        # survivrait à une régénération, et personne ne saurait d'où il vient.
        if cle(item) not in dessins:
            erreurs.append(f"{nom} : aucune fonction de dessin dans le générateur")

    tailles.sort(reverse=True)
    return tailles, erreurs


# Le groupe que `place()` écrit : une figure réemployée, son échelle et
# l'épaisseur qui compense cette échelle. Le contrôle relit les trois.
PLACE_RE = re.compile(
    r'<g transform="translate\((-?[\d.]+) (-?[\d.]+)\) scale\((-?[\d.]+)(?: (-?[\d.]+))?\)" '
    r'stroke-width="([\d.]+)"'
)


def controler_composition(items, dossier, cle=None, etiquette=None):
    """Le trait d'une figure réemployée doit rendre 4 px, et deux images ne doivent
    pas être le même fichier.

    C'est le contrôle que le générateur ne peut pas faire sur lui-même : il écrit
    une échelle et une épaisseur, et c'est leur PRODUIT qui décide de ce qu'on
    voit. Une échelle oubliée dans `place()` donne une figure dont le contour ne
    fait plus 4 px, au milieu d'autres qui les font — et cela ne se voit pas dans
    le code, cela se voit à l'œil, sur une planche qu'on n'a pas encore regardée.

    Deux fichiers identiques sont refusés pour une raison plus simple : deux
    images identiques dans un exercice de remise en ordre, c'est un exercice sans
    réponse. Le contrôle par empreinte le dit, là où quatre lignes de code
    semblables ne le diraient pas.
    """
    cle = cle or (lambda i: slug(i["mot"]))
    etiquette = etiquette or (lambda i: i["mot"])
    erreurs = []
    empreintes = {}

    for item in items:
        nom = etiquette(item)
        chemin = dossier / f"ill_{cle(item)}.svg"
        if not chemin.exists():
            continue
        brut = chemin.read_bytes()
        empreintes.setdefault(hashlib.sha256(brut).hexdigest(), []).append(nom)

        texte = brut.decode("utf-8")
        groupes = PLACE_RE.findall(texte)
        if not groupes:
            erreurs.append(
                f"{nom} : aucune figure réemployée — une scène qui ne reprend aucune "
                f"figure de la série est une scène écrite à part"
            )
        for _, _, sx, _, epaisseur in groupes:
            rendu = abs(float(sx)) * float(epaisseur)
            if abs(rendu - GI.EPAISSEUR) > 1e-6:
                erreurs.append(
                    f"{nom} : une figure à l'échelle {sx} porte {epaisseur} — le trait "
                    f"rend {rendu:.4f} px au lieu de {GI.EPAISSEUR}"
                )

    for empreinte, noms in empreintes.items():
        if len(noms) > 1:
            erreurs.append(
                f"{', '.join(sorted(noms))} : même fichier à l'octet — deux images "
                f"identiques ne se remettent pas dans l'ordre"
            )

    return erreurs


def _lisibilite(mot, rang, cp, ce1, vc):
    """Le mot est-il lisible au rang ? Rend (ok, détail).

    Un mot mémorisé passe : c'est ainsi que « œil » est lisible au rang 30 — il
    n'est pas déchiffré, il est reconnu. La distinction compte, parce qu'elle
    change ce que l'exercice peut demander : on ne fait pas déchiffrer un mot
    qu'on a déclaré irrégulier.
    """
    ecartes = vc.mots_ecartes(cp, ce1, rang)
    if mot in ecartes:
        return True, f"mémorisé ({ecartes[mot]})"
    problemes, inconnus = vc.controler_mot(
        mot, rang, vc.cgp_autorisees(cp, ce1, rang), vc.exceptions_prononcees(ce1),
        vc.lettres_sans_son(ce1), vc.mots_en_ent_nasal(ce1),
    )
    if problemes or inconnus:
        return False, "; ".join(r for _, _, r in problemes + inconnus)
    return True, "décodable"


def controler_ce1(corpus=None):
    """Le corpus du CE1, contre lui-même, contre le décodeur et contre la banque.

    `corpus` permet de passer un corpus MODIFIÉ, et c'est ainsi que le contrôle
    est éprouvé : `tester-images-ce1.py` lui présente douze corpus faux, un
    défaut à la fois, et exige que chacun soit vu. Un contrôle qu'on n'a jamais vu
    échouer ne prouve rien — c'est la leçon des deux contrôles qui ne pouvaient
    pas échouer, trouvés dans cette tranche.
    """
    if corpus is None:
        corpus = charger("images-ce1.json")
    banque = charger("exercices-ce1.json")
    prog = charger("progression-ce1.json")
    mots_gs = {m["mot"] for m in charger("mots-gs.json")["mots"]}
    vc = charger_module("verifier_textes_ce1", ICI / "verifier-textes-ce1.py")
    cp, ce1, _ = vc.charger_tables()

    erreurs = []
    items = corpus["items"]
    non_ill = corpus["non_illustrables"]
    motifs = set(corpus["motifs_de_refus"])
    besoins = {b["id"]: b for b in banque["besoins"]}
    par_exercice = {e["id"]: e for e in banque["exercices"]}
    unite_de = {u["rang"]: u for u in prog["unites"]}
    servis = ["B04", "B13", "B30"]

    # 1. Le cadrage est repris par RÉFÉRENCE, jamais recopié : deux copies d'une
    # même règle divergent, et c'est ce qui est arrivé aux graphies.
    verifier_cadrage(corpus, erreurs)

    # 2. Les mots illustrés.
    declares = {n["mot"] for n in non_ill}
    vus_mot, vus_objet = {}, {}
    for item in items:
        mot = item["mot"]
        if mot in vus_mot:
            erreurs.append(f"{mot} : deux briefs pour le même mot")
        vus_mot[mot] = item
        if mot in mots_gs:
            erreurs.append(f"{mot} : déjà illustré dans la tranche GS — deux images pour un mot")
        if mot in declares:
            erreurs.append(f"{mot} : à la fois illustré et déclaré non illustrable")
        if not item.get("objet", "").strip():
            erreurs.append(f"{mot} : aucun objet décrit — le brief n'est pas exécutable")
        if not isinstance(item.get("interdit"), list):
            erreurs.append(f"{mot} : `interdit` doit être une liste (même vide)")
        objet = item.get("objet", "")
        if objet and objet in vus_objet:
            erreurs.append(
                f"{mot} et {vus_objet[objet]} reçoivent le même objet — l'image ne "
                f"pourrait pas dire lequel des deux mots est visé"
            )
        vus_objet[objet] = mot

        besoin = item.get("besoin")
        if besoin not in besoins:
            erreurs.append(f"{mot} : besoin « {besoin} » absent de la banque du CE1")

        emploi = item.get("employable_par") or {}
        exercice = emploi.get("exercice")
        if exercice not in par_exercice:
            erreurs.append(f"{mot} : exercice « {exercice} » absent de la banque du CE1")
            continue
        e = par_exercice[exercice]
        rang = e["unite"]
        if item.get("rang") != rang:
            erreurs.append(
                f"{mot} : rang déclaré {item.get('rang')}, rang de l'unité de {exercice} : {rang}"
            )
        if e.get("besoin_id") != besoin:
            erreurs.append(
                f"{mot} : le besoin déclaré est {besoin}, mais {exercice} déclare "
                f"« {e.get('besoin_id')} » — le corpus ne répond pas au même besoin"
            )
        unite = unite_de.get(rang, {})
        if "image" not in (unite.get("action") or ""):
            erreurs.append(
                f"{mot} : l'unité {rang} n'annonce aucun geste d'image "
                f"(« {unite.get('action')} ») — l'image n'a pas d'emploi annoncé"
            )

        # La lisibilité, calculée par le décodeur du CE1.
        ok, detail = _lisibilite(mot, rang, cp, ce1, vc)
        if not ok:
            erreurs.append(
                f"{mot} : illisible au rang {rang}, où l'exercice l'affiche — {detail}"
            )

        # La découpe déclarée doit être celle du décodeur. Un changement de
        # découpe change la lecture, et rien d'autre ne le signalerait.
        reelle = [g for g, _, _ in vc.decouper_ce1(mot)]
        if item.get("decoupe") != reelle:
            erreurs.append(
                f"{mot} : découpe déclarée {item.get('decoupe')}, découpe réelle {reelle}"
            )

        # Le corpus dit la VÉRITÉ sur son emploi : on compare à la série réelle.
        present = mot in (e.get("mots") or []) or mot in (e.get("affiches") or [])
        if emploi.get("present_dans_la_serie") is not present:
            erreurs.append(
                f"{mot} : `present_dans_la_serie` vaut "
                f"{emploi.get('present_dans_la_serie')} alors que {exercice} "
                f"{'affiche' if present else 'n\'affiche pas'} le mot"
            )
        if not (emploi.get("ce_qu_il_faudrait") or "").strip():
            erreurs.append(f"{mot} : `ce_qu_il_faudrait` est vide — l'emploi n'est pas dit")

        for r in item.get("risque") or []:
            if r.get("avec") is None and not r.get("hors_banque"):
                erreurs.append(
                    f"{mot} : risque sans mot de la banque et sans `hors_banque` — "
                    f"on ne sait pas de quelle confusion on parle"
                )
            if r.get("avec") is not None and r["avec"] not in mots_gs:
                erreurs.append(
                    f"{mot} : risque déclaré avec « {r['avec']} », absent de la tranche GS"
                )
            for champ in ("pourquoi", "parade"):
                if not (r.get(champ) or "").strip():
                    erreurs.append(f"{mot} : risque sans `{champ}` — la parade n'est pas dite")

    # 3. Les mots déclarés non illustrables.
    vus_refus = {}
    for n in non_ill:
        mot = n["mot"]
        if mot in vus_refus:
            erreurs.append(f"{mot} : déclaré non illustrable deux fois")
        vus_refus[mot] = n
        if n.get("besoin") not in besoins:
            erreurs.append(f"{mot} : besoin « {n.get('besoin')} » absent de la banque")
        if n.get("motif") not in motifs:
            erreurs.append(
                f"{mot} : motif « {n.get('motif')} » hors de la liste fermée — "
                f"un motif libre ne se compte pas, et un refus qui ne se compte pas "
                f"ne se vérifie pas"
            )
        if not (n.get("raison") or "").strip():
            erreurs.append(f"{mot} : refus sans raison — une case vide se lit comme un oubli")
        if not isinstance(n.get("rang"), int):
            erreurs.append(f"{mot} : refus sans rang")

    # 4. LA RÉPONSE DÉCLARÉE AUX TROIS BESOINS.
    #    Sans ce datum, un mot illustré qui DISPARAÎT du corpus ne ferait échouer
    #    aucun contrôle : le contrôle de couverture part des mots que les
    #    exercices affichent, et un mot illustré que nul exercice n'affiche encore
    #    n'est réclamé par personne. C'est la falsification qui l'a montré — le
    #    corpus privé de « foin » restait vert — et non la lecture du code.
    rep = corpus.get("reponse_aux_besoins")
    if not rep:
        erreurs.append(
            "`reponse_aux_besoins` absent — un mot illustré qui disparaît du corpus "
            "n'est alors réclamé par rien"
        )
    else:
        for besoin in servis:
            declare = rep.get(besoin) or {}
            attendu = set(declare.get("illustrables") or [])
            obtenu = {i["mot"] for i in items if i.get("besoin") == besoin}
            if attendu != obtenu:
                erreurs.append(
                    f"reponse_aux_besoins.{besoin} : déclare {sorted(attendu)}, le corpus "
                    f"illustre {sorted(obtenu)} — les deux sources ont divergé"
                )
            if not attendu and not (declare.get("raison_si_aucun") or "").strip():
                erreurs.append(
                    f"reponse_aux_besoins.{besoin} : aucun mot illustrable et aucune raison "
                    f"— un besoin sans réponse et sans raison est un besoin tu"
                )
            if not (declare.get("ce_que_le_dessin_ne_peut_pas") or "").strip():
                erreurs.append(
                    f"reponse_aux_besoins.{besoin} : ce que le dessin ne peut pas est vide"
                )

    # 5. LE CONTRÔLE QUI FAIT DU CORPUS UNE RÉPONSE.
    #    Tout mot qu'un exercice des trois besoins affiche doit être illustré —
    #    ici ou dans la tranche GS — ou déclaré non illustrable avec sa raison.
    mots_affiches = {}
    for e in banque["exercices"]:
        if e.get("besoin_id") not in servis:
            continue
        for mot in e.get("mots") or []:
            mots_affiches.setdefault(mot, []).append(e["id"])
    illustres = set(vus_mot) | mots_gs
    for mot in sorted(mots_affiches):
        if mot in illustres or mot in vus_refus:
            continue
        erreurs.append(
            f"{mot} : affiché par {', '.join(mots_affiches[mot])} et ni illustré ni "
            f"déclaré non illustrable — c'est exactement le mot oublié que ce contrôle existe "
            f"pour trouver"
        )

    # 6. Un motif déclaré mais jamais employé est une case qui ne sert pas.
    employes = {n["motif"] for n in non_ill}
    inutiles = sorted(motifs - employes)
    if inutiles:
        erreurs.append(f"motifs déclarés et jamais employés : {inutiles}")

    detail = {
        "mots examinés": len(items) + len(non_ill),
        "mots illustrés": len(items),
        "mots déclarés non illustrables": len(non_ill),
        "mots affichés par les trois besoins": len(mots_affiches),
        "images à produire": len(items),
    }
    return detail, items, non_ill, erreurs


def _lignes_ecrites(contenu):
    """Les lignes du fichier, telles qu'elles y sont écrites : une phrase par ligne.

    Ce ne sont PAS les lignes de lecture — `lignes_du_texte` du contrôle des
    textes plie le texte à la largeur de l'écran, et c'est ce pliage qui compte
    pour le compte de lignes d'un texte. Ici ce qu'on cherche est la PHRASE : le
    moment d'un récit est une phrase du texte, et c'est cette phrase qui est citée.
    """
    return [
        ligne.strip() for ligne in contenu.splitlines()
        if ligne.strip() and not ligne.strip().startswith("#")
    ]


def _identifiant_valide(ident):
    """Un identifiant d'étape est un nom de fichier, et rien d'autre.

    Lui appliquer le slug des mots effacerait son tiret bas — « e19_1 »
    deviendrait « e191 » — et deux identifiants pourraient se confondre. Le
    contrôle refuse donc ce que le slug changerait, au lieu de le laisser passer.
    """
    return bool(ident) and ident == re.sub(r"[^a-z0-9_]", "", ident)


NOMBRES = {"un": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6}


def _nombre_annonce(serie):
    """Le nombre d'images qu'une série annonce, ou None si elle ne le dit pas.

    Le motif exige le nom de ce qui est compté — « quatre images », « quatre
    moments », « quatre étapes ». Chercher le seul mot « quatre » aurait compté
    l'article « un » d'une phrase comme « un texte lu d'abord », et rendu 1 pour
    un exercice à quatre images.
    """
    for ligne in serie:
        m = re.search(
            r"\b(un|deux|trois|quatre|cinq|six)\s+(images?|étapes?|moments?|dessins?)\b",
            ligne, re.I,
        )
        if m:
            return NOMBRES[m.group(1).lower()]
    return None


def controler_recit(corpus=None):
    """Les huit images de récit, contre le texte, contre la banque et contre elles-mêmes.

    `corpus` permet de passer un corpus MODIFIÉ, et c'est ainsi que le contrôle
    est éprouvé : `tester-images-recit.py` lui présente un défaut à la fois et
    exige que chacun soit vu, et vu pour la bonne raison.

    Le contrôle central est l'ORDRE : la ligne citée est cherchée LITTÉRALEMENT
    dans le fichier du texte, et sa position doit croître avec l'ordre de l'étape.
    Sans lui, quatre dessins pourraient être rangés dans un ordre que le texte ne
    porte pas, et rien ne le dirait — c'est le seul défaut de ce corpus qui ne se
    voie ni dans le code ni dans un fichier.
    """
    if corpus is None:
        corpus = charger("images-recit-ce1.json")
    ve = charger_module("verifier_exercices", ICI / "verifier-exercices.py")
    ctx = ve.contexte_ce1()
    banque = ctx["banque"]
    textes = ctx["textes"]

    erreurs = []
    reperes = corpus["reperes"]
    interdits = corpus["interdits"]
    regles = corpus["regles_du_recit"]
    recits = corpus["recits"]

    # 1. Le cadrage, par référence — ici TRANSITIVE : le corpus du récit renvoie
    #    au corpus lexical du CE1, qui renvoie lui-même à la GS.
    verifier_cadrage(corpus, erreurs)

    # 2. Ce que le corpus dit de lui-même.
    for cle in ("ce_qu_une_image_de_recit_doit_faire", "ce_qu_elle_ne_doit_pas_faire"):
        if not regles.get(cle):
            erreurs.append(f"regles_du_recit.{cle} : vide — la règle n'est pas dite")
    if not (regles.get("comment_les_figures_sont_prises") or "").strip():
        erreurs.append("regles_du_recit.comment_les_figures_sont_prises : vide")
    if not interdits:
        erreurs.append("`interdits` : liste vide — ce qu'une image ne doit pas faire n'est pas dit")
    for interdit in interdits:
        if not str(interdit).strip():
            erreurs.append("`interdits` : une entrée vide")
    if not reperes:
        erreurs.append("`reperes` : liste vide — sans repères, rien ne distingue quatre images")

    # 3. Les récits.
    par_exercice = {e["id"]: e for e in banque["exercices"]}
    ids_vus, objets_vus, reperes_employes = {}, {}, set()
    cache_lignes = {}

    for recit in recits:
        ex = recit["exercice"]
        if ex not in par_exercice:
            erreurs.append(f"{ex} : exercice absent de la banque du CE1")
            continue
        e = par_exercice[ex]
        if e.get("mecanique") != "ordonner_recit":
            erreurs.append(
                f"{ex} : la banque le déclare « {e.get('mecanique')} » — des images de "
                f"récit n'ont pas d'emploi dans une autre mécanique"
            )
        if e.get("texte") != recit["texte"]:
            erreurs.append(
                f"{ex} : le récit illustre {recit['texte']}, la banque déclare "
                f"« {e.get('texte')} » — les images ne montrent pas le texte de l'exercice"
            )
        if e.get("unite") != recit["unite"]:
            erreurs.append(
                f"{ex} : unité {recit['unite']} déclarée par le récit, "
                f"{e.get('unite')} par la banque"
            )

        # Le rang se lit DANS le texte, comme partout ailleurs : le redonner ici
        # serait une seconde source de la même vérité, et elle divergerait.
        nom_texte = recit["texte"]
        if nom_texte not in textes:
            erreurs.append(f"{nom_texte} : texte absent de contenu/textes-ce1/")
            continue
        if textes[nom_texte]["rang"] != recit["rang"]:
            erreurs.append(
                f"{nom_texte} : rang {recit['rang']} déclaré par le récit, "
                f"{textes[nom_texte]['rang']} écrit dans le texte"
            )
        if nom_texte not in cache_lignes:
            cache_lignes[nom_texte] = _lignes_ecrites(textes[nom_texte]["contenu"])
        lignes = cache_lignes[nom_texte]

        # Le nombre d'étapes doit être celui que la série de l'exercice annonce.
        attendu = _nombre_annonce(e.get("serie") or [])
        if attendu is None:
            erreurs.append(
                f"{ex} : sa série n'annonce pas combien d'images — on ne sait pas à "
                f"combien d'images l'exercice s'attend"
            )
        elif attendu != len(recit["etapes"]):
            erreurs.append(
                f"{ex} : la série annonce {attendu} images, le récit en déclare "
                f"{len(recit['etapes'])}"
            )

        if not (recit.get("ce_que_l_image_ne_dit_pas") or "").strip():
            erreurs.append(f"{ex} : `ce_que_l_image_ne_dit_pas` est vide")

        # L'ORDRE. C'est le contrôle central.
        position_precedente = -1
        ordres = []
        for etape in recit["etapes"]:
            ident = etape["id"]
            ordres.append(etape["ordre"])
            if ident in ids_vus:
                erreurs.append(f"{ident} : deux étapes portent le même identifiant")
            ids_vus[ident] = etape
            if not _identifiant_valide(ident):
                erreurs.append(
                    f"{ident} : l'identifiant doit être un nom de fichier — minuscules, "
                    f"chiffres et tirets bas seulement"
                )
            if ident not in GI.DESSINS_RECIT:
                erreurs.append(f"{ident} : aucune fonction de dessin dans le générateur")

            if not (etape.get("moment") or "").strip():
                erreurs.append(f"{ident} : aucun moment décrit")
            objet = (etape.get("objet") or "").strip()
            if not objet:
                erreurs.append(f"{ident} : aucun objet décrit — le brief n'est pas exécutable")
            elif objet in objets_vus:
                erreurs.append(
                    f"{ident} et {objets_vus[objet]} reçoivent le même objet — les deux "
                    f"images seraient les mêmes"
                )
            else:
                objets_vus[objet] = ident

            repere = etape.get("repere")
            if repere not in reperes:
                erreurs.append(
                    f"{ident} : repère « {repere} » hors de la liste fermée — un repère "
                    f"libre ne se compte pas, et un repère qui ne se compte pas ne se vérifie pas"
                )
            reperes_employes.add(repere)

            ligne = etape.get("ligne_citee", "")
            if not ligne.strip():
                erreurs.append(f"{ident} : aucune ligne citée")
            elif ligne not in lignes:
                erreurs.append(
                    f"{ident} : la ligne « {ligne} » ne se trouve pas littéralement dans "
                    f"{nom_texte} — un moment qu'on ne peut pas montrer dans le texte est "
                    f"un moment qu'on a inventé"
                )
            else:
                position = lignes.index(ligne)
                if position <= position_precedente:
                    erreurs.append(
                        f"{ident} : la ligne citée est à la position {position + 1} du "
                        f"texte, après une étape citée à la position "
                        f"{position_precedente + 1} — l'ordre dessiné n'est pas celui du texte"
                    )
                position_precedente = position

        if ordres != list(range(1, len(ordres) + 1)):
            erreurs.append(
                f"{ex} : les ordres déclarés sont {ordres}, et doivent être 1 à "
                f"{len(ordres)} sans trou ni répétition"
            )

        # Deux étapes d'un même récit ne peuvent pas s'appuyer sur le même repère.
        vus_ici = {}
        for etape in recit["etapes"]:
            r = etape.get("repere")
            if r in vus_ici:
                erreurs.append(
                    f"{ex} : {etape['id']} et {vus_ici[r]} s'appuient tous deux sur "
                    f"« {r} » — deux repères identiques, ce sont deux images "
                    f"interchangeables, donc un exercice sans réponse"
                )
            vus_ici[r] = etape["id"]

        # 4. Les risques de confusion, et leur RÉCIPROCITÉ.
        identifiants = {et["id"] for et in recit["etapes"]}
        craintes = {}
        for etape in recit["etapes"]:
            for r in etape.get("risque") or []:
                avec = r.get("avec")
                if avec not in identifiants:
                    erreurs.append(
                        f"{etape['id']} : risque déclaré avec « {avec} », qui n'est pas "
                        f"une étape de {ex}"
                    )
                    continue
                if avec == etape["id"]:
                    erreurs.append(f"{etape['id']} : se craint elle-même")
                for champ in ("pourquoi", "parade"):
                    if not (r.get(champ) or "").strip():
                        erreurs.append(f"{etape['id']} : risque sans `{champ}`")
                craintes.setdefault(etape["id"], set()).add(avec)
        for a, autres in sorted(craintes.items()):
            for b in sorted(autres):
                if a not in craintes.get(b, set()):
                    erreurs.append(
                        f"{a} craint {b}, mais {b} ne craint pas {a} — la crainte est "
                        f"réciproque par nature, et ne l'écrire qu'une fois est la façon "
                        f"dont on oublie la moitié"
                    )

    # 5. Un repère déclaré et jamais employé est une case qui ne sert pas.
    inutiles = sorted(set(reperes) - reperes_employes)
    if inutiles:
        erreurs.append(f"repères déclarés et jamais employés : {inutiles}")

    # 6. LA RÉCIPROQUE, QUI FAIT DU CORPUS UNE RÉPONSE.
    #    Ce n'est pas « tout exercice de remise en ordre » qui a besoin d'images :
    #    c'est tout exercice dont l'UNITÉ annonce un geste d'image. La progression
    #    le dit unité par unité, et c'est elle qui tranche — pas le corpus. Le
    #    contrôle a trouvé là les deux exercices que le cadrage ne mentionnait
    #    pas : E39 et E51 remettent un récit dans l'ordre, mais leurs unités — 32
    #    et 38 — ne demandent pas d'images, elles demandent de lire. Les couvrir
    #    contredirait la progression ; les passer sous silence les aurait tus.
    unite_de = {u["rang"]: u for u in charger("progression-ce1.json")["unites"]}
    ordonnent = [e for e in banque["exercices"] if e.get("mecanique") == "ordonner_recit"]
    avec_images, sans_images = set(), set()
    for e in ordonnent:
        action = unite_de.get(e.get("unite"), {}).get("action") or ""
        (avec_images if "image" in action else sans_images).add(e["id"])

    couverts = {r["exercice"] for r in recits}
    declares = {d["exercice"] for d in corpus.get("exercices_sans_images") or []}

    for ex in sorted(avec_images - couverts):
        erreurs.append(
            f"{ex} : son unité annonce un geste d'image et aucune image de récit ne le "
            f"couvre — c'est exactement l'exercice sans images que ce contrôle existe "
            f"pour trouver"
        )
    for ex in sorted(couverts - avec_images):
        erreurs.append(
            f"{ex} : couvert par le corpus, mais l'unité de la banque n'annonce aucun "
            f"geste d'image — la progression et le corpus ne disent pas la même chose"
        )
    for ex in sorted(sans_images - declares):
        erreurs.append(
            f"{ex} : remet un récit dans l'ordre sans que son unité annonce un geste "
            f"d'image — il joue sur le texte, et cela se DÉCLARE dans "
            f"`exercices_sans_images` au lieu de rester tu"
        )
    for ex in sorted(declares - sans_images):
        erreurs.append(
            f"{ex} : déclaré sans images, mais son unité annonce un geste d'image — "
            f"la déclaration contredit la progression"
        )
    for d in corpus.get("exercices_sans_images") or []:
        if not (d.get("raison") or "").strip():
            erreurs.append(f"{d.get('exercice')} : déclaré sans images, sans raison")

    detail = {
        "récits": len(recits),
        "images de récit": sum(len(r["etapes"]) for r in recits),
        "exercices de remise en ordre": len(ordonnent),
        "dont sur les images": len(avec_images),
        "dont sur le texte": len(sans_images),
        "repères déclarés": len(reperes),
        "repères employés": len(reperes_employes),
    }
    return detail, recits, erreurs


def main_gs():
    detail, items, erreurs = controler()
    tailles, e_fichiers = controler_fichiers(items, IMAGES, GI.DESSINS)
    for k, v in detail.items():
        print(f"{k:38s} {v:>4}")

    print(f"\n{'plus gros fichier':38s} {tailles[0][1]} — {tailles[0][0]} octets")
    print(f"{'total des 44 SVG':38s} {sum(t for t, _ in tailles)} octets")

    print("\nImages à produire :")
    for item in items:
        note = "" if item.get("risque") else "   (sans ambiguïté déclarée)"
        print(f"  ill_{slug(item['mot'])}.svg".ljust(22) + f"{item['mot']:12s}{note}")

    erreurs = erreurs + e_fichiers
    if erreurs:
        print(f"\nNON CONFORME — {len(erreurs)} problème(s) :")
        for e in erreurs:
            print(f"  {e}")
        return 1
    print("\nRésultat : conforme")
    return 0


def main_ce1():
    detail, items, non_ill, erreurs = controler_ce1()
    tailles, e_fichiers = controler_fichiers(items, IMAGES_CE1, GI.DESSINS_CE1)
    for k, v in detail.items():
        print(f"{k:38s} {v:>4}")

    if tailles:
        print(f"\n{'plus gros fichier':38s} {tailles[0][1]} — {tailles[0][0]} octets")
        print(f"{'total des 3 SVG':38s} {sum(t for t, _ in tailles)} octets")

    print("\nMots illustrés :")
    for item in items:
        emploi = item["employable_par"]
        present = "dans la série" if emploi["present_dans_la_serie"] else "PAS ENCORE dans la série"
        print(f"  ill_{slug(item['mot'])}.svg".ljust(22)
              + f"{item['mot']:10s}rang {item['rang']:>2}  {item['besoin']}  "
              + f"{emploi['exercice']} — {present}")

    print("\nMots déclarés non illustrables :")
    par_motif = {}
    for n in non_ill:
        par_motif.setdefault(n["motif"], []).append(n["mot"])
    for motif in sorted(par_motif):
        print(f"  {motif:22s}{len(par_motif[motif]):>3}  {', '.join(par_motif[motif])}")

    erreurs = erreurs + e_fichiers
    if erreurs:
        print(f"\nNON CONFORME — {len(erreurs)} problème(s) :")
        for e in erreurs:
            print(f"  {e}")
        return 1
    print("\nRésultat : conforme")
    return 0


def main_recit():
    detail, recits, erreurs = controler_recit()
    etapes = [e for r in recits for e in r["etapes"]]
    tailles, e_fichiers = controler_fichiers(
        etapes, IMAGES_RECIT, GI.DESSINS_RECIT,
        cle=lambda i: i["id"], etiquette=lambda i: i["id"],
    )
    e_composition = controler_composition(
        etapes, IMAGES_RECIT, cle=lambda i: i["id"], etiquette=lambda i: i["id"],
    )
    for k, v in detail.items():
        print(f"{k:38s} {v:>4}")

    if tailles:
        print(f"\n{'plus gros fichier':38s} {tailles[0][1]} — {tailles[0][0]} octets")
        print(f"{'total des 8 SVG':38s} {sum(t for t, _ in tailles)} octets")

    for recit in recits:
        print(f"\n{recit['exercice']} — {recit['titre_du_texte']} "
              f"(texte {recit['texte']}, rang {recit['rang']}, unité {recit['unite']})")
        for etape in recit["etapes"]:
            print(f"  {etape['ordre']}. {etape['id']:8s}{etape['repere']:20s}"
                  f"« {etape['ligne_citee']} »")

    erreurs = erreurs + e_fichiers + e_composition
    if erreurs:
        print(f"\nNON CONFORME — {len(erreurs)} problème(s) :")
        for e in erreurs:
            print(f"  {e}")
        return 1
    print("\nRésultat : conforme")
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--ce1":
        return main_ce1()
    if len(sys.argv) > 1 and sys.argv[1] == "--recit":
        return main_recit()
    return main_gs()


if __name__ == "__main__":
    sys.exit(main())
