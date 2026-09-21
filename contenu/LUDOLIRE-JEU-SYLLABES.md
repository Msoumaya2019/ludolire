# Ludo'Lire — Le mot à trous (jeu de syllabes manquantes)

**Statut :** proposition. Banque de 42 items — 84 intruses — écrite, dérivée et vérifiée. Version 0.2.0.
**Source de vérité :** `outils/jeu-syllabes.json`. Le tableau du § 5 en est le rendu, produit par `outils/generer-table.py`.
**Dépend de :** `outils/mots-gs.json` et `outils/mots-cp.json` (les mots), `outils/collisions-fr.json` (les reconstitutions interdites), `contenu/LUDOLIRE-IMAGES-GS.md` (l'image qui identifie le mot au rendu oral), `contenu/LUDOLIRE-PROGRESSION-GS.md` (les unités servies).

---

## 1. La mécanique

Un mot connu, découpé en syllabes, une case par syllabe. **Une case est vide.** En bas de l'écran, un choix de cartes. L'enfant choisit la carte qui manque et la fait glisser dans le trou.

L'exercice entraîne la même chose que l'unité « dénombrer les syllabes », mais dans l'autre sens : là, l'enfant découpe un mot entendu ; ici, il **reconstruit** un mot à partir de ses morceaux. C'est la manipulation syllabique du programme — supprimer, ajouter, remplacer, fusionner — rendue jouable.

## 2. Ce sont les intruses qui font l'exercice

C'est le point de conception qui décide de tout le reste.

**Une intruse lointaine rend le jeu devinable.** Si le mot est `banane` et que le choix est `na` / `ri`, l'enfant entend « ri » et sait que ce n'est pas ça — sans jamais avoir discriminé quoi que ce soit. Il réussit, et n'apprend rien.

**Une intruse voisine oblige à discriminer.** Si le choix est `na` / `ma` / `ta`, l'enfant doit entendre la différence entre /n/, /m/ et /t/ pour trouver la bonne carte. C'est cette différence-là que la GS travaille — et c'est exactement ce que le programme demande : « articuler distinctement les couples de consonnes proches », « discriminer et identifier les mots auditivement proches ».

### 2.1 Pourquoi deux intruses, et pas une

La banque a d'abord été écrite avec **une seule intruse**. C'est une erreur, et elle se voit à l'arithmétique : à une intruse, l'enfant a **une chance sur deux** de tomber juste sans rien discriminer. Ce n'est pas un exercice, c'est un pile ou face.

À deux intruses, la chance tombe à une sur trois — et surtout, chaque mauvaise carte est une voisine, donc il faut vraiment entendre la différence. La banque est passée de 42 à **84 intruses**, dont 76 consonantiques et 8 vocaliques.

### 2.2 La règle, en deux sortes

Chaque intruse est une **voisine** de la syllabe cachée, et d'une des deux sortes :

- **consonantique** — elle partage la voyelle et la coda, et n'en diffère que par la consonne d'attaque, prise dans une paire de consonnes proches. C'est **la carte qui compte** : c'est la consonne proche qui fait trébucher un lecteur débutant. 76 des 84 intruses sont de cette sorte.
- **vocalique** — elle partage l'attaque et la coda, et n'en diffère que par la voyelle, prise dans une paire de voyelles proches. C'est un **complément, pas un équivalent** : une voyelle se distingue plus facilement qu'une consonne. On n'y a recours que quand la syllabe n'offre pas deux voisines consonantiques.

Une intruse **lointaine**, qui ne partage ni la voyelle ni la consonne, est interdite. Elle s'écarte d'emblée et n'ajoute aucune difficulté.

### 2.3 La troisième condition : le mot reconstitué

Les deux premières conditions ne suffisent pas. Si l'intruse placée dans le trou reconstitue un **mot français que l'enfant connaît**, la faute ne se voit plus : l'enfant produit un mot, ce mot est un mot, et il peut le tenir pour juste.

`poisson` avec l'intruse `bois` donne `boisson`. `mouton` avec `bou` donne `bouton`. `pomme` avec `pe` donne `pompe`. Ce sont trois vrais défauts, trouvés en imprimant les 84 reconstitutions et en les lisant une par une — et **`bouton` n'a été vu qu'à la deuxième lecture**.

Le critère n'est pas « est-ce un mot français ? » mais « l'enfant peut-il le prendre pour juste ? ». Un mot réel mais inconnu ne gêne pas : l'enfant entend le résultat, ne le reconnaît pas, et sait que ce n'est pas le mot cherché. `rune`, `écale` ou `camard` sont tolérés pour cette raison. Un **homophone** compte comme familier : `mure` se prononce comme `mûre`, donc `mure` est interdit.

Sept reconstitutions sont interdites et évitées par la dérivation ; sept autres sont tolérées et déclarées, chacune avec sa raison. La liste est dans `outils/collisions-fr.json` — et elle est **incomplète par construction** : sans lexique embarqué, elle ne contient que ce qu'une lecture humaine a vu. C'est une garantie de non-régression, pas d'exhaustivité.

### 2.4 Comment la banque est produite

La banque n'est plus écrite à la main. Chercher, pour chacun des 42 mots, un trou dont la syllabe cachée admette deux voisines **est un calcul** — et le faire à la main est précisément ce qui avait produit la banque à une intruse.

`outils/proposer-intruses.py` dérive et fige la banque. Ce qui reste un jugement, et n'est donc pas calculé : le choix du trou gardé quand plusieurs conviennent, et le champ `sert`. Ces deux valeurs sont lues dans la banque existante et préservées à chaque dérivation. `verifier-corpus.py` vérifie ensuite le résultat — et il a refusé deux fois, ce qui est exactement son rôle :

- d'abord parce que les secondes intruses introduisaient des graphèmes non encore enseignés au rang de l'item (`lama` au rang 10 recevait `pa` et `ba`) ;
- ensuite parce que `poisson` ne pouvait recevoir deux voisines déchiffrables à son rang.

Le second refus a produit une distinction utile : **le rang d'un item n'est pas celui de son mot, c'est celui de sa carte la plus tardive.** `poisson` se déchiffre au rang 21 ; `an` n'arrive qu'au rang 22. L'item `K12` est donc déclaré au rang 22, et le mot reste déchiffrable — c'est la seule issue honnête.

## 3. Le problème : à la GS, l'enfant ne lit pas

Le jeu tel qu'on l'imagine — un mot écrit avec un trou, des cartes de syllabes écrites — suppose que l'enfant **lise les cartes**. À la GS, il ne le fait pas. Une carte écrite ne serait pas un exercice difficile : ce serait un exercice impossible.

Deux solutions, et une seule est honnête.

| | Rendu oral | Rendu écrit |
|---|---|---|
| **Quand** | toute la tranche GS | CP, au rang indiqué par l'item |
| **Le mot** | son image, une seule ; la découpe est montrée par des cases vides | le mot écrit, avec un blanc |
| **Une carte** | un bouton sonore : l'appui fait entendre la syllabe | la syllabe écrite |
| **Ce que l'enfant fait** | il écoute, il compare, il place | il décode, il compare, il place |

**Une correction sur ce point.** Une première version de ce document disait « le mot est montré comme une suite d'images, une par syllabe ». C'est irréalisable, et l'erreur mérite d'être notée parce qu'elle est facile à refaire : **il n'y a pas d'image de « na »**. Ce qu'on montre, c'est le **mot entier** par son image ; la découpe syllabique est montrée par des cases vides, une par syllabe, qui disent combien de syllabes et non lesquelles. C'est l'image qui identifie le mot — ce qui rend la contrainte d'ambiguïté de `contenu/LUDOLIRE-IMAGES-GS.md` d'autant plus lourde.

**Ce n'est pas une version dégradée.** À la GS, l'objectif est phonologique : entendre et manipuler des sons. Le rendu oral n'enlève rien à l'exercice, il le met au bon niveau. C'est le rendu écrit qui serait hors sujet.

## 4. Trois régimes de légalité, pas deux

Il faut être précis sur ce qui est permis à chaque endroit, parce que les trois régimes n'obéissent pas à la même règle.

1. **GS, rendu oral** — aucune contrainte de graphème : le mot est *entendu*. La seule contrainte est celle de la tranche : le mot doit être **connu de l'enfant à l'oral**. C'est `outils/mots-gs.json` qui la porte.
2. **GS, rendu écrit** — **impossible**, et il faut le dire. À la GS, l'enfant connaît le *nom* de toutes les lettres, mais la valeur sonore est connue « hormis les occlusives ». Une carte `ba` ou `pa` demande de passer de la lettre au son : c'est hors de portée. Et les digrammes (`ou`, `an`, `on`, `ch`) sont du CP. Le rendu écrit de la GS se réduirait à des syllabes consonantiques sans occlusive — un jeu appauvri qui n'apprend rien de plus que le rendu oral.
3. **CP, rendu écrit** — **la version décrite au départ, telle quelle**, avec une contrainte : chaque carte et chaque mot doivent être déchiffrables au rang de l'item. Le contrôle les éprouve avec le même segmenteur que les textes de lecture.

Autrement dit : le jeu écrit existe, il est écrit, et il s'ouvre avec la tranche CP. La GS en prend la moitié orale.

## 5. La banque d'items

42 items : 30 au rendu oral pour la GS, 12 au rendu écrit pour le CP. La colonne « Trou » donne le numéro de la syllabe manquante, en comptant à partir de 1.

<!-- DEBUT TABLE GENEREE -->

| Item | Rendu | Rang | Mot | Syllabes | Trou | La carte à trouver | Intruse 1 | Intruse 2 | Sert l'unité |
|---|---|---|---|---|---|---|---|---|---|
| `J01` | oral | — | **banane** | ba-na-ne | 2 | `na` | `ma` (m/n, consonne) | `ta` (t/n, consonne) | 13 |
| `J02` | oral | — | **tomate** | to-ma-te | 2 | `ma` | `pa` (p/m, consonne) | `ba` (b/m, consonne) | 13 |
| `J03` | oral | — | **papa** | pa-pa | 2 | `pa` | `ba` (p/b, consonne) | `ma` (p/m, consonne) | 13 |
| `J04` | oral | — | **vélo** | vé-lo | 2 | `lo` | `no` (l/n, consonne) | `ro` (l/r, consonne) | 13 |
| `J05` | oral | — | **café** | ca-fé | 2 | `fé` | `vé` (f/v, consonne) | `fè` (é/è, voyelle) | 13 |
| `J06` | oral | — | **gâteau** | gâ-teau | 2 | `teau` | `deau` (t/d, consonne) | `neau` (t/n, consonne) | 13 |
| `J07` | oral | — | **jupe** | ju-pe | 1 | `ju` | `chu` (ch/j, consonne) | `zu` (j/z, consonne) | 13 |
| `J08` | oral | — | **pomme** | pom-me | 2 | `me` | `be` (b/m, consonne) | `ne` (m/n, consonne) | 13 |
| `J09` | oral | — | **zèbre** | zè-bre | 1 | `zè` | `sè` (s/z, consonne) | `jè` (j/z, consonne) | 13 |
| `J10` | oral | — | **lapin** | la-pin | 1 | `la` | `na` (l/n, consonne) | `ra` (l/r, consonne) | 13 |
| `J11` | oral | — | **maison** | mai-son | 1 | `mai` | `pai` (p/m, consonne) | `bai` (b/m, consonne) | 13 |
| `J12` | oral | — | **canard** | ca-nard | 2 | `nard` | `mard` (m/n, consonne) | `tard` (t/n, consonne) | 13 |
| `J13` | oral | — | **mouton** | mou-ton | 1 | `mou` | `pou` (p/m, consonne) | `nou` (m/n, consonne) | 13 |
| `J14` | oral | — | **cheval** | che-val | 1 | `che` | `je` (ch/j, consonne) | `se` (ch/s, consonne) | 13 |
| `J15` | oral | — | **bonbon** | bon-bon | 1 | `bon` | `pon` (p/b, consonne) | `mon` (b/m, consonne) | 13 |
| `J16` | oral | — | **avion** | a-vion | 2 | `vion` | `fion` (f/v, consonne) | `vuon` (i/u, voyelle) | 13 |
| `J17` | oral | — | **soleil** | so-leil | 1 | `so` | `zo` (s/z, consonne) | `cho` (ch/s, consonne) | 13 |
| `J18` | oral | — | **valise** | va-li-se | 3 | `se` | `ze` (s/z, consonne) | `che` (ch/s, consonne) | 13 |
| `J19` | oral | — | **cerise** | ce-ri-se | 3 | `se` | `ze` (s/z, consonne) | `che` (ch/s, consonne) | 13 |
| `J20` | oral | — | **girafe** | gi-ra-fe | 2 | `ra` | `la` (l/r, consonne) | `rè` (a/è, voyelle) | 13 |
| `J21` | oral | — | **koala** | ko-a-la | 3 | `la` | `na` (l/n, consonne) | `ra` (l/r, consonne) | 13 |
| `J22` | oral | — | **pyjama** | py-ja-ma | 3 | `ma` | `pa` (p/m, consonne) | `ba` (b/m, consonne) | 13 |
| `J23` | oral | — | **cartable** | car-ta-ble | 2 | `ta` | `da` (t/d, consonne) | `na` (t/n, consonne) | 13 |
| `J24` | oral | — | **chocolat** | cho-co-lat | 1 | `cho` | `jo` (ch/j, consonne) | `so` (ch/s, consonne) | 13 |
| `J25` | oral | — | **éléphant** | é-lé-phant | 2 | `lé` | `né` (l/n, consonne) | `ré` (l/r, consonne) | 13 |
| `J26` | oral | — | **parapluie** | pa-ra-pluie | 1 | `pa` | `ba` (p/b, consonne) | `ma` (p/m, consonne) | 13 |
| `J27` | oral | — | **crocodile** | cro-co-di-le | 3 | `di` | `ti` (t/d, consonne) | `ni` (d/n, consonne) | 13 |
| `J28` | oral | — | **téléphone** | té-lé-pho-ne | 4 | `ne` | `me` (m/n, consonne) | `te` (t/n, consonne) | 13 |
| `J29` | oral | — | **école** | é-co-le | 3 | `le` | `ne` (l/n, consonne) | `re` (l/r, consonne) | 13 |
| `J30` | oral | — | **ananas** | a-na-nas | 3 | `nas` | `mas` (m/n, consonne) | `tas` (t/n, consonne) | 13 |
| `K01` | ecrit | 10 | **lune** | lu-ne | 1 | `lu` | `nu` (l/n, consonne) | `ru` (l/r, consonne) | 23 |
| `K02` | ecrit | 10 | **lama** | la-ma | 1 | `la` | `na` (l/n, consonne) | `ra` (l/r, consonne) | 23 |
| `K03` | ecrit | 10 | **mule** | mu-le | 2 | `le` | `ne` (l/n, consonne) | `lé` (e/é, voyelle) | 23 |
| `K04` | ecrit | 10 | **rame** | ra-me | 2 | `me` | `ne` (m/n, consonne) | `mé` (e/é, voyelle) | 23 |
| `K05` | ecrit | 10 | **lime** | li-me | 1 | `li` | `ni` (l/n, consonne) | `lu` (i/u, voyelle) | 23 |
| `K06` | ecrit | 11 | **lilas** | li-las | 2 | `las` | `nas` (l/n, consonne) | `ras` (l/r, consonne) | 23 |
| `K07` | ecrit | 14 | **tapis** | ta-pis | 1 | `ta` | `na` (t/n, consonne) | `tè` (a/è, voyelle) | 14 |
| `K08` | ecrit | 17 | **dodu** | do-du | 1 | `do` | `to` (t/d, consonne) | `no` (d/n, consonne) | 17 |
| `K09` | ecrit | 18 | **papa** | pa-pa | 1 | `pa` | `ba` (p/b, consonne) | `ma` (p/m, consonne) | 18 |
| `K10` | ecrit | 18 | **bébé** | bé-bé | 1 | `bé` | `pé` (p/b, consonne) | `mé` (b/m, consonne) | 18 |
| `K11` | ecrit | 21 | **mouton** | mou-ton | 1 | `mou` | `pou` (p/m, consonne) | `nou` (m/n, consonne) | 21 |
| `K12` | ecrit | 22 | **poisson** | pois-son | 2 | `son` | `chon` (ch/s, consonne) | `san` (on/an, voyelle) | 21 |

<!-- FIN TABLE GENEREE -->

## 6. Le retour, sans micro

L'application ne note pas la prononciation : elle n'entend pas. Le seul verdict possible est **mécanique** — le mot reconstitué est-il le mot attendu ? — et il est **audible** : l'app fait entendre le mot obtenu.

C'est suffisant, et c'est même mieux qu'un score. Un enfant qui place `ma` dans `banane` n'a pas besoin qu'on lui dise qu'il a faux : il entend « bamane », et il entend que ce n'est pas le mot. Le retour est dans l'oreille, pas dans une pastille verte.

## 7. Ce que le jeu ne vérifie pas

- **L'articulation de la paire par l'enfant.** Le jeu entraîne la discrimination — entendre la différence — pas la production. La production se vérifie à l'oreille d'un adulte, hors application.
- **La raison d'une erreur.** Un enfant qui place `ma` peut avoir mal entendu, ou avoir confondu les cartes, ou s'être trompé de case. L'app ne distingue pas les trois.
- **Les reconstitutions françaises non déclarées.** Le contrôle ne sait pas si le mot reconstitué est un mot français : il ne connaît que la liste écrite dans `collisions-fr.json`. Cette liste est incomplète par construction, et une intruse ajoutée plus tard doit être relue à la main.
- **L'intérêt du jeu.** Aucun script ne mesure si l'enfant a envie de revenir demain.

## 8. Comment on vérifie

```bash
python outils/verifier-corpus.py        # découpes, intruses, voisinage, collisions, rangs, déchiffrabilité
python outils/proposer-intruses.py      # imprime les voisines possibles de chaque trou, n'écrit rien
python outils/generer-table.py          # met la table à jour depuis le JSON
```

`verifier-corpus.py` refuse un item dont :
- le mot est absent des deux banques ;
- le trou tombe hors du mot ;
- **le nombre d'intruses n'est pas deux** — à une seule, l'enfant a une chance sur deux de tomber juste sans discriminer ;
- une intruse est en réalité une syllabe du mot — ce serait ambigu ;
- une intruse n'est pas une voisine : elle ne partage ni la voyelle ni la consonne, donc elle s'écarte d'emblée ;
- la paire déclarée ne produit pas réellement l'intruse, ou la sorte déclarée ne correspond pas à la règle ;
- **l'intruse reconstitue un mot français familier** — l'enfant peut le tenir pour juste ;
- au rendu écrit, une carte ou le mot n'est pas déchiffrable au rang déclaré ;
- au rendu écrit, le rang est inférieur au rang minimal du mot ;
- au rendu oral, un rang est déclaré — le rendu oral n'en a pas besoin.

Il refuse aussi une déclaration de `collisions-fr.json` qui décrit une banque qui n'existe plus — un mot déclaré toléré que la banque ne produit plus. Ce contrôle-là a attrapé deux déclarations périmées lors de sa première exécution.
