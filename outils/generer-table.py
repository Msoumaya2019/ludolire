"""Engendre les tableaux des documents à partir des JSON, entre deux marqueurs.

Un document est la source de vérité ; le tableau qu'il contient est un RENDU. Ce
script le régénère, et n'écrit que si le rendu a changé — la commande, et non la
relecture, tient les tableaux d'accord avec les JSON.

Chaque rendu est confronté à la région déjà présente dans le document. Si les
deux diffèrent, c'est le document qui est réécrit : un rendu faux ne peut donc
pas passer inaperçu, il se voit au diff.
"""

import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
OUTILS = RACINE / "outils"
CONTENU = RACINE / "contenu"

DEBUT = "<!-- DEBUT TABLE GENEREE -->"
FIN = "<!-- FIN TABLE GENEREE -->"

LARGEUR_LIGNE = 34


def charger(nom):
    return json.loads((OUTILS / nom).read_bytes().decode("utf-8"))


def charger_module(nom, chemin):
    """Importe un script dont le nom de fichier porte un tiret."""
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------
# Petits outillages partagés
# --------------------------------------------------------------------------

UNITES = [
    "", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
    "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize",
]
DIZAINES = {
    2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante",
    6: "soixante", 7: "soixante", 8: "quatre-vingt", 9: "quatre-vingt",
}


def en_lettres(n):
    """Écrit un entier en français, pour les titres de section."""
    if n < 17:
        return UNITES[n]
    if n < 20:
        return "dix-" + UNITES[n - 10]
    dizaine, unite = divmod(n, 10)
    if dizaine == 7 or dizaine == 9:
        return DIZAINES[dizaine] + "-" + UNITES[10 + unite]
    if unite == 0:
        return DIZAINES[dizaine]
    if unite == 1 and dizaine != 8:
        return DIZAINES[dizaine] + "-et-un"
    return DIZAINES[dizaine] + "-" + UNITES[unite]


def slug(mot):
    """Le mot en minuscules, sans accent, réduit à a-z et 0-9."""
    decompose = unicodedata.normalize("NFD", mot.lower())
    return "".join(
        c for c in decompose if unicodedata.category(c) != "Mn" and (c.isalnum() and c.isascii())
    )


def echapper(valeur):
    """Échappe la barre verticale d'un texte rapporté.

    Un découpage en graphèmes s'écrit `f | euil | l | e`, et une barre nue casse
    aussi bien un tableau markdown qu'une phrase lue : la casse se lirait comme
    une erreur de contenu, pas comme une erreur de mise en forme.
    """
    return str(valeur).replace("|", "\\|")


def tableau(entetes, lignes):
    """Un tableau markdown : en-tête, séparateur, lignes."""
    sortie = ["| " + " | ".join(echapper(e) for e in entetes) + " |",
              "|" + "---|" * len(entetes)]
    sortie.extend("| " + " | ".join(echapper(c) for c in ligne) + " |" for ligne in lignes)
    return sortie


def bloc_corrections(titre, corrections):
    """Les corrections consignées : un titre, puis trois lignes par correction."""
    bloc = [titre]
    for n, c in enumerate(corrections, 1):
        bloc.extend([
            "", f"**{n}. {echapper(c['objet'])}**", "",
            f"- *Le défaut.* {echapper(c['defaut'])}",
            f"- *La correction.* {echapper(c['correction'])}",
            f"- *Pourquoi il était coûteux.* {echapper(c['pourquoi_c_est_grave'])}",
        ])
    return "\n".join(bloc)


def mots_du_texte(corps):
    """Compte les mots d'un texte.

    Une forme élidée vaut deux mots : `l'agneau` se lit « l » puis « agneau »,
    et c'est ce que l'enfant déchiffre. Compter les espaces seuls sous-estime
    la charge d'un texte dès qu'il contient une élision.
    """
    return len([mot for mot in re.split(r"[\s'’]+", corps) if mot])


def liste(valeurs, vide="—", gabarit="`{}`", separateur=", "):
    if not valeurs:
        return vide
    return separateur.join(gabarit.format(v) for v in valeurs)


# --------------------------------------------------------------------------
# 1. La table des correspondances du CP
# --------------------------------------------------------------------------

def rendre_cp(d):
    lignes = [
        [str(u["rang"]), str(u["semaine"]), f"`{u['cgp'][0]}`", u["phoneme"],
         liste(u["graphies"]), u["critere"]]
        for u in d["unites"]
    ]
    return "\n".join(tableau(
        ["Rang", "Semaine", "CGP", "Phonème", "Graphies", "Pourquoi ici"], lignes
    ))


# --------------------------------------------------------------------------
# 2. La table de progression de la GS
# --------------------------------------------------------------------------

def rendre_gs(d):
    libelles = {x["id"]: x["libelle"] for x in d["domaines"]}
    lignes = [
        [str(u["rang"]), str(u["periode"]), libelles[u["domaine"]], u["palier"],
         u["colonne"], u["objectif"], "oui" if u.get("production") else "—",
         u["exemples"], u["action"]]
        for u in d["unites"]
    ]
    return "\n".join(tableau(
        ["Rang", "Période", "Domaine", "Palier", "Colonne du programme", "Objectif",
         "Production ?", "Exemples du programme", "Ce que l'enfant fait"], lignes
    ))


# --------------------------------------------------------------------------
# 3. Le corpus audio de la GS
# --------------------------------------------------------------------------

def rendre_corpus(d):
    parties = []

    lignes = [[cle.replace("_", " "), valeur] for cle, valeur in d["specification"].items()]
    parties.append("\n".join(
        ["### Le cahier des charges d'enregistrement", ""]
        + tableau(["Point", "Règle"], lignes)
    ))

    lignes = [[f"`{f['prefixe']}_`", f["libelle"], f["contenu"]] for f in d["familles"]]
    parties.append("\n".join(["### Les familles", ""] + tableau(["Préfixe", "Famille", "Contenu"], lignes)))

    lignes = [
        [f"`{p['api']}`", p["categorie"], "oui" if p["isole"] else f"**non** — {p['categorie'].split()[-1]}", p["mot"]]
        for p in d["phonemes"]
    ]
    parties.append("\n".join(
        [f"### Les {en_lettres(len(d['phonemes']))} phonèmes", ""]
        + tableau(["Phonème", "Catégorie", "Enregistré seul ?", "Mot porteur"], lignes)
    ))

    lettres = d["lettres"]
    lignes = []
    for debut in range(0, len(lettres), 4):
        morceau = lettres[debut:debut + 4]
        cellule = []
        for x in morceau:
            cellule.extend([f"`{x['lettre']}`", x["nom"]])
        cellule.extend(["", ""] * (4 - len(morceau)))
        lignes.append(cellule)
    parties.append("\n".join(
        [f"### Les {en_lettres(len(lettres))} noms de lettres", ""]
        + tableau(["Lettre", "Nom"] * 4, lignes)
    ))

    lignes = [[f"`con_{c['slug']}`", f"« {c['texte']} »"] for c in d["consignes"]]
    parties.append("\n".join(
        ["### Les consignes", ""] + tableau(["Fichier", "Ce que la voix dit"], lignes)
    ))

    lignes = [[f"`ret_{r['slug']}`", f"« {r['texte']} »"] for r in d["retours"]]
    parties.append("\n".join(
        ["### Les retours", ""] + tableau(["Fichier", "Ce que la voix dit"], lignes)
    ))

    isoles = sum(1 for p in d["phonemes"] if p["isole"])
    mots_gs = len(charger("mots-gs.json")["mots"])
    prises = mots_gs * 2
    total = isoles + len(d["phonemes"]) + len(lettres) + len(d["consignes"]) + len(d["retours"]) + prises
    lignes = [
        ["Phonèmes isolés", str(isoles)],
        ["Mots porteurs de phonème", str(len(d["phonemes"]))],
        ["Noms de lettres", str(len(lettres))],
        ["Consignes", str(len(d["consignes"]))],
        ["Retours", str(len(d["retours"]))],
        [f"Mots du corpus GS (entier + scandé)", str(prises)],
        ["**Total**", f"**{total}**"],
    ]
    parties.append("\n".join(["### Le décompte", ""] + tableau(["Famille", "Fichiers"], lignes)))

    return "\n\n".join(parties)


# --------------------------------------------------------------------------
# 4. Le jeu de syllabes manquantes
# --------------------------------------------------------------------------

def rendre_jeu(d):
    syllabes = {m["mot"]: m["syllabes"] for m in charger("mots-gs.json")["mots"]}
    syllabes.update({m["mot"]: m["syllabes"] for m in charger("mots-cp.json")["mots"]})

    lignes = []
    for item in d["items"]:
        decoupe = syllabes[item["mot"]]
        cachee = decoupe[item["trou"]]
        intruses = [
            f"`{i['syllabe']}` ({i['paire']}, {i['sorte']})"
            for i in item["intruses"]
        ]
        lignes.append([
            f"`{item['id']}`",
            item["rendu"],
            str(item["rang"]) if "rang" in item else "—",
            f"**{item['mot']}**",
            "-".join(decoupe),
            str(item["trou"] + 1),
            f"`{cachee}`",
            intruses[0],
            intruses[1],
            str(item["sert"]),
        ])
    return "\n".join(tableau(
        ["Item", "Rendu", "Rang", "Mot", "Syllabes", "Trou", "La carte à trouver",
         "Intruse 1", "Intruse 2", "Sert l'unité"], lignes
    ))


# --------------------------------------------------------------------------
# 5. Le brief des illustrations de la GS
# --------------------------------------------------------------------------

def rendre_images(d):
    # Le libellé n'est pas dans le brief : il vient du corpus de mots, qui dit ce
    # que l'image doit montrer. Le brief, lui, dit comment le dessiner.
    libelles = {m["mot"]: m["illustration"] for m in charger("mots-gs.json")["mots"]}

    def parade(r):
        """Une ambiguïté est nommée, ou bien elle vient d'un mot hors banque."""
        if r.get("avec"):
            return f"**{r['avec']}** — {r['parade']}"
        return f"hors banque : {r['hors_banque']} — {r['parade']}"

    parties = []

    lignes = [[cle.replace("_", " "), valeur] for cle, valeur in d["cadrage"]["technique"].items()]
    parties.append("\n".join(
        ["### Le cadrage technique", ""] + tableau(["Point", "Règle"], lignes)
    ))

    lignes = [[cle.replace("_", " "), valeur] for cle, valeur in d["cadrage"]["nommage"].items()]
    parties.append("\n".join(["### Le nommage", ""] + tableau(["Point", "Règle"], lignes)))

    lignes = []
    for item in d["items"]:
        risques = item.get("risque") or []
        lignes.append([
            f"**{item['mot']}**",
            f"`ill_{slug(item['mot'])}.svg`",
            libelles[item["mot"]],
            item["objet"],
            " ; ".join(item["interdit"]) or "—",
            " ; ".join(parade(r) for r in risques) or "—",
        ])
    parties.append("\n".join(
        [f"### Les {en_lettres(len(d['items']))} images", ""]
        + tableau(["Mot", "Fichier", "Libellé", "Objet à dessiner", "Interdit",
                   "Ambiguïté déclarée, et la parade"], lignes)
    ))

    avec = sum(1 for i in d["items"] if i.get("risque"))
    lignes = [
        ["Mots de la banque GS", str(len(d["items"]))],
        ["Images à produire", str(len(d["items"]))],
        ["Mots dont l'image porte une ambiguïté déclarée", str(avec)],
        ["Mots dont l'image n'en porte aucune", str(len(d["items"]) - avec)],
    ]
    parties.append("\n".join(["### Le décompte", ""] + tableau(["Point", "Nombre"], lignes)))

    return "\n\n".join(parties)


# --------------------------------------------------------------------------
# 6. La table de progression du CE1
# --------------------------------------------------------------------------

def rendre_ce1(d):
    libelles = {x["id"]: x["libelle"] for x in d["domaines"]}
    prod = [u for u in d["unites"] if u.get("production")]

    banque = charger("exercices-ce1.json")
    exercices = banque["exercices"]
    inv = sorted({e["unite"] for e in exercices if e.get("inversion")})
    hors = sorted({e["unite"] for e in exercices if e.get("pourquoi_hors_app")})

    # Une unité de production « a un geste » quand son exercice peut la juger :
    # l'inversion EST ce geste. Celles dont l'exercice est hors app n'en ont aucun,
    # et c'est l'application qui n'est pas l'instrument — pas l'unité qui manque.
    avec = [u for u in prod if u["rang"] in inv]
    sans = [u for u in prod if u["rang"] not in inv]

    parties = []

    lignes = [
        [str(u["rang"]), str(u["periode"]), libelles[u["domaine"]], u["objectif"],
         "**oui**" if u.get("production") else "—", u["exemples"], u["exemples_source"],
         u["source"], u["action"]]
        for u in d["unites"]
    ]
    parties.append("\n".join(
        [f"### Les {en_lettres(len(d['unites']))} unités", ""]
        + tableau(["Rang", "Période", "Domaine", "Objectif", "Production ?", "Exemples",
                   "Source de l'exemple", "D'où vient l'objectif", "Ce que l'enfant fait"], lignes)
    ))

    par_unite = {}
    for e in exercices:
        par_unite.setdefault(e["unite"], []).append(e)
    sans_reponse = [u["rang"] for u in prod if u["rang"] not in set(inv) | set(hors)]
    double = sorted(set(inv) & set(hors))

    # Une unité qui paie les deux se lit `inversion` : c'est le geste qui la solde,
    # et l'autre ligne du tableau porte déjà le hors app.
    dette = {}
    for u in prod:
        if u["rang"] in inv:
            dette[u["rang"]] = "`inversion`"
        elif u["rang"] in hors:
            dette[u["rang"]] = "`pourquoi_hors_app`"
        else:
            dette[u["rang"]] = "**non soldée**"

    paragraphe = (
        "Chacune oblige l'exercice qui la couvre à dire ce qu'il fait de la production, et "
        f"ce sera l'une de deux choses : une `inversion` — ce que le geste reprend — pour les "
        f"{len(avec)} unités qui ont un geste, ou un `pourquoi_hors_app` pour les {len(sans)} "
        "unités qui n'en ont aucun, l'application n'étant alors pas l'instrument. La colonne "
        "« Ce que l'enfant fait dans l'application » est une dette, pas une déclaration : elle "
        "est soldée par la banque d'exercices du CE1.\n"
        f" Elle la solde : sur les {len(prod)} unités de production, **{len(inv)}** déclarent "
        f"une `inversion` et **{len([r for r in hors if r in {u['rang'] for u in prod}])}** "
        "un `pourquoi_hors_app`\n"
        f" — l'unité {double[0]} paie les deux\n"
        ". Aucune ne reste sans réponse."
    ) if not sans_reponse else (
        "Chacune oblige l'exercice qui la couvre à dire ce qu'il fait de la production. "
        f"**{len(sans_reponse)} unité(s) de production ne sont pas soldées** : "
        f"{', '.join(str(r) for r in sans_reponse)}."
    )

    lignes = [
        [str(u["rang"]), libelles[u["domaine"]], u["objectif"], u["action"], dette[u["rang"]]]
        for u in prod
    ]
    parties.append("\n".join(
        [f"### Les {len(prod)} unités dont l'objectif porte un acte de parole", "",
         paragraphe, ""]
        + tableau(["Rang", "Domaine", "Objectif", "Ce que l'enfant fait dans l'application",
                   "Dette"], lignes)
    ))

    palier = d["palier_de_sortie"]
    lignes = [[p["objectif"], p["verifiable"]] for p in palier]
    parties.append("\n".join(
        [f"### Le palier de sortie — {len(palier)} réussites", ""]
        + tableau(["Objectif", "Où il se vérifie"], lignes)
    ))

    citations = d["meta"]["citations_officielles"]
    bloc = [
        f"### Les {len(citations)} citations officielles", "",
        "C'est contre ces passages que se relisent les exemples annoncés « programme ». Le "
        "contrôle vérifie qu'un tel exemple est bien contenu dans l'une d'elles ; il ne vérifie "
        "pas que la citation est fidèle au Bulletin officiel — cela se relit, et c'est une "
        "relecture humaine.",
    ]
    for c in citations:
        bloc.append("")
        bloc.append(f"**p. {c['page']} — {c['section']}**")
        bloc.append("")
        bloc.append(f"> {c['texte']}")
    # Un bloc de citations se détache du titre qui suit : la citation est une
    # pièce rapportée, pas la fin de la section.
    parties.append("\n".join(bloc) + "\n")

    hors_tranche = d["hors_tranche"]
    lignes = [[x] for x in hors_tranche["contenu"]]
    parties.append("\n".join(
        ["### Ce qui n'est pas de la tranche", "", f"*{hors_tranche['note']}*", ""]
        + tableau(["Domaine écarté"], lignes)
        + ["", f"*Pourquoi.* {hors_tranche['raison']}"]
    ))

    par_domaine = {x["id"]: 0 for x in d["domaines"]}
    for u in d["unites"]:
        par_domaine[u["domaine"]] += 1
    verifiables = sum(1 for p in palier if p["verifiable"].startswith("dans l'app"))
    lignes = [
        ["Unités", str(len(d["unites"]))],
        ["Domaines — les quatre du programme", str(len(d["domaines"]))],
    ]
    lignes.extend(
        [f"dont {x['id']} — {x['libelle']}", str(par_domaine[x["id"]])] for x in d["domaines"]
    )
    lignes.extend([
        ["Unités dont l'objectif porte un acte de parole", str(len(prod))],
        ["dont avec un geste — dette d'une `inversion`", str(len(avec))],
        ["dont sans geste — dette d'un `pourquoi_hors_app`", str(len(sans))],
        ["Exemples repris du programme",
         str(sum(1 for u in d["unites"] if u["exemples_source"] == "programme"))],
        ["Exemples de notre main",
         str(sum(1 for u in d["unites"] if u["exemples_source"] != "programme"))],
        ["Citations officielles", str(len(citations))],
        ["Réussites au palier de sortie", str(len(palier))],
        ["dont vérifiables dans l'app", str(verifiables)],
        ["dont hors app, au bilan", str(len(palier) - verifiables)],
        ["Domaines écartés de la tranche", str(len(hors_tranche["contenu"]))],
    ])
    parties.append("\n".join(["### Le décompte", ""] + tableau(["Point", "Nombre"], lignes)))

    return "\n\n".join(parties)


# --------------------------------------------------------------------------
# 7. La table des textes du CE1
# --------------------------------------------------------------------------

def rendre_textes_ce1(dossier):
    ce1 = charger("cgp-ce1.json")
    prog = charger("progression-ce1.json")
    periode = {u["rang"]: u["periode"] for u in prog["unites"]}
    nouvelle = {u["rang"]: u["cgp"][0] for u in ce1["unites"] if u.get("cgp")}

    verifier = charger_module("verifier_textes_ce1", OUTILS / "verifier-textes-ce1.py")

    lignes = []
    for chemin in sorted(dossier.glob("*.txt")):
        brut = chemin.read_bytes().decode("utf-8")
        entetes = [l for l in brut.split("\n") if l.startswith("# ")]
        rang = int(entetes[0].split(":")[1].strip())
        titre = entetes[1][2:].strip()
        corps = "\n".join(
            l for l in brut.split("\n") if l.strip() and not l.startswith("# ")
        )
        lignes.append([
            f"`{chemin.name}`",
            str(rang),
            str(periode[rang]),
            titre,
            str(len(verifier.lignes_du_texte(corps))),
            str(mots_du_texte(corps)),
            nouvelle.get(rang, "—"),
        ])
    return "\n".join(tableau(
        ["Texte", "Rang", "Période", "Titre", "Lignes de 34 signes", "Mots",
         "CGP nouvelle du rang"], lignes
    ))


# --------------------------------------------------------------------------
# 7 bis. Les textes courts du CE1
# --------------------------------------------------------------------------

def rendre_textes_courts(dossier):
    """Le corpus des textes courts : ce qu'ils sont, ce qu'ils disent, et qui les cite.

    Les textes courts ne sont pas des textes du palier : ils font de deux à six
    lignes, ils sont portés par un exercice, et ils ne se relisent pas seuls. Ils
    ont pourtant un rang, un type et un titre — c'est le type qui rend vérifiable
    la réponse d'un exercice qui demande de distinguer un récit d'un documentaire.
    """
    verifier = charger_module("verifier_textes_ce1", OUTILS / "verifier-textes-ce1.py")
    vtc = charger_module("verifier_textes_courts_ce1", OUTILS / "verifier-textes-courts-ce1.py")
    d = charger("exercices-ce1.json")

    employeurs = {}
    for e in d["exercices"]:
        for nom in e.get("textes_courts", []):
            employeurs.setdefault(nom, []).append(e["id"])

    fiches = []
    for chemin in sorted(dossier.glob("*.txt")):
        brut = chemin.read_bytes().decode("utf-8")
        meta, titre, corps = vtc.analyser(brut)
        fiches.append((chemin, meta, titre, corps))

    lignes = [
        [f"`{chemin.name}`", meta.get("rang", "?"), meta.get("type", "?"), titre or "—",
         str(len(verifier.lignes_du_texte("\n".join(corps)))),
         liste(employeurs.get(chemin.stem)) if employeurs.get(chemin.stem) else "**aucun**"]
        for chemin, meta, titre, corps in fiches
    ]
    parties = ["\n".join(
        [f"### Les {len(lignes)} textes courts", ""]
        + tableau(["Texte", "Rang", "Type", "Titre", "Lignes de 34 signes", "Cité par"], lignes)
    )]

    lignes = [[f"`{chemin.name}`", titre or "—", " / ".join(corps)]
              for chemin, _, titre, corps in fiches]
    parties.append("\n".join(
        [f"### Ce que disent les {len(lignes)} textes courts", ""]
        + tableau(["Texte", "Titre", "Le texte"], lignes)
    ))

    return "\n\n".join(parties)


# --------------------------------------------------------------------------
# 8. La banque d'exercices de la GS
# --------------------------------------------------------------------------

def rendre_exercices(d):
    prog = charger("progression-gs.json")
    corpus = charger("corpus-gs.json")
    consignes = {c["slug"]: c["texte"] for c in corpus["consignes"]}
    par_unite = {u["rang"]: u for u in prog["unites"]}
    exercices = d["exercices"]

    employeurs = {}
    for e in exercices:
        employeurs.setdefault(e["consigne"], []).append(e["id"])

    # Un exercice hors app peut n'avoir aucune consigne : l'application n'a rien
    # à dire, et une cellule vide se lirait comme un oubli.
    def dire(identifiant):
        return f"« {consignes[identifiant]} »" if identifiant else "—"

    def mecanique_de(e):
        # Un exercice entièrement hors app peut n'employer aucune mécanique.
        return f"`{e['mecanique']}`" if e.get("mecanique") else "—"

    parties = []

    lignes = [
        [f"`{m['id']}` — {m['libelle']}", m["ce_que_l_enfant_fait"],
         m["ce_que_l_application_fait"], m["verdict"]]
        for m in d["mecaniques"]
    ]
    parties.append("\n".join(
        [f"### Les {en_lettres(len(d['mecaniques']))} mécaniques", ""]
        + tableau(["Mécanique", "Ce que l'enfant fait", "Ce que l'application fait", "Verdict"],
                  lignes)
    ))

    lignes = [
        [f"`{e['id']}`", str(e["unite"]), mecanique_de(e), e["titre"],
         dire(e.get("consigne")), e["geste"], e["verdict"], f"{e['duree_s']} s"]
        for e in exercices
    ]
    parties.append("\n".join(
        [f"### Les {en_lettres(len(exercices))} exercices", ""]
        + tableau(["Item", "Unité", "Mécanique", "Titre", "Ce que la voix dit",
                   "Ce que l'enfant fait", "Verdict", "Durée"], lignes)
    ))

    lignes = []
    for e in exercices:
        affiches = e.get("affiches") or []
        lignes.append([
            f"`{e['id']}`",
            liste(e.get("serie"), gabarit="{}", separateur=" ; "),
            liste(e.get("mots")),
            liste(affiches) if affiches else "—",
            liste(e.get("phonemes")),
            liste(e.get("lettres")),
        ])
    parties.append("\n".join(
        ["### Le contenu et le matériel", ""]
        + tableau(["Item", "Contenu de la série", "Mots employés", "Dont affichés en image",
                   "Phonèmes", "Lettres"], lignes)
    ))

    lignes = [[f"`{e['id']}`", e["entraine"], e["ne_verifie_pas"]] for e in exercices]
    parties.append("\n".join(
        ["### Ce que chaque exercice entraîne, et ce qu'il ne vérifie pas", ""]
        + tableau(["Item", "Entraîne", "Ne vérifie pas"], lignes)
    ))

    inversions = [e for e in exercices if e.get("inversion")]
    lignes = [
        [f"`{e['id']}`", str(e["unite"]), par_unite[e["unite"]]["objectif"], e["inversion"]]
        for e in inversions
    ]
    parties.append("\n".join(
        [f"### Les {len(inversions)} inversions — ce que le geste reprend", ""]
        + tableau(["Item", "Unité", "Objectif de l'unité", "Ce que le geste reprend"], lignes)
    ))

    hors = [e for e in exercices if e.get("pourquoi_hors_app")]
    lignes = [
        [f"`{e['id']}`", str(e["unite"]), e["pourquoi_hors_app"], e.get("substitution") or "—"]
        for e in hors
    ]
    parties.append("\n".join(
        [f"### Les {len(hors)} exercices hors app", ""]
        + tableau(["Item", "Unité", "Pourquoi l'application ne peut pas juger", "Substitution"],
                  lignes)
    ))

    lignes = [
        [f"`{b['id']}`", str(b["unite"]), b["manque"], b["detail"],
         "**oui**" if b["bloque"] else "non"]
        for b in d["besoins"]
    ]
    parties.append("\n".join(
        ["### Les besoins déclarés", ""]
        + tableau(["Id", "Unité", "Ce qui manque", "Détail", "Bloque ?"], lignes)
    ))

    parties.append(bloc_corrections("### Les corrections consignées", d["corrections"]))

    employees = [m for m in d["mecaniques"] if any(e.get("mecanique") == m["id"] for e in exercices)]
    lignes = [
        ["Unités de la progression", str(len(prog["unites"]))],
        ["Unités servies par au moins un exercice", str(len({e["unite"] for e in exercices}))],
        ["Unités dont l'objectif porte une production",
         str(sum(1 for u in prog["unites"] if u.get("production")))],
        ["Mécaniques", str(len(d["mecaniques"]))],
        ["Mécaniques employées", str(len(employees))],
        ["Exercices", str(len(exercices))],
        ["dont jugés par l'application",
         str(sum(1 for e in exercices if e["verdict"] != "hors app"))],
        ["dont hors app", str(len(hors))],
        ["dont avec une inversion déclarée", str(len(inversions))],
        ["Besoins déclarés", str(len(d["besoins"]))],
        ["dont bloquants", str(sum(1 for b in d["besoins"] if b["bloque"]))],
        ["Corrections consignées", str(len(d["corrections"]))],
        ["Durée cumulée des exercices", f"{sum(e['duree_s'] for e in exercices)} s"],
    ]
    parties.append("\n".join(["### Le décompte", ""] + tableau(["Point", "Nombre"], lignes)))

    return "\n\n".join(parties)


# --------------------------------------------------------------------------
# 9. La banque d'exercices du CE1
# --------------------------------------------------------------------------

def rendre_exercices_ce1(d):
    prog = charger("progression-ce1.json")
    par_unite = {u["rang"]: u for u in prog["unites"]}
    domaines = {u["rang"]: u["domaine"] for u in prog["unites"]}
    consignes = {c["id"]: c["texte"] for c in d["consignes"]}
    exercices = d["exercices"]
    # Les pseudo-mots sont CITÉS : le tableau montre la suite, et l'identifiant
    # entre parenthèses, parce que c'est l'identifiant qui est dans la banque et
    # la suite qui est dans le corpus. Montrer l'un sans l'autre laisserait
    # croire que la banque porte encore les mots.
    suites_pm = {p["id"]: p["mot"] for p in charger("pseudo-mots-ce1.json")["pseudo_mots"]}

    employeurs = {}
    for e in exercices:
        employeurs.setdefault(e["consigne"], []).append(e["id"])

    def dire(identifiant):
        return f"« {consignes[identifiant]} »" if identifiant else "—"

    parties = []

    lignes = [
        [f"`{m['id']}` — {m['libelle']}", m["ce_que_l_enfant_fait"],
         m["ce_que_l_application_fait"], m["verdict"]]
        for m in d["mecaniques"]
    ]
    parties.append("\n".join(
        [f"### Les {len(d['mecaniques'])} mécaniques", ""]
        + tableau(["Mécanique", "Ce que l'enfant fait", "Ce que l'application fait", "Verdict"],
                  lignes)
    ))

    lignes = [
        [f"`{c['id']}`", dire(c["id"]), c["picto"],
         liste(employeurs.get(c["id"], [])) if employeurs.get(c["id"]) else "**aucune**"]
        for c in d["consignes"]
    ]
    parties.append("\n".join(
        [f"### Les {len(d['consignes'])} consignes — le script à enregistrer", ""]
        + tableau(["Consigne", "Ce que la voix dit", "Pictogramme", "Employée par"], lignes)
    ))

    lignes = [
        [f"`{e['id']}`", str(e["unite"]), domaines[e["unite"]], f"`{e['mecanique']}`",
         e["titre"], dire(e.get("consigne")), e["geste"], e["verdict"],
         f"{e['duree_s']} s"]
        for e in exercices
    ]
    parties.append("\n".join(
        [f"### Les {len(exercices)} exercices", ""]
        + tableau(["Item", "Unité", "Domaine", "Mécanique", "Titre", "Ce que la voix dit",
                   "Ce que l'enfant fait", "Verdict", "Durée"], lignes)
    ))

    lignes = []
    for e in exercices:
        affiches = e.get("affiches") or []
        courts = e.get("textes_courts") or []
        lignes.append([
            f"`{e['id']}`",
            liste(e.get("serie"), gabarit="{}", separateur=" ; "),
            liste(e.get("mots")),
            liste(affiches) if affiches else "—",
            liste(e.get("phonemes")),
            liste(e.get("graphies")),
            e.get("texte") or "—",
            liste(courts) if courts else "—",
            liste([f"`{suites_pm.get(pid, pid)}` ({pid})" for pid in e["pseudo_mots"]])
            if e.get("pseudo_mots") else "—",
        ])

    parties.append("\n".join(
        ["### Le contenu et le matériel", ""]
        + tableau(["Item", "Contenu de la série", "Mots", "Dont affichés en image", "Phonèmes",
                   "Graphies", "Texte adossé", "Textes courts cités", "Pseudo-mots"], lignes)
    ))

    lignes = [[f"`{e['id']}`", e["entraine"], e["ne_verifie_pas"]] for e in exercices]
    parties.append("\n".join(
        ["### Ce que chaque exercice entraîne, et ce qu'il ne vérifie pas", ""]
        + tableau(["Item", "Entraîne", "Ne vérifie pas"], lignes)
    ))

    questions = []
    for e in exercices:
        # Une question porte sur un texte de la tranche, ou sur les textes courts
        # que l'exercice CITE : la colonne les nomme, et ne se contente plus de
        # dire « textes courts » — une citation qu'on ne nomme pas ne se vérifie
        # pas à la lecture du document.
        courts = e.get("textes_courts") or []
        support = e.get("texte") or (liste(courts) if courts else "—")
        for q in e.get("questions") or []:
            questions.append([
                f"`{e['id']}`", support, q["question"], q["bonne"],
                " ; ".join(q["intrus"]), f"« {q['phrase_preuve']} »",
            ])
    parties.append("\n".join(
        [f"### Les {len(questions)} questions, et leur phrase-preuve", ""]
        + tableau(["Item", "Texte", "Question", "Bonne réponse", "Intrus", "Phrase-preuve"],
                  questions)
    ))

    inversions = [e for e in exercices if e.get("inversion")]
    lignes = [
        [f"`{e['id']}`", str(e["unite"]), par_unite[e["unite"]]["objectif"], e["inversion"]]
        for e in inversions
    ]
    parties.append("\n".join(
        [f"### Les {len(inversions)} inversions — ce que le geste reprend", ""]
        + tableau(["Item", "Unité", "Objectif de l'unité", "Ce que le geste reprend"], lignes)
    ))

    hors = [e for e in exercices if e.get("pourquoi_hors_app")]
    lignes = [
        [f"`{e['id']}`", str(e["unite"]), e["pourquoi_hors_app"], e.get("substitution") or "—"]
        for e in hors
    ]
    parties.append("\n".join(
        [f"### Les {len(hors)} exercices hors app", ""]
        + tableau(["Item", "Unité", "Pourquoi l'application ne peut pas juger", "Substitution"],
                  lignes)
    ))

    lignes = [
        [f"`{b['id']}`", str(b["unite"]), b["manque"], b["detail"],
         "**oui**" if b["bloque"] else "non"]
        for b in d["besoins"]
    ]
    parties.append("\n".join(
        [f"### Les {len(d['besoins'])} besoins déclarés", ""]
        + tableau(["Id", "Unité", "Ce qui manque", "Détail", "Bloque ?"], lignes)
    ))

    parties.append(bloc_corrections(
        f"### Les {len(d['corrections'])} corrections consignées", d["corrections"]
    ))

    textes = {e["texte"] for e in exercices if e.get("texte")}
    lignes = [
        ["Unités de la progression", str(len(prog["unites"]))],
        ["Unités servies par au moins un exercice", str(len({e["unite"] for e in exercices}))],
        ["Unités dont l'objectif porte une production",
         str(sum(1 for u in prog["unites"] if u.get("production")))],
        ["Mécaniques", str(len(d["mecaniques"]))],
        ["Mécaniques employées", str(len({e["mecanique"] for e in exercices}))],
        ["Consignes déclarées", str(len(d["consignes"]))],
        ["Consignes employées", str(len({e["consigne"] for e in exercices}))],
        ["Exercices", str(len(exercices))],
        ["dont jugés par l'application",
         str(sum(1 for e in exercices if e["verdict"] != "hors app"))],
        ["dont hors app", str(len(hors))],
        ["dont avec une inversion déclarée", str(len(inversions))],
        ["dont adossés à un texte", str(sum(1 for e in exercices if e.get("texte")))],
        ["Textes de la tranche employés", str(len(textes))],
        ["Questions avec leur phrase-preuve", str(len(questions))],
        ["Exercices citant des textes courts",
         str(sum(1 for e in exercices if e.get("textes_courts")))],
        ["Citations de textes courts",
         str(sum(len(e.get("textes_courts") or []) for e in exercices))],
        ["Exercices citant des pseudo-mots",
         str(sum(1 for e in exercices if e.get("pseudo_mots")))],
        ["Citations de pseudo-mots",
         str(sum(len(e.get("pseudo_mots") or []) for e in exercices))],
        ["Besoins déclarés", str(len(d["besoins"]))],
        ["dont bloquants", str(sum(1 for b in d["besoins"] if b["bloque"]))],
        ["Corrections consignées", str(len(d["corrections"]))],
        ["Durée cumulée des exercices", f"{sum(e['duree_s'] for e in exercices)} s"],
    ]
    parties.append("\n".join(["### Le décompte", ""] + tableau(["Point", "Nombre"], lignes)))

    return "\n\n".join(parties)


# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# 10. Les images du CE1
# --------------------------------------------------------------------------

def rendre_images_ce1(d):
    """Les deux tableaux du corpus d'images du CE1.

    Les deux sont nécessaires, et pour la même raison : un corpus qui ne montrerait
    que ses images laisserait croire que les vingt-deux autres mots n'ont jamais
    été examinés. Le premier tableau dit ce qui est DESSINÉ, le second ce qui est
    DÉCLARÉ non dessinable — et le second est la vraie réponse aux besoins.
    """
    lignes = []
    for i in d["items"]:
        emploi = i["employable_par"]
        ou = f"`{emploi['exercice']}`"
        if not emploi["present_dans_la_serie"]:
            ou += " — **à ajouter à la série**"
        lignes.append([
            f"`{i['mot']}`", str(i["rang"]), i["besoin"], f"`{i['graphie']}`",
            " | ".join(i["decoupe"]), i["objet"], ou,
        ])
    premier = tableau(
        ["Mot", "Rang", "Besoin", "Graphie", "Découpe", "Objet du dessin", "Emploi"],
        lignes,
    )

    refus = sorted(
        d["non_illustrables"], key=lambda n: (n["besoin"], n["rang"], n["mot"])
    )
    second = tableau(
        ["Besoin", "Mot", "Rang", "Motif", "Raison"],
        [[n["besoin"], f"`{n['mot']}`", str(n["rang"]), n["motif"], n["raison"]]
         for n in refus],
    )

    motifs = {}
    for n in d["non_illustrables"]:
        motifs[n["motif"]] = motifs.get(n["motif"], 0) + 1
    recapitulatif = tableau(
        ["Motif", "Mots"],
        [[m, str(c)] for m, c in sorted(motifs.items(), key=lambda p: (-p[1], p[0]))],
    )

    return "\n\n".join([
        "\n".join(premier),
        "\n".join(second),
        "\n".join(recapitulatif),
    ])


def rendre_images_recit(d):
    """Les trois tableaux du corpus d'images de récit.

    Le premier dit les moments DANS L'ORDRE — c'est la seule disposition qui
    montre ce que ces images doivent faire, et un tableau trié par identifiant ne
    le montrerait pas, puisque l'ordre EST l'information. Le deuxième dit les
    confusions redoutées et leur parade : c'est la matière du travail, parce que
    quatre images qui se ressemblent sont quatre images qu'on ne peut pas remettre
    dans l'ordre. Le troisième dit les exercices de la même mécanique qui ne
    jouent PAS sur des images — un corpus qui ne montrerait que ses deux récits
    laisserait croire que la banque n'en compte que deux.
    """
    lignes = []
    for r in d["recits"]:
        for e in r["etapes"]:
            lignes.append([
                f"`{r['exercice']}`", str(e["ordre"]), f"`{e['id']}`", e["moment"],
                f"« {e['ligne_citee']} »", e["repere"],
            ])
    moments = tableau(
        ["Exercice", "Ordre", "Étape", "Moment", "Ligne citée", "Repère"],
        lignes,
    )

    risques = []
    for r in d["recits"]:
        for e in r["etapes"]:
            for x in e.get("risque") or []:
                risques.append([
                    f"`{e['id']}`", f"`{x['avec']}`", x["pourquoi"], x["parade"],
                ])
    confusions = tableau(["Étape", "Craint", "Pourquoi", "Parade"], risques)

    sans = tableau(
        ["Exercice", "Raison"],
        [[f"`{x['exercice']}`", x["raison"]] for x in d["exercices_sans_images"]],
    )

    return "\n\n".join([
        "\n".join(moments),
        "\n".join(confusions),
        "\n".join(sans),
    ])


# --------------------------------------------------------------------------
# 12 bis. Les pseudo-mots du CE1
# --------------------------------------------------------------------------

def rendre_pseudo_mots(d):
    """Le corpus des pseudo-mots : ce que la voix dit, et ce que chaque suite fait travailler.

    LA LECTURE EST DÉRIVÉE ICI, PAS RECOPIÉE. Elle est calculée par le contrôle
    lui-même, avec le même décodeur et les mêmes tables. Une transcription
    recopiée dans un document diverge du jour où la table change, et personne ne
    le voit. C'est le script de l'enregistrement : la voix dit ce que ce tableau
    donne, et rien d'autre.
    """
    vpm = charger_module("verifier_pseudo_mots", OUTILS / "verifier-pseudo-mots.py")
    vc = charger_module("verifier_textes_ce1", OUTILS / "verifier-textes-ce1.py")
    cp, ce1 = charger("cgp-cp.json"), charger("cgp-ce1.json")
    phonemes, _rangs, _tranches, _erreurs = vpm.tables()
    autorisees = vc.cgp_autorisees(cp, ce1, vpm.RANG_DE_LECTURE)
    sans_son = vc.lettres_sans_son(ce1)
    banque = charger("exercices-ce1.json")

    employeurs = {}
    for e in banque["exercices"]:
        for pid in e.get("pseudo_mots", []):
            employeurs.setdefault(pid, []).append(e["id"])

    lignes = []
    for p in d["pseudo_mots"]:
        lecture, _inconnus = vpm.lecture_mecanique(
            p["mot"], vc, autorisees, phonemes, sans_son
        )
        lignes.append([
            f"`{p['id']}`", f"`{p['mot']}`", lecture, liste(p["graphies"]),
            p["complexite"], p["origine"], liste(employeurs.get(p["id"])),
        ])
    parties = ["\n".join(
        [f"### Les {len(lignes)} pseudo-mots", ""]
        + tableau(["Identifiant", "Suite", "Lecture dérivée", "Graphies", "Complexité",
                   "Origine", "Cité par"], lignes)
    )]

    # Les graphies qui ne se lisent pas : le document les nomme, parce que c'est
    # ce qui explique pourquoi aucune suite du corpus n'est bâtie sur elles.
    rang_de = {}
    for u in cp["unites"] + ce1["unites"]:
        for g in u.get("graphies", []):
            rang_de.setdefault(g, (u["rang"], u.get("phoneme")))
    lignes = [
        [f"`{g}`", str(rang_de[g][0]), rang_de[g][1]]
        for g in vpm.graphies_sans_lecture()
    ]
    parties.append("\n".join(
        [f"### Les {len(lignes)} graphies dont la lecture ne se dérive pas", ""]
        + tableau(["Graphie", "Unité qui l'enseigne", "Ce que la table déclare"], lignes)
    ))
    return "\n\n".join(parties)


TRAVAUX = [
    {"donnees": "cgp-cp.json", "document": "contenu/LUDOLIRE-CGP-CP.md", "rendu": rendre_cp},
    {"donnees": "progression-gs.json", "document": "contenu/LUDOLIRE-PROGRESSION-GS.md", "rendu": rendre_gs},
    {"donnees": "corpus-gs.json", "document": "contenu/LUDOLIRE-CORPUS-AUDIO-GS.md", "rendu": rendre_corpus},
    {"donnees": "jeu-syllabes.json", "document": "contenu/LUDOLIRE-JEU-SYLLABES.md", "rendu": rendre_jeu},
    {"donnees": "images-gs.json", "document": "contenu/LUDOLIRE-IMAGES-GS.md", "rendu": rendre_images},
    {"donnees": "exercices-gs.json", "document": "contenu/LUDOLIRE-EXERCICES-GS.md", "rendu": rendre_exercices},
    {"donnees": "progression-ce1.json", "document": "contenu/LUDOLIRE-PROGRESSION-CE1.md", "rendu": rendre_ce1},
    {"dossier": "contenu/textes-ce1", "document": "contenu/LUDOLIRE-TEXTES-CE1.md", "rendu": rendre_textes_ce1},
    {"dossier": "contenu/textes-courts-ce1", "document": "contenu/LUDOLIRE-TEXTES-COURTS-CE1.md", "rendu": rendre_textes_courts},
    {"donnees": "exercices-ce1.json", "document": "contenu/LUDOLIRE-EXERCICES-CE1.md", "rendu": rendre_exercices_ce1},
    {"donnees": "images-ce1.json", "document": "contenu/LUDOLIRE-IMAGES-CE1.md", "rendu": rendre_images_ce1},
    {"donnees": "images-recit-ce1.json", "document": "contenu/LUDOLIRE-IMAGES-RECIT-CE1.md", "rendu": rendre_images_recit},
    {"donnees": "pseudo-mots-ce1.json", "document": "contenu/LUDOLIRE-PSEUDO-MOTS-CE1.md", "rendu": rendre_pseudo_mots},
]


def rendre(travail):
    if "dossier" in travail:
        return travail["rendu"](RACINE / travail["dossier"])
    return travail["rendu"](charger(travail["donnees"]))


def traiter(travail):
    chemin = RACINE / travail["document"]
    texte = chemin.read_bytes().decode("utf-8")
    if DEBUT not in texte or FIN not in texte:
        print(f"  {travail['document']} : MARQUEURS ABSENTS")
        return False

    corps = rendre(travail)
    debut = texte.index(DEBUT) + len(DEBUT)
    fin = texte.index(FIN)
    attendu = "\n\n" + corps + "\n\n"

    if texte[debut:fin] == attendu:
        print(f"  {travail['document']} : déjà à jour.")
        return False

    chemin.write_bytes((texte[:debut] + attendu + texte[fin:]).encode("utf-8"))
    print(f"  {travail['document']} : écrit.")
    return True


def main():
    ecrits = 0
    for travail in TRAVAUX:
        if traiter(travail):
            ecrits += 1
    print()
    print(f"{len(TRAVAUX)} tableaux, {ecrits} réécrit(s), {len(TRAVAUX) - ecrits} déjà à jour.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
