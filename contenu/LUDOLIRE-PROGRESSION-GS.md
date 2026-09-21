# Ludo'Lire — Progression de la tranche GS

**Statut :** proposition, version 0.2.0. La relecture pédagogique est faite par le porteur du projet, en testant l'application.
**Source du cadre :** BO n° 41 du 31 octobre 2024, programme d'enseignement pour le développement et la structuration du langage oral et écrit du cycle 1 (arrêté du 22 octobre 2024, application rentrée 2025-2026).
**Source de vérité de la table :** `outils/progression-gs.json`. Le tableau du § 3 en est le rendu, produit par `outils/generer-table.py`.

---

## 0. Ce qui a changé en version 0.2.0

La version 0.1.0 de cette table comportait une erreur de méthode, et il faut la consigner parce qu'elle est facile à refaire.

Le programme de cycle 1 organise ses attendus en **trois colonnes d'âge** : « Avant 4 ans », « À partir de 4 ans », « À partir de 5 ans ». La première extraction du PDF était en texte plat — et **une extraction en texte plat aplatit les trois colonnes**, donc fait perdre l'attribution. La version 0.1.0 s'y est fiée et a promu en « GS » des objectifs qui sont en réalité « à partir de 4 ans » : compter les syllabes, comparer des mots selon leur longueur, nommer les lettres de son prénom, reproduire des intonations, composer un mot avec des lettres mobiles.

Le tableau a été repris en extrayant le PDF en **mode « layout »**, colonnes préservées. Chaque unité porte maintenant un champ `colonne` qui dit d'où elle vient, et le contrôle vérifie que le palier et la colonne ne se contredisent pas.

Trois corrections de fond en découlent, au-delà de la réattribution :

| Ce qui était écrit | Ce que dit le programme |
|---|---|
| Paires distinctives de la GS : `f/v, s/z, p/b, t/d, k/g` | ce sont les paires « **à partir de 4 ans** ». Celles de la GS sont `ch/s, ch/j, ch/z` |
| Consonnes continues de la GS : `l, m, r, s, f, v` | le programme nomme `s/r/f/v/j/ch` et la liquide `l`, et précise que la valeur sonore des lettres est connue « **hormis les occlusives** » |
| « Fusionner deux phonèmes », « supprimer ou substituer un phonème » | la colonne « à partir de 5 ans » ne demande la manipulation que sur les **syllabes**. Manipuler des phonèmes est un objectif du **CP** — ces deux unités sont sorties de la tranche |

La table passe de 28 à **45 unités**, et le partage change de nature : **27 unités préparatoires, 18 unités GS.**

## 1. Pourquoi la GS n'est pas un CP en plus facile

Au CP, la progression est **graphémique** : trente correspondances, dans un ordre, et un texte ne peut employer que celles déjà vues. À la GS, il n'y a **rien à décoder** — et donc aucun texte à contrôler. La progression est **phonologique** : l'enfant apprend à entendre, à découper, à manipuler des unités sonores, et à reconnaître les lettres qui les transcriront plus tard.

Trois conséquences structurelles :

1. **La sortie de la tranche n'est pas un texte lu** mais des habiletés installées. Elle se vérifie par des réussites, pas par une lecture.
2. **La tranche GS peut être complète là où la CP est partielle.** La colonne « à partir de 5 ans » ne compte que dix-huit objectifs : couvrir l'année entière est atteignable. La CP, elle, s'arrête au palier de milieu d'année. C'est une asymétrie assumée, et elle joue en faveur de la GS.
3. **Le contrôle de conformité n'a pas le même objet.** Au CP, on vérifie qu'un texte n'emploie que des graphèmes connus. À la GS, on vérifie qu'un exercice n'emploie que des **mots connus de l'enfant à l'oral** et des **phonèmes déjà travaillés**. La machinerie est la même ; la clé de comparaison change.

## 2. L'organisation officielle, et la nôtre

Le programme organise ses attendus **par âge**, pas par période. Nous traduisons ses trois colonnes en **cinq périodes**, et nous marquons chaque unité de deux façons :

| Palier | Colonnes d'origine | Unités | À quoi il sert |
|---|---|---|---|
| **préparatoire** | « Avant 4 ans » et « À partir de 4 ans » | 27 | le **chemin de rattrapage** d'un enfant que le diagnostic place en dessous du niveau GS |
| **GS** | « À partir de 5 ans » | 18 | le corps de la tranche |

Cette distinction n'est pas cosmétique. Elle signifie que **le diagnostic initial ne sert pas seulement à placer l'enfant dans la bonne tranche, mais dans le bon palier** — et qu'un enfant de GS qui n'entend pas encore les syllabes n'est pas en échec : il commence au rang 10.

Elle a aussi une conséquence sur ce qu'on annonce. **Une tranche « GS » dont les deux tiers du contenu sont préparatoires ne se vend pas comme une tranche de GS.** Le contenu est justifié — c'est le programme, et c'est ce dont un enfant de GS a besoin quand il est en difficulté — mais il faut le dire dans la fiche de store plutôt que de laisser le parent découvrir qu'on compte les syllabes en grande section.

## 3. La table

<!-- DEBUT TABLE GENEREE -->

| Rang | Période | Domaine | Palier | Colonne du programme | Objectif | Production ? | Exemples du programme | Ce que l'enfant fait |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | Écouter, identifier, discriminer et reproduire des sons | préparatoire | Avant 4 ans | Discriminer et identifier des sons familiers, localiser la source | — | retrouver d'où vient le bruit | toucher la zone d'où vient le son |
| 2 | 1 | Écouter, identifier, discriminer et reproduire des sons | préparatoire | Avant 4 ans | Reconnaître les sons de la langue les plus fréquents dans une suite | — | repérer un son connu dans une suite énoncée | lever la main quand le son connu revient |
| 3 | 1 | Écouter, identifier, discriminer et reproduire des sons | préparatoire | Avant 4 ans | Comparer, apparier et reproduire des sons | oui | deux boîtes identiques parmi quatre | apparier deux boîtes identiques |
| 4 | 1 | Écouter, identifier, discriminer et reproduire des sons | préparatoire | À partir de 4 ans | Discriminer et identifier les sons de la langue, les localiser dans une suite | — | placer un jeton sur l'image quand on entend le son | placer un jeton sur l'image |
| 5 | 1 | Écouter, identifier, discriminer et reproduire des sons | préparatoire | À partir de 4 ans | Reproduire des sons | oui | onomatopées | imiter le son entendu |
| 6 | 1 | Écouter, identifier, discriminer et reproduire des sons | préparatoire | À partir de 4 ans | Reproduire des intonations | oui | sirènes vocales ascendantes et descendantes | suivre la sirène avec la main, de bas en haut |
| 7 | 1 | Écouter, identifier, discriminer et reproduire des sons | préparatoire | Avant 4 ans | Commencer à percevoir les distinctions entre des mots proches phonologiquement | — | deux mots qui ne diffèrent que par un son | désigner l'image du mot entendu |
| 8 | 1 | Manipuler les syllabes orales | préparatoire | Avant 4 ans | Prononcer son prénom, puis une comptine, en scandant les syllabes | oui | son prénom | frapper dans ses mains en disant son prénom |
| 9 | 1 | Manipuler les syllabes orales | préparatoire | Avant 4 ans | Frapper les syllabes d'un mot | — | dans ses mains, sur ses cuisses, avec un instrument | frapper les syllabes sur ses cuisses |
| 10 | 2 | Manipuler les syllabes orales | préparatoire | À partir de 4 ans | Scander les syllabes d'un mot | — | ba-na-ne | frapper une fois par syllabe |
| 11 | 2 | Manipuler les syllabes orales | préparatoire | À partir de 4 ans | Dénombrer les syllabes de mots familiers, à l'oral et sans support écrit | — | ba-na-ne vaut trois | poser un jeton par syllabe |
| 12 | 2 | Manipuler les syllabes orales | préparatoire | À partir de 4 ans | Comparer les mots selon le nombre de syllabes et les classer | — | un mot plus long qu'un autre, à l'oral et sans écrit | ranger du plus court au plus long |
| 13 | 2 | Manipuler les syllabes orales | préparatoire | À partir de 4 ans | Discriminer une syllabe cible dans une suite de syllabes énoncées | — | MA puis FA puis PA puis MA puis SA | lever la main quand la syllabe cible revient |
| 14 | 2 | Manipuler les syllabes orales | préparatoire | À partir de 4 ans | Ajouter, supprimer, permuter, répéter, fusionner, substituer les syllabes d'un mot dit à l'oral | oui | RI-VE devient VE-RI | dire le mot transformé |
| 15 | 2 | Manipuler les syllabes orales | préparatoire | Avant 4 ans | Dire des comptines courtes comprenant des phonèmes proches | oui | une comptine apprise en classe | réciter la comptine avec le groupe |
| 16 | 2 | Phonèmes | préparatoire | À partir de 4 ans | Distinguer et produire correctement les nasales | oui | é/in, a/an, o/on | trier des images selon la nasale entendue |
| 17 | 2 | Articulation | préparatoire | Avant 4 ans | Articuler distinctement des couples de consonnes proches | oui | t/k, f/s, m/n | répéter la paire après le modèle |
| 18 | 2 | Articulation | préparatoire | Avant 4 ans | Prononcer correctement des paires distinctives | oui | cour/tour, cube/tube, cassé/café, pouce/pouf, nain/main | désigner l'image du mot entendu |
| 19 | 3 | Articulation | préparatoire | À partir de 4 ans | Articuler distinctement des couples de consonnes proches | oui | f/v, s/z, p/b, t/d, k/g | répéter la paire après le modèle |
| 20 | 3 | Articulation | préparatoire | À partir de 4 ans | Prononcer correctement des paires distinctives et des mots à phonèmes proches | oui | ville/fil, dessert/désert, poison/poisson, pépé/bébé, doigt/toit, gare/car, boule/poule | désigner l'image du mot entendu |
| 21 | 3 | Connaître le nom des lettres | préparatoire | Avant 4 ans | Retrouver l'étiquette de son prénom écrit en capitales parmi d'autres | — | en prenant des indices sur les lettres | toucher son étiquette |
| 22 | 3 | Connaître le nom des lettres | préparatoire | Avant 4 ans | Reconnaître et nommer certaines lettres de son prénom écrit en capitales | oui | la première lettre de son prénom | nommer la lettre désignée |
| 23 | 3 | Connaître le nom des lettres | préparatoire | À partir de 4 ans | Nommer les lettres de son prénom et quelques lettres de mots connus | oui | le professeur nomme systématiquement les lettres | nommer la lettre désignée |
| 24 | 3 | Connaître le nom des lettres | préparatoire | À partir de 4 ans | Connaître la correspondance entre les lettres scriptes majuscules et minuscules et les lettres cursives minuscules | — | la même lettre dans deux écritures | apparier deux étiquettes de la même lettre |
| 25 | 3 | Connaître le nom des lettres | préparatoire | À partir de 4 ans | Épeler son prénom ou un mot connu afin qu'un tiers puisse le composer | oui | dire les lettres dans l'ordre | dire les lettres dans l'ordre |
| 26 | 3 | Connaître le nom des lettres | préparatoire | À partir de 4 ans | Composer un mot connu en commençant par la première lettre et en respectant l'ordre des lettres | — | même graphie, puis graphies différentes | déplacer les lettres dans l'ordre |
| 27 | 3 | Principe alphabétique — le son des lettres | préparatoire | À partir de 4 ans | Utiliser le nom de quelques lettres connues pour représenter les sons entendus | oui | les voyelles | toucher la lettre qui fait le son entendu |
| 28 | 4 | Écouter, identifier, discriminer et reproduire des sons | GS | À partir de 5 ans | Discriminer et identifier les sons de la langue, les localiser dans une suite et les mémoriser | — | retrouver l'ordre des sons entendus | refaire la suite d'images dans l'ordre |
| 29 | 4 | Écouter, identifier, discriminer et reproduire des sons | GS | À partir de 5 ans | Différencier les sons proches | — | on, en, un | trier des images selon le son entendu |
| 30 | 4 | Écouter, identifier, discriminer et reproduire des sons | GS | À partir de 5 ans | Discriminer et identifier les mots auditivement proches | — | poule/boule/roule/moule/coule/foule | désigner l'image du mot entendu |
| 31 | 4 | Écouter, identifier, discriminer et reproduire des sons | GS | À partir de 5 ans | Augmenter sa mémoire auditive et sa capacité de concentration | — | redire une suite de trois sons dans l'ordre | refaire la suite dans l'ordre |
| 32 | 4 | Manipuler les syllabes orales | GS | À partir de 5 ans | Fusionner les syllabes d'attaque et la syllabe finale de deux mots pour obtenir un pseudo-mot | oui | POISSON + SOURIS donnent POIRIS | dire le pseudo-mot obtenu |
| 33 | 4 | Manipuler les syllabes orales | GS | À partir de 5 ans | Supprimer, ajouter, remplacer, inverser, substituer, fusionner les syllabes d'un mot | oui | RI-VE devient VE-RI | dire le mot transformé |
| 34 | 4 | Attaques, rimes et assonances | GS | À partir de 5 ans | Repérer et produire des rimes et des assonances | oui | bateau et gâteau | apparier deux images qui riment |
| 35 | 4 | Phonèmes | GS | À partir de 5 ans | Trouver un phonème cible dans une liste de mots | — | le son /f/ | lever la main quand on entend /f/ |
| 36 | 4 | Phonèmes | GS | À partir de 5 ans | Trouver l'intrus à l'initiale | — | sac, Sacha, cartable | désigner l'intrus |
| 37 | 5 | Phonèmes | GS | À partir de 5 ans | Localiser un phonème dans un mot | — | début ou fin de mot | placer un jeton au début ou à la fin |
| 38 | 5 | Articulation | GS | À partir de 5 ans | Prononcer correctement des couples de consonnes proches | oui | ch/s, ch/j, ch/z | répéter la paire après le modèle |
| 39 | 5 | Articulation | GS | À partir de 5 ans | Prononcer correctement les doubles consonnes | oui | br, cr, bl, pl, sl | répéter après le modèle |
| 40 | 5 | Connaître le nom des lettres | GS | À partir de 5 ans | Reconnaître et nommer toutes les lettres d'un mot écrit dans les trois graphies | oui | capitale, scripte, cursive | nommer chaque lettre désignée |
| 41 | 5 | Connaître le nom des lettres | GS | À partir de 5 ans | Connaître les différentes graphies d'une même lettre | — | majuscule capitale, minuscules scriptes, cursives | apparier les trois graphies d'une même lettre |
| 42 | 5 | Connaître le nom des lettres | GS | À partir de 5 ans | Connaître le nom des lettres de l'alphabet | oui | les vingt-six lettres | nommer la lettre désignée |
| 43 | 5 | Connaître le nom des lettres | GS | À partir de 5 ans | Épeler les lettres d'un mot connu afin qu'un tiers puisse l'écrire | oui | dire les lettres dans l'ordre | dire les lettres dans l'ordre |
| 44 | 5 | Principe alphabétique — le son des lettres | GS | À partir de 5 ans | Prolonger les phonèmes pour retrouver les lettres auxquelles ils correspondent | oui | voyelles, fricatives s/r/f/v/j/ch, liquide l | prolonger le phonème avec la main |
| 45 | 5 | Principe alphabétique — le son des lettres | GS | À partir de 5 ans | Connaître la valeur sonore des lettres | — | toutes les lettres, hormis les occlusives | toucher la lettre qui fait le son entendu |

<!-- FIN TABLE GENEREE -->

## 4. Le palier de sortie

Sept réussites, toutes tirées de la colonne « à partir de 5 ans ». Quatre se vérifient dans l'application, trois non — et il faut le dire avant de promettre quoi que ce soit.

| Réussite | Où elle se vérifie |
|---|---|
| Reconnaître et nommer toutes les lettres d'un mot dans les trois graphies | **dans l'app** |
| Connaître le nom des lettres de l'alphabet | **dans l'app** |
| Connaître la valeur sonore des lettres, hormis les occlusives | **dans l'app** |
| Repérer une rime, localiser un phonème, trouver l'intrus à l'initiale | **dans l'app** |
| Épeler les lettres d'un mot connu afin qu'un tiers puisse l'écrire | hors app, au bilan |
| Prononcer avec exactitude l'ensemble des trente-six phonèmes | hors app — il faut entendre la prononciation |
| Prononcer les couples `ch/s, ch/j, ch/z` et les doubles consonnes `br/cr/bl/pl/sl` | hors app — il faut entendre la prononciation |

Les trois dernières lignes ne sont pas des échecs : ce sont les **limites déclarées** de la tranche. Une application qui prétendrait les vérifier sans micro mentirait.

## 5. La règle de contenu, équivalent GS de la déchiffrabilité

> **Un exercice de GS n'emploie que des mots connus de l'enfant à l'oral, et que des phonèmes déjà travaillés.**

La raison est la même qu'au CP, retournée : au CP, un mot non déchiffrable empêche de lire ; à la GS, un mot inconnu empêche de **découper**. On ne peut pas compter les syllabes d'un mot qu'on ne connaît pas, ni entendre une rime dans un mot qu'on n'a jamais dit.

Cette règle est désormais outillée : `outils/mots-gs.json` porte **44 mots** avec leur découpe syllabique orale, et `outils/verifier-corpus.py` refuse une découpe qui ne redonne pas le mot exactement.

## 6. Ce que la décision « pas de reconnaissance vocale » coûte à la GS

C'est ici que la décision 3 pèse le plus lourd. À la GS, presque tout est oral : dire le nombre de syllabes, répéter une paire distinctive, dire un mot qui rime. Sans micro, **l'application n'entend rien**.

La parade tient en une règle de conception :

> **Toute consigne se donne par la voix, et toute réponse se donne par le geste.**

L'enfant ne *dit* pas le nombre de syllabes : il pose un jeton par syllabe, ou touche un dé. Il ne *répète* pas un mot qui rime : il touche l'image qui rime. Chaque unité de la table porte, en dernière colonne, l'action attendue — c'est elle qui rend l'unité implémentable sans micro.

Le coût de cette règle est un **corpus audio de 207 fichiers**, inventorié dans `contenu/LUDOLIRE-CORPUS-AUDIO-GS.md` : 30 phonèmes isolés (les six occlusives n'ont pas d'isolé), 36 mots porteurs, 26 noms de lettres, 20 consignes, 7 retours, et 88 prises de mots. Une voix humaine, pas une synthèse.

## 7. Ce qui reste à produire

- **Le corpus audio** — inventorié, pas enregistré. Voir `contenu/LUDOLIRE-CORPUS-AUDIO-GS.md`.
- **Les images** — chaque mot du corpus et chaque paire distinctive ont besoin d'une illustration. Le rendu oral du jeu de syllabes en dépend directement.
- **Les exercices**, un par unité au minimum, chacun avec sa consigne orale et son geste de réponse.
- **L'extension du corpus de mots** — 44 mots sont un point de départ, pas un aboutissement.

## 8. Ce que cette table ne règle pas

- **L'ordre n'est pas validé en classe.** Il suit la logique du programme (du son familier au phonème, de la syllabe à l'attaque, de l'oreille à la lettre) ; il n'a pas été éprouvé.
- **Le découpage en cinq périodes est le nôtre.** Le programme organise par âge ; nous traduisons. La traduction est raisonnable, elle n'est pas officielle.
- **L'attribution aux colonnes d'âge repose sur une extraction.** Elle a été relevée en mode « layout », ce qui est fiable pour les colonnes entières, mais un item à cheval sur deux colonnes dans le PDF publié resterait ambigu. Le champ `colonne` rend l'attribution contestable item par item — c'est le but.
- **Le corpus de mots n'est pas validé.** La règle du § 5 dit ce qu'il doit être ; les 44 mots sont notre proposition.
