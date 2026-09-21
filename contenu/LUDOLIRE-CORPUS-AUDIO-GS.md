# Ludo'Lire — Corpus audio de la tranche GS

**Statut :** inventaire clos pour les familles phonèmes, lettres, consignes et retours. Enregistrable.
**Source de vérité :** `outils/corpus-gs.json`. Le tableau du § 4 en est le rendu, produit par `outils/generer-table.py`.
**Dépend de :** `contenu/LUDOLIRE-PROGRESSION-GS.md` (les 45 unités que le corpus doit servir) et `outils/mots-gs.json` (les mots du corpus).

---

## 1. Pourquoi un corpus, et pas une synthèse vocale

À la GS, presque tout est oral. Une consigne lue à l'écran ne sert à rien : l'enfant de cinq ans ne lit pas. **Le corpus audio n'est donc pas un habillage, c'est le canal par lequel la tranche existe.**

Et ce corpus doit être enregistré par une voix humaine. Un phonème isolé produit par une voix de synthèse est souvent faux ou inaudible — or c'est précisément ce qu'on demande à l'enfant d'entendre. Une application qui entraîne l'oreille avec des sons approximatifs entraîne à la mauvaise chose.

C'est le poste de coût dominant de la tranche GS, et il faut l'assumer : **207 fichiers** (§ 4).

## 2. La conséquence de la décision « pas de reconnaissance vocale »

La décision 3 produit ici son effet le plus lourd. Sans micro, **l'application n'entend rien**. La parade tient en une règle de conception :

> **Toute consigne se donne par la voix, et toute réponse se donne par le geste.**

L'enfant ne *dit* pas le nombre de syllabes : il pose un jeton par syllabe. Il ne *répète* pas une paire distinctive : il désigne l'image. Chaque unité de la progression porte pour cela une colonne « ce que l'enfant fait » — et c'est cette colonne qui dit de quel son le corpus a besoin.

Corollaire : **le corpus ne contient aucune phrase de félicitation longue, aucun bavardage.** Un retour s'entend des dizaines de fois par séance. Sept retours courts suffisent (§ 4).

## 3. Ce que le corpus ne peut pas remplacer

Trois objectifs de la tranche restent hors de portée, et le corpus ne fait que les accompagner :

| Objectif | Pourquoi il échappe à l'app | Traitement |
|---|---|---|
| Articulation des paires distinctives | il faut entendre l'enfant prononcer | activité guidée par le parent, non notée |
| Reproduction des intonations | il faut entendre la hauteur | idem |
| Prononciation des trente-six phonèmes | il faut entendre chaque phonème | hors app, au bilan de sortie |

Le corpus **fait entendre le modèle**. Il ne vérifie pas que l'enfant l'a imité.

## 4. L'inventaire

<!-- DEBUT TABLE GENEREE -->

### Le cahier des charges d'enregistrement

| Point | Règle |
|---|---|
| master | WAV, 48 kHz, 24 bits, mono |
| livraison | AAC ou Opus, mono, 48 kHz, 96 kbit/s |
| niveau consignes | -16 LUFS (EBU R128) |
| niveau phonemes | -20 LUFS — un phonème isolé est court ; le monter au niveau des consignes le rend agressif |
| crete max | -1 dBTP |
| traitement | aucun — ni compression, ni réverbération, ni dé-esseur, ni dé-bruitage |
| silence | 150 ms avant, 250 ms après chaque item — sans quoi la lecture est tronquée sur certains appareils |
| duree max | consigne 6 s, mot 1,5 s, phonème 1 s |
| nommage | <prefixe>_<slug>.wav — un fichier par item, jamais un fichier qui en contient plusieurs |
| conditions | pièce calme, micro à 20 cm, une seule séance par famille — la voix ne doit pas changer entre deux items de la même famille |
| versionnage | les fichiers sont versionnés avec le projet ; un item réenregistré change de nom (suffixe _v2) plutôt que d'écraser l'ancien |

### Les familles

| Préfixe | Famille | Contenu |
|---|---|---|
| `ph_` | Phonèmes | le phonème isolé, quand il est prononçable seul, puis un mot porteur |
| `let_` | Noms de lettres | le nom de chacune des vingt-six lettres |
| `con_` | Consignes | les phrases d'instruction, enregistrées une fois et réutilisées dans tous les exercices |
| `ret_` | Retours | les phrases de feedback, courtes, réutilisées partout |
| `mot_` | Mots | un mot du corpus de mots, dit normalement puis scandé syllabe par syllabe |

### Les trente-six phonèmes

| Phonème | Catégorie | Enregistré seul ? | Mot porteur |
|---|---|---|---|
| `/a/` | voyelle orale | oui | chat |
| `/e/` | voyelle orale | oui | été |
| `/ɛ/` | voyelle orale | oui | lait |
| `/i/` | voyelle orale | oui | lit |
| `/o/` | voyelle orale | oui | château |
| `/ɔ/` | voyelle orale | oui | pomme |
| `/u/` | voyelle orale | oui | loup |
| `/y/` | voyelle orale | oui | lune |
| `/ø/` | voyelle orale | oui | deux |
| `/œ/` | voyelle orale | oui | fleur |
| `/ə/` | voyelle orale | oui | le |
| `/ɑ/` | voyelle orale | oui | pâte |
| `/ɑ̃/` | voyelle nasale | oui | chant |
| `/ɛ̃/` | voyelle nasale | oui | lapin |
| `/ɔ̃/` | voyelle nasale | oui | bonbon |
| `/œ̃/` | voyelle nasale | oui | brun |
| `/j/` | semi-voyelle | oui | fille |
| `/w/` | semi-voyelle | oui | oui |
| `/ɥ/` | semi-voyelle | oui | huit |
| `/p/` | consonne occlusive | **non** — occlusive | papa |
| `/b/` | consonne occlusive | **non** — occlusive | bébé |
| `/t/` | consonne occlusive | **non** — occlusive | tapis |
| `/d/` | consonne occlusive | **non** — occlusive | dodo |
| `/k/` | consonne occlusive | **non** — occlusive | café |
| `/g/` | consonne occlusive | **non** — occlusive | gâteau |
| `/f/` | consonne fricative | oui | fenêtre |
| `/v/` | consonne fricative | oui | vélo |
| `/s/` | consonne fricative | oui | soleil |
| `/z/` | consonne fricative | oui | zèbre |
| `/ʃ/` | consonne fricative | oui | chat |
| `/ʒ/` | consonne fricative | oui | jupe |
| `/m/` | consonne nasale | oui | maman |
| `/n/` | consonne nasale | oui | nez |
| `/ɲ/` | consonne nasale | oui | agneau |
| `/l/` | consonne liquide | oui | lune |
| `/ʁ/` | consonne liquide | oui | rat |

### Les vingt-six noms de lettres

| Lettre | Nom | Lettre | Nom | Lettre | Nom | Lettre | Nom |
|---|---|---|---|---|---|---|---|
| `a` | a | `b` | bé | `c` | cé | `d` | dé |
| `e` | e | `f` | effe | `g` | gé | `h` | ache |
| `i` | i | `j` | ji | `k` | ka | `l` | elle |
| `m` | emme | `n` | enne | `o` | o | `p` | pé |
| `q` | ku | `r` | erre | `s` | esse | `t` | té |
| `u` | u | `v` | vé | `w` | double vé | `x` | ixe |
| `y` | i grec | `z` | zède |  |  |  |  |

### Les consignes

| Fichier | Ce que la voix dit |
|---|---|
| `con_ecoute_bien` | « Écoute bien. » |
| `con_montre_image_son` | « Montre l'image du son que tu entends. » |
| `con_pose_jeton_syllabe` | « Pose un jeton pour chaque syllabe. » |
| `con_frappe_syllabes` | « Frappe dans tes mains en disant le mot. » |
| `con_leve_main_son` | « Lève la main quand tu entends le son. » |
| `con_range_court_long` | « Range les images du mot le plus court au mot le plus long. » |
| `con_touche_lettre_son` | « Touche la lettre qui fait ce son. » |
| `con_nomme_lettre` | « Nomme la lettre que je montre. » |
| `con_apparie_qui_rime` | « Montre les deux images qui riment. » |
| `con_repete_apres_moi` | « Répète après moi. » |
| `con_ecoute_encore` | « Écoute encore une fois. » |
| `con_trouve_intrus` | « Quel mot ne commence pas comme les autres ? » |
| `con_debut_ou_fin` | « Où entends-tu le son : au début ou à la fin du mot ? » |
| `con_deplace_lettres` | « Déplace les lettres dans l'ordre. » |
| `con_dis_mot_obtenu` | « Dis le mot que tu obtiens. » |
| `con_carte_manquante` | « Choisis la carte qui manque et pose-la dans le mot. » |
| `con_ecoute_mot_obtenu` | « Écoute le mot que tu obtiens. » |
| `con_trie_images` | « Mets ensemble les images qui commencent par le même son. » |
| `con_compte_syllabes` | « Combien de syllabes entends-tu dans ce mot ? » |
| `con_meme_son_debut` | « Montre l'image qui commence par le même son. » |
| `con_touche_zone_son` | « Touche l'endroit d'où vient le son. » |
| `con_apparie_meme_son` | « Trouve les deux boîtes qui font le même son. » |
| `con_pose_jeton_sur_image` | « Pose un jeton sur l'image quand tu entends le son. » |
| `con_suis_voix_doigt` | « Suis la voix avec ton doigt. » |
| `con_montre_image_mot` | « Montre l'image du mot que tu entends. » |
| `con_trie_images_son` | « Mets ensemble les images où tu entends le même son. » |
| `con_compose_syllabes` | « Pose les syllabes dans l'ordre que tu entends. » |
| `con_touche_lettre_nom` | « Touche la lettre dont j'ai dit le nom. » |
| `con_touche_lettres_ordre` | « Touche les lettres dans l'ordre que tu entends. » |
| `con_apparie_graphies` | « Assemble les trois écritures de la même lettre. » |
| `con_remets_ordre_images` | « Remets les images dans l'ordre que tu as entendu. » |

### Les retours

| Fichier | Ce que la voix dit |
|---|---|
| `ret_bravo` | « Bravo ! » |
| `ret_cest_ca` | « C'est ça ! » |
| `ret_tu_as_trouve` | « Tu as trouvé ! » |
| `ret_presque` | « Presque. Essaie encore. » |
| `ret_regarde_bien` | « Regarde bien. » |
| `ret_on_recommence` | « On recommence ensemble. » |
| `ret_fin_seance` | « C'est fini pour aujourd'hui. Bravo ! » |

### Le décompte

| Famille | Fichiers |
|---|---|
| Phonèmes isolés | 30 |
| Mots porteurs de phonème | 36 |
| Noms de lettres | 26 |
| Consignes | 31 |
| Retours | 7 |
| Mots du corpus GS (entier + scandé) | 88 |
| **Total** | **218** |

<!-- FIN TABLE GENEREE -->

## 5. Deux points de méthode

**Le nom d'une lettre n'est pas son son.** « erre » et /ʁ/ sont deux choses différentes, et les confondre est l'erreur la plus fréquente dans l'enseignement de la lecture. Le corpus porte les deux, dans deux familles séparées : `let_` pour le nom, `ph_` pour le son.

**Six phonèmes n'ont pas d'isolé.** Les occlusives — /p/, /b/, /t/, /d/, /k/, /g/ — ne se prononcent pas seules : on dit « pe » ou rien. Le programme le dit à sa façon, en demandant que la valeur sonore des lettres soit connue « **hormis les occlusives** ». On ne demande donc jamais à l'enfant de prononcer /p/ seul, et le corpus ne contient pas cet enregistrement. Les 36 phonèmes donnent 30 fichiers isolés, pas 36.

## 6. Ce qui reste à produire

- **Les mots** — la famille `mot_` dépend de `outils/mots-gs.json`, qui est désormais écrit (44 mots). Deux prises par mot : le mot entier, et le mot scandé. Soit 88 fichiers, déjà comptés dans le total.
- **Les images** — *produites*. 44 images, une par mot du corpus GS : le brief est `outils/images-gs.json` → `contenu/LUDOLIRE-IMAGES-GS.md`, et les fichiers sont dans `contenu/images/` (`ill_<slug>.svg`), engendrés par `outils/generer-images.py`. Elles ne servent pas d'illustration d'agrément : au rendu oral du jeu de syllabes, c'est **l'image qui identifie le mot**, les cases ne portant que le nombre de syllabes. La contrainte n'est donc pas « l'image doit être claire » mais « l'image ne doit convenir à aucun autre mot » — **vingt-quatre** des quarante-quatre portent une ambiguïté déclarée, et il a fallu deux lectures des reconstitutions du jeu pour voir `bouton`. **Cet environnement ne dispose d'aucun outil de génération d'image** : les images sont écrites **comme du code**, ce qui règle la licence par construction et permet un contrôle de structure — mais pas un jugement sur la reconnaissance, qui se fait en regardant la planche `contenu/images/planche.html`.
  *Correction :* une version antérieure de cette section disait « chaque paire distinctive aussi ». C'est faux — les cartes du jeu sont des **syllabes**, pas des images. Les paires de sons proches n'ont pas d'illustration et n'en ont pas besoin.
- **Le corpus de mots n'est pas figé.** Les 44 mots sont un point de départ : la règle du § 5 de la progression (mots connus de l'enfant à l'oral) autorise à en ajouter, pas à en improviser. Toute addition entraîne une image de plus — et une relecture à la main des reconstitutions du jeu, parce que le contrôle des collisions ne connaît que la liste écrite.

## 7. Comment on vérifie

```bash
python outils/verifier-corpus.py        # découpes, paires, rangs, slugs, décompte
python outils/generer-table.py          # met les tables à jour depuis les JSON
```

`verifier-corpus.py` refuse un slug mal formé, un doublon, une découpe syllabique qui ne redonne pas le mot, un phonème dont la catégorie et le caractère isolable se contredisent, et un rang de mot qui n'est pas minimal.
