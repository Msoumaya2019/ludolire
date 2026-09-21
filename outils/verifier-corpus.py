"""Éprouve les banques de mots, le corpus audio et la banque du jeu de syllabes.

Ce qui est vérifié ici ne se voit pas à l'oeil :

  - la découpe syllabique écrite à la main redonne bien le mot, exactement ;
  - un mot du CP est déchiffrable au rang qu'il déclare, **et pas au rang
    précédent** — sans quoi le rang déclaré n'est pas le rang minimal ;
  - une intruse du jeu est bien une VOISINE de la syllabe cachée, et la paire
    déclarée la produit réellement ;
  - au rendu écrit, chaque carte et chaque mot sont déchiffrables au rang de
    l'item, par le même contrôle que les textes de lecture.

Usage :
    python verifier-corpus.py
"""

import importlib.util
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("verifier_textes", ICI / "verifier-textes.py")
vt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vt)

# Les tables de voisinage vivent dans l'outil de dérivation, pas ici : la banque
# est dérivée avec elles, et le contrôle doit comparer à la MÊME règle. Deux
# copies de la liste des paires divergeraient — c'est exactement le défaut que ce
# contrôle existe pour attraper.
spec = importlib.util.spec_from_file_location("proposer_intruses", ICI / "proposer-intruses.py")
pi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pi)


def charger(nom):
    return json.loads((ICI / nom).read_text(encoding="utf-8"))


def controler_banques():
    """Découpes exactes, et rangs du CP réellement minimaux."""
    gs = charger("mots-gs.json")["mots"]
    cp = charger("mots-cp.json")["mots"]
    donnees = vt.charger()
    erreurs = []

    for banque, nom in ((gs, "mots-gs"), (cp, "mots-cp")):
        vus = set()
        for m in banque:
            mot, syl = m["mot"], m["syllabes"]
            if mot in vus:
                erreurs.append(f"{nom} : {mot} présent deux fois")
            vus.add(mot)
            if not syl or any(not s for s in syl):
                erreurs.append(f"{nom} : {mot} a une syllabe vide")
                continue
            if "".join(syl) != mot:
                erreurs.append(f"{nom} : {mot} — la découpe {'-'.join(syl)} redonne « {''.join(syl)} »")
            if any(" " in s for s in syl):
                erreurs.append(f"{nom} : {mot} — une syllabe contient une espace")

    for m in cp:
        mot, rang = m["mot"], m["rang"]
        autorisees = vt.cgp_autorisees(donnees, rang)
        problemes, inconnus = vt.controler_mot(mot, donnees, rang, autorisees)
        for mm, g, raison in problemes + inconnus:
            erreurs.append(f"mots-cp : {mot} déclaré au rang {rang} — « {g} » {raison}")
        if rang > 1:
            avant = vt.cgp_autorisees(donnees, rang - 1)
            p_av, i_av = vt.controler_mot(mot, donnees, rang - 1, avant)
            if not (p_av or i_av):
                erreurs.append(
                    f"mots-cp : {mot} passe déjà au rang {rang - 1} — le rang {rang} n'est pas minimal"
                )

    return gs, cp, erreurs


def controler_audio(mots_gs, mots_cp):
    """Les familles closes sont complètes, uniques, et nommables."""
    d = charger("corpus-gs.json")
    erreurs = []

    ph = d["phonemes"]
    if len(ph) != 36:
        erreurs.append(f"phonèmes : {len(ph)} au lieu de 36")
    if len({p["api"] for p in ph}) != len(ph):
        erreurs.append("phonèmes : un doublon d'API")
    for p in ph:
        attendu = "occlusive" not in p["categorie"]
        if p["isole"] != attendu:
            erreurs.append(
                f"phonème {p['api']} : isole={p['isole']} alors que « {p['categorie']} » "
                f"implique isole={attendu}"
            )

    let = d["lettres"]
    if len(let) != 26:
        erreurs.append(f"lettres : {len(let)} au lieu de 26")
    if len({l["lettre"] for l in let}) != len(let):
        erreurs.append("lettres : un doublon")

    for famille in ("consignes", "retours"):
        vus = set()
        for item in d[famille]:
            s = item["slug"]
            if s in vus:
                erreurs.append(f"{famille} : slug « {s} » en double")
            vus.add(s)
            nu = s.replace("_", "")
            if s != s.lower() or not nu.isascii() or not nu.isalnum():
                erreurs.append(f"{famille} : slug « {s} » non conforme (minuscules ASCII et _ attendus)")

    isolés = sum(1 for p in ph if p["isole"])
    detail = {
        "phonèmes isolés": isolés,
        "mots porteurs de phonème": len(ph),
        "noms de lettres": len(let),
        "consignes": len(d["consignes"]),
        "retours": len(d["retours"]),
        f"mots du corpus GS (entier + scandé)": 2 * len(mots_gs),
        "TOTAL de fichiers à enregistrer": isolés
        + len(ph)
        + len(let)
        + len(d["consignes"])
        + len(d["retours"])
        + 2 * len(mots_gs),
    }
    return detail, erreurs


def controler_jeu(mots_gs, mots_cp):
    """Les intruses sont des voisines, au nombre de deux, et l'écrit est déchiffrable."""
    d = charger("jeu-syllabes.json")
    par_mot = {m["mot"]: m["syllabes"] for m in mots_gs}
    par_mot.update({m["mot"]: m["syllabes"] for m in mots_cp})
    rang_cp = {m["mot"]: m["rang"] for m in mots_cp}
    cp = vt.charger()
    erreurs = []
    vus = set()
    sortes = {"consonne": 0, "voyelle": 0}

    for item in d["items"]:
        i = item["id"]
        if i in vus:
            erreurs.append(f"{i} : identifiant en double")
        vus.add(i)

        mot = item["mot"]
        if mot not in par_mot:
            erreurs.append(f"{i} : « {mot} » absent des deux banques de mots")
            continue
        syl = par_mot[mot]
        trou = item["trou"]
        if not 0 <= trou < len(syl):
            erreurs.append(f"{i} : trou {trou} hors de « {mot} » ({len(syl)} syllabes)")
            continue
        cachee = syl[trou]

        # Le voisinage autorisé, calculé par la même règle que la dérivation.
        cons, voy = pi.voisines(cachee, set(syl))
        autorisees = {s: p for s, p in cons}
        autorisees.update({s: p for s, p in voy})
        attendues = {s: ("consonne" if s in dict(cons) else "voyelle") for s in autorisees}

        if len(item["intruses"]) != 2:
            erreurs.append(
                f"{i} : {len(item['intruses'])} intruse(s) au lieu de 2 — "
                f"à une seule, l'enfant a une chance sur deux de tomber juste sans discriminer"
            )

        vues_ici = set()
        for intr in item["intruses"]:
            s = intr["syllabe"]
            if s in vues_ici:
                erreurs.append(f"{i} : l'intruse « {s} » est présente deux fois")
            vues_ici.add(s)
            if s in syl:
                erreurs.append(f"{i} : l'intruse « {s} » est une syllabe du mot — ambigu")
            if s not in autorisees:
                erreurs.append(
                    f"{i} : intruse « {s} » — n'est pas une voisine de « {cachee} » : "
                    f"elle ne partage ni la voyelle ni la consonne, donc elle s'écarte "
                    f"d'emblée et n'ajoute aucune difficulté"
                )
                continue
            if intr.get("sorte") != attendues[s]:
                erreurs.append(
                    f"{i} : intruse « {s} » déclarée « {intr.get('sorte')} » alors que "
                    f"la règle en fait une intruse « {attendues[s]} »"
                )
            if intr.get("paire") != autorisees[s]:
                erreurs.append(
                    f"{i} : intruse « {s} » — paire déclarée « {intr.get('paire')} », "
                    f"la règle produit « {autorisees[s]} »"
                )
            sortes[attendues[s]] = sortes.get(attendues[s], 0) + 1

        if item["rendu"] == "ecrit":
            rang = item["rang"]
            if mot in rang_cp and rang < rang_cp[mot]:
                erreurs.append(
                    f"{i} : rang {rang} inférieur au rang {rang_cp[mot]} déclaré pour « {mot} »"
                )
            autorisees_cgp = vt.cgp_autorisees(cp, rang)
            for segment in [mot] + syl + [intr["syllabe"] for intr in item["intruses"]]:
                p, inc = vt.controler_mot(segment, cp, rang, autorisees_cgp)
                for m, g, raison in p + inc:
                    erreurs.append(f"{i} (rang {rang}) : « {m} » segment « {g} » — {raison}")
        elif "rang" in item:
            erreurs.append(f"{i} : rendu oral mais un rang est déclaré")

    return len(d["items"]), sortes, erreurs


def controler_collisions(par_mot):
    """Aucune intruse ne doit reconstituer un mot français que l'enfant connaît.

    La liste est dans `collisions-fr.json` et elle est INCOMPLÈTE par
    construction : sans lexique embarqué, elle ne contient que ce qu'une lecture
    humaine a vu. Le contrôle ne peut donc garantir qu'une chose — la
    non-régression — et il faut le dire plutôt que de laisser croire à une
    exhaustivité qu'il n'a pas. Les `toleres`, eux, sont vérifiés dans l'autre
    sens : ils doivent être réellement produits, sinon la liste décrit une banque
    qui n'existe plus.
    """
    d = charger("jeu-syllabes.json")
    collisions = charger("collisions-fr.json")
    interdits = {c["mot"] for c in collisions["interdits"]}
    toleres = {c["mot"]: c["item"] for c in collisions["toleres"]}
    erreurs = []
    produites = set()

    for item in d["items"]:
        syllabes = par_mot[item["mot"]]
        trou = item["trou"]
        for intr in item["intruses"]:
            mot = "".join(syllabes[:trou] + [intr["syllabe"]] + syllabes[trou + 1:])
            produites.add(mot)
            if mot in interdits:
                erreurs.append(
                    f"{item['id']} : l'intruse « {intr['syllabe']} » reconstitue « {mot} », "
                    f"mot français familier — l'enfant peut le tenir pour juste"
                )

    for mot, item in toleres.items():
        if mot not in produites:
            erreurs.append(
                f"collisions-fr.json déclare « {mot} » toléré sur {item}, "
                f"mais la banque ne le produit plus — la déclaration est périmée"
            )

    return len(interdits), len(toleres), erreurs


def main():
    mots_gs, mots_cp, e_banques = controler_banques()
    detail, e_audio = controler_audio(mots_gs, mots_cp)
    n_jeu, sortes, e_jeu = controler_jeu(mots_gs, mots_cp)
    par_mot = {m["mot"]: m["syllabes"] for m in mots_gs + mots_cp}
    n_interdits, n_toleres, e_collisions = controler_collisions(par_mot)

    print(f"Banque GS           : {len(mots_gs)} mots")
    print(f"Banque CP           : {len(mots_cp)} mots")
    print(f"Banque du jeu       : {n_jeu} items, {2 * n_jeu} intruses")
    print(f"  dont              : {sortes['consonne']} consonantiques, "
          f"{sortes['voyelle']} vocaliques")
    print(f"Collisions          : {n_interdits} évitées, {n_toleres} tolérées")
    print("\nFichiers audio à enregistrer :")
    for k, v in detail.items():
        print(f"  {k:42s} {v:>5}")

    erreurs = e_banques + e_audio + e_jeu + e_collisions
    if erreurs:
        print(f"\nNON CONFORME — {len(erreurs)} problème(s) :")
        for e in erreurs:
            print(f"  {e}")
        return 1
    print("\nRésultat : conforme")
    return 0


if __name__ == "__main__":
    sys.exit(main())
