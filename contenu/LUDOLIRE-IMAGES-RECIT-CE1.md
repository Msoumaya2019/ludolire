# Ludo'Lire — Les images de récit du CE1

Huit dessins, pour deux exercices : quatre moments du texte « L'éléphant et le
téléphone » (unité 14) et quatre du texte « Le chat » (unité 37). L'enfant lit le
texte, puis il touche les quatre images dans l'ordre où les moments arrivent.

Ces images ne portent pas un mot — c'est le métier des icônes — elles portent un
**moment**. Et ce n'est pas une nuance de vocabulaire : une icône se vérifie
seule, une image de récit ne se vérifie que **dans son ordre**. C'est ce qui
justifie un corpus à part, et un contrôle à part.

- Données : `outils/images-recit-ce1.json`
- Dessins : `outils/generer-images.py --recit` → `contenu/images-recit-ce1/`
- Contrôle : `outils/verifier-images.py --recit`
- Épreuve du contrôle : `outils/tester-images-recit.py`

---

## 1. Ce que ces images doivent faire

Quatre images mélangées doivent pouvoir être remises dans l'ordre du texte. Cela
impose deux choses, et la seconde est celle qu'on oublie :

1. chaque image doit être **reconnaissable** au premier coup d'œil, à la taille de
   l'application, comme les icônes ;
2. chaque image doit se **distinguer des trois autres** par un repère déclaré.

La seconde est la vraie contrainte. Deux images qui se ressemblent sont deux
images interchangeables : l'exercice n'a plus de réponse, et rien dans le code ne
le signale. Le corpus déclare donc, étape par étape, sur quoi le dessin s'appuie
pour être reconnu — *le personnage*, *le cadre*, *le moment du jour*, *le décor*,
*le geste du corps* — et le contrôle refuse deux étapes d'un même récit qui
s'appuieraient sur le même repère.

Un repère est ce que le dessinateur met en avant, pas une propriété exclusive :
Maman rit à l'étape 4 du premier récit, et le bébé est à l'étape 4 du second. Ce
qui compte est que les quatre étapes d'un récit ne s'appuient pas sur la même
idée, sans quoi l'une des quatre est de trop.

## 2. Le cadrage, par référence transitive

Ce corpus ne recopie pas le cadrage de la GS — deux copies d'une même règle
divergent, et c'est ce qui a valu quatre mots refusés et un mot lu de travers à la
tranche précédente. Il **référence** le corpus lexical du CE1, qui référence
lui-même celui de la GS.

Il a fallu pour cela que la référence devienne **transitive** : le corpus du CE1
n'a qu'un saut à faire, celui du récit en a deux, et le contrôle suit la chaîne
jusqu'au fichier qui porte le cadrage. Une chaîne qui s'arrête sans l'atteindre
est refusée ; une chaîne qui boucle aussi, même si ce cas n'est pas atteignable
depuis le corpus — la garde reste, et le harnais dit qu'il ne l'éprouve pas.

## 3. Le corpus en trois tableaux

Le premier tableau est le seul endroit où les moments sont écrits **dans l'ordre**
— c'est l'information même de ce corpus, et un tableau trié par identifiant la
perdrait. Le deuxième dit les confusions redoutées et leur parade. Le troisième
dit les exercices de la **même mécanique** qui ne jouent pas sur des images : un
document qui ne montrerait que ses deux récits laisserait croire que la banque
n'en compte que deux.

<!-- DEBUT TABLE GENEREE -->

| Exercice | Ordre | Étape | Moment | Ligne citée | Repère |
|---|---|---|---|---|---|
| `E19` | 1 | `e19_1` | Papa tient une photo | « Papa a une photo. » | le personnage |
| `E19` | 2 | `e19_2` | L'éléphant au téléphone, vu dans la photo | « Sur la photo, un éléphant a un téléphone. » | le cadre |
| `E19` | 3 | `e19_3` | L'éléphant arrive à la maison, le soir | « Le soir, l'éléphant a rejoint la maison. » | le moment du jour |
| `E19` | 4 | `e19_4` | Maman rit | « Maman rit encore. » | le geste du corps |
| `E45` | 1 | `e45_1` | Le chat dort sur une chaise, le jour | « Le jour, il dort sur une chaise. » | le moment du jour |
| `E45` | 2 | `e45_2` | Le chat lèche sa patte | « Il lave sa robe avec sa langue. » | le geste du corps |
| `E45` | 3 | `e45_3` | Le chat monte à l'échelle | « Il monte sur l'échelle. » | le décor |
| `E45` | 4 | `e45_4` | Le chat et l'enfant, l'un près de l'autre | « Le chat est un bon compagnon. » | le personnage |

| Étape | Craint | Pourquoi | Parade |
|---|---|---|---|
| `e19_1` | `e19_2` | les deux étapes montrent une photo : ici elle est tenue, là c'est elle qui remplit l'image, et qui regarde les deux y voit deux fois une photo | à l'étape 1 le personnage est là et le contenu de la photo n'est pas dessiné ; à l'étape 2 il n'y a aucun personnage et le cadre fait tout le tour de l'image |
| `e19_2` | `e19_1` | les deux étapes montrent une photo | le cadre fait ici tout le tour, et aucun personnage n'y figure — l'inverse exact de l'étape 1 |
| `e19_2` | `e19_3` | l'éléphant est dans les deux étapes : c'est la seule figure du récit qui revient | à l'étape 2 il est dans un cadre et tient un téléphone ; à l'étape 3 il est dehors, devant une maison, sous la lune |
| `e19_3` | `e19_2` | l'éléphant est dans les deux étapes | ici l'éléphant est tourné vers la maison et il n'y a ni cadre ni téléphone |
| `e45_1` | `e45_4` | ce sont les deux étapes où le chat ne fait rien : elles sont interchangeables tant qu'on ne regarde que le chat | ici il est seul, couché, sur une chaise, sous un soleil ; là il est debout près d'un enfant, et il n'y a ni chaise ni soleil |
| `e45_2` | `e45_3` | le chat est debout dans les deux étapes, et c'est la même figure : seule la patte levée les sépare | ici la patte est au museau ; là le chat est posé sur un barreau, entre les deux montants d'une échelle |
| `e45_3` | `e45_2` | le chat est debout dans les deux étapes | l'échelle est le seul décor de tout le corpus, et elle ne peut pas être confondue avec une chaise |
| `e45_4` | `e45_1` | ce sont les deux étapes où le chat ne fait rien, donc celles qu'on peut intervertir sans que le geste proteste | ici le bébé est là et le chat est debout ; là le chat est seul et couché |

| Exercice | Raison |
|---|---|
| `E39` | L'unité 32 ne demande pas d'images : elle demande de réaliser ce qu'un texte prescriptif dit, et l'ordre des étapes d'une recette est DANS le texte. Dessiner la recette retirerait la lecture, qui est tout l'objet de l'unité — son geste annoncé est « ordonner les étapes d'une recette dans l'ordre où le texte les donne », et il ne dit pas le mot image. |
| `E51` | L'unité 38 est une unité de lecture en autonomie : son geste annoncé est « un texte entier, et les questions des unités précédentes ». Les cinq étapes de « La pomme d'or » sont des phrases, et c'est en les lisant qu'on les ordonne. L'image ne remplacerait pas la lecture, elle l'éviterait. |

<!-- FIN TABLE GENEREE -->

## 4. Comment les figures sont prises

Les figures d'une scène ne sont **pas redessinées** : ce sont celles de la série —
le même papa, le même éléphant, le même chat — placées et réduites. Les
redessiner donnerait deux éléphants, et c'est ainsi qu'une application se met à
parler deux langues.

Réduire une figure réduit aussi son contour : la scène porterait un trait de 2 px
au milieu de figures à 4 px. La parade habituelle serait
`vector-effect="non-scaling-stroke"` — **le moteur de rendu l'ignore**. Cela a été
mesuré plutôt que supposé : à l'échelle 0,25, le contour rendu fait 1 px, que
l'attribut soit posé sur le groupe qui porte le trait, sur la forme, ou nulle
part. Trois variantes, un seul résultat.

La compensation est donc écrite à la main — et c'est mieux ainsi : le facteur est
**dans le fichier**, donc le contrôle peut le relire. Il refuse un couple
(échelle, épaisseur) dont le produit ne redonne pas 4 px. C'est le contrôle que le
générateur ne peut pas faire sur lui-même : il écrit deux nombres, et c'est leur
produit qui décide de ce qu'on voit.

Une figure réemployée garde sa pose, **sauf ce qu'il faut pour dire le moment** :
les deux yeux de Maman sont recouverts de la couleur du visage et redessinés en
arcs, sans quoi elle ne rirait pas, elle regarderait. C'est visible dans le code,
et c'est le seul endroit où une figure de la série est retouchée.

## 5. Quatre exercices remettent un récit dans l'ordre, deux seulement ont des images

C'est le contrôle qui l'a trouvé, pas la lecture du cadrage — le cadrage ne
parlait que des unités 14 et 37. Quatre exercices de la banque emploient la
mécanique `ordonner_recit` : **E19** (unité 14), **E39** (unité 32), **E45**
(unité 37) et **E51** (unité 38).

Ce n'est pas « tout exercice de remise en ordre » qui a besoin d'images : c'est
tout exercice **dont l'unité annonce un geste d'image**. Et c'est la progression
qui tranche, unité par unité — la même source que le corpus lexical emploie déjà :

| Unité | Ce que la progression annonce | Images ? |
|---|---|---|
| 14 | « remettre des **images** dans l'ordre du récit » | oui |
| 32 | « ordonner les **étapes d'une recette** dans l'ordre où le texte les donne » | non |
| 37 | « ordonner les **images** du récit, qui tiennent lieu de résumé » | oui |
| 38 | « un **texte** entier, et les questions des unités précédentes » | non |

Les deux unités qui n'annoncent pas d'images ne sont pas un manque : elles
demandent de **lire**. L'unité 32 demande de réaliser ce qu'un texte prescriptif
dit, et l'ordre des étapes d'une recette est dans le texte ; l'unité 38 est une
unité de lecture en autonomie, et les cinq étapes de « La pomme d'or » sont des
phrases. Dessiner l'une ou l'autre retirerait la lecture, qui est tout leur objet.

Le corpus les **déclare** dans `exercices_sans_images`, avec leur raison. Le
contrôle refuse trois choses, et chacune a été falsifiée : un exercice dont
l'unité annonce un geste d'image et que nul récit ne couvre ; un exercice qui joue
sur le texte et qui n'est pas déclaré comme tel ; et une déclaration qui
contredirait la progression.

## 6. Ce que le contrôle voit, et ce qu'il ne voit pas

**Ce qu'il voit**, et c'est beaucoup :

- **l'ordre**, qui est le contrôle central : la ligne citée par chaque étape est
  cherchée **littéralement** dans le fichier du texte, et sa position doit croître
  avec l'ordre de l'étape. Sans lui, quatre dessins pourraient être rangés dans un
  ordre que le texte ne porte pas, et rien ne le dirait ;
- que les images montrent bien **le texte de l'exercice** — le texte et son rang
  sont comparés à ceux de la banque et à l'en-tête du fichier ;
- que le nombre d'étapes est celui que la **série** de l'exercice annonce ;
- les repères : liste fermée, pas deux fois le même dans un récit, aucun repère
  déclaré et jamais employé ;
- la **réciprocité** des craintes de confusion : si une étape en craint une autre,
  l'autre la craint aussi ;
- le fichier : cadre, palette fermée, aucun texte, trait rendu de 4 px, et deux
  images qui ne peuvent pas être le même fichier à l'octet.

**Ce qu'il ne voit pas.** Il ne sait pas si un dessin est *reconnu* comme le
moment qu'il annonce. Un fichier peut être parfaitement conforme et montrer autre
chose. C'est la planche qui le donne à voir — `contenu/images-recit-ce1/planche.html`
et `planche.svg` — et l'œil qui le juge. Il ne voit pas non plus si l'ordre est
*juste* au sens du texte : il vérifie que l'ordre dessiné suit l'ordre des lignes,
pas que ces quatre moments sont les bons. Choisir les quatre moments est un acte
pédagogique, et il appartient au porteur du projet.

## 7. Ce que ce travail a fait apparaître

### 7.1 Le cadrage ne mentionnait que deux exercices sur quatre

Il annonçait « les images de récit des unités 14 et 37 » — huit dessins. Le
contrôle de couverture, écrit pour vérifier que *tout* exercice de remise en ordre
est couvert, a trouvé E39 et E51. Le premier réflexe a été de conclure à un
manque ; la progression a montré le contraire : ces deux unités demandent de lire,
pas de regarder. La conclusion n'est donc pas « il manque onze images », c'est
« deux exercices jouent sur le texte, et il faut le dire ». Un contrôle qui refuse
tout ne sert à rien ; un contrôle qui refuse ce qui n'aurait pas dû être fait a
obligé à trancher.

### 7.2 La référence de cadrage était transitive, et personne ne le savait

Le corpus du CE1 référençait la GS en un saut. Le corpus du récit en demande deux,
et le contrôle ne savait en faire qu'un. Ce n'est pas un défaut de la référence,
c'est un défaut du contrôle : il lisait `cadrage_de_reference` comme un chemin,
alors que c'est une chaîne. La résolution est maintenant unique et partagée par
les deux modes — deux résolutions auraient divergé.

### 7.3 Une garde qu'on ne peut pas éprouver depuis le corpus

La garde contre une chaîne de références qui boucle n'est pas atteignable en
mutant le corpus : `resoudre_cadrage` relit les fichiers référencés **sur le
disque**, donc muter la référence en mémoire ne change que le premier saut, et la
chaîne repart sur la vraie. La falsification l'a montré — l'essai était vert alors
qu'il visait un défaut réel. La garde reste, parce qu'un fichier mal édité la
déclenche ; mais le harnais **écrit** qu'il ne l'éprouve pas au lieu de laisser
croire que tout est couvert.

## 8. Ce qui reste

- **Relire les huit scènes**, une par une. Elles sont conformes au brief et
  contrôlées par script, mais aucun script ne juge si un dessin est
  reconnaissable. La planche les montre à 168 px — plus grand que l'application,
  qui les affiche à 112 px — parce qu'une scène se regarde de plus près qu'une
  icône : il y a quatre figures dedans, pas une.
- **Les deux récits seuls sont illustrés.** Si l'unité 32 ou l'unité 38 devaient
  un jour jouer sur des images, il faudrait onze dessins de plus — six pour la
  recette, cinq pour « La pomme d'or » — et la progression devrait changer
  d'abord, puisque c'est elle qui décide.
- **La ligne citée n'est pas affichée à l'enfant.** Les quatre moments se
  présentent nus ; c'est le texte, lu avant, qui les ordonne. Si l'application
  devait un jour montrer la phrase sous l'image, elle l'aurait — la citation est
  dans le corpus — mais ce serait un autre exercice.
