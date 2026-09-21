"""Dessine les illustrations des trois tranches, en SVG écrit comme du code.

Trois jeux, trois métiers. La **GS** (44 icônes, `contenu/images/`) : l'image
PORTE le mot, l'enfant ne lit pas encore. Le **CE1 lexical** (3 icônes,
`contenu/images-ce1/`) : l'image VÉRIFIE le mot, l'enfant l'a lu d'abord. Le
**récit du CE1** (8 scènes, `contenu/images-recit-ce1/`) : l'image porte un
MOMENT, et quatre moments doivent pouvoir être remis dans l'ordre du texte.

Pourquoi du SVG écrit à la main plutôt qu'un outil de génération d'image. Trois
raisons, dans l'ordre d'importance :

  1. **Aucun outil de génération d'image n'est disponible ici.** La connexion au
     service de génération ne délivre aucun identifiant, et l'outil lui-même
     n'existe pas dans cette configuration.
  2. **La licence.** L'application vise la catégorie enfant sur les stores, dans un
     dépôt public. Un jeu d'images produit par un outil dont les conditions
     d'utilisation ne sont pas claires est un passif, pas un actif. Ici les images
     sont du code : elles appartiennent au projet, sans question à trancher.
  3. **Le contrôle.** Le brief impose une règle — « une image ne doit convenir à
     aucun autre mot ». Une image écrite comme du code est vérifiable par un
     script : palette fermée, pas de texte, cadrage constant, trait constant. Une
     image produite par un modèle ne l'est pas.

Ce que ces images sont, et ne sont pas. Ce sont des **icônes fonctionnelles**,
dessinées pour être reconnues sans hésitation à 112 points sur un écran de
téléphone, dans un style plat à contour constant. Ce ne sont pas des
illustrations d'auteur : elles ne cherchent ni le charme ni la matière. Le brief
ne demande pas la beauté, il demande l'absence d'ambiguïté — et c'est ce qui est
tenu ici. Une relecture par un illustrateur reste souhaitable avant publication ;
elle n'est pas nécessaire pour valider la mécanique.

Usage :
    python generer-images.py            # les 44 SVG de la GS et leur planche
    python generer-images.py --ce1      # les 3 images du CE1, dans contenu/images-ce1/
    python generer-images.py --recit    # les 8 scènes de récit, dans contenu/images-recit-ce1/
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

ICI = Path(__file__).resolve().parent
SORTIE = ICI.parent / "contenu" / "images"
SORTIE_CE1 = ICI.parent / "contenu" / "images-ce1"
SORTIE_RECIT = ICI.parent / "contenu" / "images-recit-ce1"

# --- La palette fermée --------------------------------------------------------
# Toute couleur employée doit venir d'ici : le contrôle refuse une couleur hors
# palette. C'est ce qui tient la série ensemble, et c'est aussi ce qui la rend
# lisible par un enfant daltonien — les teintes sont choisies pour se distinguer
# en niveaux de gris autant qu'en couleur.

ENCRE = "#2E2A26"
PEAU = "#F0C9A6"
PEAU_F = "#D8A87F"
ROUGE = "#D9503F"
ROUGE_F = "#A93B2E"
VERT = "#5FA463"
VERT_F = "#33703C"
JAUNE = "#F2C24C"
JAUNE_F = "#D9A32E"
ORANGE = "#E58B3C"
BRUN = "#8B5E3C"
BRUN_C = "#C08552"
BLEU = "#4C81BE"
BLEU_C = "#A9CCE8"
GRIS = "#C3BDB6"
GRIS_F = "#7E7770"
BLANC = "#FFFFFF"
ROSE = "#E9A6AE"
VIOLET = "#8E7CC3"

PALETTE = [
    ENCRE, PEAU, PEAU_F, ROUGE, ROUGE_F, VERT, VERT_F, JAUNE, JAUNE_F, ORANGE,
    BRUN, BRUN_C, BLEU, BLEU_C, GRIS, GRIS_F, BLANC, ROSE, VIOLET,
]

COTE = 512
EPAISSEUR = 4


# --- Les primitives -----------------------------------------------------------

def c(cx, cy, rayon, f):
    return f'<circle cx="{cx}" cy="{cy}" r="{rayon}" fill="{f}"/>'


def e(cx, cy, rx, ry, f, rot=0):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{f}"{t}/>'


def r(x, y, largeur, hauteur, rayon, f):
    return (
        f'<rect x="{x}" y="{y}" width="{largeur}" height="{hauteur}" '
        f'rx="{rayon}" fill="{f}"/>'
    )


def p(d, f):
    return f'<path d="{d}" fill="{f}"/>'


def trait(d, largeur=None):
    lw = f' stroke-width="{largeur}"' if largeur else ""
    return f'<path d="{d}" fill="none"{lw}/>'


def place(dessin, cx, cy, echelle, miroir=False):
    """Une figure RÉEMPLOYÉE dans une scène, posée par son centre.

    Une scène de récit n'a pas de figures à elle : elle emploie celles de la
    série — le même papa, le même éléphant, le même chat que l'enfant a déjà
    rencontrés. Les redessiner donnerait deux éléphants, et c'est ainsi qu'une
    application se met à parler deux langues.

    `miroir` retourne la figure. Toutes celles de la série regardent à droite —
    c'est le sens de lecture — et un éléphant qui a rejoint la maison doit
    regarder la maison, sinon le dessin dit qu'il s'en va.

    Le trait est COMPENSÉ, et il faut dire pourquoi. Réduire une figure de
    moitié réduit aussi son contour : la scène porterait alors un trait de 2 px
    au milieu de figures à 4 px, et cesserait d'être du même dessin. La parade
    habituelle serait `vector-effect="non-scaling-stroke"` ; **le moteur de
    rendu l'ignore**, et cela a été MESURÉ plutôt que supposé : à l'échelle
    0,25, le contour rendu fait 1 px, que l'attribut soit posé sur le groupe qui
    porte le trait, sur la forme, ou nulle part — trois variantes, un seul
    résultat. La compensation est donc écrite à la main, et c'est mieux ainsi :
    le facteur est DANS le fichier, donc le contrôle peut le relire. Il refuse
    un couple (échelle, épaisseur) qui ne redonne pas 4 px.

    Les largeurs explicites — les détails d'une figure, comme les moustaches du
    chat — ne sont pas compensées : elles font partie de la figure et suivent
    son échelle, ce qui est leur rôle.
    """
    dx = cx + 256 * echelle if miroir else cx - 256 * echelle
    dy = cy - 256 * echelle
    sx = f"-{echelle:.4f}" if miroir else f"{echelle:.4f}"
    return (
        f'<g transform="translate({dx:.3f} {dy:.3f}) scale({sx} {echelle:.4f})" '
        f'stroke-width="{EPAISSEUR / echelle:.6f}">{dessin()}</g>'
    )


def sol(y=424):
    """La ligne de sol. Elle ne distingue rien : elle est dans toutes les scènes
    sauf une, celle qui est une photo — et c'est justement ce qui la distingue."""
    return trait(f"M40 {y} h432", 6)


# --- Les quarante-quatre dessins ----------------------------------------------
# Une fonction par mot, dans l'ordre de la banque GS. Le sujet tient dans 80 % du
# cadre, de 51 à 461, contour compris.

def papa():
    return (
        r(214, 372, 34, 82, 15, BLEU) + r(264, 372, 34, 82, 15, BLEU)
        + trait("M256 300 v80")
        + r(198, 236, 116, 152, 34, VERT)
        + trait("M206 262 l-38 96") + trait("M306 262 l38 96")
        + c(256, 172, 62, PEAU)
        + p("M194 168 a62 62 0 0 1 124 0 q-20 -22 -62 -22 q-42 0 -62 22 z", BRUN)
        + p("M212 196 q44 74 88 0 q-6 62 -44 62 q-38 0 -44 -62 z", BRUN)
        + c(234, 172, 6, ENCRE) + c(278, 172, 6, ENCRE)
    )


def maman():
    return (
        r(214, 372, 34, 82, 15, VIOLET) + r(264, 372, 34, 82, 15, VIOLET)
        + trait("M256 300 v80")
        + r(198, 236, 116, 152, 34, ROSE)
        + trait("M206 262 l-38 96") + trait("M306 262 l38 96")
        + c(256, 172, 62, PEAU)
        + c(256, 104, 30, BRUN)
        + p("M194 172 a62 62 0 0 1 124 0 l0 44 q-14 -54 -62 -54 q-48 0 -62 54 z", BRUN)
        + c(234, 178, 6, ENCRE) + c(278, 178, 6, ENCRE)
    )


def bebe():
    return (
        c(256, 168, 72, PEAU)
        + p("M184 148 a72 72 0 0 1 144 0 q-22 -26 -72 -26 q-50 0 -72 26 z", BRUN_C)
        + c(232, 172, 6, ENCRE) + c(280, 172, 6, ENCRE)
        + trait("M240 204 q16 16 32 0")
        + p("M168 268 q88 -40 176 0 q10 118 -88 118 q-98 0 -88 -118 z", JAUNE)
        + e(196, 386, 30, 24, PEAU) + e(316, 386, 30, 24, PEAU)
    )


def dodo():
    return (
        r(96, 236, 320, 34, 10, BRUN_C)
        + r(112, 270, 22, 118, 8, BRUN)
        + r(378, 270, 22, 118, 8, BRUN)
        + r(118, 206, 276, 34, 12, BLANC)
        + e(176, 200, 52, 32, BLANC)
        + c(206, 176, 46, PEAU)
        + p("M180 166 a46 46 0 0 1 52 0 q-26 -18 -52 0 z", BRUN)
        + trait("M190 180 q10 10 20 0") + trait("M216 180 q10 10 20 0")
        + p("M232 208 q142 -30 154 46 q-6 44 -154 44 z", BLEU)
        + trait("M232 212 q140 -26 152 44", EPAISSEUR)
    )


def lit():
    return (
        r(96, 236, 320, 34, 10, BRUN_C)
        + r(112, 270, 22, 118, 8, BRUN)
        + r(378, 270, 22, 118, 8, BRUN)
        + r(118, 206, 276, 34, 12, BLANC)
        + e(178, 198, 54, 32, BLANC)
        + trait("M128 240 h256", EPAISSEUR)
    )


def velo():
    return (
        c(148, 352, 76, BLANC) + c(364, 352, 76, BLANC)
        + trait("M148 276 v152") + trait("M72 352 h152")
        + trait("M364 276 v152") + trait("M288 352 h152")
        + trait("M148 352 l96 -84 h84") + trait("M244 268 l-32 84")
        + r(214, 250, 40, 14, 6, ENCRE)
        + trait("M328 268 l24 -42 h40")
        + c(148, 352, 12, ENCRE) + c(364, 352, 12, ENCRE)
        + c(268, 344, 20, ENCRE)
        + trait("M248 344 h40", EPAISSEUR)
    )


def moto():
    return (
        c(140, 356, 70, BLANC) + c(372, 356, 70, BLANC)
        + c(140, 356, 14, ENCRE) + c(372, 356, 14, ENCRE)
        + trait("M140 286 v140") + trait("M372 286 v140")
        + p("M150 262 q106 -46 212 0 q22 42 0 74 h-212 q-22 -32 0 -74 z", ROUGE)
        + r(190, 276, 130, 74, 14, GRIS_F)
        + trait("M206 292 v42") + trait("M240 292 v42") + trait("M274 292 v42")
        + r(160, 218, 92, 34, 14, ENCRE)
        + trait("M330 250 l40 -52 h44")
        + trait("M140 356 l52 -94")
    )


def cafe():
    return (
        e(256, 386, 172, 44, BLANC)
        + p("M152 176 h208 l-22 152 q-4 30 -82 30 q-78 0 -82 -30 z", BLANC)
        + e(256, 176, 104, 26, BRUN)
        + p("M360 214 q64 0 64 52 q0 52 -64 52", BLANC)
        + trait("M360 214 q64 0 64 52 q0 52 -64 52")
    )


def gateau():
    return (
        r(126, 292, 260, 130, 16, BRUN_C)
        + e(256, 292, 130, 34, ROSE)
        + r(126, 300, 260, 24, 0, ROSE)
        + trait("M126 326 h260")
        + r(186, 196, 20, 96, 8, BLEU)
        + r(246, 196, 20, 96, 8, VERT)
        + r(306, 196, 20, 96, 8, JAUNE)
        + p("M196 196 q0 -34 12 -34 q12 0 12 34 z", ORANGE)
        + p("M256 196 q0 -34 12 -34 q12 0 12 34 z", ORANGE)
        + p("M316 196 q0 -34 12 -34 q12 0 12 34 z", ORANGE)
    )


def lune():
    return (
        c(256, 256, 138, JAUNE)
        + c(214, 208, 34, JAUNE_F) + c(304, 232, 24, JAUNE_F)
        + c(238, 322, 40, JAUNE_F) + c(320, 318, 20, JAUNE_F)
        + p("M92 96 l14 34 34 14 -34 14 -14 34 -14 -34 -34 -14 34 -14 z", JAUNE_F)
        + p("M420 132 l10 26 26 10 -26 10 -10 26 -10 -26 -26 -10 26 -10 z", JAUNE_F)
        + p("M400 388 l10 26 26 10 -26 10 -10 26 -10 -26 -26 -10 26 -10 z", JAUNE_F)
    )


def jupe():
    return (
        r(150, 150, 212, 34, 10, BLEU)
        + p("M150 184 h212 l58 216 q-164 44 -328 0 z", BLEU_C)
        + trait("M196 200 l-14 190")
        + trait("M256 200 v196")
        + trait("M316 200 l14 190")
    )


def pomme():
    return (
        p("M256 152 q-52 -46 -104 -12 q-58 38 -46 122 q14 100 74 138 q44 26 76 4 "
          "q32 22 76 -4 q60 -38 74 -138 q12 -84 -46 -122 q-52 -34 -104 12 z", ROUGE)
        + trait("M256 156 q0 -56 26 -72", 10)
        + e(320, 122, 52, 26, VERT, -28)
        + trait("M318 122 q-30 8 -46 -6", EPAISSEUR)
    )


def tomate():
    return (
        c(256, 288, 150, ROUGE)
        + p("M256 138 l30 42 50 -22 -16 52 50 20 -50 22 16 52 -50 -22 -30 42 "
            "-30 -42 -50 22 16 -52 -50 -22 50 -20 -16 -52 50 22 z", VERT)
        + c(256, 176, 30, VERT)
        + trait("M256 150 v-40", 12)
    )


def cerise():
    return (
        c(190, 356, 74, ROUGE) + c(322, 356, 74, ROUGE)
        + trait("M190 282 q6 -110 76 -158", 10)
        + trait("M322 282 q-6 -96 -56 -158", 10)
        + e(300, 138, 66, 28, VERT, -24)
        + c(164, 330, 16, BLANC) + c(296, 330, 16, BLANC)
    )


def zebre():
    return (
        e(256, 286, 148, 92, BLANC)
        + r(160, 350, 30, 96, 12, BLANC) + r(230, 350, 30, 96, 12, BLANC)
        + r(300, 350, 30, 96, 12, BLANC) + r(354, 350, 30, 96, 12, BLANC)
        + p("M382 258 q46 -22 62 -70 l34 12 q-10 78 -56 96 z", BLANC)
        + p("M448 200 l10 -46 30 8 -8 46 z", BLANC)
        + e(436, 152, 20, 12, BLANC, -20)
        + p("M124 244 q-30 -10 -44 -50 l24 -14 q24 30 44 34 z", ENCRE)
        + trait("M188 202 l-14 168", 10) + trait("M238 194 l-10 172", 10)
        + trait("M288 194 l10 172", 10) + trait("M338 202 l14 168", 10)
        + trait("M406 214 l24 56", 10) + trait("M418 168 l22 34", 10)
        + c(442, 148, 7, ENCRE)
    )


def cheval():
    return (
        e(256, 286, 148, 92, BRUN_C)
        + r(160, 350, 30, 96, 12, BRUN_C) + r(230, 350, 30, 96, 12, BRUN_C)
        + r(300, 350, 30, 96, 12, BRUN_C) + r(354, 350, 30, 96, 12, BRUN_C)
        + p("M382 258 q46 -22 62 -70 l34 12 q-10 78 -56 96 z", BRUN_C)
        + p("M448 200 l10 -46 30 8 -8 46 z", BRUN_C)
        + e(436, 152, 20, 12, BRUN_C, -20)
        # La crinière. Deux versions ont échoué ici. La première la posait à
        # l'extrémité gauche du corps — à la place de la queue — et l'animal se
        # lisait de travers. La seconde la dessinait en mèches perpendiculaires à
        # l'encolure : vues à la taille de l'application, ces mèches se lisent
        # comme des RAYURES, c'est-à-dire comme le trait distinctif du zèbre — qui
        # est dans la même banque. La crinière est donc une crête pleine et
        # touffue qui DÉBORDE de l'encolure. Une crête qui déborde se lit comme
        # un poil ; une bande posée sur le contour se lit comme une rayure.
        + p("M382 258 L360 238 Q352 220 374 208 Q364 188 388 176 "
            "Q380 156 406 148 L444 188 Z", BRUN)
        # La queue, à gauche, en une mèche unique et touffue.
        + p("M136 232 q-54 -6 -68 -66 q46 8 72 32 q12 18 -4 34 z", BRUN)
        + c(442, 148, 7, ENCRE)
    )


def lapin():
    return (
        e(272, 328, 122, 92, GRIS)
        + e(186, 158, 30, 88, GRIS, -14) + e(238, 154, 30, 88, GRIS, 6)
        + e(186, 158, 16, 62, ROSE, -14) + e(238, 154, 16, 62, ROSE, 6)
        + c(160, 296, 82, GRIS)
        + c(130, 282, 8, ENCRE) + c(182, 282, 8, ENCRE)
        + p("M152 318 l-8 16 16 0 z", ROSE)
        + c(396, 344, 26, BLANC)
        + r(196, 400, 26, 52, 10, GRIS) + r(320, 400, 26, 52, 10, GRIS)
    )


def canard():
    return (
        e(272, 300, 128, 84, JAUNE)
        + c(392, 210, 62, JAUNE)
        + p("M446 202 q42 8 42 24 q0 16 -42 24 z", ORANGE)
        + c(404, 192, 8, ENCRE)
        + p("M320 250 q46 -34 78 -8 q-30 -8 -78 8 z", JAUNE_F)
        + p("M150 292 q-46 12 -50 44 q40 -18 78 -12 z", JAUNE_F)
        + r(232, 372, 24, 44, 10, ORANGE) + r(316, 372, 24, 44, 10, ORANGE)
        + trait("M64 428 q64 -22 128 0 q64 22 128 0 q64 -22 128 0", 6)
    )


def mouton():
    return (
        # La toison est une grappe de cercles qui se chevauchent. Un seul ovale
        # blanc se lisait comme un nuage, pas comme un mouton : c'est le nombre de
        # bosses qui fait la toison.
        c(196, 268, 60, BLANC) + c(256, 236, 72, BLANC) + c(316, 268, 60, BLANC)
        + c(206, 306, 54, BLANC) + c(306, 306, 54, BLANC) + c(256, 300, 62, BLANC)
        + c(232, 214, 42, BLANC) + c(288, 214, 42, BLANC)
        + c(170, 300, 40, BLANC) + c(342, 300, 40, BLANC)
        # La tête sort à droite, plus sombre, avec son oreille.
        + e(392, 278, 58, 54, GRIS_F)
        + e(432, 240, 26, 17, GRIS_F, -30)
        + e(410, 300, 34, 22, GRIS)
        + c(378, 264, 9, ENCRE) + c(378, 264, 3, BLANC)
        # Quatre pattes, sombres et bien séparées.
        + r(184, 344, 26, 90, 10, GRIS_F) + r(238, 344, 26, 90, 10, GRIS_F)
        + r(300, 344, 26, 90, 10, GRIS_F) + r(352, 344, 26, 90, 10, GRIS_F)
    )


def koala():
    return (
        r(88, 356, 336, 30, 14, BRUN)
        + e(262, 300, 96, 88, GRIS)
        + c(196, 190, 62, GRIS) + c(330, 190, 62, GRIS)
        + c(196, 190, 34, GRIS_F) + c(330, 190, 34, GRIS_F)
        + c(262, 200, 88, GRIS)
        + e(262, 230, 34, 26, GRIS_F)
        + c(232, 178, 9, ENCRE) + c(292, 178, 9, ENCRE)
        + r(196, 356, 26, 46, 10, GRIS_F) + r(304, 356, 26, 46, 10, GRIS_F)
    )


def girafe():
    return (
        e(238, 320, 122, 84, JAUNE)
        + p("M322 300 l46 -180 h62 l-24 186 z", JAUNE)
        + e(396, 116, 56, 46, JAUNE)
        + e(360, 88, 14, 22, JAUNE, -24) + e(410, 84, 14, 22, JAUNE, 10)
        + c(420, 108, 8, ENCRE)
        + e(350, 116, 10, 8, ORANGE) + e(390, 146, 10, 8, ORANGE)
        + e(262, 300, 16, 12, ORANGE) + e(200, 336, 16, 12, ORANGE)
        + e(300, 340, 16, 12, ORANGE)
        + r(178, 386, 26, 60, 10, JAUNE_F) + r(232, 386, 26, 60, 10, JAUNE_F)
        + r(292, 386, 26, 60, 10, JAUNE_F)
        + p("M150 296 q-40 -8 -46 -46 q34 12 52 24 z", JAUNE_F)
    )


def elephant():
    return (
        e(272, 288, 128, 96, GRIS_F)
        + c(384, 236, 78, GRIS_F)
        + e(438, 216, 62, 76, GRIS)
        + p("M384 292 q-10 96 42 116 q34 12 40 -22 q-30 -4 -34 -34 q-4 -32 -10 -60 z", GRIS)
        + c(412, 212, 9, ENCRE)
        + r(198, 362, 30, 74, 12, GRIS_F) + r(264, 362, 30, 74, 12, GRIS_F)
        + r(330, 362, 30, 74, 12, GRIS_F)
        + p("M148 254 q-34 -10 -44 -46 q34 8 54 24 z", GRIS)
        + trait("M414 396 q10 22 -6 30", 8)
    )


def crocodile():
    return (
        p("M96 300 q40 -46 128 -46 h150 q54 0 78 26 q24 -18 34 4 q-30 12 -34 30 "
          "q-24 26 -78 26 h-150 q-88 0 -128 -40 z", VERT)
        + p("M150 262 q34 -22 66 -18 l-8 20 q-30 -2 -58 12 z", VERT_F)
        + p("M214 244 q30 -18 62 -14 l-6 18 q-28 -2 -56 10 z", VERT_F)
        + p("M278 230 q30 -16 62 -12 l-6 18 q-28 -2 -56 8 z", VERT_F)
        + p("M342 216 q32 -14 62 -8 l-6 18 q-28 -4 -56 4 z", VERT_F)
        + c(160, 288, 9, ENCRE)
        + p("M118 322 q-30 30 -6 62 q14 -34 30 -46 z", VERT)
        + p("M170 342 q-10 40 10 52 q6 -34 16 -46 z", VERT)
        + p("M300 342 q-10 40 10 52 q6 -34 16 -46 z", VERT)
        + trait("M120 302 q10 10 20 0 q10 -10 20 0 q10 10 20 0 q10 -10 20 0 "
                "q10 10 20 0 q10 -10 20 0 q10 10 20 0 q10 -10 20 0", 5)
    )


def loup():
    return (
        e(246, 300, 136, 92, GRIS_F)
        + r(160, 362, 28, 78, 12, GRIS_F) + r(232, 362, 28, 78, 12, GRIS_F)
        + r(302, 362, 28, 78, 12, GRIS_F)
        + c(374, 226, 66, GRIS_F)
        + p("M318 200 l-22 -50 46 18 z", GRIS_F)
        + p("M416 200 l22 -50 -46 18 z", GRIS_F)
        + p("M374 240 q46 4 52 30 q-24 24 -52 24 z", GRIS_F)
        + c(400, 268, 9, ENCRE) + c(352, 214, 9, ENCRE)
        + p("M120 268 q-42 -22 -54 -74 q34 10 52 34 q22 -22 60 -24 q-34 30 -58 64 z", GRIS_F)
        + p("M356 262 l10 14 10 -14 z", ENCRE)
    )


def chat():
    return (
        e(268, 330, 118, 84, GRIS)
        + p("M392 306 q54 -22 62 -80 q26 44 4 84 q-24 34 -60 30 z", GRIS)
        + c(184, 268, 84, GRIS)
        + p("M118 210 l-6 -66 54 30 z", GRIS)
        + p("M250 210 l6 -66 -54 30 z", GRIS)
        + c(158, 254, 9, ENCRE) + c(212, 254, 9, ENCRE)
        + p("M184 288 l-8 14 16 0 z", ROSE)
        + trait("M126 280 h-58", 5) + trait("M130 296 l-56 20", 5)
        + trait("M242 280 h58", 5) + trait("M238 296 l56 20", 5)
        + r(212, 400, 26, 54, 10, GRIS) + r(300, 400, 26, 54, 10, GRIS)
    )


def rat():
    return (
        e(226, 320, 116, 82, GRIS_F)
        + c(150, 274, 62, GRIS_F)
        + p("M100 286 q-38 6 -48 22 q22 12 48 4 z", GRIS_F)
        + c(92, 316, 9, ENCRE)
        + e(152, 218, 32, 30, GRIS_F) + e(152, 218, 18, 17, ROSE)
        + trait("M110 304 l-34 10", 4)
        + trait("M334 300 q96 10 116 74 q-44 -6 -62 -34", 10)
        + r(180, 384, 24, 62, 10, PEAU_F) + r(258, 384, 24, 62, 10, PEAU_F)
        + c(138, 268, 8, ENCRE)
    )


def maison():
    return (
        r(126, 264, 260, 168, 10, BRUN_C)
        + p("M256 152 l172 116 h-344 z", ROUGE_F)
        + r(322, 116, 44, 78, 6, BRUN)
        + r(206, 322, 88, 110, 8, BRUN)
        + c(276, 376, 8, JAUNE)
        + r(154, 300, 52, 52, 6, BLEU_C)
        + trait("M180 300 v52") + trait("M154 326 h52")
        + r(310, 300, 52, 52, 6, BLEU_C)
        + trait("M336 300 v52") + trait("M310 326 h52")
    )


def ecole():
    return (
        r(76, 218, 360, 190, 8, BRUN_C)
        + p("M60 218 l196 -86 196 86 z", ROUGE_F)
        + r(88, 244, 60, 58, 6, BLEU_C) + r(176, 244, 60, 58, 6, BLEU_C)
        + r(276, 244, 60, 58, 6, BLEU_C) + r(364, 244, 60, 58, 6, BLEU_C)
        + r(88, 322, 60, 58, 6, BLEU_C) + r(364, 322, 60, 58, 6, BLEU_C)
        + r(212, 322, 88, 86, 8, BRUN)
        + c(256, 168, 32, BLANC) + c(256, 168, 26, JAUNE)
        + trait("M256 150 v18") + trait("M256 186 v8")
        + r(212, 108, 88, 26, 6, ROUGE)
        + trait("M40 424 h432", 8)
    )


def valise():
    return (
        r(112, 236, 288, 196, 16, BRUN)
        + r(140, 262, 232, 144, 8, BRUN_C)
        + trait("M216 236 q0 -54 40 -54 q40 0 40 54", 12)
        + r(150, 300, 40, 30, 6, GRIS_F) + r(322, 300, 40, 30, 6, GRIS_F)
        + trait("M256 262 v144")
    )


def cartable():
    # Le point difficile, et il a été manqué une première fois : ne PAS ressembler
    # à `valise`. Ce qui les sépare est écrit dans le brief — le rabat, les deux
    # bretelles, et les cahiers qui dépassent. Une boîte brune à poignée ne dit ni
    # l'un ni l'autre : elle dit « valise », et deux images diraient le même mot.
    return (
        # Les cahiers qui dépassent, derrière le rabat.
        r(292, 138, 68, 84, 6, BLANC)
        + r(310, 122, 56, 84, 6, BLEU_C)
        # Les deux bretelles, en boucles derrière le corps.
        + trait("M168 236 q0 -86 46 -86 q46 0 46 86", 14)
        + trait("M252 236 q0 -86 46 -86 q46 0 46 86", 14)
        # Le corps, plus haut que large — un cartable se porte debout.
        + r(116, 200, 280, 224, 26, BRUN)
        # Le rabat, qui couvre le tiers supérieur et descend en arrondi.
        + p("M116 236 q140 96 280 0 v-36 h-280 z", BRUN_C)
        + trait("M116 234 q140 98 280 0", EPAISSEUR)
        # La boucle du rabat.
        + r(238, 302, 36, 32, 6, JAUNE)
    )


def sac():
    return (
        p("M118 250 h276 l30 174 q-168 26 -336 0 z", VERT)
        + e(256, 250, 138, 34, VERT_F)
        + trait("M172 246 q0 -110 84 -110 q84 0 84 110", 14)
        + trait("M130 300 h252", 6)
    )


def telephone():
    return (
        r(152, 76, 208, 360, 30, ENCRE)
        + r(172, 108, 168, 268, 12, GRIS_F)
        + c(256, 410, 16, GRIS)
        + r(224, 88, 64, 10, 5, GRIS_F)
    )


def parapluie():
    return (
        p("M64 258 q0 -170 192 -170 q192 0 192 170 q-48 -34 -96 0 q-48 -34 -96 0 "
          "q-48 -34 -96 0 q-48 -34 -96 0 z", BLEU)
        # Les nervures vont du sommet aux creux du bord. Tracées vers l'extérieur,
        # elles sortaient du cadre — une nervure qui dépasse se voit tout de suite.
        + trait("M256 96 l-96 162", 3)
        + trait("M256 96 l96 162", 3)
        + trait("M256 92 v166")
        + trait("M256 258 v156 q0 44 -44 44 q-34 0 -38 -30", 8)
        + c(256, 88, 12, GRIS_F)
    )


def avion():
    return (
        p("M96 268 q0 -40 60 -48 l200 -22 q56 -6 84 18 q22 20 22 40 "
          "q0 20 -22 40 q-28 24 -84 18 l-200 -22 q-60 -8 -60 -24 z", BLANC)
        + p("M232 250 l-96 -108 h58 l124 100 z", BLEU_C)
        + p("M232 316 l-96 108 h58 l124 -100 z", BLEU_C)
        + p("M420 236 l50 -74 h34 l-14 74 z", BLEU)
        + c(150, 268, 12, BLEU_C) + c(196, 268, 12, BLEU_C)
        + c(242, 268, 12, BLEU_C) + c(288, 268, 12, BLEU_C)
    )


def bateau():
    return (
        p("M118 330 h276 l-34 96 q-104 20 -208 0 z", BRUN)
        + trait("M256 330 v-186", 10)
        + p("M266 148 l132 168 h-132 z", BLANC)
        + p("M246 168 l-96 148 h96 z", BLEU_C)
        + trait("M64 452 q64 -22 128 0 q64 22 128 0 q64 -22 128 0", 6)
    )


def soleil():
    return (
        c(256, 256, 110, JAUNE)
        # Les rayons partent du BORD du disque, pas du centre : tracés depuis le
        # centre, ils barrent le disque et l'ensemble se lit comme une roue.
        + "".join(
            trait(
                f"M{256 + round(136 * dx)} {256 + round(136 * dy)} "
                f"l{round(64 * dx)} {round(64 * dy)}",
                14,
            )
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1),
                           (0.71, 0.71), (-0.71, 0.71), (0.71, -0.71), (-0.71, -0.71))
        )
        + c(226, 226, 16, JAUNE_F) + c(288, 250, 12, JAUNE_F)
    )


def fleur():
    return (
        trait("M256 300 v160", 10)
        + e(190, 366, 58, 26, VERT, -28) + e(322, 366, 58, 26, VERT, 28)
        + "".join(
            e(256 + round(104 * dx), 246 + round(104 * dy), 58, 58, ROSE)
            for dx, dy in ((0, -1), (0.95, -0.31), (0.59, 0.81), (-0.59, 0.81), (-0.95, -0.31))
        )
        + c(256, 246, 46, JAUNE)
    )


def banane():
    return (
        p("M96 156 q6 190 160 226 q116 28 168 -40 q-96 12 -168 -46 "
          "q-58 -46 -58 -140 q-58 0 -102 0 z", JAUNE)
        + p("M96 156 q44 0 102 0 l-2 -34 h-92 z", BRUN)
        + trait("M110 190 q10 150 148 186", 5)
    )


def ananas():
    # La texture est un treillis de diagonales, DÉCOUPÉ à l'ellipse du corps. Sans
    # le découpage, les lignes dépassent de l'ananas et partent dans le vide —
    # c'est le défaut le plus visible de la première version.
    treillis = "".join(trait(f"M{40 + i * 56} 120 l344 344", 3) for i in range(0, 9))
    treillis += "".join(trait(f"M{40 + i * 56} 464 l344 -344", 3) for i in range(0, 9))
    return (
        '<defs><clipPath id="corps"><ellipse cx="256" cy="296" rx="122" ry="156"/></clipPath></defs>'
        + e(256, 296, 122, 156, ORANGE)
        + f'<g clip-path="url(#corps)">{treillis}</g>'
        + p("M256 142 q-32 -62 -80 -78 q24 48 32 78 z", VERT_F)
        + p("M256 142 q0 -68 -24 -100 q-16 54 -8 100 z", VERT)
        + p("M256 142 q32 -62 80 -78 q-24 48 -32 78 z", VERT_F)
        + p("M256 142 q-14 -62 0 -96 q14 34 0 96 z", VERT)
    )


def bonbon():
    return (
        e(256, 256, 96, 84, ROSE)
        + p("M160 256 l-84 -66 v132 z", ROSE)
        + p("M352 256 l84 -66 v132 z", ROSE)
        + trait("M156 190 q100 -22 200 0", 5)
        + trait("M156 322 q100 22 200 0", 5)
    )


def chocolat():
    return (
        r(112, 140, 288, 232, 10, BRUN)
        + "".join(trait(f"M184 {140 + i * 58} h216") for i in range(1, 4))
        + "".join(trait(f"M{184 + i * 72} 140 v232") for i in range(1, 3))
        + r(400, 330, 72, 58, 8, BRUN_C)
        + trait("M400 330 h72") + trait("M400 388 h72")
        + trait("M400 330 v58") + trait("M472 330 v58")
    )


def pyjama():
    return (
        r(150, 118, 212, 156, 20, BLEU)
        + r(96, 132, 60, 100, 20, BLEU) + r(356, 132, 60, 100, 20, BLEU)
        + p("M226 118 q30 40 60 0 z", BLANC)
        + trait("M256 130 v140")
        + r(176, 296, 74, 116, 16, BLEU_C) + r(262, 296, 74, 116, 16, BLEU_C)
        + trait("M176 340 h74") + trait("M262 340 h74")
    )


def nez():
    # Trois passes, et la leçon vaut pour toute la série.
    #
    # Première version : de face, forme lisse et effilée, arrondie au bout. Elle
    # se lisait comme un doigt — c'est-à-dire comme un autre mot, ce qui viole la
    # règle qui prime sur toutes les autres.
    #
    # Deuxième version : de profil, en croyant que la vue sauverait la forme.
    # Faux. Le profil a produit une corne, puis une voile. Le raisonnement était
    # mauvais : ce n'est pas la VUE qui fait nommer un objet, ce sont ses traits
    # distinctifs. Un nez se nomme par sa base large, ses deux narines et ses
    # ailes ; tant que ces trois traits manquent, aucune vue ne le sauve.
    #
    # Troisième version : de face, base large, deux narines, columelle, ailes en
    # lobes. C'est celle-ci. La règle a été ajoutée au cadrage du brief.
    return (
        p("M236 132 C232 180 212 226 198 270 C186 304 170 328 158 350 "
          "C146 372 148 396 172 402 C192 406 210 398 222 388 "
          "Q256 370 290 388 C302 398 320 406 340 402 "
          "C364 396 366 372 354 350 C342 328 326 304 314 270 "
          "C300 226 280 180 276 132 Q256 118 236 132 Z", PEAU)
        + e(214, 370, 23, 13, ENCRE, -12)
        + e(298, 370, 23, 13, ENCRE, 12)
        + trait("M256 398 v-16", 6)
    )


def main_dessin():
    return (
        p("M150 430 L150 196 Q150 164 178 164 Q206 164 206 196 L206 236 "
          "L206 156 Q206 124 234 124 Q262 124 262 156 L262 236 "
          "L262 176 Q262 144 290 144 Q318 144 318 176 L318 236 "
          "L318 196 Q318 164 346 164 Q374 164 374 196 L374 340 "
          "Q374 432 262 432 Q150 432 150 430 Z", PEAU)
        + p("M150 306 q-56 -6 -68 -48 q-8 -32 18 -42 q24 -8 36 20 l14 28 z", PEAU)
        + trait("M178 208 v-14") + trait("M234 168 v-14")
        + trait("M290 188 v-14") + trait("M346 208 v-14")
        + trait("M186 372 q70 18 140 0", 6)
    )


# --- Les trois dessins du CE1 -------------------------------------------------
# Le corpus du CE1 est court, et c'est une propriété du lexique, pas un choix :
# les deux nasales rares et les mots irréguliers sont les endroits du français où
# le nom concret se raréfie. Sur vingt-huit mots examinés pour les trois besoins
# B04, B13 et B30, trois sont illustrables. Les autres sont déclarés, avec leur
# raison, dans outils/images-ce1.json — et le contrôle refuse un mot déclaré sans
# raison. Mêmes primitives, même palette, même cadre : la série ne doit pas se
# voir en deux morceaux.

def foin():
    """Une meule de foin : un tas en dôme de brins dorés, plus large que haut.

    La première version était une botte — un bloc arrondi serré par une corde — et
    elle se lisait comme une CAISSE : le contour régulier disait le contenant, pas
    le contenu, et la corde disait la sangle. Ce qui fait nommer le foin, c'est la
    forme du tas : une base nette et un sommet irrégulier, dont quelques brins
    dépassent. C'est ce qui distingue le foin COUPÉ et RASSEMBLÉ de l'herbe, qui
    est un tapis et n'a pas de forme.
    """
    return (
        p("M112 400 Q120 302 168 258 Q196 232 226 224 "
          "Q238 190 262 196 Q282 176 300 200 "
          "Q330 206 340 236 Q382 274 400 400 Z", JAUNE)
        # Les brins qui dépassent du sommet : c'est ce qui fait que le tas est en
        # foin et non en neige, ni en sable.
        + trait("M226 224 l-18 -30", 5)
        + trait("M262 196 l-2 -32", 5)
        + trait("M300 200 l18 -28", 5)
        + trait("M196 240 l-24 -20", 5)
        + trait("M334 220 l20 -22", 5)
        + trait("M152 272 l-22 -14", 5)
        # Les brins du tas, courts et serrés, jamais jusqu'au bord.
        + "".join(trait(f"M{140 + i * 32} 392 v-44", 4) for i in range(0, 9))
        + trait("M118 390 l-26 -14", 5)
        + trait("M394 390 l26 -14", 5)
        + trait("M112 400 h288", 6)
    )


def parfum():
    """Un flacon de parfum, poire à vaporiser comprise.

    La poire est le trait distinctif, et c'est écrit dans le brief : sans elle,
    un flacon se nomme « une bouteille ». La première version la dessinait comme
    une bille au bout d'un fil, et l'ensemble se lisait comme un ballon — le
    collier qui joint le tube au bulbe est ce qui rattache la poire au flacon.
    """
    return (
        # Le flacon : panse trapue, épaule marquée, col court.
        r(136, 222, 164, 168, 16, BLEU_C)
        + r(228, 186, 56, 26, 4, BLEU_C)
        # Le bouchon doré, et l'embout qui le surmonte.
        + r(218, 148, 76, 40, 8, JAUNE_F)
        + trait("M256 148 v-16", 8)
        # La poire à vaporiser : le tube, le collier, puis le bulbe.
        + trait("M294 164 q56 -8 62 74", 8)
        + r(348, 232, 16, 14, 4, ROSE)
        + p("M356 240 q30 2 36 42 q6 46 -36 46 q-42 0 -36 -46 q6 -40 36 -42 z", ROSE)
    )


def oeil():
    """Un œil vu de face, en gros plan.

    L'iris et la pupille sont les traits distinctifs : sans eux, un ovale blanc
    bordé de cils se lit comme un sourcil. C'est le risque déclaré du mot, et la
    parade est ce qui est dessiné — l'œil entier, avec ce que l'œil a et que le
    sourcil n'a pas.
    """
    return (
        p("M104 256 Q256 106 408 256 Q256 406 104 256 Z", BLANC)
        + c(256, 256, 78, BLEU)
        + c(256, 256, 36, ENCRE)
        + c(234, 232, 15, BLANC)
        + trait("M256 178 v-42", 8)
        + trait("M196 192 l-28 -34", 8)
        + trait("M316 192 l28 -34", 8)
        + trait("M146 216 l-32 -24", 8)
        + trait("M366 216 l32 -24", 8)
    )


DESSINS_CE1 = {"foin": foin, "parfum": parfum, "oeil": oeil}


# --- Les huit images de récit -------------------------------------------------
# Une icône PORTE un mot : elle doit être reconnue, seule, sans contexte. Une
# image de récit porte un MOMENT : elle doit être reconnue parmi trois autres et
# se laisser remettre à sa place dans une suite. Ce n'est pas le même métier, et
# c'est pourquoi le corpus est séparé au lieu d'être ajouté à celui du CE1.
#
# Ce qui les sépare se vérifie : quatre images mélangées ne se remettent dans
# l'ordre que si chacune porte un REPÈRE que les trois autres n'ont pas — le
# corpus le déclare étape par étape, et le contrôle refuse deux étapes qui
# s'appuieraient sur le même. Un repère partagé, ce sont deux images
# interchangeables, donc un exercice sans réponse.


def recit_e19_1():
    """« Papa a une photo. » — E19, étape 1.

    Le repère est LE PERSONNAGE : Papa, et lui seul, occupe la scène. Ce que la
    photo montre n'est pas dessiné — c'est l'étape 2, et le dessiner ici ferait
    deux fois la même image à deux échelles.
    """
    return (
        place(papa, 256, 296, 0.64)
        + r(200, 316, 112, 88, 8, BLANC)
        + r(208, 324, 96, 72, 4, BLEU_C)
        + c(200, 360, 13, PEAU) + c(312, 360, 13, PEAU)
        + sol()
    )


def recit_e19_2():
    """« Sur la photo, un éléphant a un téléphone. » — E19, étape 2.

    Le repère est LE CADRE : un cadre blanc fait tout le tour, et la scène est
    vue à travers lui. C'est la seule des huit images sans ligne de sol — une
    photo n'a pas de sol, elle a un bord.
    """
    return (
        r(24, 24, 464, 464, 30, BLANC)
        + r(52, 52, 408, 408, 16, BLEU_C)
        + place(elephant, 250, 300, 0.5)
        + place(telephone, 342, 386, 0.2)
    )


def recit_e19_3():
    """« Le soir, l'éléphant a rejoint la maison. » — E19, étape 3.

    Le repère est LE MOMENT DU JOUR : la lune. La maison dit le lieu, la lune
    dit l'heure, et rien d'autre dans les quatre étapes n'est situé dans le
    temps.
    """
    return (
        place(lune, 418, 104, 0.26)
        + place(maison, 150, 322, 0.55)
        + place(elephant, 344, 330, 0.5, miroir=True)
        + sol()
    )


def recit_e19_4():
    """« Maman rit encore. » — E19, étape 4.

    Le repère est LE GESTE DU CORPS : la bouche ouverte et les yeux fermés du
    rire. Une figure réemployée garde sa pose — sauf ce qu'il faut pour dire le
    moment : les deux yeux de la série sont recouverts de la couleur du visage
    et redessinés en arcs, sans quoi Maman ne rirait pas, elle regarderait.
    """
    return (
        place(maman, 256, 282, 0.72)
        + c(240, 226, 10, PEAU) + c(272, 226, 10, PEAU)
        + trait("M231 229 q9 -9 18 0", 4)
        + trait("M263 229 q9 -9 18 0", 4)
        + e(256, 253, 16, 11, ROUGE_F)
        + sol()
    )


def recit_e45_1():
    """« Le jour, il dort sur une chaise. » — E45, étape 1.

    Le repère est LE MOMENT DU JOUR : le soleil. Le chat est COUCHÉ et ses yeux
    sont fermés — un chat debout sur une chaise ne dirait pas qu'il dort, et
    c'est la seule étape des quatre où le chat n'est pas sur ses pattes.
    """
    return (
        place(soleil, 420, 100, 0.26)
        + r(316, 176, 30, 176, 10, BRUN_C)
        + r(140, 322, 206, 28, 8, BRUN_C)
        + r(150, 350, 24, 74, 8, BRUN)
        + r(312, 350, 24, 74, 8, BRUN)
        + e(252, 292, 78, 32, GRIS)
        + c(174, 286, 36, GRIS)
        + p("M148 258 l-6 -34 30 18 z", GRIS)
        + p("M200 258 l6 -34 -30 18 z", GRIS)
        + trait("M157 286 q9 11 18 0", 6)
        + trait("M183 286 q9 11 18 0", 6)
        + p("M174 302 l-7 11 14 0 z", ROSE)
        + trait("M326 300 q24 14 16 48 q-6 24 -26 22", 9)
        + sol()
    )


def recit_e45_2():
    """« Il lave sa robe avec sa langue. » — E45, étape 2.

    Le repère est LE GESTE DU CORPS : la langue au museau et la patte levée.
    Le chat est celui de la série, dans sa pose de debout ; ce qui est ajouté
    est le geste, pas un second chat.
    """
    return (
        place(chat, 256, 300, 0.62)
        + trait("M252 394 q-18 -14 -22 -34", 12)
        + e(228, 352, 19, 15, GRIS)
        + e(211, 336, 7, 12, ROSE)
        + sol()
    )


def recit_e45_3():
    """« Il monte sur l'échelle. » — E45, étape 3.

    Le repère est LE DÉCOR : l'échelle. Le chat est posé sur un barreau, entre
    les deux montants — le poser au sol ferait une image où il ne monte rien.
    """
    bas, haut = 424, 168
    barreaux = "".join(
        trait(
            f"M{150 + 26 * (bas - y) / (bas - haut):.1f} {y} "
            f"h{212 - 52 * (bas - y) / (bas - haut):.1f}",
            12,
        )
        for y in (196, 246, 296, 346, 390)
    )
    return (
        trait(f"M150 {bas} L176 {haut}", 14)
        + trait(f"M362 {bas} L336 {haut}", 14)
        + barreaux
        + place(chat, 256, 280, 0.55)
        + sol()
    )


def recit_e45_4():
    """« Le chat est un bon compagnon. » — E45, étape 4.

    Le repère est LE PERSONNAGE : le bébé, et lui seul. Le chat ne fait rien —
    et c'est précisément ce que l'étape doit dire : un compagnon ne fait rien.
    """
    return (
        place(bebe, 164, 322, 0.6)
        + place(chat, 336, 322, 0.5)
        + sol()
    )


DESSINS_RECIT = {
    "e19_1": recit_e19_1, "e19_2": recit_e19_2,
    "e19_3": recit_e19_3, "e19_4": recit_e19_4,
    "e45_1": recit_e45_1, "e45_2": recit_e45_2,
    "e45_3": recit_e45_3, "e45_4": recit_e45_4,
}


DESSINS = {
    "papa": papa, "maman": maman, "bebe": bebe, "dodo": dodo, "lit": lit,
    "velo": velo, "moto": moto, "cafe": cafe, "gateau": gateau, "lune": lune,
    "jupe": jupe, "pomme": pomme, "tomate": tomate, "cerise": cerise,
    "zebre": zebre, "cheval": cheval, "lapin": lapin, "canard": canard,
    "mouton": mouton, "koala": koala, "girafe": girafe, "elephant": elephant,
    "crocodile": crocodile, "loup": loup, "chat": chat, "rat": rat,
    "maison": maison, "ecole": ecole, "valise": valise, "cartable": cartable,
    "sac": sac, "telephone": telephone, "parapluie": parapluie, "avion": avion,
    "bateau": bateau, "soleil": soleil, "fleur": fleur, "banane": banane,
    "ananas": ananas, "bonbon": bonbon, "chocolat": chocolat, "pyjama": pyjama,
    "nez": nez, "main": main_dessin,
}


def planche_svg(items, dessins, colonnes=6):
    """Une planche unique, en SVG pur — donc rastérisable, donc regardable.

    La planche HTML sert à l'oeil humain dans un navigateur. Celle-ci existe pour
    une autre raison : un rendu SVG ne s'inspecte pas, il se REGARDE, et pour cela
    il faut une image. Un SVG unique se rastérise en une image unique, ce qui rend
    les 44 dessins vérifiables d'un seul coup d'oeil au lieu de quarante-quatre.

    Le texte est autorisé ici : la planche n'est pas une image de l'application,
    c'est un outil de relecture.

    Le nombre de rangées se calcule : la planche du CE1 n'a que trois dessins, et
    une grille de huit rangées pour trois vignettes serait un cadre vide de sept
    rangées. Le calcul redonne huit pour quarante-quatre, donc la planche de la GS
    est inchangée à l'octet.
    """
    rangees = max(1, -(-len(items) // colonnes))
    cw, ch, marge = 224, 252, 24
    largeur = marge * 2 + colonnes * cw
    hauteur = marge * 2 + rangees * ch
    echelle = 200 / COTE

    m = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" '
        f'width="{largeur}" height="{hauteur}">',
        f'<rect width="{largeur}" height="{hauteur}" fill="#FAF9F7"/>',
    ]
    for k, item in enumerate(items):
        col, ligne = k % colonnes, k // colonnes
        x = marge + col * cw
        y = marge + ligne * ch
        m.append(
            f'<g transform="translate({x + 12} {y + 8}) scale({echelle:.5f})">'
            f'<g fill="none" stroke="{ENCRE}" stroke-width="{EPAISSEUR}" '
            f'stroke-linecap="round" stroke-linejoin="round">'
            f'{dessins[slug(item["mot"])]()}</g></g>'
        )
        m.append(
            f'<text x="{x + cw / 2}" y="{y + 234}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="20" fill="#2E2A26">{item["mot"]}</text>'
        )
        if item.get("risque"):
            m.append(
                f'<text x="{x + cw / 2}" y="{y + 246}" text-anchor="middle" '
                f'font-family="sans-serif" font-size="11" fill="#A93B2E">ambigu</text>'
            )
    m.append("</svg>")
    return "".join(m)


def slug(mot):
    """Le nom de fichier d'un mot : minuscules, sans accent, hors a-z et 0-9.

    Les ligatures se TRANSLITTÈRENT au lieu de disparaître. NFD ne décompose pas
    « œ » — ce n'est pas une lettre accentuée, c'est une ligature — et sans cette
    ligne « œil » donnait le slug « il » : deux lettres perdues, un nom de fichier
    qui ne dit plus le mot, et un risque réel de collision avec un autre mot.
    """
    sans_accent = unicodedata.normalize("NFD", mot)
    sans_accent = "".join(ch for ch in sans_accent if unicodedata.category(ch) != "Mn")
    sans_accent = (
        sans_accent.replace("œ", "oe").replace("Œ", "oe")
        .replace("æ", "ae").replace("Æ", "ae")
    )
    return re.sub(r"[^a-z0-9]", "", sans_accent.lower())


def envelopper(corps):
    """Le cadre : viewBox constant, contour constant, aucun fond, aucun texte."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {COTE} {COTE}" '
        f'width="{COTE}" height="{COTE}" role="img">'
        f'<g fill="none" stroke="{ENCRE}" stroke-width="{EPAISSEUR}" '
        f'stroke-linecap="round" stroke-linejoin="round">{corps}</g></svg>'
    )


# La feuille de style des planches. Extraite en constante quand la planche du
# récit est venue s'y ajouter : deux copies de la même feuille auraient divergé,
# et c'est exactement le défaut que cette tranche a déjà trouvé deux fois.
CSS_PLANCHE = [
    "body{font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:#FAF9F7;",
    "color:#2E2A26;margin:0;padding:32px}",
    "h1{font-size:20px;margin:0 0 4px}p.intro{margin:0 0 28px;color:#6B655F;font-size:14px;line-height:1.5}",
    ".grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(152px,1fr));gap:18px}",
    ".carte{background:#fff;border:1px solid #E4E0DA;border-radius:14px;padding:12px;",
    "display:flex;flex-direction:column;align-items:center}",
    ".carte svg{width:112px;height:112px;display:block}",
    ".mot{margin-top:8px;font-weight:600;font-size:14px}",
    ".fichier{font-size:10px;color:#8A847D;font-family:ui-monospace,monospace}",
    ".objet{margin-top:6px;font-size:11px;color:#6B655F;text-align:center;line-height:1.35}",
    ".alerte{margin-top:6px;font-size:10px;color:#A93B2E;text-align:center;line-height:1.3}",
]

# Ce que la planche du récit ajoute. Une scène se regarde de plus près qu'une
# icône — il y a quatre figures dedans, pas une — et les quatre moments d'un
# récit doivent se voir côte à côte, dans l'ordre, pour que la relecture ait un
# sens : une planche rangée par ordre alphabétique ne montrerait pas l'ordre.
CSS_RECIT = [
    "h2{font-size:16px;margin:36px 0 2px}",
    ".carte.scene svg{width:168px;height:168px}",
    ".moment{margin-top:8px;font-weight:600;font-size:13px;text-align:center;line-height:1.3}",
    ".ligne{margin-top:6px;font-size:11px;color:#6B655F;text-align:center;font-style:italic;line-height:1.35}",
    ".repere{margin-top:6px;font-size:10px;color:#33703C;text-align:center}",
    ".ordre{margin-top:2px;font-size:10px;color:#8A847D;font-family:ui-monospace,monospace}",
]


def ecrire_planches(items, dessins, libelles, sortie, titre_document, titre_page, intro):
    """Les deux planches de contrôle : HTML pour l'oeil, SVG pour le rastérisage."""
    planche = [
        "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>",
        f"<title>Ludo'Lire — {titre_document}</title>",
        "<style>",
        *CSS_PLANCHE,
        "</style></head><body>",
        f"<h1>{titre_page}</h1>",
        f"<p class='intro'>{intro}</p>",
        "<div class='grille'>",
    ]
    for item in items:
        mot = item["mot"]
        svg = envelopper(dessins[slug(mot)]())
        alerte = ""
        if item.get("risque"):
            cibles = ", ".join(
                r["avec"] if r.get("avec") else r.get("hors_banque", "?") for r in item["risque"]
            )
            alerte = f"<div class='alerte'>ne pas confondre avec {cibles}</div>"
        planche.append(
            f"<div class='carte'>{svg}<div class='mot'>{mot}</div>"
            f"<div class='fichier'>ill_{slug(mot)}.svg</div>"
            f"<div class='objet'>{libelles.get(mot, '')}</div>{alerte}</div>"
        )
    planche.append("</div></body></html>")
    (sortie / "planche.html").write_bytes("\n".join(planche).encode("utf-8"))
    (sortie / "planche.svg").write_bytes(planche_svg(items, dessins).encode("utf-8"))


def _controler_dessins(items, dessins, cle=None, etiquette=None):
    """Un mot sans dessin, ou un dessin vide, ne doit pas partir en silence : un
    fichier SVG vide s'affiche comme un cadre blanc, et rien ne le signale.

    `cle` et `etiquette` disent comment désigner un item. Par défaut c'est son
    mot réduit en slug ; le récit, lui, est désigné par son identifiant, qui est
    déjà un nom de fichier — lui appliquer le slug des mots effacerait son tiret
    bas, et « e19_1 » deviendrait « e191 ».
    """
    cle = cle or (lambda i: slug(i["mot"]))
    etiquette = etiquette or (lambda i: i["mot"])
    manquants = [etiquette(i) for i in items if cle(i) not in dessins]
    vides = [s for s, f in dessins.items() if not f().strip()]
    for nom in manquants:
        print(f"Aucun dessin pour « {nom} »")
    for s in vides:
        print(f"Dessin vide pour « {s} »")
    return not manquants and not vides


def main_gs():
    brief = json.loads((ICI / "images-gs.json").read_text(encoding="utf-8"))
    mots = json.loads((ICI / "mots-gs.json").read_text(encoding="utf-8"))["mots"]
    libelles = {m["mot"]: m["illustration"] for m in mots}

    if not _controler_dessins(brief["items"], DESSINS):
        print("Rien a ete ecrit.")
        return 1

    SORTIE.mkdir(parents=True, exist_ok=True)
    for item in brief["items"]:
        chemin = SORTIE / f"ill_{slug(item['mot'])}.svg"
        chemin.write_bytes(envelopper(DESSINS[slug(item["mot"])]()).encode("utf-8"))

    ecrire_planches(
        brief["items"], DESSINS, libelles, SORTIE,
        "planche des 44 illustrations",
        "Les 44 illustrations de la tranche GS",
        "Écrites en SVG, comme du code — aucune dépendance, aucune question de "
        "licence. La mention rouge signale une ambiguïté déclarée dans le brief. Une image qui ne "
        "se reconnaît pas du premier coup d'oeil est un défaut à corriger, pas un détail de style.",
    )

    print(f"{len(brief['items'])} SVG écrits dans contenu/images/")
    print(f"Palette fermée : {len(PALETTE)} couleurs")
    print("Planche de contrôle : contenu/images/planche.html et planche.svg")
    return 0


def main_ce1():
    """Les images du CE1. Mêmes primitives, même palette, même cadre, autre dossier.

    Le corpus est court parce que le lexique l'est : les deux nasales rares et les
    mots irréguliers comptent trois noms concrets sur vingt-huit mots examinés.
    Les mots qui ne se dessinent pas ne sont pas absents du corpus pour autant :
    ils sont déclarés dans `non_illustrables`, avec leur raison, et le contrôle
    refuse un mot déclaré sans raison.
    """
    corpus = json.loads((ICI / "images-ce1.json").read_text(encoding="utf-8"))
    libelles = {i["mot"]: i["objet"] for i in corpus["items"]}

    if not _controler_dessins(corpus["items"], DESSINS_CE1):
        print("Rien a ete ecrit.")
        return 1

    SORTIE_CE1.mkdir(parents=True, exist_ok=True)
    for item in corpus["items"]:
        chemin = SORTIE_CE1 / f"ill_{slug(item['mot'])}.svg"
        chemin.write_bytes(envelopper(DESSINS_CE1[slug(item["mot"])]()).encode("utf-8"))

    ecrire_planches(
        corpus["items"], DESSINS_CE1, libelles, SORTIE_CE1,
        "planche des 3 illustrations du CE1",
        "Les trois illustrations de la tranche CE1",
        "Trois images pour trois besoins déclarés, et vingt-deux mots déclarés "
        "non illustrables — c'est le lexique qui est court, pas le travail. La mention rouge "
        "signale une ambiguïté déclarée dans le brief.",
    )

    print(f"{len(corpus['items'])} SVG écrits dans contenu/images-ce1/")
    print(f"{len(corpus['non_illustrables'])} mots déclarés non illustrables")
    print("Planche de contrôle : contenu/images-ce1/planche.html et planche.svg")
    return 0


def planche_recit_svg(recits, dessins):
    """La planche du récit, rastérisable — donc regardable.

    Une rangée par récit, les quatre moments DANS L'ORDRE, chacun sous la ligne
    qu'il illustre. C'est la seule disposition qui permette de juger ce que ces
    images doivent faire : quatre dessins qu'on doit pouvoir remettre dans cet
    ordre-là. Une planche triée par identifiant, comme celle des icônes, ne le
    montrerait pas — et l'ordre est ici l'information, pas la mise en page.

    La ligne citée n'est pas pliée : elle est courte (quarante-deux signes au
    plus) et tient sur une ligne à 11 points. La plier aurait demandé de
    réécrire ici la règle de pliage du contrôle des textes, et deux règles de
    pliage divergeraient.
    """
    colonnes, cw, ch, marge = 4, 300, 372, 28
    largeur = marge * 2 + colonnes * cw
    hauteur = marge * 2 + len(recits) * ch
    echelle = 220 / COTE
    m = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" '
        f'width="{largeur}" height="{hauteur}">',
        f'<rect width="{largeur}" height="{hauteur}" fill="#FAF9F7"/>',
    ]
    for r, recit in enumerate(recits):
        y0 = marge + r * ch
        m.append(
            f'<text x="{marge}" y="{y0 + 20}" font-family="sans-serif" font-size="18" '
            f'font-weight="600" fill="#2E2A26">{_echapper(recit["exercice"])} — '
            f'{_echapper(recit["titre_du_texte"])} (texte {recit["texte"]}, '
            f'rang {recit["rang"]})</text>'
        )
        for k, etape in enumerate(recit["etapes"]):
            x, y = marge + k * cw, y0 + 34
            m.append(
                f'<rect x="{x}" y="{y}" width="{cw - 16}" height="{ch - 34}" rx="12" '
                f'fill="#FFFFFF" stroke="#E4E0DA"/>'
            )
            m.append(
                f'<g transform="translate({x + 28} {y + 14}) scale({echelle:.5f})">'
                f'<g fill="none" stroke="{ENCRE}" stroke-width="{EPAISSEUR}" '
                f'stroke-linecap="round" stroke-linejoin="round">'
                f'{dessins[etape["id"]]()}</g></g>'
            )
            m.append(
                f'<text x="{x + (cw - 16) / 2}" y="{y + ch - 82}" text-anchor="middle" '
                f'font-family="sans-serif" font-size="12" fill="#2E2A26">'
                f'« {_echapper(etape["ligne_citee"])} »</text>'
            )
            m.append(
                f'<text x="{x + (cw - 16) / 2}" y="{y + ch - 60}" text-anchor="middle" '
                f'font-family="ui-monospace,monospace" font-size="11" fill="#8A847D">'
                f'{etape["id"]} · ordre {etape["ordre"]}</text>'
            )
            m.append(
                f'<text x="{x + (cw - 16) / 2}" y="{y + ch - 42}" text-anchor="middle" '
                f'font-family="sans-serif" font-size="11" fill="#33703C">'
                f'repère : {_echapper(etape["repere"])}</text>'
            )
    m.append("</svg>")
    return "".join(m)


def _echapper(texte):
    """Trois caractères, et rien de plus : une esperluette dans un texte ferait
    échouer la lecture XML de la planche, et le message d'erreur parlerait de la
    planche au lieu de parler du texte."""
    return texte.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ecrire_planche_recit(corpus, dessins, sortie):
    """Les deux planches du récit : HTML pour l'œil, SVG pour le rastérisage."""
    recits = corpus["recits"]
    planche = [
        "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>",
        "<title>Ludo'Lire — planche des images de récit du CE1</title>",
        "<style>",
        *CSS_PLANCHE,
        *CSS_RECIT,
        "</style></head><body>",
        "<h1>Les huit images de récit de la tranche CE1</h1>",
        "<p class='intro'>Deux exercices de remise en ordre, quatre moments chacun, "
        "montrés ICI DANS L'ORDRE — c'est celui du texte, et le contrôle le vérifie en "
        "relisant la ligne citée dans le fichier du texte. Une scène se regarde à "
        "168 px parce qu'il y a quatre figures dedans ; l'application la montre à "
        "112 px, comme les icônes.</p>",
    ]
    for recit in recits:
        planche.append(
            f"<h2>{_echapper(recit['exercice'])} — {_echapper(recit['titre_du_texte'])} "
            f"<span class='fichier'>texte {recit['texte']}, rang {recit['rang']}, "
            f"unité {recit['unite']}</span></h2>"
        )
        planche.append(f"<p class='intro'>{_echapper(recit['ce_que_l_exercice_demande'])}</p>")
        planche.append("<div class='grille'>")
        for etape in recit["etapes"]:
            planche.append(
                f"<div class='carte scene'>{envelopper(dessins[etape['id']]())}"
                f"<div class='ordre'>ordre {etape['ordre']} · {etape['id']}</div>"
                f"<div class='moment'>{_echapper(etape['moment'])}</div>"
                f"<div class='ligne'>« {_echapper(etape['ligne_citee'])} »</div>"
                f"<div class='repere'>repère : {_echapper(etape['repere'])}</div>"
                f"</div>"
            )
        planche.append("</div>")
    planche.append("</body></html>")
    (sortie / "planche.html").write_bytes("\n".join(planche).encode("utf-8"))
    (sortie / "planche.svg").write_bytes(planche_recit_svg(recits, dessins).encode("utf-8"))


def main_recit():
    """Les images de récit. Autre corpus, autre dossier, autres invariants.

    Ce que ce mode produit n'est pas une variante des icônes : c'est le seul
    endroit où quatre dessins doivent pouvoir être REMIS DANS UN ORDRE. Le
    générateur ne le vérifie pas — il écrit ; c'est `verifier-images.py --recit`
    qui relit la ligne citée dans le fichier du texte et qui refuse un ordre que
    le texte ne porte pas.
    """
    corpus = json.loads((ICI / "images-recit-ce1.json").read_text(encoding="utf-8"))
    etapes = [e for r in corpus["recits"] for e in r["etapes"]]

    if not _controler_dessins(etapes, DESSINS_RECIT, cle=lambda i: i["id"]):
        print("Rien a ete ecrit.")
        return 1

    SORTIE_RECIT.mkdir(parents=True, exist_ok=True)
    for etape in etapes:
        chemin = SORTIE_RECIT / f"ill_{etape['id']}.svg"
        chemin.write_bytes(envelopper(DESSINS_RECIT[etape["id"]]()).encode("utf-8"))

    ecrire_planche_recit(corpus, DESSINS_RECIT, SORTIE_RECIT)

    print(f"{len(etapes)} SVG écrits dans contenu/images-recit-ce1/")
    print(f"{len(corpus['recits'])} récits, {len(corpus['reperes'])} repères déclarés, "
          f"{len(corpus['interdits'])} interdits")
    print("Planche de contrôle : contenu/images-recit-ce1/planche.html et planche.svg")
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--ce1":
        return main_ce1()
    if len(sys.argv) > 1 and sys.argv[1] == "--recit":
        return main_recit()
    return main_gs()


if __name__ == "__main__":
    raise SystemExit(main())
