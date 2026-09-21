# Ludo'Lire — Les pseudo-mots du CE1

*Corpus de la tranche CE1 — `outils/pseudo-mots-ce1.json` → ce document.*
*Contrôlé par `outils/verifier-pseudo-mots.py`, éprouvé par `outils/tester-pseudo-mots.py`.*

Un pseudo-mot est une suite de lettres qui **se décode et qui ne se reconnaît pas**. C'est
l'objet le plus fragile de la tranche : il n'existe nulle part ailleurs que dans
l'application, il ne s'appuie sur aucun mot connu, et rien dans le lexique ne peut dire si on
l'a bien prononcé. Ce document dit d'où viennent les dix suites du corpus, ce que le contrôle
en refuse, et ce qu'il ne peut pas en voir.

---

## 1. Pourquoi un corpus à part

Le programme donne lui-même cinq exemples — doir, stag, choust, valin, cagnou — et deux
exercices de l'unité 35 les emploient. Tous deux les **portaient**, chacun dans son coin, et
la même liste de cinq se trouvait donc deux fois dans la banque.

Deux copies de la même chose divergent. Ici elles avaient déjà divergé, et dans le sens le
plus coûteux : `E42` fait **entendre** les cinq suites et les fait retrouver parmi trois
écrites ; `E43` les fait **lire** et demande de décider si c'est un mot. Les deux exercices de
la même unité travaillaient donc sur exactement les mêmes cinq suites. L'enfant qui venait de
toucher `valin` dans le premier n'avait plus besoin de le décoder dans le second — alors que
`E43` déclare lui-même entraîner « décoder d'abord, décider ensuite », et déclare ne pas
vérifier « ce que l'enfant fait d'un mot qu'il croit reconnaître sans le lire ». L'exercice
fabriquait exactement la situation qu'il dit ne pas mesurer.

Le corpus est désormais la seule copie. Les exercices **citent** un identifiant, le contrôle
le résout, et deux exercices de la même unité ne peuvent plus citer la même suite : c'est une
règle du contrôle, pas une intention.

---

## 2. Ce qu'est un pseudo-mot, et pourquoi sa lecture est dérivée

Un pseudo-mot n'a pas de prononciation à connaître : il n'est dans aucun dictionnaire. La
seule lecture qu'un enfant puisse en produire est **mécanique** — chaque graphie est lue par
la correspondance qui l'enseigne. C'est cette lecture-là qui est dérivée, et non déclarée :
elle est calculée avec `decouper_ce1` et `resoudre_ce1`, le décodeur du projet, puis chaque
correspondance est lue dans la table des phonèmes.

Déclarer la prononciation à la main aurait produit dix valeurs que rien n'aurait pu vérifier.
La dériver la rend vérifiable, et c'est **le script de l'enregistrement** : la voix dit ce que
le tableau du § 3 donne, et rien d'autre.

**La seule lettre muette admise est le `e` final.** Une consonne finale se lit donc par sa
correspondance : `doir` se dit /dwaʁ/, `choust` /ʃust/, `stag` /stag/. Ce n'est pas un oubli,
c'est la décision — la règle des consonnes finales muettes s'apprend mot par mot (« loup »,
« tabac », « fusil »), et un pseudo-mot n'est dans aucun lexique. Un enfant ne peut pas savoir
qu'une lettre finale d'un mot qu'il n'a jamais vu est muette ; le contrôle ne peut donc pas le
savoir à sa place.

### Une règle qui a été essayée, et qui ne marche pas

Les banques de mots du CP déclarent un **rang minimal** : un mot du CP doit être déchiffrable à
son rang et **pas au rang précédent**, sans quoi son rang n'est pas le rang minimal. L'idée
naturelle était de faire pareil pour les pseudo-mots — une suite déchiffrable dès le rang 1
n'entraîne rien de l'unité 35.

La mesure l'a tuée : **au CE1, tout le CP est acquis dès le rang 1** — le décodeur l'applique
ainsi, parce qu'au CE1 les trente correspondances du CP sont supposées connues. Un pseudo-mot
fait des seules graphies du CP est donc déchiffrable au rang 1, par construction. Mesuré sur
les cinq exemples du programme : `doir`, `choust` et `valin` sont déchiffrables au **rang 1**,
et ne portent **aucune** graphie que le CE1 enseigne ; `stag` au rang 26, `cagnou` au rang 9.
Le rang minimal ne dit donc rien ici, et la règle qui le remplace est celle de la
**complexité** : une suite est complexe quand elle porte au moins une graphie que le CE1
enseigne. L'objectif de l'unité 35 est de décoder des pseudo-mots **complexes** : le contrôle
refuse un exercice dont aucune suite citée n'est complexe.

---

## 3. Les pseudo-mots

<!-- DEBUT TABLE GENEREE -->

### Les 10 pseudo-mots

| Identifiant | Suite | Lecture dérivée | Graphies | Complexité | Origine | Cité par |
|---|---|---|---|---|---|---|
| `pm01` | `doir` | /dwaʁ/ | `oi`, `r` | simple | programme | `E42` |
| `pm02` | `stag` | /stag/ | `g` | simple | programme | `E42` |
| `pm03` | `choust` | /ʃust/ | `ch`, `ou` | simple | programme | `E42` |
| `pm04` | `valin` | /valɛ̃/ | `in` | simple | programme | `E42` |
| `pm05` | `cagnou` | /kaɲu/ | `gn`, `ou` | complexe | programme | `E42` |
| `pm06` | `flaption` | /flapsjɔ̃/ | `tion` | complexe | ecrit | `E43` |
| `pm07` | `trumpon` | /tʁœ̃pɔ̃/ | `um` | complexe | ecrit | `E43` |
| `pm08` | `pharmou` | /faʁmu/ | `ph` | complexe | ecrit | `E43` |
| `pm09` | `girou` | /ʒiʁu/ | `g`, `ou` | complexe | ecrit | `E43` |
| `pm10` | `poinche` | /pwɛ̃ʃ/ | `oin`, `ch` | complexe | ecrit | `E43` |

### Les 9 graphies dont la lecture ne se dérive pas

| Graphie | Unité qui l'enseigne | Ce que la table déclare |
|---|---|---|
| `ail` | 18 | /j/ |
| `aille` | 18 | /j/ |
| `eil` | 18 | /j/ |
| `eille` | 18 | /j/ |
| `euil` | 18 | /j/ |
| `euille` | 18 | /j/ |
| `ill` | 10 | /j/ |
| `ouille` | 18 | /j/ |
| `y` | 10 | /j/ |

<!-- FIN TABLE GENEREE -->

Les cinq premiers sont les exemples du programme, et le corpus les déclare comme tels : leur
modification est une décision pédagogique, et la déclaration la fait voir. Les cinq derniers
ont été écrits pour `E43`, une suite par graphie que le CE1 ajoute et que les cinq exemples ne
couvraient pas — `tion`, `um`, `ph`, le `g` doux, `oin`.

`um` mérite un mot : c'est la graphie dont l'absence dans la table avait fait refuser
« parfum » et lire « humble » de travers. Elle n'apparaît que dans une poignée de mots
français, et un pseudo-mot est précisément l'endroit où elle peut être exercée sans dépendre
d'un mot rare.

---

## 4. Ce que le contrôle refuse

- **Une suite qui est déjà un mot de l'application.** C'est la crainte que B35 déclare :
  « un pseudo-mot enregistré par erreur comme un mot deviendrait un mot ». Le contrôle ne
  regarde pas les textes du palier — il regarde **tout le lexique de l'application** : les deux
  banques de mots, le jeu de syllabes et ses intruses, le corpus audio, les images, les dix-huit
  textes du CE1, les cinq textes courts, les séries, les questions et les intrus des deux
  banques d'exercices. Une suite que l'enfant a déjà lue comme un mot n'est plus un pseudo-mot
  pour lui, et l'exercice lui demanderait alors de décider qu'un mot n'en est pas un.
- **Une suite qui se lit comme un mot connu.** Sa lecture mécanique est comparée à celle de
  toutes les formes du lexique. « musiqe » passerait le contrôle précédent — ce n'est pas un
  mot de l'application — et se lirait pourtant /myzik/ comme `musique` : l'exercice ferait lire
  l'homophone d'un mot connu.
- **Une suite qui n'est pas déchiffrable à l'unité de l'exercice qui la cite.** C'est toute la
  question de l'exercice : une suite trop complexe ne se décode pas, elle se devine.
- **Une graphie déclarée qui n'est pas dans la suite**, ou qui n'est rattachée à aucune
  correspondance enseignée.
- **Une complexité déclarée qui n'est pas celle de la table.**
- **Une origine menteuse** : une suite déclarée exemple du programme qui n'en est pas un, ou
  l'inverse.
- **Deux exercices de la même unité citant la même suite** — le défaut mesuré au § 1.
- **Une suite que personne ne cite**, et **une citation qui ne se résout pas**.
- Et, dans l'autre sens, **un mot réel offert par un exercice « vrai mot ou pas » qui ne serait
  dans aucun corpus de l'application** : on ne peut pas demander de reconnaître un mot qu'on n'a
  jamais lu.

Le contrôle a été falsifié avant d'être cru : `outils/tester-pseudo-mots.py` joue **20 corpus
faux** et un témoin, et **éprouve la dérivation de lecture sur douze mots réels** dont la
prononciation est connue. C'est la partie du banc qui compte le plus : une transcription qui
dériverait de travers serait verte partout ailleurs, et enverrait à l'enregistrement une
prononciation que les lettres ne donnent pas.

---

## 5. Ce que le contrôle ne voit pas

- **Qu'une suite ne soit pas un mot français.** Il n'y a pas de lexique embarqué. Le contrôle
  ne voit que les mots **de l'application** — ce qui est le seul cas où l'enfant l'aurait déjà
  lue comme un mot — et les homophones de ces mots. Une suite qui serait un mot français absent
  de l'application passerait. C'est la même limite que la liste des collisions du jeu de
  syllabes, et elle est déclarée pour la même raison.
- **La qualité exacte des voyelles.** La table donne **un** phonème par graphie : elle ne
  distingue pas le `o` ouvert du `o` fermé, et « école » s'y lit /ekol/. La transcription fixe
  la suite des sons et la place des muettes ; elle ne prétend pas à plus.
- **La plausibilité d'une suite.** Un pseudo-mot doit ressembler à un mot français sans en être
  un : c'est ce qui fait la difficulté de l'exercice. Aucun script ne juge cela.

---

## 6. Neuf graphies dont la table donne une étiquette de classe

C'est la découverte de ce travail, et elle est née d'un refus. Une suite avait été écrite avec
la graphie `ail`, et la lecture dérivée est sortie **/bʁɔ̃dj/** : le `a` avait disparu.

La table du CE1 déclare `/j/` pour **neuf graphies** — `ill`, `y`, `ail`, `eil`, `euil`,
`ouille`, `aille`, `eille`, `euille`. Or `/j/` est une **semi-consonne** : elle ne fait pas une
syllabe. Ce n'est donc pas la lecture de ces graphies, c'est **l'étiquette de la classe
qu'elles forment** — celle des graphies du /j/ en fin de mot. La lecture réelle se compose :
`ail` vaut /aj/, `euille` /œj/, `ill` /ij/. Et rien dans la table ne porte cette composition.

La distinction avec `qu`, `gu` et `ge` n'est pas arbitraire : ces trois-là contiennent aussi une
voyelle et rendent `/k/`, `/g/`, `/ʒ/`, qui sont des consonnes pleines — la voyelle y est muette
par convention, et la lecture est complète. Une graphie dont le phonème est **une semi-consonne
seule** alors qu'elle contient une voyelle est une étiquette de classe. La règle est dérivable
des tables, sans liste écrite à la main.

Conséquence : **aucune suite bâtie sur l'une de ces neuf graphies n'a de lecture dérivable**, et
aucune ne peut donc entrer dans ce corpus — il faudrait inventer sa prononciation, et c'est
exactement ce que la voix enregistrerait. La suite a été remplacée par `trumpon`.

**Le décodeur, lui, n'en souffre pas** : il n'a jamais besoin du phonème pour dire si un texte
est déchiffrable. C'est la transcription qui en avait besoin. Mais la leçon dépasse ce corpus :
une table qui déclare une **classe** là où on attend une **lecture** se relit autrement — et
c'est le même genre de défaut que le `um` de la nasale `un`, ou que la moitié muette de la
règle du `r` final : quelque chose est écrit, et quelque chose d'autre est mis en oeuvre.

---

## 7. Le besoin B35, et ce qu'il demandait vraiment

B35 disait : « aucun pseudo-mot n'est enregistré », et son détail ajoutait : « ils ne sont dans
aucun corpus, et ils ne peuvent pas y être : un pseudo-mot enregistré par erreur comme un mot
deviendrait un mot ».

La seconde moitié est la bonne, et c'est une crainte de **nommage**. Un pseudo-mot est un mot
pour le fichier qui le contient : rien, dans un nom de fichier, ne dit qu'il ne doit pas être
rangé avec les mots. Le corpus y répond sur deux plans :

- **l'enregistrement** : la famille s'appelle `pm`, les fichiers s'appellent `pm_<slug>.wav`, et
  ils ne voisinent pas avec les `mot_` du corpus. La spécification complète est dans `meta`
  (`enregistrement`) : niveau, silence, et surtout le script — la voix dit la suite telle que le
  tableau la transcrit, sans exemple avant et sans épeler ;
- **le contrôle** : une suite qui est déjà un mot de l'application est refusée. C'est la crainte
  de B35 rendue vérifiable.

Le reste de B35 est un **enregistrement à faire**, pas un contrôle à écrire, et il rejoint
B01a et B02 : ni les textes, ni les consignes, ni les mots du CE1, ni ces dix suites ne sont
enregistrés à ce jour. B35 quitte donc la liste des besoins, et l'enregistrement reste déclaré
là où il est : dans B01a, B02 et la spécification ci-dessus.

---

## 8. Ce qui reste

- **Les dix suites à enregistrer**, selon le script du § 3 et la spécification de `meta`.
- **Les mots réels de `E43`** — `montagne`, `soleil`, `poisson`, `cartable`, `musique` — sont
  contrôlés présents dans le lexique de l'application, mais **la relecture pédagogique de
  l'ensemble** reste au porteur du projet : le contrôle dit qu'une suite n'est pas un mot de
  l'application, il ne dit pas qu'elle est un bon pseudo-mot pour un enfant de CE1.
- **`E42` déclare trois écritures possibles par suite** (« chacune à retrouver parmi trois
  écrites ») et **ne les nomme pas**. C'est un manque de la même famille que celui que ce
  travail vient de solder : une matière portée par un exercice et invisible ailleurs. Il n'est
  pas comblé ici, et il est déclaré.
