# Ludo'Lire — Progression de la tranche CE1

**Statut :** proposition, version 0.3.0. La relecture pédagogique est faite par le porteur du projet, en testant l'application.
**Source du cadre :** Annexe 3 — programme de français du cycle 2 (arrêté du 22 octobre 2024, JO du 25 octobre 2024, BO n° 41 du 31 octobre 2024, application rentrée 2025-2026), section « Lecture », sous-section « Cours élémentaire première année ».
**Source de vérité de la table :** `outils/progression-ce1.json`. Le tableau du § 3 en est le rendu, produit par `outils/generer-table.py`. Le contrôle est `outils/verifier-progression.py`.

---

## 0. Ce qui a changé en version 0.2.0

La version 0.1.0 comportait un défaut de jugement, et il faut le consigner parce qu'il est **invisible à la lecture**.

Le champ `production` d'une unité dit si l'objectif du programme nomme un **acte de parole que l'application ne peut pas entendre** — lire à voix haute, résumer, expliciter, donner un titre. C'est l'axe qui commande le verdict des exercices : une unité de production couverte par un exercice jugé par l'application oblige cet exercice à déclarer son `inversion`, c'est-à-dire **ce que le geste reprend à la place de la production**.

Trois unités portaient un acte de parole et `production: false` :

| Unité | Objectif | Ce que le programme demande | Ce que l'application fait |
|---|---|---|---|
| 6 | Donner un titre au texte | « Il est capable de donner un titre au texte » | choisir le titre parmi trois |
| 7 | Justifier une réponse par un retour au texte | « Justifier ses réponses par un retour au texte » | toucher la phrase qui prouve la réponse |
| 25 | Caractériser les personnages | « Il est capable de caractériser les personnages » | apparier un personnage à ses traits |

Ce sont exactement les trois unités dont l'exercice devra déclarer une inversion, et le drapeau disait le contraire. La table passe de 7 à **10 unités de production**.

**Pourquoi ce défaut ne se voyait pas.** Une colonne de booléens reste pleine quand elle est fausse. Rien, dans le document, ne mettait en regard l'objectif du programme et le drapeau. Le contrôle a maintenant cette règle — et il faut dire sa limite : il est **lexical**, il cherche des actes de parole dans l'objectif et dans l'exemple, et il ne va que **dans un sens**. Il attrape une production oubliée ; il n'attrape pas une production inventée. Celle-là se lit plus loin, dans les exercices, parce qu'une inversion inventée se voit.

**La même règle n'est pas applicable à la GS**, et c'est une limite réelle, pas un oubli. Les productions de la GS sont pour la plupart **articulatoires** — « Prononcer », « Articuler », « Reproduire des sons ». Ce sont des actes de la voix, pas des actes de parole, et aucune liste de verbes ne les attrape. Appliquer la liste à la GS demanderait de basculer dix-huit unités, ce qui serait faux.

Une quatrième correction, plus discrète : l'exemple de l'unité 5 disait « Il restitue ce que le texte raconte ». Il empruntait le verbe de l'unité 14 — dont la production **est** « restituer ». Une unité de compréhension qui se prouve par le verbe d'une unité de production rend la colonne trompeuse à lire.

## 0 bis. Ce qui a changé en version 0.3.0

Le décodeur du CE1 étant écrit, il a permis un contrôle qui n'existait pas : **les mots d'un exemple doivent être lisibles au rang de leur propre unité**. Il en a trouvé deux, et tous les deux de la même famille — un exemple qui apprend à l'enfant un mot qu'il ne peut pas encore déchiffrer :

| Unité | Ce qui était écrit | Ce qui bloquait | Ce qui est écrit |
|---|---|---|---|
| 2 | Il lit craie, **neige**, père, fête | `neige` exige le `g` doux, qui n'arrive qu'à l'unité 20 | Il lit craie, père, fête, **reine** |
| 17 | Il lit **attention**, **addition**, potion | les consonnes doubles n'arrivent qu'à l'unité 28 | Il lit potion, **nation**, **station** |

Le contrôle porte sur les quatorze exemples qui sont des **listes de mots** — ceux qui commencent par « Il lit » ou « Il distingue ». Les autres exemples sont des phrases du programme : elles décrivent une réussite sans prétendre qu'on peut la lire, et le contrôle ne les examine pas. C'est une convention déclarée, pas un oubli.

## 1. Pourquoi le CE1 n'est pas un CP qui continue

Le CP apprend à **décoder**. Le CE1 lit pour **comprendre**. La progression du CP est graphémique et son palier de sortie est un nombre — trente correspondances. Le palier du CE1 est un **texte** : « Lire et comprendre en autonomie un texte narratif, informatif ou prescriptif d'une quinzaine de lignes ».

Trois conséquences structurelles :

1. **Le découpage en périodes est entièrement le nôtre.** Le programme ne donne **aucun palier de milieu d'année pour le CE1** — ses objectifs sont posés pour la fin d'année, sauf l'automatisation des correspondances du CP, demandée « tout au long de l'année ». À la GS, les colonnes d'âge étaient relevées du texte ; ici, la répartition en cinq périodes est un choix, et il est fait pour qu'aucune période ne dépende d'une autre.
2. **La longueur est fixée en lignes, pas en mots.** « Une quinzaine de lignes » est une conséquence directe pour le produit : **la largeur de ligne doit être fixée par l'application**, sinon « quinze lignes » ne désigne rien de déterminé et le palier de sortie devient invérifiable. Un texte de quinze lignes sur un téléphone n'est pas le même texte que sur une tablette.
3. **La consigne peut enfin être écrite.** C'est la première tranche où c'est vrai : l'enfant de CE1 lit seul. Les consignes écrites restent courtes et déchiffrables au rang de l'unité — une consigne illisible est une consigne absente.

## 2. L'organisation officielle, et la nôtre

Le programme organise la lecture du CE1 en **quatre ensembles**, et ce sont eux qui servent de domaines :

| Ensemble du programme | Ce qu'il couvre | Unités |
|---|---|---|
| Identifier les mots de manière de plus en plus aisée | finir le code : les correspondances complexes, les lettres muettes, les valeurs positionnelles | 21 |
| Lire à voix haute | la ponctuation, les groupes de souffle, la fluence, l'expressivité | 4 |
| Comprendre un texte | le sens global, la preuve, l'anaphore, l'implicite, les types de textes | 13 |
| Devenir lecteur | les genres, les personnages, le choix des livres, la mise en réseau | 4 |

**Ce ne sont pas des domaines inventés**, et c'est vérifié : le contrôle refuse une table dont les domaines ne sont pas ces quatre-là. Une organisation de notre main aurait été plus commode à équilibrer — quatre unités pour « Lire à voix haute » contre vingt et une pour le code — mais elle aurait cessé d'être relisible contre le programme.

Le déséquilibre est réel et il faut le dire : **la moitié de la tranche finit le code**. C'est ce que le programme demande pour le CE1, mais cela veut dire que la compréhension — qui est la finalité — ne dispose que de dix-sept unités, dont quatre seulement pour « Devenir lecteur ».

## 3. La table

<!-- DEBUT TABLE GENEREE -->

### Les quarante-deux unités

| Rang | Période | Domaine | Objectif | Production ? | Exemples | Source de l'exemple | D'où vient l'objectif | Ce que l'enfant fait |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | Identifier les mots de manière de plus en plus aisée | Automatiser le décodage des 30 CGP apprises au CP | — | Il déchiffre sans hésiter les mots construits sur les CGP apprises au CP | notre formulation | objectif | lire un mot et toucher son image parmi quatre |
| 2 | 1 | Identifier les mots de manière de plus en plus aisée | Lire /ɛ/ dans ses quatre graphies : ai, ei, è, ê | — | Il lit craie, père, fête, reine | notre formulation | objectif | toucher, dans un mot, la graphie du son entendu |
| 3 | 1 | Identifier les mots de manière de plus en plus aisée | Lire en et em, deuxième graphie de /ɑ̃/ | — | Il lit enfant, tempête, dent | notre formulation | objectif | trier des mots selon la graphie de la nasale entendue |
| 4 | 1 | Identifier les mots de manière de plus en plus aisée | Lire oin — /wɛ̃/ | — | Il lit loin, point, coin | notre formulation | objectif | toucher l'image du mot entendu |
| 5 | 1 | Comprendre un texte | Dégager le sens global d'un texte lu seul | — | Il choisit le résumé qui convient au texte qu'il vient de lire | notre formulation | objectif | toucher, parmi trois, le résumé qui convient au texte |
| 6 | 1 | Comprendre un texte | Donner un titre au texte | **oui** | Il est capable de donner un titre au texte | programme | exemple | choisir le titre parmi trois, dont deux qui conviennent presque |
| 7 | 1 | Comprendre un texte | Justifier une réponse par un retour au texte | **oui** | Il prend l'habitude de relire en autonomie un texte ou un passage pour mieux le comprendre, rechercher et repérer une information | programme | objectif | toucher, dans le texte, la phrase qui prouve la réponse |
| 8 | 1 | Lire à voix haute | Repérer les groupes de mots qui doivent être lus ensemble | — | Il repère la ponctuation et les groupes de mots qui doivent être lus ensemble (groupes de souffle respectant l'unité de sens) | programme | exemple | toucher, dans le texte, les mots à lire d'un seul souffle |
| 9 | 2 | Identifier les mots de manière de plus en plus aisée | Lire gn — /ɲ/ | — | Il lit montagne, agneau, signe | notre formulation | objectif | toucher, parmi trois, le mot qui contient le son entendu |
| 10 | 2 | Identifier les mots de manière de plus en plus aisée | Lire ill et y — /j/ et /ij/ | — | Il lit fille, billet, yeux, crayon | notre formulation | objectif | apparier les graphies d'un même son |
| 11 | 2 | Identifier les mots de manière de plus en plus aisée | Lire ph — /f/ | — | Il lit téléphone, photo, éléphant | notre formulation | objectif | toucher, parmi trois, le mot où /f/ s'écrit ph |
| 12 | 2 | Identifier les mots de manière de plus en plus aisée | Distinguer eu ouvert /œ/ de eu fermé /ø/ | — | Il distingue fleur de deux, peur de peu | notre formulation | objectif | trier des mots selon la voyelle entendue |
| 13 | 2 | Identifier les mots de manière de plus en plus aisée | Lire un — /œ̃/ | — | Il lit brun, lundi, chacun | notre formulation | objectif | toucher l'image du mot entendu |
| 14 | 2 | Comprendre un texte | Restituer les enchaînements logiques et chronologiques d'un récit | **oui** | L'élève restitue les enchaînements logiques et chronologiques d'un récit | programme | exemple | remettre des images dans l'ordre du récit |
| 15 | 2 | Comprendre un texte | Expliciter les émotions des personnages | **oui** | Il est capable d'expliciter les émotions des personnages | programme | exemple | toucher l'émotion du personnage, puis la phrase qui la montre |
| 16 | 2 | Devenir lecteur | Différencier le type narratif du type informatif | — | Il différencie le type narratif du type informatif | programme | objectif | toucher, entre deux textes courts, celui qui raconte |
| 17 | 3 | Identifier les mots de manière de plus en plus aisée | Lire tion — /sjɔ̃/ | — | Il lit potion, nation, station | notre formulation | objectif | toucher la fin du mot entendu |
| 18 | 3 | Identifier les mots de manière de plus en plus aisée | Lire ail, eil, euil, ouille — les voyelles suivies de /j/ | — | Il lit travail, soleil, fauteuil, grenouille | notre formulation | objectif | apparier deux mots qui riment |
| 19 | 3 | Identifier les mots de manière de plus en plus aisée | Connaître les valeurs positionnelles de c — /s/ et /k/ | — | Il se sert de sa connaissance des graphèmes pour établir des listes analogiques de mots | programme | exemple | trier des mots selon la valeur de la lettre |
| 20 | 3 | Identifier les mots de manière de plus en plus aisée | Connaître les valeurs positionnelles de g — /ʒ/ et /g/ | — | Il se sert de sa connaissance des graphèmes pour établir des listes analogiques de mots | programme | exemple | trier des mots selon la valeur de la lettre |
| 21 | 3 | Identifier les mots de manière de plus en plus aisée | Lire s entre deux voyelles — /z/ — et ss — /s/ | — | Il lit maison et poisson | notre formulation | objectif | toucher, parmi trois, le mot où l'on entend /z/ |
| 22 | 3 | Comprendre un texte | Se repérer dans la chaîne anaphorique | — | qui relie un nom à sa ou ses reprise(s) pronominale(s) ou à d'autres noms de sens équivalent | programme | objectif | toucher le personnage que désigne le pronom |
| 23 | 3 | Comprendre un texte | Résoudre une ambiguïté en s'appuyant sur le sens du texte | — | S'appuyer sur le sens du texte pour résoudre des ambiguïtés | programme | objectif | toucher, entre deux lectures possibles, celle que le texte impose |
| 24 | 3 | Comprendre un texte | Élucider le sens d'un mot inconnu par le contexte ou la morphologie | — | L'élève prend appui sur la morphologie d'un mot et/ou sur le contexte pour le comprendre | programme | objectif | toucher, parmi trois, ce que le mot veut dire ici |
| 25 | 3 | Devenir lecteur | Caractériser les personnages et reconnaître des types récurrents | **oui** | L'élève est capable de caractériser les personnages, de les comparer et de reconnaître des types récurrents dans la littérature de jeunesse | programme | objectif | apparier un personnage à ses traits |
| 26 | 4 | Identifier les mots de manière de plus en plus aisée | Lire les lettres finales muettes lexicales | — | Il lit le lait, le loup, le tabac sans vocaliser la finale | notre formulation | objectif | toucher le mot entendu, dont la consonne finale ne s'entend pas |
| 27 | 4 | Identifier les mots de manière de plus en plus aisée | Lire les morphèmes grammaticaux et lexicaux muets | — | Il lit des phrases contenant des morphèmes grammaticaux et lexicaux muets (ex. : ils chantent, le lait, etc.) de manière fluide sans vocaliser les lettres muettes | programme | exemple | toucher, dans une phrase, le mot qui porte la marque du pluriel |
| 28 | 4 | Identifier les mots de manière de plus en plus aisée | Lire les consonnes doubles | — | Il lit une pomme, une échelle, il arrive | notre formulation | objectif | toucher la consonne double dans le mot entendu |
| 29 | 4 | Identifier les mots de manière de plus en plus aisée | Identifier directement l'ensemble des mots courants | — | Il reconnaît sans déchiffrer et, est, elle, dans, pour, avec | notre formulation | objectif | toucher, dans une phrase affichée, le mot-outil entendu |
| 30 | 4 | Identifier les mots de manière de plus en plus aisée | Identifier les mots irréguliers fréquents | — | Il lit monsieur, femme, second, fils, œil | notre formulation | objectif | toucher l'image du mot entendu |
| 31 | 4 | Comprendre un texte | Comprendre ce qui est implicite — les inférences simples | — | Il est capable de réaliser en autonomie une inférence simple | programme | objectif | toucher, parmi trois, ce que le texte permet de conclure sans le dire |
| 32 | 4 | Comprendre un texte | Lire et comprendre un texte prescriptif | — | Il réalise ce qui est demandé dans le cas d'un texte prescriptif : une recette, l'application d'une règle du jeu | programme | objectif | ordonner les étapes d'une recette dans l'ordre où le texte les donne |
| 33 | 4 | Comprendre un texte | Lire et comprendre un texte informatif | — | Il repère l'information demandée dans un texte informatif simple | notre formulation | objectif | toucher l'information demandée dans le texte |
| 34 | 4 | Lire à voix haute | Lire après préparation en réalisant les pauses adéquates | **oui** | Il lit après préparation un texte simple en réalisant les pauses adéquates et en adoptant le ton et le rythme appropriés au sens du texte | programme | exemple | aucun geste : l'enfant lit, un adulte valide |
| 35 | 5 | Identifier les mots de manière de plus en plus aisée | Décoder des pseudo-mots complexes | — | L'élève déchiffre et écrit sous la dictée des syllabes et des pseudo-mots comportant des CGP courantes et d'autres plus complexes (ex. : doir, stag, choust, valin, cagnou, etc.) | programme | exemple | toucher, parmi trois, la suite de lettres entendue |
| 36 | 5 | Identifier les mots de manière de plus en plus aisée | Établir des listes analogiques de mots | — | Il lit des mots nouveaux en lien avec l'orthographe lexicale, il se sert de sa connaissance des graphèmes pour établir des listes analogiques de mots : ça/glaçon/garçon/nous forçons/maçon/etc. et flacon/flocon craie/etc. | programme | exemple | apparier les mots qui partagent une graphie |
| 37 | 5 | Comprendre un texte | Résumer le texte | **oui** | Il est capable de le résumer oralement | programme | exemple | ordonner les images du récit, qui tiennent lieu de résumé |
| 38 | 5 | Comprendre un texte | Lire et comprendre en autonomie un texte d'une quinzaine de lignes | — | Lire et comprendre en autonomie un texte narratif, informatif ou prescriptif d'une quinzaine de lignes | programme | objectif | un texte entier, et les questions des unités 5 à 7, 14, 22 à 24, 31 et 33 |
| 39 | 5 | Lire à voix haute | Lire un texte adapté à son niveau avec une vitesse de 70 mots par minute | **oui** | Lire un texte adapté à son niveau de lecture avec une vitesse de 70 mots par minute | programme | objectif | l'application chronomètre, l'adulte valide la lecture |
| 40 | 5 | Lire à voix haute | Lire en modifiant sa voix et sa cadence selon le sens | **oui** | Il lit un texte en modifiant sa voix et sa cadence, en fonction du sens | programme | exemple | aucun geste : l'enfant lit, un adulte valide |
| 41 | 5 | Devenir lecteur | Relier ses lectures à son expérience et à ses autres lectures | **oui** | Il est capable d'exprimer le lien entre deux lectures ou entre une lecture et sa propre expérience | programme | objectif | toucher, parmi trois, le texte qui ressemble à celui qu'on vient de lire |
| 42 | 5 | Devenir lecteur | Aller vers les livres et être capable d'en choisir à titre personnel | — | Il est capable de choisir un livre en fonction de ses propres centres d'intérêt | programme | objectif | aucun : cela ne passe pas par un écran |

### Les 10 unités dont l'objectif porte un acte de parole

Chacune oblige l'exercice qui la couvre à dire ce qu'il fait de la production, et ce sera l'une de deux choses : une `inversion` — ce que le geste reprend — pour les 7 unités qui ont un geste, ou un `pourquoi_hors_app` pour les 3 unités qui n'en ont aucun, l'application n'étant alors pas l'instrument. La colonne « Ce que l'enfant fait dans l'application » est une dette, pas une déclaration : elle est soldée par la banque d'exercices du CE1.
 Elle la solde : sur les 10 unités de production, **7** déclarent une `inversion` et **4** un `pourquoi_hors_app`
 — l'unité 41 paie les deux
. Aucune ne reste sans réponse.

| Rang | Domaine | Objectif | Ce que l'enfant fait dans l'application | Dette |
|---|---|---|---|---|
| 6 | Comprendre un texte | Donner un titre au texte | choisir le titre parmi trois, dont deux qui conviennent presque | `inversion` |
| 7 | Comprendre un texte | Justifier une réponse par un retour au texte | toucher, dans le texte, la phrase qui prouve la réponse | `inversion` |
| 14 | Comprendre un texte | Restituer les enchaînements logiques et chronologiques d'un récit | remettre des images dans l'ordre du récit | `inversion` |
| 15 | Comprendre un texte | Expliciter les émotions des personnages | toucher l'émotion du personnage, puis la phrase qui la montre | `inversion` |
| 25 | Devenir lecteur | Caractériser les personnages et reconnaître des types récurrents | apparier un personnage à ses traits | `inversion` |
| 34 | Lire à voix haute | Lire après préparation en réalisant les pauses adéquates | aucun geste : l'enfant lit, un adulte valide | `pourquoi_hors_app` |
| 37 | Comprendre un texte | Résumer le texte | ordonner les images du récit, qui tiennent lieu de résumé | `inversion` |
| 39 | Lire à voix haute | Lire un texte adapté à son niveau avec une vitesse de 70 mots par minute | l'application chronomètre, l'adulte valide la lecture | `pourquoi_hors_app` |
| 40 | Lire à voix haute | Lire en modifiant sa voix et sa cadence selon le sens | aucun geste : l'enfant lit, un adulte valide | `pourquoi_hors_app` |
| 41 | Devenir lecteur | Relier ses lectures à son expérience et à ses autres lectures | toucher, parmi trois, le texte qui ressemble à celui qu'on vient de lire | `inversion` |

### Le palier de sortie — 12 réussites

| Objectif | Où il se vérifie |
|---|---|
| Décoder toutes les CGP, y compris les plus complexes | dans l'app |
| Identifier directement l'ensemble des mots courants | dans l'app |
| Dégager le sens global d'un texte lu de façon autonome | dans l'app |
| Se repérer dans la chaîne anaphorique | dans l'app |
| Comprendre ce qui est implicite dans le texte, dans des cas simples | dans l'app |
| Justifier ses réponses par un retour au texte | dans l'app — sous forme de substitution : l'enfant touche la phrase qui prouve la réponse, il ne formule pas la justification |
| Lire et comprendre en autonomie un texte narratif, informatif ou prescriptif d'une quinzaine de lignes | dans l'app — c'est le palier de la tranche |
| Lire un texte adapté à son niveau de lecture avec une vitesse de 70 mots par minute | hors app, au bilan |
| Lire des textes narratifs, documentaires et prescriptifs en respectant tous les signes de ponctuation et les groupes de souffle | hors app, au bilan |
| Lire de manière expressive | hors app, au bilan |
| Expliciter les émotions des personnages | hors app, au bilan |
| Résumer oralement un texte | hors app, au bilan |

### Les 8 citations officielles

C'est contre ces passages que se relisent les exemples annoncés « programme ». Le contrôle vérifie qu'un tel exemple est bien contenu dans l'une d'elles ; il ne vérifie pas que la citation est fidèle au Bulletin officiel — cela se relit, et c'est une relecture humaine.

**p. 6 — Identifier les mots de manière de plus en plus aisée — objectifs d'apprentissage, CE1**

> Tout au long de l'année : automatiser le décodage des correspondances graphophonémiques (CGP) apprises au CP. En fin d'année : décoder toutes les CGP y compris les plus complexes ; avoir mémorisé l'ensemble des CGP dans tous les types d'écriture, en particulier celles des sons proches (en encodage et décodage) ; identifier directement l'ensemble des mots courants et déchiffrer avec exactitude les mots nouveaux dont le décodage n'a pas encore été automatisé.

**p. 6 — Identifier les mots de manière de plus en plus aisée — exemples de réussite, CE1**

> L'élève déchiffre et écrit sous la dictée des syllabes et des pseudo-mots comportant des CGP courantes et d'autres plus complexes (ex. : doir, stag, choust, valin, cagnou, etc.). Il lit des phrases contenant des morphèmes grammaticaux et lexicaux muets (ex. : ils chantent, le lait, etc.) de manière fluide sans vocaliser les lettres muettes. Il lit des mots nouveaux en lien avec l'orthographe lexicale, il se sert de sa connaissance des graphèmes pour établir des listes analogiques de mots : ça/glaçon/garçon/nous forçons/maçon/etc. et flacon/flocon craie/etc. (voir les valeurs positionnelles des lettres c, g, s, etc.).

**p. 6 — Lire à voix haute — objectifs d'apprentissage, CE1**

> En fin d'année : lire un texte adapté à son niveau de lecture avec une vitesse de 70 mots par minute ; lire des textes narratifs, documentaires et prescriptifs en respectant tous les signes de ponctuation et les groupes de souffle ; lire de manière expressive.

**p. 6 — Lire à voix haute — exemples de réussite, CE1**

> L'élève s'entraîne à la lecture à voix haute dans des séances spécifiques : il repère la ponctuation et les groupes de mots qui doivent être lus ensemble (groupes de souffle respectant l'unité de sens). Il lit après préparation un texte simple en réalisant les pauses adéquates et en adoptant le ton et le rythme appropriés au sens du texte. Il lit un texte en modifiant sa voix et sa cadence, en fonction du sens.

**p. 6-7 — Comprendre un texte — objectifs d'apprentissage, CE1**

> Dégager le sens global d'un texte lu, de façon autonome, à la suite d'une séance dédiée à la compréhension. Développer des stratégies pour élucider le sens des mots et des expressions inconnus. Se repérer dans la chaîne anaphorique (qui relie un nom à sa ou ses reprise(s) pronominale(s) ou à d'autres noms de sens équivalent) et s'appuyer sur le sens du texte pour résoudre des ambiguïtés. Comprendre ce qui est implicite dans le texte (inférences) dans des cas simples. Justifier ses réponses par un retour au texte. Lire et comprendre en autonomie un texte narratif, informatif ou prescriptif d'une quinzaine de lignes.

**p. 6-7 — Comprendre un texte — exemples de réussite, CE1**

> L'élève restitue les enchaînements logiques et chronologiques d'un récit. Il est capable d'expliciter les émotions des personnages. Il est capable de donner un titre au texte. Il est capable de le résumer oralement. Il réalise ce qui est demandé dans le cas d'un texte prescriptif : une recette, l'application d'une règle du jeu, etc. L'élève prend appui sur la morphologie d'un mot et/ou sur le contexte pour le comprendre. Il prend l'habitude de consulter un dictionnaire adapté. Il explicite son raisonnement pour inférer. Il prend l'habitude de relire en autonomie un texte ou un passage pour mieux le comprendre, rechercher et repérer une information. Il est capable de réaliser en autonomie une inférence simple (contexte connu de l'élève). Ex. : « J'ai pris mon parapluie » → Le temps est pluvieux.

**p. 6 — Devenir lecteur — exemples de réussite, CE1**

> L'élève est capable de caractériser les personnages, de les comparer et de reconnaître des types récurrents dans la littérature de jeunesse. Il différencie le type narratif du type informatif. Il est capable d'exprimer le lien entre deux lectures ou entre une lecture et sa propre expérience. Il est capable de choisir un livre en fonction de ses propres centres d'intérêt.

**p. 7 — Devenir lecteur — objectifs d'apprentissage, CE1**

> Lire 5 à 10 œuvres complètes et variées issues du patrimoine et de la littérature de jeunesse (albums, romans, contes, fables, poèmes, pièces de théâtre et documentaires). Se familiariser aux différents genres et types de textes. Faire preuve d'initiative dans ses lectures personnelles en empruntant des livres en fonction de ses goûts. Relier ses lectures à son expérience personnelle, être en mesure d'établir des liens entre ses différentes lectures (mise en réseau).


### Ce qui n'est pas de la tranche

*Ces domaines du programme de français du cycle 2 ne sont pas dans la tranche CE1 de la v1. Ils sont listés pour que la structure les accueille sans réécriture.*

| Domaine écarté |
|---|
| l'écriture cursive et le geste graphique |
| copier et acquérir des stratégies de copie |
| encoder puis écrire sous dictée |
| produire des écrits |
| l'orthographe lexicale et grammaticale |
| la grammaire — se repérer dans la phrase simple |
| le vocabulaire comme domaine séparé : enrichir, établir des relations entre les mots, réemployer, mémoriser l'orthographe lexicale |
| l'oral — écouter pour comprendre, dire pour être compris, participer à des échanges |
| la mesure de la fluence par la machine |
| la lecture expressive évaluée par la machine |

*Pourquoi.* La tranche CE1 ne prend que la lecture : finir le code et installer la compréhension. L'écriture, l'oral, le vocabulaire et la grammaire sont quatre autres ensembles du même programme, et ils demandent des exercices que cette tranche n'a pas — une dictée ne se corrige pas sans micro, une production d'écrit demande un clavier que l'enfant de sept ans ne maîtrise pas, et une séance de vocabulaire est un enseignement, non un exercice. Les deux dernières lignes sont d'une autre nature : la fluence et l'expressivité SE MESURENT dans l'application, elles ne s'y ÉVALUENT pas. Le chronomètre est un instrument, pas un juge.

### Le décompte

| Point | Nombre |
|---|---|
| Unités | 42 |
| Domaines — les quatre du programme | 4 |
| dont IDM — Identifier les mots de manière de plus en plus aisée | 21 |
| dont LVH — Lire à voix haute | 4 |
| dont CTX — Comprendre un texte | 13 |
| dont DVL — Devenir lecteur | 4 |
| Unités dont l'objectif porte un acte de parole | 10 |
| dont avec un geste — dette d'une `inversion` | 7 |
| dont sans geste — dette d'un `pourquoi_hors_app` | 3 |
| Exemples repris du programme | 24 |
| Exemples de notre main | 18 |
| Citations officielles | 8 |
| Réussites au palier de sortie | 12 |
| dont vérifiables dans l'app | 7 |
| dont hors app, au bilan | 5 |
| Domaines écartés de la tranche | 10 |

<!-- FIN TABLE GENEREE -->

## 4. La règle de contenu du CE1 — la déchiffrabilité porte sur un texte entier

C'est la règle du CP, mais elle change de nature en changeant d'échelle.

Au CP, un texte ne peut employer que les graphèmes déjà vus, et le contrôle porte sur les mots du texte. Au CE1, la même règle s'applique à un **texte entier** : les trente correspondances du CP, puis les correspondances du CE1 jusqu'au rang de l'unité, plus les mots-outils mémorisés et les mots irréguliers déclarés.

Ce qui change est la **conséquence d'une seule faute**. Au CP, un mot non déchiffrable dans une liste est un mot qu'on retire. Au CE1, un mot non déchiffrable dans un texte de quinze lignes **arrête la lecture de l'enfant** — et l'arrêt ne se localise pas : il emporte la phrase, puis le sens. Un texte n'est donc pas « presque déchiffrable » ; il l'est ou il ne l'est pas.

Trois conséquences pour le contrôle :

1. **Il porte sur chaque mot**, jamais sur un échantillon. Un contrôle qui compte les mots couverts ne voit pas le mot qui manque une fois.
2. **La liste des exceptions est déclarée mot par mot.** Les mots irréguliers fréquents — `monsieur`, `femme`, `second`, `fils`, `œil` — ne se déchiffrent pas ; ils se mémorisent. Les déclarer un par un rend la liste contestable, et une liste contestable se corrige.
3. **Les mots-outils mémorisés du CP sont repris**, pas réintroduits. Ils sont déjà dans `outils/cgp-cp.json` ; les redéclarer au CE1 créerait deux listes qui divergeraient.

## 5. Ce que la décision « pas de reconnaissance vocale » coûte au CE1

Elle coûte plus cher qu'à la GS, parce que le CE1 a une section officielle entière — « Lire à voix haute » — dont les trois objectifs de sortie sont inaudibles pour la machine : **70 mots par minute**, **le respect de la ponctuation et des groupes de souffle**, **la lecture expressive**.

La parade est la même qu'à la GS, mais elle a ici une forme précise : **l'application fait repérer, l'adulte fait juger.**

- « Repérer les groupes de mots qui doivent être lus ensemble » est un objectif **vérifiable dans l'application** : l'enfant touche, dans le texte, les mots à lire d'un seul souffle. La reconnaissance ne demande pas de micro.
- « Lire un texte à 70 mots par minute » ne l'est pas. L'application **chronomètre**, un adulte valide la lecture. Le chronomètre est un instrument, pas un juge — et la nuance est écrite dans la table, parce qu'un temps mesuré par la machine ne dit rien de ce qui a été lu.

C'est la raison pour laquelle dix des unités portent un acte de parole, et **trois** d'entre elles — 34, 39 et 40 — n'ont pas de geste qui solde leur dette. Deux n'ont **aucun geste** : « l'enfant lit, un adulte valide ». La troisième, 39, n'a qu'un **chronomètre** : l'application affiche le texte et compte les mots, l'adulte saisit la durée, et le temps mesuré ne dit rien de ce qui a été lu. Une unité sans geste n'est pas un trou dans la table ; c'est une unité dont l'application n'est pas l'instrument.

## 6. Ce qui reste à produire

- **Les enregistrements.** Les 18 textes du CE1, les 33 consignes de la banque et les mots du CE1 : rien de tout cela n'est enregistré à ce jour. Le corpus audio existant est celui de la GS, et il ne couvre ni les mots, ni les consignes du CE1. Les **pseudo-mots** que le programme donne lui-même en exemple font exception : ils ont leur corpus et le script de leur enregistrement (`contenu/LUDOLIRE-PSEUDO-MOTS-CE1.md`), où leur prononciation est **dérivée** des tables et non écrite à la main.
- **Les illustrations du CE1.** Le corpus d'images est celui de la GS, et la banque déclare les manques qu'elle y rencontre : aucun mot contenant `oin`, aucun contenant la nasale `un`, aucun mot irrégulier n'est illustré. Trois unités annonçaient « toucher l'image du mot entendu » ; leurs exercices emploient la mécanique qui reste possible — lire et choisir le mot, reconnaître le mot d'un seul regard — et le manque est **déclaré** plutôt que comblé par un exercice qui n'entraînerait pas l'objectif.
- **Un texte documentaire lisible avant le rang 32.** L'unité 16 demande d'opposer un récit à un documentaire ; la tranche ne contient pas de documentaire assez tôt. L'exercice porte donc ses deux textes courts, et le besoin est déclaré.

Ce qui n'est plus à produire, et qui l'était quand cette table a été écrite :

- **La table des correspondances du CE1** — *faite* : `outils/cgp-ce1.json`, 11 correspondances nouvelles, 34 mots-outils et 7 mots irréguliers déclarés, 6 familles de règles.
- **Le décodeur** — *fait* : `outils/verifier-textes-ce1.py`, éprouvé par `outils/tester-decodeur-ce1.py` (**110 essais**, dont 17 qui éprouvent la *lecture* — quels graphèmes sont muets — et pas seulement le verdict, chacun de part et d'autre d'un seuil). Il refuse avant le rang et accepte après, sur les trois règles que le CE1 change : `-ent` au rang 27, les consonnes doubles au rang 28, les muettes lexicales au rang 26.
- **Les textes du CE1** — *faits* : `contenu/textes-ce1/`, **18 textes** de six à quinze lignes, un par palier, chacun déclarant son rang dans son propre en-tête.
- **La largeur de ligne** — *fixée* : **34 signes, espaces comprises**, dans le contrôle comme dans l'application. C'est elle qui rend « une quinzaine de lignes » vérifiable, et le compte de lignes est contrôlé.
- **La banque d'exercices du CE1** — *faite* : `outils/exercices-ce1.json` et `contenu/LUDOLIRE-EXERCICES-CE1.md`, **57 exercices couvrant les 42 unités**. C'est là que les dix unités de production soldent leur dette — sept par une `inversion`, trois par un `pourquoi_hors_app`, l'unité 41 par les deux.
- **Les questions de compréhension, avec leur phrase-preuve.** Toute question a une phrase du texte qui prouve sa réponse, et l'application demande à l'enfant de la toucher. C'est ainsi que « justifier ses réponses par un retour au texte » devient vérifiable par une machine : non pas « as-tu compris ? » mais « où le texte le dit-il ? ». Le contrôle des exercices refuse une question dont la phrase citée n'est pas **littéralement** présente dans le texte qu'elle nomme.
- **Les distracteurs plausibles.** Une mauvaise réponse doit être une lecture **possible** du texte, jamais une absurdité. Un intrus doit partager le plus possible avec la bonne réponse — le même personnage, le même lieu, la même action — et ne s'en écarter que par ce que la question demande.

## 7. Ce que cette table ne règle pas

- **Elle ne dit pas si la tranche est jouable en une année.** Le programme ne donne aucun palier intermédiaire pour le CE1, donc il n'existe aucune référence officielle pour dire si nos cinq périodes sont trop chargées ou trop légères. C'est un jugement d'usage, et il se fera en testant.
- **Elle ne compare pas les citations officielles au Bulletin officiel.** Le contrôle vérifie qu'un exemple annoncé « programme » est contenu dans l'une des citations présentes dans le même fichier — donc que le bloc de citations suit les unités quand elles changent. Il ne peut pas vérifier que la citation est fidèle à l'Annexe 3 : le PDF n'est pas dans le dépôt. Cette fidélité se relit, et c'est une relecture humaine.
- **Elle ne prend que la lecture.** L'écriture, l'oral, le vocabulaire et la grammaire sont quatre autres ensembles du même programme. Ils sont listés dans la table, hors tranche, pour que la structure les accueille sans réécriture — mais ils demandent des exercices que cette tranche n'a pas : une dictée ne se corrige pas sans micro, et une production d'écrit demande un clavier que l'enfant de sept ans ne maîtrise pas.
- **Elle ne dit rien du diagnostic d'entrée.** À la GS, les trois colonnes d'âge donnaient un chemin de rattrapage naturel. Au CE1, il n'y a pas de colonne : un enfant qui entre dans la tranche sans avoir automatisé les correspondances du CP commence au rang 1, et la table ne prévoit pas de chemin plus court.
