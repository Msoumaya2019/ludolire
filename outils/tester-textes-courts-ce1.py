"""Éprouve le contrôle des textes courts du CE1 en le faisant échouer.

Le contrôle tourne sur une COPIE du corpus, dans un dossier temporaire : les
vrais fichiers ne sont jamais touchés. Chaque cas porte le message qu'il doit
déclencher, et le banc refuse un cas qui échoue pour une autre raison — ou qui
ne fait rien échouer du tout.

Un témoin vert sur le corpus réel est joué en premier : sans lui, un contrôle qui
refuserait tout passerait le banc.

CE QUE CE BANC NE PEUT PAS PROUVER : que le type déclaré d'un texte soit le bon.
Le contrôle lit le type, il ne juge pas le texte — et aucun script ne peut le
juger.
"""

import contextlib
import importlib.util
import io
import pathlib
import shutil
import sys
import tempfile

RACINE = pathlib.Path(r"C:\Users\mchik\WorkBuddy AI\2026-09-21-15-03-17")
ICI = RACINE / "outils"
SOURCE = RACINE / "contenu" / "textes-courts-ce1"


def charger_module(nom):
    spec = importlib.util.spec_from_file_location("verifier_textes_courts_ce1", ICI / nom)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VTC = charger_module("verifier-textes-courts-ce1.py")


def jouer(dossier):
    """Fait tourner le contrôle sur un dossier donné, et rend sa sortie."""
    VTC.COURTS = pathlib.Path(dossier)
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        code = VTC.main()
    return code, tampon.getvalue()


def ecrire(dossier, nom, contenu):
    chemin = pathlib.Path(dossier) / nom
    chemin.write_bytes(contenu.encode("utf-8"))


def lire(dossier, nom):
    return (pathlib.Path(dossier) / nom).read_text(encoding="utf-8")


def remplacer(dossier, nom, avant, apres):
    contenu = lire(dossier, nom)
    if avant not in contenu:
        raise SystemExit(f"ancre absente de {nom} : « {avant} »")
    ecrire(dossier, nom, contenu.replace(avant, apres, 1))


CAS = []


def cas(nom, attendu):
    def enveloppe(f):
        CAS.append((nom, attendu, f))
        return f
    return enveloppe


@cas("rang_absent", "aucun rang déclaré")
def _(d):
    remplacer(d, "C01-rang16.txt", "# rang: 16\n", "")


@cas("rang_non_numerique", "aucun rang déclaré")
def _(d):
    remplacer(d, "C01-rang16.txt", "# rang: 16", "# rang: seize")


@cas("type_absent", "aucun type déclaré")
def _(d):
    remplacer(d, "C01-rang16.txt", "# type: recit\n", "")


@cas("type_inconnu", "type « poeme » inconnu")
def _(d):
    remplacer(d, "C01-rang16.txt", "# type: recit", "# type: poeme")


@cas("titre_absent", "aucun titre")
def _(d):
    remplacer(d, "C01-rang16.txt", "# titre: L'agneau de la reine\n", "")


@cas("titre_du_palier", "reprend celui d'un texte du palier")
def _(d):
    remplacer(d, "C01-rang16.txt", "# titre: L'agneau de la reine", "# titre: Le vent")


@cas("titre_qui_contient_un_titre_du_palier", "reprend celui d'un texte du palier")
def _(d):
    remplacer(d, "C01-rang16.txt", "# titre: L'agneau de la reine", "# titre: Le vent du soir")


@cas("phrase_recopiee_du_palier", "est déjà une ligne de")
def _(d):
    remplacer(d, "C01-rang16.txt", "La reine rit.", "La reine a un chat brun.")


@cas("phrase_partagee_entre_deux_courts", "est dans deux textes courts")
def _(d):
    remplacer(d, "C03-rang27.txt", "Ils dorment le jour.", "La reine rit.")


@cas("titre_partage_entre_deux_courts", "deux textes courts portent le titre")
def _(d):
    remplacer(d, "C02-rang16.txt", "# titre: L'air qui va", "# titre: Les chats")


@cas("trop_long", "un texte court va de")
def _(d):
    remplacer(d, "C03-rang27.txt", "La reine les aime.",
              "La reine les aime.\nLes chats aiment le foin.\nIls aiment la montagne.\n"
              "Le soir, ils vont dans le jardin.\nLa reine rit.")


@cas("trop_court", "un texte court va de")
def _(d):
    ecrire(d, "C05-rang41.txt",
           "# rang: 41\n# type: recit\n# titre: Le téléphone de papa\n\nPapa a un téléphone.\n")


@cas("illisible_au_rang", "illisible au rang 16")
def _(d):
    remplacer(d, "C01-rang16.txt", "La reine rit.", "La reine a une pomme.")


@cas("fichier_vide", "le fichier ne contient aucun texte")
def _(d):
    ecrire(d, "C04-rang41.txt", "# rang: 41\n# type: recit\n# titre: Une échelle, une pomme\n")


def main():
    cas_vus, cas_rates = 0, []
    vus = []

    # Le témoin : sur une copie intacte, le contrôle doit être CONFORME.
    with tempfile.TemporaryDirectory() as racine:
        temoin = pathlib.Path(racine) / "temoin"
        shutil.copytree(SOURCE, temoin)
        code, sortie = jouer(temoin)
        if code != 0:
            print("TÉMOIN ROUGE — le contrôle refuse le corpus réel :")
            print(sortie)
            return 1
        print("Témoin : le corpus réel est accepté")

        # Le corpus vide.
        vide = pathlib.Path(racine) / "vide"
        vide.mkdir()
        code, sortie = jouer(vide)
        if code != 0 and "le corpus est vide" in sortie:
            cas_vus += 1
            vus.append("corpus_vide")
        else:
            cas_rates.append(("corpus_vide", "le corpus est vide", sortie))

        for nom, attendu, mutation in CAS:
            dossier = pathlib.Path(racine) / nom
            shutil.copytree(SOURCE, dossier)
            mutation(dossier)
            code, sortie = jouer(dossier)
            if code == 0:
                cas_rates.append((nom, attendu, "le contrôle n'a RIEN vu"))
            elif attendu not in sortie:
                cas_rates.append((nom, attendu, sortie))
            else:
                cas_vus += 1
                vus.append(nom)

    if cas_rates:
        print(f"\n{len(cas_rates)} cas raté(s) :")
        for nom, attendu, sortie in cas_rates:
            print(f"\n--- {nom} : attendu « {attendu} »")
            print(sortie.strip()[:1200])
        return 1

    total = cas_vus + 1
    print(f"{cas_vus} corpus faux et 1 témoin : {total} essais, tous vus — "
          f"le contrôle des textes courts a des dents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
