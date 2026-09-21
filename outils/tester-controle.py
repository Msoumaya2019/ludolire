"""Éprouve le contrôle de conformité des textes.

Un contrôle se falsifie avant qu'on s'y fie : ce harnais vérifie que les textes
conformes passent **et** que les contrôles négatifs sont refusés. Un harnais qui
ne vérifie que le premier point ne prouve rien — il serait vert avec un contrôle
qui accepte tout.

Les contrôles négatifs portent en plus un **fragment attendu** dans la sortie.
Un refus n'est probant que si l'on sait sur quoi il porte : un texte refusé pour
une autre raison que celle qu'on veut éprouver ne prouve rien. Le harnais vérifie
donc le code de sortie *et* la raison rapportée.

Usage :
    python tester-controle.py
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
PYTHON = sys.executable

# (fichier, rang, code attendu, libellé, fragment attendu dans la sortie ou None)
CAS = [
    ("contenu/textes/T01-rang10.txt", 10, 0, "texte conforme, rang 10", None),
    ("contenu/textes/T02-rang16.txt", 16, 0, "texte conforme, rang 16", None),
    ("contenu/textes/T03-rang23.txt", 23, 0, "texte conforme, rang 23", None),
    (
        "outils/tests/controle-negatif.txt",
        10,
        1,
        "contrôle négatif, CGP non enseignée",
        "non enseignée",
    ),
    (
        "outils/tests/controle-negatif-ent.txt",
        20,
        1,
        "contrôle négatif, terminaison -ent",
        "terminaison -ent interdite",
    ),
    (
        "outils/tests/controle-negatif-nasale.txt",
        20,
        1,
        "contrôle négatif, nasale finale",
        "CGP 'on' non enseignée",
    ),
]


# ---------------------------------------------------------------------------
# LA LECTURE, ET PAS SEULEMENT LE VERDICT.
#
# `d'un` était accepté, mais avec un d muet : la découpe jette l'apostrophe, et
# `d` arrivait au contrôle comme un mot d'une lettre dont la consonne finale
# serait muette. Accepté, mais mal lu — et un texte refusé se voit, alors qu'un
# texte accepté de travers ne se voit pas.
#
# (mot, graphèmes muets attendus, ce qui est éprouvé)
# ---------------------------------------------------------------------------
LECTURES = [
    ("d", [], "d : le d de « d'un » est une attaque, il se prononce"),
    ("s", [], "s : le s de « s'il » n'est pas un pluriel"),
    ("t", [], "t : le t de « t'a » n'est pas muet"),
    ("l", [], "l : le l de « l'âne » est une attaque"),
    ("les", ["s"], "les : le s est muet, et la queue s'arrête avant le e"),
    ("pattes", ["e", "s"], "pattes : le e et le s sont muets tous les deux"),
    ("lit", ["t"], "lit : le t final est muet"),
    ("dix", ["x"], "dix : le x final est muet"),
]


def main():
    echecs = 0
    for chemin, rang, attendu, libelle, fragment in CAS:
        fichier = RACINE / chemin
        if not fichier.exists():
            print(f"  MANQUANT   {libelle} — {chemin}")
            echecs += 1
            continue
        r = subprocess.run(
            [PYTHON, str(ICI / "verifier-textes.py"), "--rang", str(rang), str(fichier)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        ok = r.returncode == attendu
        detail = f"code {r.returncode}, attendu {attendu}"
        if ok and fragment is not None:
            if fragment in r.stdout:
                detail += f", motif « {fragment} » présent"
            else:
                ok = False
                detail += f", motif « {fragment} » ABSENT de la sortie"
        etat = "OK        " if ok else "ÉCHEC     "
        print(f"  {etat} {libelle} ({detail})")
        if not ok:
            echecs += 1

    # ------------------------------------------------------------------
    # LA LECTURE, ET PAS SEULEMENT LE VERDICT.
    #
    # Un mot accepté peut être lu de travers, et le verdict seul ne le dit pas :
    # `d'un` était accepté, mais avec un d muet. On éprouve donc aussi QUELS
    # graphèmes sont muets. C'est le même angle mort que celui trouvé au CE1.
    #
    # (mot, graphèmes muets attendus, ce qui est éprouvé)
    # ------------------------------------------------------------------
    spec = importlib.util.spec_from_file_location("vt", ICI / "verifier-textes.py")
    vt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vt)

    print()
    print("  --- la lecture : quels graphèmes sont muets ---")
    for mot, attendu, quoi in LECTURES:
        morceaux = vt.decouper(mot)
        muets = vt.indices_muets_finaux(mot, morceaux)
        obtenu = [morceaux[i][0] for i in sorted(muets)]
        if obtenu != attendu:
            echecs += 1
        etat = "OK        " if obtenu == attendu else "ÉCHEC     "
        print(f"  {etat} {mot:10s} attendu muets {str(attendu):12s} "
              f"obtenu muets {str(obtenu):12s}  {quoi}")

    print()
    if echecs:
        print(f"{echecs} cas en échec sur {len(CAS) + len(LECTURES)}.")
        return 1
    print(f"{len(CAS)} textes et {len(LECTURES)} lectures conformes à l'attendu.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
