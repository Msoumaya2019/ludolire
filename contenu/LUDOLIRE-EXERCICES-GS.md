# Ludo'Lire — Les exercices de la tranche GS

**Statut :** proposition. Banque de 50 exercices, 20 mécaniques, 7 besoins déclarés, 5 corrections consignées. Version 0.2.0.
**Source de vérité :** `outils/exercices-gs.json`. Les tableaux du § 8 en sont le rendu, produit par `outils/generer-table.py`.
**Dépend de :** `outils/progression-gs.json` (les 45 unités, et leur champ `production`), `outils/corpus-gs.json` (les consignes, les phonèmes, les noms de lettres), `outils/mots-gs.json` et `outils/images-gs.json` (le matériel), `outils/jeu-syllabes.json` (les exercices E46 à E50).

---

## 1. Ce que la banque règle, et ce qu'elle ne règle pas

La progression GS dit **ce que** chaque unité vise. Elle ne dit pas **comment** on l'entraîne sur un écran sans micro, ni ce que l'application peut vérifier. C'est l'objet de cette banque.

Elle règle trois choses, et trois seulement :

1. **ce que la voix dit** — un slug de consigne, enregistré une fois dans `corpus-gs.json` ;
2. **ce que l'enfant fait** — un geste, choisi pour être jugeable par la machine ;
3. **ce que l'application peut en conclure** — un verdict, `app` ou `hors app`.

Elle ne règle **ni** l'habillage graphique, **ni** l'ordre des exercices dans une séance, **ni** la difficulté relative de deux exercices. Deux exercices de 45 secondes ne sont pas de même difficulté parce qu'ils durent autant.

## 2. La voix donne la consigne, le geste donne la réponse

> Toute consigne se donne par la voix, et toute réponse se donne par le geste.

C'est la conséquence directe de l'absence de micro, et ce n'est pas une contrainte qu'on subit : c'est elle qui a produit la liste des mécaniques. Une unité qui demande à l'enfant de **dire** quelque chose ne peut pas être vérifiée par la machine — mais elle peut presque toujours être **retournée**.

Le patron, appliqué partout où le programme demande une production :

| Le programme demande | L'exercice demande |
|---|---|
| de nommer la lettre désignée | la voix dit le nom, l'enfant **touche** la lettre (E22, E23, E40, E42) |
| de dire les lettres d'un mot dans l'ordre | la voix les dit, l'enfant les **touche dans l'ordre** (E25, E43) |
| de dire le mot transformé | la voix le dit, l'enfant **ordonne les syllabes** (E14, E32, E33) |
| de prolonger le phonème | la voix le prolonge, le doigt **suit la ligne** (E44) |

Ce retournement ne fait pas disparaître l'objectif : il le déplace. L'unité 25 demande d'**épeler pour faire écrire** ; E25 fait **toucher pour faire composer**. Les deux entraînent la même connaissance de l'ordre des lettres, et une seule est vérifiable sans oreille. C'est pourquoi chaque exercice retourné porte une **`inversion`** : ce que le geste reprend, et ce qui reste hors app.

## 3. Les mécaniques

Vingt mécaniques, et chacune nomme deux choses : **ce que l'enfant fait** et **ce que l'application fait**. Une mécanique qui ne dirait que la première ne serait pas une mécanique, ce serait une intention.

Deux mécaniques ne sont pas jugeables, et une seule est déclarée telle :

- **`repeter_modele`** — l'application donne le modèle et s'arrête là. Elle ne peut rien conclure. C'est la mécanique des six unités d'articulation et de reproduction, et son verdict est `hors app`.
- **`jeu_syllabes`** — l'application vérifie **l'ordre des cartes**, pas la diction. Le retour est sonore : l'enfant entend le mot qu'il a composé. C'est le seul verdict possible sans micro, et il suffit — entendre « bamane » au lieu de « banane » est plus parlant qu'un score.

## 4. Ce que l'application peut juger, et ce qu'elle ne peut pas

Le palier de sortie de la GS déclare **sept réussites**. Trois d'entre elles ne sont pas vérifiables dans l'application :

| Réussite du palier | Pourquoi elle échappe à l'application |
|---|---|
| Prononcer avec exactitude les couples de consonnes proches | il faut **entendre** l'enfant |
| Prononcer les doubles consonnes | idem |
| Épeler afin qu'un tiers puisse écrire | il faut entendre la diction des lettres |

Ces trois-là sont couvertes par des exercices déclarés **`hors app`**, et chacune porte une **`substitution`** : le jumeau réceptif qui vérifie quelque chose de voisin, ou la mention explicite qu'il n'y en a pas.

Le cas le plus net est **E39**, les doubles consonnes : *aucune substitution possible — la difficulté EST dans l'enchaînement de deux consonnes, et aucune image ne l'attrape*. L'application donne le modèle, l'enfant répète, un adulte juge. Écrire « aucune » vaut mieux que d'inventer un équivalent qui n'en serait pas un.

Et un exercice hors app pour une raison qui n'est pas technique : **E21**, l'étiquette du prénom. L'unité repose sur le prénom de l'enfant ; l'application n'en collecte aucun, n'en stocke aucun, n'en transmet aucun — c'est le § 7 de la note de cadrage. Ce n'est pas un manque, c'est une décision de produit, et elle est consignée comme telle.

## 5. L'inversion de charge, et les unités de production

Toutes les unités ne demandent pas une production. « Frapper les syllabes d'un mot » est un objectif **oral** qui n'est pas une production : le geste *est* l'objectif. « Prononcer correctement les paires distinctives » en est une : sans voix, l'objectif n'est pas atteint.

C'est un axe, et il est déclaré une fois pour toutes dans la progression — le champ `production` de chaque unité. Il commande le verdict des exercices :

- unité de production couverte par un exercice **`hors app`** → l'exercice dit **pourquoi** ;
- unité de production couverte par un exercice **`app`** → l'exercice dit **ce que le geste reprend** (`inversion`) ;
- unité sans production → ni l'un ni l'autre.

Sans cet axe, un objectif non entraîné passerait pour un objectif entraîné : l'exercice existe, il est vert, et personne ne voit que la moitié de l'unité n'est pas couverte.

**Cet axe a été pris en défaut une fois.** Trois unités — 14, 32, 33 — avaient été déclarées sans production, au motif que la manipulation des syllabes est vérifiée par un geste. Le raisonnement s'arrêtait à la vérification : le programme demande aussi de **dire** le mot transformé. C'est le contrôle qui l'a vu, par l'autre bout — trois exercices déclaraient une inversion sur une unité censée ne pas en avoir besoin. Le défaut est consigné au § 7.

## 6. Les besoins : ce que la banque ne peut pas faire sans matériel

Un exercice est une intention jusqu'à ce que son matériel existe. Six fois, la banque a demandé quelque chose que le corpus ne contient pas. Ces manques sont déclarés **à deux endroits** — sur l'exercice, par une référence (`besoin_id`), et dans la liste consolidée — et le contrôle vérifie l'accord **dans les deux sens**.

Pourquoi les deux sens : un besoin déclaré sans entrée consolidée est un manque qu'on ne retrouve nulle part ; une entrée consolidée sans déclarant est une entrée périmée. N'écrire qu'un sens est exactement la façon dont on oublie la moitié.

Deux besoins sont **bloquants**, et c'est la même famille : il manque des **formes qui ne sont pas des mots du corpus**.

- **unité 13** — les syllabes isolées. L'unité fait discriminer une syllabe cible dans une suite énoncée ; le corpus contient les mots et leur version scandée, aucune syllabe seule. La famille `syl_` reste à créer, une trentaine de fichiers.
- **unité 14** — les mots transformés. La voix doit pouvoir dire « li-va », « ne-ba-na ». Même famille.

Les quatre autres ne bloquent pas : ils appauvriront l'exercice, ils ne l'empêcheront pas.

## 7. Les corrections consignées

Cinq défauts sont consignés dans la banque, avec ce qui les a rendus invisibles. C'est la partie la plus utile du fichier : un défaut qui n'est pas écrit se refait.

Trois d'entre eux sont **le même mode d'échec** — une table pleine qui cache un trou :

- le champ `sert` du jeu de syllabes désignait des unités d'**articulation** alors que le jeu ne fait jamais prononcer ;
- les besoins déclarés avaient été consolidés en dédoublonnant **par unité**, ce qui a absorbé le second besoin de l'unité 14 ;
- le champ `substitution` portait **deux sens** — le jumeau réceptif d'un côté, l'inversion de charge de l'autre — et chaque valeur, lue seule, était plausible.

Le quatrième est un **matériel plausible pris pour un matériel disponible** : E46 annonçait huit mots qui ne sont l'objet d'aucun item du jeu, parce que la liste avait été remplie avec « les mots courts du corpus » au lieu de « les items courts du jeu ». Tous ces mots sont effectivement courts, et c'est pour cela que le défaut ne se voyait pas.

Le cinquième est le jugement du § 5, pris en défaut par le contrôle.

## 8. La banque

<!-- DEBUT TABLE GENEREE -->

### Les vingt mécaniques

| Mécanique | Ce que l'enfant fait | Ce que l'application fait | Verdict |
|---|---|---|---|
| `localiser_son` — Localiser un son dans l'espace | toucher la zone de l'écran d'où le son est venu | joue un son depuis un point de l'écran, puis un autre depuis un autre point | app |
| `lever_main` — Signaler une cible dans une suite | toucher un bouton à chaque fois que la cible revient | énonce une suite et enregistre les appuis, avec leur position dans la suite | app |
| `apparier_sons` — Apparier deux sons identiques | toucher deux boîtes qui font le même son | remplit six boîtes de trois sons joués deux fois chacun, dans un ordre tiré | app |
| `poser_jeton` — Poser un jeton | pose un jeton sur une image, ou sur une position, quand il entend la cible | joue la suite et enregistre la position de chaque jeton | app |
| `frapper_syllabes` — Frapper les syllabes | touche un tambour une fois par syllabe, en disant le mot | fait entendre le mot, puis compare le nombre de frappes au nombre de syllabes | app |
| `suivre_voix` — Suivre la voix du doigt | suit du doigt une courbe qui monte et descend | joue une intonation et vérifie que le doigt l'a suivie, sans juger la voix | app |
| `designer_image` — Désigner l'image d'un mot | touche l'image du mot entendu parmi deux à quatre images | dit un mot et enregistre l'image touchée | app |
| `trier_images` — Trier des images | glisse des images dans deux colonnes | fait entendre chaque mot et vérifie le rangement | app |
| `ranger_longueur` — Ranger du plus court au plus long | ordonne des images selon le nombre de syllabes | fait entendre les mots, un par un, et vérifie l'ordre | app |
| `remettre_ordre` — Remettre une suite dans l'ordre | replace des images dans l'ordre où elles ont été entendues | énonce une suite, la cache, puis vérifie l'ordre | app |
| `apparier_rime` — Apparier deux images qui riment | touche les deux images dont les mots riment | dit les mots et vérifie la paire | app |
| `trouver_intrus` — Trouver l'intrus à l'initiale | touche l'image dont le mot ne commence pas comme les autres | dit les mots et vérifie l'intrus | app |
| `position_son` — Situer un son dans le mot | pose un jeton au début ou à la fin du mot | dit le mot et vérifie la position | app |
| `toucher_lettre` — Toucher une lettre | touche la lettre qui fait le son entendu, ou dont le nom a été dit | produit le son ou le nom, et vérifie la lettre touchée | app |
| `apparier_graphies` — Apparier les écritures d'une même lettre | assemble la capitale, la scripte et la cursive d'une même lettre | vérifie l'assemblage, sans nommer la lettre | app |
| `toucher_lettres_ordre` — Toucher les lettres dans l'ordre | touche les lettres d'un mot dans l'ordre où elles ont été dites | dit les noms de lettres un par un et vérifie l'ordre des appuis | app |
| `deplacer_lettres` — Déplacer des lettres | place des lettres pour composer un mot entendu | dit le mot, puis vérifie la composition | app |
| `composer_syllabes` — Composer un mot avec des cartes-syllabes | glisse des cartes-syllabes dans l'ordre entendu | dit le mot — ou le mot transformé — puis vérifie l'ordre des cartes | app |
| `repeter_modele` — Répéter après le modèle | répète ce que la voix vient de dire | donne le modèle, et s'arrête là | hors app |
| `jeu_syllabes` — Le mot à trous | choisit la carte-syllabe manquante et la pose dans le mot | fait entendre le mot reconstitué ; c'est le retour, et il ne dépend pas d'un score | app |

### Les cinquante exercices

| Item | Unité | Mécanique | Titre | Ce que la voix dit | Ce que l'enfant fait | Verdict | Durée |
|---|---|---|---|---|---|---|---|
| `E01` | 1 | `localiser_son` | D'où vient le son ? | « Touche l'endroit d'où vient le son. » | toucher le coin de l'écran d'où le son est venu | app | 45 s |
| `E02` | 2 | `lever_main` | Le son qui revient | « Lève la main quand tu entends le son. » | toucher le bouton à chaque retour du son cible | app | 45 s |
| `E03` | 3 | `apparier_sons` | Les deux boîtes jumelles | « Trouve les deux boîtes qui font le même son. » | toucher deux boîtes qui font le même son | app | 45 s |
| `E04` | 4 | `poser_jeton` | Pose le jeton quand tu entends | « Pose un jeton sur l'image quand tu entends le son. » | poser un jeton sur l'image du mot quand la cible est entendue | app | 45 s |
| `E05` | 5 | `repeter_modele` | Répète le son | « Répète après moi. » | aucun geste de réponse : l'enfant répète | hors app | 30 s |
| `E06` | 6 | `suivre_voix` | La sirène | « Suis la voix avec ton doigt. » | suivre du doigt une courbe qui monte et descend | app | 45 s |
| `E07` | 7 | `designer_image` | Le mot que tu entends | « Montre l'image du mot que tu entends. » | toucher l'image du mot entendu parmi deux | app | 45 s |
| `E08` | 8 | `frapper_syllabes` | Une tape par syllabe | « Frappe dans tes mains en disant le mot. » | toucher le tambour une fois par syllabe, en disant le mot | app | 45 s |
| `E09` | 9 | `frapper_syllabes` | Une tape par syllabe, mots longs | « Frappe dans tes mains en disant le mot. » | toucher le tambour une fois par syllabe | app | 45 s |
| `E10` | 10 | `frapper_syllabes` | Scander le mot entendu | « Frappe dans tes mains en disant le mot. » | toucher le tambour une fois par syllabe, sans voir l'image | app | 45 s |
| `E11` | 11 | `poser_jeton` | Combien de syllabes ? | « Pose un jeton pour chaque syllabe. » | poser un jeton par syllabe, puis valider | app | 60 s |
| `E12` | 12 | `ranger_longueur` | Du plus court au plus long | « Range les images du mot le plus court au mot le plus long. » | ordonner des images selon le nombre de syllabes | app | 60 s |
| `E13` | 13 | `lever_main` | La syllabe qui revient | « Lève la main quand tu entends le son. » | toucher le bouton à chaque retour de la syllabe cible | app | 45 s |
| `E14` | 14 | `composer_syllabes` | Le mot à l'envers | « Pose les syllabes dans l'ordre que tu entends. » | glisser les cartes-syllabes dans l'ordre entendu | app | 60 s |
| `E15` | 15 | `repeter_modele` | La comptine | — | aucun geste de réponse : la comptine se dit à plusieurs | hors app | 0 s |
| `E16` | 16 | `trier_images` | Les nasales | « Mets ensemble les images où tu entends le même son. » | glisser chaque image dans la colonne de la nasale entendue | app | 60 s |
| `E17` | 17 | `repeter_modele` | Les couples de consonnes | « Répète après moi. » | aucun geste de réponse : l'enfant répète la paire | hors app | 30 s |
| `E18` | 18 | `designer_image` | Le mot entendu, paires distinctives | « Montre l'image du mot que tu entends. » | toucher l'image du mot entendu parmi deux | app | 45 s |
| `E19` | 19 | `repeter_modele` | Les couples f/v, s/z, p/b, t/d, k/g | « Répète après moi. » | aucun geste de réponse : l'enfant répète la paire | hors app | 30 s |
| `E20` | 20 | `designer_image` | Paires distinctives, deuxième série | « Montre l'image du mot que tu entends. » | toucher l'image du mot entendu parmi deux | app | 60 s |
| `E21` | 21 | — | L'étiquette du prénom | — | aucun | hors app | 0 s |
| `E22` | 22 | `toucher_lettre` | La première lettre | « Touche la lettre dont j'ai dit le nom. » | toucher la lettre dont le nom vient d'être dit | app | 60 s |
| `E23` | 23 | `toucher_lettre` | Les lettres d'un mot connu | « Touche la lettre dont j'ai dit le nom. » | toucher la lettre dont le nom vient d'être dit, dans un mot affiché | app | 60 s |
| `E24` | 24 | `apparier_graphies` | La même lettre, deux écritures | « Assemble les trois écritures de la même lettre. » | assemble la capitale et la scripte minuscule d'une même lettre | app | 60 s |
| `E25` | 25 | `toucher_lettres_ordre` | Épeler un mot connu | « Touche les lettres dans l'ordre que tu entends. » | toucher les lettres dans l'ordre où elles sont dites | app | 60 s |
| `E26` | 26 | `deplacer_lettres` | Composer le mot | « Déplace les lettres dans l'ordre. » | déplacer les lettres pour composer le mot entendu | app | 60 s |
| `E27` | 27 | `toucher_lettre` | La lettre qui fait le son | « Touche la lettre qui fait ce son. » | toucher la lettre qui fait le son entendu | app | 45 s |
| `E28` | 28 | `remettre_ordre` | La suite dans l'ordre | « Remets les images dans l'ordre que tu as entendu. » | remettre trois images dans l'ordre entendu | app | 45 s |
| `E29` | 29 | `trier_images` | Les nasales, deuxième série | « Mets ensemble les images où tu entends le même son. » | glisser chaque image dans la colonne du son entendu | app | 60 s |
| `E30` | 30 | `designer_image` | Les mots qui se ressemblent | « Montre l'image du mot que tu entends. » | toucher l'image du mot entendu parmi quatre | app | 60 s |
| `E31` | 31 | `remettre_ordre` | Trois, quatre, cinq sons | « Remets les images dans l'ordre que tu as entendu. » | remettre les images dans l'ordre entendu | app | 60 s |
| `E32` | 32 | `composer_syllabes` | Le mot-valise | « Pose les syllabes dans l'ordre que tu entends. » | poser les deux cartes-syllabes dans l'ordre entendu | app | 60 s |
| `E33` | 33 | `composer_syllabes` | Supprimer, inverser, remplacer | « Pose les syllabes dans l'ordre que tu entends. » | poser les cartes-syllabes dans l'ordre entendu | app | 60 s |
| `E34` | 34 | `apparier_rime` | Les deux qui riment | « Montre les deux images qui riment. » | toucher les deux images dont les mots riment | app | 60 s |
| `E35` | 35 | `lever_main` | Le son /f/ | « Lève la main quand tu entends le son. » | toucher le bouton quand /f/ est entendu | app | 60 s |
| `E36` | 36 | `trouver_intrus` | L'intrus à l'initiale | « Quel mot ne commence pas comme les autres ? » | toucher l'image dont le mot ne commence pas comme les autres | app | 60 s |
| `E37` | 37 | `position_son` | Au début ou à la fin | « Où entends-tu le son : au début ou à la fin du mot ? » | poser le jeton au début ou à la fin du mot affiché | app | 60 s |
| `E38` | 38 | `repeter_modele` | Les couples ch/s, ch/j, ch/z | « Répète après moi. » | aucun geste de réponse : l'enfant répète la paire | hors app | 30 s |
| `E39` | 39 | `repeter_modele` | Les doubles consonnes | « Répète après moi. » | aucun geste de réponse : l'enfant répète après le modèle | hors app | 30 s |
| `E40` | 40 | `toucher_lettre` | Toutes les lettres d'un mot, trois écritures | « Touche la lettre dont j'ai dit le nom. » | toucher la lettre dont le nom est dit, dans la graphie demandée | app | 60 s |
| `E41` | 41 | `apparier_graphies` | Les trois écritures | « Assemble les trois écritures de la même lettre. » | assembler capitale, scripte et cursive d'une même lettre | app | 60 s |
| `E42` | 42 | `toucher_lettre` | Les vingt-six lettres | « Touche la lettre dont j'ai dit le nom. » | toucher la lettre dont le nom vient d'être dit | app | 90 s |
| `E43` | 43 | `toucher_lettres_ordre` | Épeler pour faire écrire | « Touche les lettres dans l'ordre que tu entends. » | toucher les lettres dans l'ordre dit | app | 60 s |
| `E44` | 44 | `toucher_lettre` | Prolonger le son, trouver la lettre | « Touche la lettre qui fait ce son. » | toucher la lettre qui fait le son prolongé entendu | app | 60 s |
| `E45` | 45 | `toucher_lettre` | La valeur sonore des lettres | « Touche la lettre qui fait ce son. » | toucher la lettre qui fait le son entendu | app | 90 s |
| `E46` | 11 | `jeu_syllabes` | Le mot à trous, mots courts | « Choisis la carte qui manque et pose-la dans le mot. » | glisser la carte-syllabe manquante dans le trou | app | 90 s |
| `E47` | 13 | `jeu_syllabes` | Le mot à trous, discrimination de la syllabe | « Choisis la carte qui manque et pose-la dans le mot. » | glisser la carte-syllabe manquante dans le trou | app | 120 s |
| `E48` | 14 | `jeu_syllabes` | Le mot à trous, manipuler une syllabe | « Choisis la carte qui manque et pose-la dans le mot. » | glisser la carte-syllabe manquante dans le trou | app | 120 s |
| `E49` | 30 | `jeu_syllabes` | Le mot à trous, voisines consonantiques | « Choisis la carte qui manque et pose-la dans le mot. » | glisser la carte-syllabe manquante dans le trou | app | 120 s |
| `E50` | 33 | `jeu_syllabes` | Le mot à trous, syllabe médiane et finale | « Choisis la carte qui manque et pose-la dans le mot. » | glisser la carte-syllabe manquante dans le trou | app | 120 s |

### Le contenu et le matériel

| Item | Contenu de la série | Mots employés | Dont affichés en image | Phonèmes | Lettres |
|---|---|---|---|---|---|
| `E01` | /a/ depuis le coin haut-gauche ; /ʃ/ depuis le coin bas-droit ; /m/ depuis le coin haut-droit ; /f/ depuis le coin bas-gauche | — | — | `/a/`, `/ʃ/`, `/m/`, `/f/` | — |
| `E02` | suite de sept phonèmes où /a/ revient trois fois ; puis une suite où /ʃ/ revient trois fois | — | — | `/a/`, `/ʃ/`, `/i/`, `/m/` | — |
| `E03` | six boîtes : /m/, /f/, /ʃ/ joués deux fois chacun, dans un ordre tiré | — | — | `/m/`, `/f/`, `/ʃ/` | — |
| `E04` | trois images : chat, rat, sac ; la voix dit les mots un par un, /a/ en cible | `chat`, `rat`, `sac` | `chat`, `rat`, `sac` | `/a/` | — |
| `E05` | /m/, /f/, /ʃ/, /l/, /ʁ/, /s/ | — | — | `/m/`, `/f/`, `/ʃ/`, `/l/`, `/ʁ/`, `/s/` | — |
| `E06` | sirène montante sur /a/ ; sirène descendante sur /a/ ; sirène montante puis descendante sur /ɔ/ | — | — | `/a/`, `/ɔ/` | — |
| `E07` | chat / rat ; rat / chat, dans l'ordre inverse | `chat`, `rat` | `chat`, `rat` | `/ʃ/`, `/ʁ/` | — |
| `E08` | papa (2) ; dodo (2) ; café (2) ; moto (2) ; loup (1) ; chat (1) | `papa`, `dodo`, `café`, `moto`, `loup`, `chat` | `papa`, `dodo`, `café`, `moto`, `loup`, `chat` | — | — |
| `E09` | banane (3) ; tomate (3) ; ananas (3) ; valise (3) ; chocolat (3) ; crocodile (4) | `banane`, `tomate`, `ananas`, `valise`, `chocolat`, `crocodile` | `banane`, `tomate`, `ananas`, `valise`, `chocolat`, `crocodile` | — | — |
| `E10` | six mots tirés du corpus, entendus scandés puis entiers | `banane`, `tomate`, `maison`, `bateau`, `éléphant`, `parapluie` | — | — | — |
| `E11` | loup (1) ; papa (2) ; banane (3) ; crocodile (4) ; tomate (3) ; chocolat (3) | `loup`, `papa`, `banane`, `crocodile`, `tomate`, `chocolat` | `loup`, `papa`, `banane`, `crocodile`, `tomate`, `chocolat` | — | — |
| `E12` | loup (1) ; papa (2) ; banane (3) ; crocodile (4) | `loup`, `papa`, `banane`, `crocodile` | `loup`, `papa`, `banane`, `crocodile` | — | — |
| `E13` | MA, FA, PA, MA, SA, MA ; puis BA, DA, BA, LA, BA | — | — | — | — |
| `E14` | va-lise entendu li-va ; pa-pa entendu pa-pa ; ba-na-ne entendu ne-ba-na | `valise`, `papa`, `banane` | `valise`, `papa`, `banane` | — | — |
| `E15` | — | — | — | — | — |
| `E16` | colonne /ɔ̃/ : mouton, bonbon, maison, avion ; colonne /ɑ̃/ : canard, ananas, éléphant, banane | `mouton`, `bonbon`, `maison`, `avion`, `canard`, `ananas`, `éléphant`, `banane` | `mouton`, `bonbon`, `maison`, `avion`, `canard`, `ananas`, `éléphant`, `banane` | `/ɔ̃/`, `/ɑ̃/` | — |
| `E17` | t / k ; f / s ; m / n | — | — | `/t/`, `/k/`, `/f/`, `/s/`, `/m/`, `/n/` | — |
| `E18` | chat / rat ; rat / chat, dans l'ordre inverse | `chat`, `rat` | `chat`, `rat` | `/ʃ/`, `/ʁ/` | — |
| `E19` | f / v ; s / z ; p / b ; t / d ; k / g | — | — | `/f/`, `/v/`, `/s/`, `/z/`, `/p/`, `/b/`, `/t/`, `/d/`, `/k/`, `/g/` | — |
| `E20` | chat / rat ; cerise / valise | `chat`, `rat`, `cerise`, `valise` | `chat`, `rat`, `cerise`, `valise` | `/ʃ/`, `/ʁ/`, `/s/`, `/v/`, `/l/` | — |
| `E21` | — | — | — | — | — |
| `E22` | les lettres de papa : p, a ; les lettres de loup : l, o, u, p ; les lettres de chat : c, h, a, t | `papa`, `loup`, `chat` | `papa`, `loup`, `chat` | — | `p`, `a`, `l`, `o`, `u`, `c`, `h`, `t` |
| `E23` | loup ; chat ; rat ; sac ; lit ; nez ; main ; fleur | `loup`, `chat`, `rat`, `sac`, `lit`, `nez`, `main`, `fleur` | `loup`, `chat`, `rat`, `sac`, `lit`, `nez`, `main`, `fleur` | — | `l`, `o`, `u`, `p`, `c`, `h`, `a`, `t`, `r`, `s`, `i`, `n`, `e`, `z`, `m`, `f` |
| `E24` | a, m, l, t, s, o | — | — | — | `a`, `m`, `l`, `t`, `s`, `o` |
| `E25` | loup ; chat ; rat ; sac ; lit ; nez ; main ; fleur | `loup`, `chat`, `rat`, `sac`, `lit`, `nez`, `main`, `fleur` | `loup`, `chat`, `rat`, `sac`, `lit`, `nez`, `main`, `fleur` | — | `l`, `o`, `u`, `p`, `c`, `h`, `a`, `t`, `r`, `s`, `i`, `n`, `e`, `z`, `m`, `f` |
| `E26` | loup ; chat ; rat ; sac ; lit ; nez ; main | `loup`, `chat`, `rat`, `sac`, `lit`, `nez`, `main` | — | — | `l`, `o`, `u`, `p`, `c`, `h`, `a`, `t`, `r`, `s`, `i`, `n`, `e`, `z`, `m` |
| `E27` | a, i, o, u, e, é | — | — | `/a/`, `/i/`, `/o/`, `/y/`, `/ə/`, `/e/` | `a`, `i`, `o`, `u`, `e`, `é` |
| `E28` | loup, chat, rat ; rat, loup, chat ; chat, rat, loup | `loup`, `chat`, `rat` | `loup`, `chat`, `rat` | — | — |
| `E29` | colonne /ɔ̃/ : bonbon, mouton ; colonne /ɛ̃/ : lapin, main | `bonbon`, `mouton`, `lapin`, `main` | `bonbon`, `mouton`, `lapin`, `main` | `/ɔ̃/`, `/ɛ̃/` | — |
| `E30` | chat, rat, sac, loup — la voix dit l'un des quatre | `chat`, `rat`, `sac`, `loup` | `chat`, `rat`, `sac`, `loup` | `/ʃ/`, `/ʁ/`, `/s/`, `/l/` | — |
| `E31` | suites de trois, puis quatre, puis cinq images tirées du corpus illustré | `loup`, `chat`, `rat`, `sac`, `lit`, `nez` | `loup`, `chat`, `rat`, `sac`, `lit`, `nez` | — | — |
| `E32` | mou-ton + cha-peau → mou-cha ; ba-na-ne + ton → ba-ton | `mouton`, `chocolat`, `banane` | `mouton`, `chocolat`, `banane` | — | — |
| `E33` | valise → lise ; banane → nane ; tomate → mate ; papa → pa | `valise`, `banane`, `tomate`, `papa` | `valise`, `banane`, `tomate`, `papa` | — | — |
| `E34` | bateau / gâteau ; maison / mouton ; cerise / valise | `bateau`, `gâteau`, `maison`, `mouton`, `cerise`, `valise` | `bateau`, `gâteau`, `maison`, `mouton`, `cerise`, `valise` | — | — |
| `E35` | fleur, café, téléphone, éléphant, girafe ; puis les mêmes avec /v/ en cible | `fleur`, `café`, `téléphone`, `éléphant`, `girafe` | — | `/f/`, `/v/` | — |
| `E36` | sac, soleil, cerise — intrus : chat ; loup, lit, lune — intrus : rat | `sac`, `soleil`, `cerise`, `chat`, `loup`, `lit`, `lune`, `rat` | `sac`, `soleil`, `cerise`, `chat`, `loup`, `lit`, `lune`, `rat` | `/s/`, `/ʃ/`, `/l/`, `/ʁ/` | — |
| `E37` | /l/ au début : loup, lune, lapin, lit ; /l/ à la fin : cheval, soleil | `loup`, `lune`, `lapin`, `lit`, `cheval`, `soleil` | `loup`, `lune`, `lapin`, `lit`, `cheval`, `soleil` | `/l/` | — |
| `E38` | ch / s ; ch / j ; ch / z | — | — | `/ʃ/`, `/s/`, `/ʒ/`, `/z/` | — |
| `E39` | br de zèbre ; cr de crocodile ; bl de cartable ; pl de parapluie | `zèbre`, `crocodile`, `cartable`, `parapluie` | — | — | — |
| `E40` | loup en capitale, en scripte, en cursive ; fleur en capitale, en scripte, en cursive | `loup`, `fleur` | `loup`, `fleur` | — | `l`, `o`, `u`, `p`, `f`, `e`, `r` |
| `E41` | a, m, l, t, s, o, e, r | — | — | — | `a`, `m`, `l`, `t`, `s`, `o`, `e`, `r` |
| `E42` | les vingt-six lettres, par séries de six | — | — | — | `a`, `b`, `c`, `d`, `e`, `f`, `g`, `h`, `i`, `j`, `k`, `l`, `m`, `n`, `o`, `p`, `q`, `r`, `s`, `t`, `u`, `v`, `w`, `x`, `y`, `z` |
| `E43` | les mots d'une syllabe du corpus ; puis deux mots de deux syllabes | `loup`, `chat`, `rat`, `sac`, `lit`, `nez`, `main`, `fleur`, `papa`, `maman` | `loup`, `chat`, `rat`, `sac`, `lit`, `nez`, `main`, `fleur`, `papa`, `maman` | — | `l`, `o`, `u`, `p`, `c`, `h`, `a`, `t`, `r`, `s`, `i`, `n`, `e`, `z`, `m`, `f` |
| `E44` | voyelles : a, i, o, u, e, é ; fricatives : s, r, f, v, j, ch ; liquide : l | — | — | `/a/`, `/i/`, `/o/`, `/y/`, `/ə/`, `/e/`, `/s/`, `/ʁ/`, `/f/`, `/v/`, `/ʒ/`, `/ʃ/`, `/l/` | `a`, `i`, `o`, `u`, `e`, `é`, `s`, `r`, `f`, `v`, `j`, `l` |
| `E45` | toutes les lettres, hormis les six occlusives ; puis les lettres de la série `ch`, `ou`, `on`, `an` | — | — | `/a/`, `/i/`, `/o/`, `/y/`, `/ə/`, `/e/`, `/ɛ/`, `/ø/`, `/œ/`, `/f/`, `/v/`, `/s/`, `/z/`, `/ʃ/`, `/ʒ/`, `/m/`, `/n/`, `/ɲ/`, `/l/`, `/ʁ/` | `a`, `i`, `o`, `u`, `e`, `é`, `è`, `f`, `v`, `s`, `z`, `m`, `n`, `l`, `r`, `j`, `c`, `g` |
| `E46` | les quinze items oraux du jeu dont le mot compte une ou deux syllabes ; le nombre de cases est le nombre de syllabes, et c'est ce nombre que l'exercice fait compter | `avion`, `bonbon`, `café`, `canard`, `cheval`, `gâteau`, `jupe`, `lapin`, `maison`, `mouton`, `papa`, `pomme`, `soleil`, `vélo`, `zèbre` | `avion`, `bonbon`, `café`, `canard`, `cheval`, `gâteau`, `jupe`, `lapin`, `maison`, `mouton`, `papa`, `pomme`, `soleil`, `vélo`, `zèbre` | — | — |
| `E47` | les trente items oraux du jeu, dont les deux intruses sont des syllabes voisines de la syllabe cachée | `banane`, `tomate`, `papa`, `vélo`, `café`, `gâteau`, `jupe`, `pomme`, `zèbre`, `lapin`, `maison`, `canard`, `mouton`, `cheval`, `bonbon`, `avion`, `soleil`, `valise`, `cerise`, `girafe`, `koala`, `pyjama`, `cartable`, `chocolat`, `éléphant`, `parapluie`, `crocodile`, `téléphone`, `école`, `ananas` | `banane`, `tomate`, `papa`, `vélo`, `café`, `gâteau`, `jupe`, `pomme`, `zèbre`, `lapin`, `maison`, `canard`, `mouton`, `cheval`, `bonbon`, `avion`, `soleil`, `valise`, `cerise`, `girafe`, `koala`, `pyjama`, `cartable`, `chocolat`, `éléphant`, `parapluie`, `crocodile`, `téléphone`, `école`, `ananas` | — | — |
| `E48` | les items du jeu dont le mot compte trois syllabes et plus : le trou y porte sur une syllabe qu'il faut retrouver, donc ajouter au mot amputé | `banane`, `tomate`, `ananas`, `cerise`, `girafe`, `koala`, `pyjama`, `valise`, `école`, `cartable`, `chocolat`, `éléphant`, `parapluie`, `crocodile`, `téléphone` | `banane`, `tomate`, `ananas`, `cerise`, `girafe`, `koala`, `pyjama`, `valise`, `école`, `cartable`, `chocolat`, `éléphant`, `parapluie`, `crocodile`, `téléphone` | — | — |
| `E49` | les items dont les deux intruses sont consonantiques — elles ne diffèrent de la syllabe cachée que par la consonne d'attaque | `banane`, `mouton`, `lapin`, `bonbon`, `maison`, `canard`, `cheval`, `avion`, `valise`, `girafe`, `cartable`, `chocolat`, `téléphone`, `ananas` | `banane`, `mouton`, `lapin`, `bonbon`, `maison`, `canard`, `cheval`, `avion`, `valise`, `girafe`, `cartable`, `chocolat`, `téléphone`, `ananas` | — | — |
| `E50` | les items du jeu dont le trou porte sur une syllabe médiane ou finale — la position où la manipulation se voit | `banane`, `tomate`, `ananas`, `cerise`, `girafe`, `valise`, `cartable`, `crocodile`, `téléphone`, `parapluie` | `banane`, `tomate`, `ananas`, `cerise`, `girafe`, `valise`, `cartable`, `crocodile`, `téléphone`, `parapluie` | — | — |

### Ce que chaque exercice entraîne, et ce qu'il ne vérifie pas

| Item | Entraîne | Ne vérifie pas |
|---|---|---|
| `E01` | localiser un son dans l'espace, et tenir son attention sur une source | la reconnaissance du phonème lui-même — l'exercice ne demande que de savoir d'où vient le son |
| `E02` | reconnaître un phonème connu dans une suite, et attendre | la discrimination entre deux phonèmes proches — c'est l'objet de E03 et de E16 |
| `E03` | comparer deux sons et les garder en mémoire le temps de la comparaison | ce que l'enfant se dit pour les distinguer |
| `E04` | repérer une occurrence dans une suite, sur un support montré | la position du son dans le mot — poser un jeton dit « je l'ai entendu », pas « je sais où » |
| `E05` | produire le son après un modèle | tout. Cette unité est une étape de production : l'application donne le modèle et passe. |
| `E06` | suivre une intonation, et faire le lien entre la voix et un tracé | la justesse de la voix de l'enfant : le doigt est jugé, pas la gorge |
| `E07` | percevoir qu'un seul son sépare deux mots | le nombre de paires disponibles : voir `besoins`, l'unité n'en a qu'une illustrée |
| `E08` | découper un mot en syllabes, avec un geste qui compte | la prononciation du mot pendant la frappe |
| `E09` | tenir le découpage sur des mots de trois et quatre syllabes | l'endroit exact où l'enfant place la coupe — une coupe orale n'est pas une coupe écrite |
| `E10` | découper à l'oreille seule, sans support | ce que l'enfant fait des mots de plus de quatre syllabes : le corpus n'en contient pas |
| `E11` | dénombrer les syllabes d'un mot familier, sans support écrit | la correspondance entre le jeton et la syllabe : l'exercice compte, il ne nomme pas |
| `E12` | comparer des mots selon leur longueur orale | que l'enfant distingue longueur orale et longueur écrite — l'exercice ne montre aucun mot écrit, c'est délibéré |
| `E13` | isoler une syllabe et l'attendre dans une suite | l'écriture de la syllabe — à la GS la syllabe s'entend, elle ne se lit pas |
| `E14` | manipuler l'ordre des syllabes d'un mot | que l'enfant entende que le résultat n'est plus un mot |
| `E15` | rien dans l'application | tout. Cette unité est déclarée hors app, et elle est comptée comme telle. |
| `E16` | distinguer deux nasales proches | la prononciation des nasales, qui est un objectif de production déclaré hors app |
| `E17` | articuler | tout. |
| `E18` | discriminer deux mots qui ne diffèrent que par un son | les paires du programme : voir `besoins` |
| `E19` | articuler un couple de consonnes proches | tout. |
| `E20` | discriminer des mots proches sur deux positions | les paires ville/fil, dessert/désert, poison/poisson, pépé/bébé, doigt/toit, gare/car, boule/poule : voir `besoins` |
| `E21` | rien dans l'application | tout. |
| `E22` | reconnaître une lettre à son nom | la capacité à nommer la lettre soi-même, qui est l'objectif de production de l'unité |
| `E23` | repérer une lettre dans un mot écrit | la nomination |
| `E24` | reconnaître une lettre sous deux écritures | l'écriture de la lettre — l'exercice fait reconnaître, pas tracer |
| `E25` | tenir l'ordre des lettres d'un mot connu | la diction des noms de lettres |
| `E26` | composer un mot connu lettre après lettre | que le mot composé soit lu : à la GS, il est reconnu comme une suite de lettres, pas déchiffré |
| `E27` | faire le lien entre un son et la lettre qui l'écrit | le cas de `e`, dont la valeur dépend de la position : l'exercice ne le présente qu'en position stable |
| `E28` | garder en mémoire une suite de sons et la restituer | la mémoire à long terme : la suite est courte, et l'exercice mesure la mémoire de travail, pas l'apprentissage |
| `E29` | distinguer /ɔ̃/ et /ɛ̃/ | le troisième terme du programme, /œ̃/, qui n'a aucun mot porteur illustré : voir `besoins` |
| `E30` | discriminer dans un choix de quatre, et non de deux | la série du programme — poule, boule, roule, moule, coule, foule — dont aucun mot n'est illustré : voir `besoins` |
| `E31` | augmenter la mémoire auditive en allongeant la suite | la concentration, qui n'est pas mesurable par la réussite d'un exercice |
| `E32` | fusionner l'attaque d'un mot et la fin d'un autre | la diction du pseudo-mot |
| `E33` | manipuler les syllabes d'un mot — supprimer, inverser | que le résultat entendu soit reconnu comme un mot ou non |
| `E34` | entendre une rime et apparier deux mots qui la partagent | la production d'une rime — l'unité la demande, et l'application ne peut pas l'entendre |
| `E35` | trouver un phonème cible dans une liste de mots | la position du /f/ dans le mot — l'unité ne demande que de l'entendre |
| `E36` | isoler l'attaque d'un mot et repérer celle qui diffère | la raison du choix : l'enfant peut tomber juste par élimination sur une autre propriété |
| `E37` | localiser un phonème dans un mot, au début ou à la fin | la position médiane, qui n'est pas demandée à la GS |
| `E38` | articuler les couples proches de la GS | tout. |
| `E39` | articuler une double consonne | tout. |
| `E40` | reconnaître toutes les lettres d'un mot dans les trois graphies | la nomination — c'est la première réussite du palier de sortie, et elle est vérifiée dans l'app par reconnaissance, pas par diction |
| `E41` | apparier les trois graphies d'une même lettre | le tracé de la cursive |
| `E42` | connaître le nom des vingt-six lettres | la récitation de l'alphabet dans l'ordre, qui n'est demandée par aucun attendu |
| `E43` | épeler un mot connu afin qu'un tiers puisse l'écrire | la diction des lettres |
| `E44` | faire le lien entre un phonème qu'on peut tenir et la lettre qui l'écrit | les occlusives, qui ne se prolongent pas et que le programme exclut explicitement |
| `E45` | connaître la valeur sonore des lettres | les six occlusives, exclues par le programme lui-même — et c'est la troisième réussite vérifiée dans l'app, annoncée au palier de sortie |
| `E46` | compter les syllabes d'un mot court, sur un support qui en montre le nombre | la diction du mot reconstitué — l'application le fait entendre et l'enfant juge |
| `E47` | discriminer une syllabe parmi ses voisines — c'est la mécanique même du jeu | la prononciation de la paire : le jeu entraîne la discrimination, pas la production |
| `E48` | restituer une syllabe manquante — ajouter, au sens du programme | les autres manipulations de l'unité — supprimer, permuter, inverser — que le jeu ne demande pas. E33 les couvre. |
| `E49` | discriminer deux syllabes qui ne diffèrent que par leur consonne d'attaque | la discrimination entre mots entiers — c'est E30, sur les images |
| `E50` | repérer où manque la syllabe, et la remettre à sa place | l'inversion et la substitution, que E33 entraîne sur des cartes |

### Les 20 inversions — ce que le geste reprend

| Item | Unité | Objectif de l'unité | Ce que le geste reprend |
|---|---|---|---|
| `E03` | 3 | Comparer, apparier et reproduire des sons | le programme demande aussi de REPRODUIRE les sons. L'appariement n'en garde que la comparaison : deux boîtes qui font le même son se reconnaissent sans être imitées. Reproduire se vérifie à l'oreille d'un adulte, et c'est l'objet de l'unité 5, déclarée hors app. |
| `E06` | 6 | Reproduire des intonations | le programme demande de REPRODUIRE l'intonation. Le doigt suit le contour sur une courbe : c'est la perception du contour qui est vérifiée, jamais la gorge. Reproduire une voix qui monte et descend se vérifie à l'oreille d'un adulte. |
| `E08` | 8 | Prononcer son prénom, puis une comptine, en scandant les syllabes | le programme demande de scander SON PRÉNOM. L'application ne connaît aucun prénom et n'en demandera jamais : l'exercice tourne sur les mots du corpus, qui sont connus de l'enfant à l'oral. |
| `E14` | 14 | Ajouter, supprimer, permuter, répéter, fusionner, substituer les syllabes d'un mot dit à l'oral | le programme demande de DIRE le mot transformé. Le geste le remplace : l'enfant pose les syllabes dans l'ordre qu'il a entendu, et l'application vérifie l'ordre. C'est la permutation qui est vérifiée, pas la diction. |
| `E16` | 16 | Distinguer et produire correctement les nasales | le programme demande de PRODUIRE les nasales. Le tri n'en garde que la distinction : ranger mouton avec bonbon se fait sans prononcer. Produire correctement se vérifie à l'oreille d'un adulte. |
| `E18` | 18 | Prononcer correctement des paires distinctives | le programme demande de PRONONCER les paires distinctives. Toucher l'image du mot entendu vérifie qu'elles sont DISTINGUÉES à l'écoute, et non qu'elles sont dites distinctement. La diction reste un objectif, et il est hors app. |
| `E20` | 20 | Prononcer correctement des paires distinctives et des mots à phonèmes proches | même inversion que E18, sur une deuxième série. La discrimination est vérifiée par le geste ; la prononciation des paires reste un objectif hors app. |
| `E22` | 22 | Reconnaître et nommer certaines lettres de son prénom écrit en capitales | le programme demande de NOMMER la lettre désignée. Le geste inverse la charge : la voix dit le nom, l'enfant touche la lettre. Nommer reste un objectif, mais il est déclaré hors app. |
| `E23` | 23 | Nommer les lettres de son prénom et quelques lettres de mots connus | même inversion que E22 : la voix nomme, l'enfant touche. Le programme demande de nommer quelques lettres de mots connus ; l'application vérifie la reconnaissance. |
| `E25` | 25 | Épeler son prénom ou un mot connu afin qu'un tiers puisse le composer | le programme demande de DIRE les lettres dans l'ordre afin qu'un tiers puisse composer le mot. Le geste fait composer directement : l'enfant touche les lettres dans l'ordre entendu, et l'application vérifie la suite. |
| `E27` | 27 | Utiliser le nom de quelques lettres connues pour représenter les sons entendus | le programme demande d'UTILISER le nom des lettres — donc de le dire. La charge est inversée : l'application fait entendre le son, l'enfant touche la lettre qui l'écrit. Dire le nom reste un objectif, vérifié ailleurs par reconnaissance (E22, E42). |
| `E32` | 32 | Fusionner les syllabes d'attaque et la syllabe finale de deux mots pour obtenir un pseudo-mot | le programme demande de DIRE le pseudo-mot obtenu. Un pseudo-mot n'a pas d'image : le geste ne peut donc pas être « toucher l'image ». Il est « poser les syllabes dans l'ordre », et c'est l'ordre qui est vérifié. |
| `E33` | 33 | Supprimer, ajouter, remplacer, inverser, substituer, fusionner les syllabes d'un mot | même inversion que E32 : l'application dit le mot transformé, l'enfant compose, l'ordre est vérifié. |
| `E34` | 34 | Repérer et produire des rimes et des assonances | le programme demande de REPÉRER et de PRODUIRE une rime. L'appariement entraîne le repérage ; produire une rime se vérifie à l'oreille d'un adulte, seul juge de deux mots qui riment. |
| `E40` | 40 | Reconnaître et nommer toutes les lettres d'un mot écrit dans les trois graphies | la voix nomme la lettre et la graphie, l'enfant touche. Nommer soi-même reste hors app. |
| `E42` | 42 | Connaître le nom des lettres de l'alphabet | la voix dit le nom, l'enfant touche la lettre. C'est la deuxième réussite du palier de sortie : « connaître le nom des lettres » se vérifie dans l'app par reconnaissance ; le dire de mémoire est une autre habileté. |
| `E43` | 43 | Épeler les lettres d'un mot connu afin qu'un tiers puisse l'écrire | même inversion que E25, sur un mot plus long. |
| `E44` | 44 | Prolonger les phonèmes pour retrouver les lettres auxquelles ils correspondent | le programme demande de PROLONGER le phonème avec la main pour retrouver la lettre. Le geste est conservé — le doigt suit la ligne — mais la voix est celle de l'application : prolonger soi-même reste un objectif hors app. |
| `E48` | 14 | Ajouter, supprimer, permuter, répéter, fusionner, substituer les syllabes d'un mot dit à l'oral | le programme demande de DIRE le mot manipulé. Le jeu fait poser la syllabe manquante, et c'est l'application qui dit le mot reconstitué : l'enfant juge à l'oreille au lieu de prononcer. |
| `E50` | 33 | Supprimer, ajouter, remplacer, inverser, substituer, fusionner les syllabes d'un mot | le programme demande d'ajouter, de supprimer, de remplacer, d'inverser et de fusionner les syllabes. Le jeu n'en fait qu'une — ajouter — et il la fait sans prononcer : la syllabe se pose, le mot se dit par l'application. Les quatre autres manipulations sont entraînées par E33, sur des cartes. |

### Les 7 exercices hors app

| Item | Unité | Pourquoi l'application ne peut pas juger | Substitution |
|---|---|---|---|
| `E05` | 5 | l'application ne peut pas entendre. Reproduire un son se vérifie à l'oreille d'un adulte, et le palier de sortie le déclare déjà hors app. | le jumeau réceptif est E04 : la voix dit le mot porteur, l'enfant touche son image. Il vérifie la reconnaissance du son, jamais sa production. |
| `E15` | 15 | l'unité demande de dire une comptine avec le groupe. Ni l'apprentissage, ni la récitation ne passent par un écran, et l'application ne peut pas entendre. | aucune. Une comptine n'est pas un exercice individuel : elle s'apprend en groupe, avec un adulte qui la dit et la reprend. L'application n'a rien à y faire, et le dire vaut mieux que d'inventer un équivalent qui n'en serait pas un. |
| `E17` | 17 | articuler distinctement deux consonnes proches se vérifie à l'oreille d'un adulte. C'est la première des trois réussites du palier de sortie déclarées hors app. | le jumeau réceptif est E16 : la voix dit le mot, l'enfant le range par la nasale entendue. Il vérifie la discrimination, pas l'articulation. |
| `E19` | 19 | l'articulation d'un couple de consonnes proches ne s'entend pas par la machine. | le jumeau réceptif est E20 : la voix dit le mot, l'enfant touche son image. La paire entendue est la même ; c'est la réponse qui change de nature. |
| `E21` | 21 | l'unité repose sur le prénom de l'enfant. Aucun prénom n'est demandé, stocké ni transmis, et cette unité ne justifie pas d'ouvrir une collecte. | aucune, et c'est une décision de produit, pas un manque technique : reconnaître son étiquette suppose que l'application connaisse le prénom de l'enfant. Or elle ne collecte rien (§ 7 de la note de cadrage). L'équivalent le plus proche — retrouver un mot connu parmi d'autres par sa première lettre — est l'objet de E22. |
| `E38` | 38 | c'est la deuxième réussite du palier de sortie déclarée hors app — il faut entendre la prononciation. | le jumeau réceptif est E36 : la voix dit trois mots, l'enfant touche l'intrus à l'initiale. C'est la même discrimination, jugée par le geste. |
| `E39` | 39 | c'est la troisième réussite du palier de sortie déclarée hors app. | aucune substitution possible : la difficulté EST dans l'enchaînement de deux consonnes, et aucune image ne l'attrape. L'application donne le modèle, l'enfant répète, un adulte juge. |

### Les besoins déclarés

| Id | Unité | Ce qui manque | Détail | Bloque ? |
|---|---|---|---|---|
| `B07` | 7 | des paires distinctives illustrées | Le programme nomme cour/tour, cube/tube, cassé/café, pouce/pouf, nain/main. Sur les 44 mots illustrés, une seule paire ne diffère que par un son : chat/rat. | non |
| `B13` | 13 | les syllabes isolées, enregistrées | L'unité fait discriminer une syllabe cible dans une suite énoncée. Le corpus contient les mots et leur version scandée, mais aucune syllabe isolée : la famille `syl_` reste à créer, une trentaine de fichiers. | **oui** |
| `B14a` | 14 | les mots transformés, enregistrés | L'unité fait manipuler l'ordre des syllabes. La voix doit pouvoir dire le mot transformé — li-va, ne-ba-na — et le corpus ne contient que les mots du corpus, entiers ou scandés. Même famille que le besoin de l'unité 13 : des formes qui ne sont pas des mots du corpus. | **oui** |
| `B14b` | 14 | les variantes du jeu pour les autres manipulations de l'unité | L'unité demande d'ajouter, de supprimer, de permuter et d'inverser les syllabes. Le jeu ne fait qu'ajouter une syllabe manquante : les quatre autres manipulations n'ont aucun item. E33 les entraîne sur des cartes-syllabes, mais sans le retour sonore qui fait la force du jeu — l'enfant y compose sans entendre le résultat. | non |
| `B20` | 20 | les paires distinctives de la GS, illustrées | ville/fil, dessert/désert, poison/poisson, pépé/bébé, doigt/toit, gare/car, boule/poule. Deux paires seulement sont disponibles dans le corpus illustré. | non |
| `B29` | 29 | un mot porteur de /œ̃/, illustré | Le programme cite on, en, un. `brun` est enregistré comme mot porteur du phonème mais n'a pas d'image : la colonne /œ̃/ ne peut pas exister. | non |
| `B30` | 30 | la série poule / boule / roule / moule / coule / foule | Six mots qui ne diffèrent que par l'attaque. Aucun n'est dans le corpus GS. C'est la série que le programme donne en exemple, et la plus efficace de la tranche : elle mérite six images. | non |

### Les corrections consignées

**1. outils/jeu-syllabes.json — le champ `sert` des trente items oraux**

- *Le défaut.* Les items oraux déclaraient servir les unités 17, 19 et 38, dont les objectifs sont d'ARTICULER des couples de consonnes proches. Or le jeu ne demande jamais de prononcer : il demande de choisir une syllabe parmi des voisines. Le champ avait été rempli en appariant les PAIRES du jeu aux paires citées par ces unités, et non en comparant les objectifs.
- *La correction.* Les trente items oraux servent désormais l'unité 13, dont l'objectif est de discriminer une syllabe cible. Le jeu sert en outre les unités 11, 14, 30 et 33, déclarées sur la mécanique (`mecanique.sert_les_unites`), et les exercices E46 à E50 les couvrent.
- *Pourquoi il était coûteux.* Un item rattaché à une unité qui ne l'entraîne pas ne se voit pas à la lecture : le tableau a l'air rempli. C'est le mode d'échec le plus coûteux d'un inventaire — il fait croire qu'une unité est outillée quand elle ne l'est pas.

**2. outils/exercices-gs.json — la consolidation des besoins déclarés par les exercices**

- *Le défaut.* Les sept besoins déclarés ont été consolidés en dédoublonnant par UNITÉ. Or une unité peut manquer de deux choses différentes : l'unité 14 manque à la fois des mots transformés (E14) et des variantes du jeu (E48). Le besoin de E48 a été absorbé par celui de E14 — six entrées pour sept besoins déclarés, et la liste avait l'air complète.
- *La correction.* Chaque besoin consolidé porte un identifiant, et l'exercice ne porte plus le texte de son besoin mais sa référence (`besoin_id`), comme il porte le slug de sa consigne plutôt que son texte. Deux entrées pour l'unité 14 : B14a et B14b. Le contrôle vérifie l'accord dans les deux sens.
- *Pourquoi il était coûteux.* Un dédoublonnage par unité est un aplatissement : il fait disparaître les besoins multiples d'une même unité, et rien dans la liste ne le signale. Même mode d'échec que le champ `sert` du jeu — une table pleine qui cache un trou.

**3. outils/exercices-gs.json — le champ `substitution`**

- *Le défaut.* Le champ portait deux choses différentes. Sur un exercice hors app, il nommait le jumeau réceptif qui vérifie ce que la machine ne peut pas juger. Sur un exercice jugé par l'app, il expliquait quelle charge le geste reprend quand le programme demande une production. Onze exercices relevaient du second sens, aucun du premier — mais rien dans le nom ne le disait, et un contrôle qui aurait exigé `substitution` sur tout exercice hors app aurait été satisfait par un texte parlant d'autre chose.
- *La correction.* Deux champs. `substitution` ne vaut que pour un exercice hors app : le jumeau réceptif, ou « aucune ». `inversion` dit ce que le geste reprend quand l'unité porte un objectif de production. Les unités de production sont déclarées dans la progression (champ `production`), et le contrôle exige qu'un exercice jugé par l'app couvrant une telle unité déclare son `inversion`.
- *Pourquoi il était coûteux.* Un champ à deux sens ne se voit pas : chaque valeur, lue seule, est plausible. C'est le même piège que le champ `sert`, et il se referme deux fois — une fois sur la donnée, une fois sur le contrôle censé la garder.

**4. outils/exercices-gs.json — le matériel de E46 (« Le mot à trous, mots courts »)**

- *Le défaut.* L'exercice est adossé au jeu de syllabes et annonçait treize mots. Cinq seulement sont l'objet d'un item du jeu ; les huit autres — loup, chat, rat, sac, lit, nez, main, fleur — venaient du corpus GS. La liste avait été remplie en prenant « les mots courts du corpus » au lieu de « les items courts du jeu », et elle avait l'air juste parce que tous ces mots sont effectivement courts.
- *La correction.* Le matériel est celui des items ORAL du jeu dont le mot compte une ou deux syllabes : quinze mots, tous illustrés. Le contrôle vérifie désormais que tout mot d'un exercice adossé au jeu est l'objet d'un item de ce jeu.
- *Pourquoi il était coûteux.* Un matériel plausible n'est pas un matériel disponible. L'exercice aurait demandé à l'application de montrer huit mots qu'elle n'a pas dans cette banque, et le défaut ne se voit qu'en croisant deux fichiers — jamais en relisant celui-ci.

**5. outils/progression-gs.json — le champ `production` des unités 14, 32 et 33**

- *Le défaut.* Ces trois unités avaient été déclarées sans objectif de production, au motif que la manipulation des syllabes est vérifiée par un geste. Le raisonnement s'arrêtait à la vérification : le programme demande aussi de DIRE le mot transformé, et le geste ne le dit pas. Le contrôle l'a signalé par l'autre bout — trois exercices déclaraient une inversion sur une unité censée ne pas en avoir besoin. C'est le texte des exercices qui avait raison.
- *La correction.* Les unités 14, 32 et 33 passent à `production: true`, et les deux exercices adossés au jeu qui les couvrent — E48 et E50 — déclarent leur inversion.
- *Pourquoi il était coûteux.* Un axe rempli au jugement ne se falsifie pas tout seul. Ici il a été pris en défaut par un accord entre deux fichiers, et c'est le seul genre de contrôle qui pouvait le voir : relire la liste des unités de production ne montre rien, puisqu'elle a l'air d'une liste.

### Le décompte

| Point | Nombre |
|---|---|
| Unités de la progression | 45 |
| Unités servies par au moins un exercice | 45 |
| Unités dont l'objectif porte une production | 24 |
| Mécaniques | 20 |
| Mécaniques employées | 20 |
| Exercices | 50 |
| dont jugés par l'application | 43 |
| dont hors app | 7 |
| dont avec une inversion déclarée | 20 |
| Besoins déclarés | 7 |
| dont bloquants | 2 |
| Corrections consignées | 5 |
| Durée cumulée des exercices | 2865 s |

<!-- FIN TABLE GENEREE -->

## 9. Ce que la banque ne dit pas

- **La difficulté relative de deux exercices.** Elle se juge à l'usage, pas dans un tableau.
- **L'ordre dans une séance.** C'est un choix d'écran, et il n'est pas fait.
- **La durée réelle.** `duree_s` est une intention d'auteur, pas une mesure.
- **L'effet sur l'enfant.** Aucun script ne mesure si l'enfant revient demain.

## 10. Comment on vérifie

```bash
python outils/verifier-exercices.py     # unités servies, verdicts, matériel, besoins, inversions
python outils/generer-table.py          # met les tableaux à jour depuis les JSON
```

`verifier-exercices.py` refuse :

- une unité de la progression **sans aucun exercice** — un objectif annoncé et non entraîné ;
- un exercice déclaré `app` dont la **mécanique est hors app** — le verdict promet plus que la mécanique ;
- un exercice hors app **sans `pourquoi_hors_app`** ou sans `substitution` — l'absence de jumeau se déclare, elle ne se tait pas ;
- un exercice `app` couvrant une **unité de production sans `inversion`** ;
- une `inversion` sur une unité qui ne porte **aucune production** ;
- un mot, un phonème ou une lettre **absent du corpus**, une affiche qui n'est **pas un mot illustré** ;
- une consigne qui **nomme la lettre** sur une lettre **sans nom enregistré** — c'est ce qui autorise `é` et `è` dans les exercices de valeur sonore, et l'interdit ailleurs ;
- une consigne qui **fait entendre le son** sans aucun phonème déclaré ;
- un **besoin déclaré sans entrée consolidée**, ou une **entrée sans déclarant** ;
- un exercice adossé au jeu qui sert une unité que **le jeu ne déclare pas servir** ;
- un exercice adossé au jeu qui emploie un mot **qui n'est l'objet d'aucun item** de ce jeu ;
- un **champ inattendu** — c'est ainsi qu'une faute de frappe (`ne_verifies_pas`) se voit au lieu de dormir dans le fichier.
