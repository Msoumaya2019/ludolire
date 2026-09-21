# Ludo'Lire — Les illustrations du CE1

**Statut :** proposition à valider. Trois images sont produites et contrôlées ; les vingt-deux mots qui ne peuvent pas l'être sont déclarés avec leur raison. L'intérêt pédagogique se jugera en éprouvant l'application, pas à la lecture de ce document.
**Dépend de :** `outils/exercices-ce1.json` (les besoins B04, B13 et B30), `outils/cgp-ce1.json` (les graphies), `outils/verifier-textes-ce1.py` (le décodeur, qui dit si un mot est lisible), `outils/images-gs.json` (le cadrage, repris par référence).
**Suite de :** `contenu/LUDOLIRE-IMAGES-GS.md`. Ce document ne répète pas le cadrage de la GS : il dit **ce que le CE1 y change**.

---

## 1. L'image change de rôle

À la GS, l'image était le **seul** accès au mot : un enfant de cinq ans ne lit pas, et si l'image ne suffit pas, l'exercice n'est pas difficile, il est impossible. Le corpus de la GS est donc bâti sur une contrainte unique — *un mot connu à l'oral, illustrable sans ambiguïté* — et ses quarante-quatre images sont autant de portes d'entrée.

Au CE1, l'enfant lit. L'image ne porte plus le mot, elle le **vérifie** : on lit le mot écrit d'abord, et l'image confirme. Cela déplace trois choses, et chacune est devenue une règle du corpus.

1. **Le mot doit être lisible au rang de l'unité qui l'affiche.** Le contrôle le décode avec `verifier-textes-ce1.py` et refuse un mot que l'enfant ne peut pas encore lire. C'est la règle qui a écarté `poing` : la graphie `oin` y est bien, mais son `g` final n'est couvert par aucune règle avant le rang 26, et le décodeur le dit.
2. **Le mot doit être employable par un exercice de l'unité qui déclare le besoin** — et le corpus dit la **vérité** sur son emploi : le champ `present_dans_la_serie` est comparé aux mots réels de l'exercice nommé. Une image que rien n'affiche est un dessin qui ne sert pas, et le corpus n'a pas le droit de le prétendre employé.
3. **Un mot qu'on ne peut pas dessiner doit être déclaré, avec sa raison.** Le silence serait la faute : une case vide se lit comme un oubli, alors que « on ne peut pas le dessiner, et voici pourquoi » est une réponse.

## 2. Le cadrage n'est pas recopié

Les règles de dessin, la palette fermée, l'épaisseur du contour, le cadrage à 80 %, le nommage des fichiers et la licence sont ceux de la GS, et ils **ne sont pas recopiés** dans `outils/images-ce1.json` : le fichier les reprend par référence (`cadrage_de_reference`), et le contrôle refuse une référence absente ou un cadrage incomplet.

Ce n'est pas une économie de place. C'est la leçon de cette tranche, et elle a coûté cher : la liste des graphies du CE1 était écrite **deux fois** — dans la table et dans le code — et les deux copies avaient divergé, si bien qu'`oreille`, `taille`, `bataille` et `abeille` étaient refusés comme « graphème non enseigné » et que `feuille` était lu `/fœjl/`. **Deux copies d'une même règle divergent, toujours.** Ici, il n'y en a qu'une.

## 3. Le corpus en trois tableaux

Les trois tableaux ci-dessous sont **engendrés** à partir de `outils/images-ce1.json` par `outils/generer-table.py`. Le premier dit ce qui est **dessiné**, le deuxième ce qui est **déclaré non dessinable**, le troisième **compte les motifs de refus** — parce qu'un motif qu'on invente ne se compte pas, et qu'un refus qui ne se compte pas ne se vérifie pas.

<!-- DEBUT TABLE GENEREE -->

| Mot | Rang | Besoin | Graphie | Découpe | Objet du dessin | Emploi |
|---|---|---|---|---|---|---|
| `foin` | 4 | B04 | `oin` | f \| oin | une meule de foin : un tas en dôme de brins dorés, plus large que haut, posé au sol, quelques brins dépassant du sommet | `E09` — **à ajouter à la série** |
| `parfum` | 13 | B13 | `un` | p \| a \| r \| f \| um | un flacon de parfum : une panse trapue à épaule marquée, un col court, un bouchon doré, et une poire à vaporiser reliée au bouchon par un tube | `E18` — **à ajouter à la série** |
| `œil` | 30 | B30 | `irregulier` | œ \| i \| l | un œil vu de face, en gros plan : un ovale blanc, un iris bleu et une pupille noire, deux cils sur le bord supérieur | `E36` |

| Besoin | Mot | Rang | Motif | Raison |
|---|---|---|---|---|
| B04 | `besoin` | 4 | abstrait | un nom abstrait : il n'y a rien à montrer. |
| B04 | `coin` | 4 | abstrait | un coin n'est pas un objet, c'est une partie d'un autre : le coin d'une page se nomme « page », le coin d'une pièce se nomme « mur ». L'image ferait nommer le tout. |
| B04 | `groin` | 4 | nomme autre chose | un groin se dessine — un museau rose à deux narines — mais un enfant de sept ans nomme « un cochon » ce qu'il voit, pas « un groin ». L'image ferait nommer un autre mot que le mot visé. |
| B04 | `joint` | 4 | forme verbale | le mot est d'abord un participe ; le dessin d'une jointure se nomme « jointure », et un joint de plomberie est un objet que l'enfant ne connaît pas. |
| B04 | `loin` | 4 | abstrait | un adverbe de lieu : le dessiner demande deux objets et une distance entre eux, et l'image nommerait les deux objets, pas le mot visé. |
| B04 | `poing` | 4 | illisible au rang | le mot porte la graphie, mais son g final n'est couvert par aucune règle avant le rang 26 : « poing » n'est pas lisible au rang 4, donc pas affichable. C'est le décodeur qui le dit, pas une impression. |
| B04 | `point` | 4 | abstrait | un point est une marque, pas un objet : le dessin d'un point se nomme « un rond » ou « une bille », et c'est le mot que l'enfant dirait. |
| B04 | `poisson` | 4 | la graphie n'y est pas | « poisson » contient les lettres o-i-n dans cet ordre, mais pas la graphie : il se décode `p \| oi \| ss \| on`, soit /pwasɔ̃/. Illustrer un poisson ne servirait pas l'unité 4 — et c'était la première idée, fausse, et c'est le décodeur qui l'a montrée fausse. |
| B04 | `rejoint` | 4 | forme verbale | l'image d'un verbe montrerait deux objets et un mouvement, donc deux noms et une action : elle ne dirait pas le mot. |
| B13 | `aucun` | 13 | pronom | un pronom indéfini, et de surcroît négatif : la négation ne se dessine pas. |
| B13 | `brun` | 13 | couleur | une couleur n'est pas un objet : le dessin d'une tache brune se nomme « une tache » ou « du chocolat », et la série n'illustre aucune couleur. |
| B13 | `brune` | 13 | couleur | la forme féminine de la même couleur, avec la même impossibilité. |
| B13 | `chacun` | 13 | pronom | un pronom indéfini : il ne désigne pas un objet mais une répartition. Rien à montrer. |
| B13 | `emprunt` | 13 | abstrait | un nom abstrait : le dessin d'un objet prêté ne dit pas qu'il est prêté, il nomme l'objet. |
| B13 | `humble` | 13 | abstrait | un adjectif : la modestie ne se dessine pas, et le dessin d'une personne modeste se nomme « un enfant » ou « une dame ». |
| B13 | `lundi` | 13 | jour | un jour de la semaine ne se dessine pas sans écrire son nom : l'image d'un calendrier se nomme « calendrier », et la charte interdit tout texte dans une image. |
| B30 | `huit` | 26 | nombre | même raison que « sept » : un nombre se montre par un chiffre, et c'est interdit. |
| B30 | `sept` | 26 | nombre | un nombre s'écrit : l'image d'un nombre est un chiffre, et la charte interdit tout chiffre. Le mot est mémorisé au rang 26, mais il n'est pas illustrable. |
| B30 | `femme` | 30 | convention tenue | même raison que « monsieur », du côté de « maman ». Un quatrième adulte dans une série qui en compte deux ne s'ajoute pas : il défait la paire. |
| B30 | `fils` | 30 | relation | une relation, pas un objet : le dessin d'un garçon se nomme « garçon », et le dessin d'un garçon près d'un adulte se nomme « famille ». Le lien ne se voit pas. |
| B30 | `monsieur` | 30 | convention tenue | un adulte seul ne se distingue pas de « papa ». La série a FIXÉ une convention — barbe courte pour papa, cheveux attachés pour maman — et une seule. En ajouter une seconde pour « monsieur » ferait deux conventions pour un seul trait distinctif, et c'est la première qui perdrait : « papa » deviendrait ambigu. |
| B30 | `second` | 30 | nombre | un ordinal : il dit un rang, pas un objet. L'image d'un rang est un chiffre, et la charte interdit tout chiffre dans une image. |

| Motif | Mots |
|---|---|
| abstrait | 6 |
| nombre | 3 |
| convention tenue | 2 |
| couleur | 2 |
| forme verbale | 2 |
| pronom | 2 |
| illisible au rang | 1 |
| jour | 1 |
| la graphie n'y est pas | 1 |
| nomme autre chose | 1 |
| relation | 1 |

<!-- FIN TABLE GENEREE -->

## 4. Ce qui est dessiné

Trois images, produites dans `contenu/images-ce1/` par `outils/generer-images.py --ce1`, avec les mêmes primitives, la même palette et le même cadre que la série de la GS. La planche de contrôle — `contenu/images-ce1/planche.html` et `planche.svg` — les montre à la taille de l'application.

**Une image se regarde, elle ne s'inspecte pas.** Les trois dessins ont été relus sur la planche rastérisée, et deux ont été refaits : la première version du foin était une botte arrondie serrée par une corde, et elle se lisait comme une **caisse** — le contour régulier disait le contenant, pas le contenu ; la première version du parfum dessinait la poire à vaporiser comme une bille au bout d'un fil, et l'ensemble se lisait comme un **ballon**. Ce sont deux applications de la même règle, celle du cadrage : *un objet se nomme par ses traits distinctifs, pas par son contour.*

## 5. Ce qui ne peut pas être dessiné

C'est ici que se trouve la vraie réponse aux besoins. Sur **vingt-cinq mots examinés**, trois sont illustrables.

Le motif du refus vient d'une **liste fermée**, et le contrôle refuse un motif libre. Chaque refus porte aussi une **raison écrite** : le contrôle refuse une raison vide, parce qu'une case vide se lit comme un oubli.

## 6. La raison de fond : le lexique, pas le corpus

Les trois besoins déclarés — B04 pour `oin`, B13 pour la nasale `un`, B30 pour les mots irréguliers — ont ceci en commun qu'ils portent sur **les endroits du français où le nom concret se raréfie**.

- La nasale `/wɛ̃/` se rencontre dans `coin`, `point`, `loin`, `besoin`, `soin`, `moins`, `joint`, `témoin`, `lointain` : des pronoms, des adverbes, des participes, une partie d'objet. Le seul nom concret est `foin`.
- La nasale `/œ̃/` est plus rare encore. Hors les mots grammaticaux (`un`, `aucun`, `chacun`, `quelqu'un`), il reste `lundi` — un jour, qui s'écrit — `brun`, une couleur, et `parfum`, le seul objet.
- Les mots irréguliers de l'unité 30 sont un nom d'adulte, un nom d'adulte, un rang, une relation et un objet. Un seul se dessine.

**Ce n'est donc pas une paresse du corpus, et ce n'est pas un manque à combler par un illustrateur.** Ces trois besoins ne se soldent pas par un dessin : ils se soldent par une **lecture**, et c'est ce que les exercices font déjà — E09 lit et choisit le mot où le son s'entend, E18 sépare la nasale de deux lettres qui se suivent, E36 reconnaît le mot d'un seul regard. Le corpus ne remplace pas ces exercices : il les **complète là où c'est possible**, et il dit où ça ne l'est pas.

## 7. Ce que ce travail a fait apparaître

### 7.1 Un défaut du décodeur : le `um` n'était déclaré nulle part

La table des correspondances déclare `on/om`, `an/am`, `in/im`, `ain/ein` — une nasale devant `p` ou `b` s'écrit avec un `m`. L'unité 13 ne déclarait que `un`. Conséquence : `parfum` était **refusé** (son `m` final n'est couvert par aucune règle avant le rang 26), et `humble`, découpé `h | u | m | b | l | e`, était lu `/ymbl/` au lieu de `/œ̃bl/` — **accepté, et de travers**, le sens d'erreur le plus dangereux.

Le défaut est apparu en cherchant l'image d'un mot porteur de la nasale, c'est-à-dire **en dehors des dix-huit textes** : aucun ne contient de `um`. Il est corrigé.

### 7.2 Un contrôle qui ne regardait pas ce qu'il devait garder

Le correctif du `um` a été **falsifié** : le `um` a été retiré du garde-fou des nasales, puis de la table, et le harnais du décodeur a été rejoué. Le second retrait a produit cinq échecs. Le premier **n'a rien produit du tout** — parce que le harnais n'éprouvait que le verdict et les graphèmes muets, et que `humide` découpé `h | um | i | d | e` donne le même verdict et la même liste de muets que `h | u | m | i | d | e`.

Le harnais a donc une **troisième section**, qui éprouve la **découpe** : quels graphèmes sont reconnus, dans quel ordre. Dix essais, et le harnais passe de cent dix à cent vingt-neuf. C'est la même leçon que la section précédente, poussée d'un cran : *un contrôle ne prouve que ce qu'il regarde, et il faut le falsifier pour savoir ce qu'il regarde vraiment.*

### 7.3 Un mot illustré qui disparaît ne faisait échouer aucun contrôle

La falsification du corpus — vingt-trois corpus faux, un défaut à la fois — a montré qu'en **retirant `foin`** du corpus, tout restait vert. La raison : le contrôle de couverture part des mots que les exercices affichent, et `foin` n'est pas encore dans la série de E09 — il n'était donc réclamé par rien.

Le corpus porte maintenant un datum, `reponse_aux_besoins`, qui **déclare** la réponse mot pour mot. Deux sources de la même chose se surveillent l'une l'autre : celle-ci est écrite à la main, celle des mots illustrés est calculée, et le contrôle refuse qu'elles divergent.

### 7.4 Deux exercices dont l'énoncé décrit une autre série que la leur

Ce n'est pas un défaut d'image, mais c'est le corpus qui l'a mis au jour en comparant les mots affichés aux énoncés.

- **E09** annonce « six mots affichés, un seul porte `oin` ». Sa série est `coin`, `point`, `loin`, `besoin`, `joint`, `rejoint` : **six mots qui portent tous la graphie**. L'exercice n'a donc pas de mauvaise réponse, et l'enfant qui ne sait pas encore lire `oin` n'a rien à trouver.
- **E18** annonce « six mots affichés, dont trois portent la nasale `un` et trois le `u` suivi de `n` ». Sa série en compte **quatre et deux**.

Le corpus **consigne** ces écarts — dans `employable_par.ce_qu_il_faudrait`, pour `foin` et pour `parfum` — et **ne les corrige pas**. Choisir quels mots une unité affiche est une décision pédagogique, et la relecture pédagogique appartient au porteur du projet. Corriger la série de E09 demanderait d'y faire entrer des mots qui ne portent pas `oin`, ce qui change l'exercice ; c'est une décision, pas une réparation.

## 8. Ce que le contrôle ne voit pas

- **Si un dessin est reconnaissable.** Le contrôle établit que le cadre est le bon, que la palette est fermée, qu'aucune image ne contient de texte, qu'aucun fichier n'est vide ni démesuré — et que le dessin existe dans le générateur, faute de quoi un fichier écrit à la main survivrait à une régénération sans que rien ne dise d'où il vient. Il ne peut pas établir qu'un enfant de sept ans nomme l'objet. La planche existe pour ça, et elle se regarde.
- **Si le mot est connu de l'enfant.** `parfum`, `foin` et `œil` sont des mots de la vie courante, mais rien ne le garantit mécaniquement.
- **Si le motif du refus est le bon.** Le contrôle vérifie qu'un motif appartient à la liste fermée et qu'une raison est écrite ; il ne juge pas la raison. Un refus mal motivé passerait.
- **L'emploi réel.** Le corpus dit la vérité sur ce que les exercices affichent **aujourd'hui** ; il ne dit pas ce qu'ils devraient afficher. Le passage de « employable » à « employé » demande de toucher la banque, et c'est une décision.

## 9. Ce qui reste

- **Deux mots à faire entrer dans une série** : `foin` dans E09 et `parfum` dans E18. Pour E09, l'ajout suppose de revoir la série entière — voir 7.4. Pour E18, il suffit d'ajouter le mot et de corriger le compte de l'énoncé.
- **La mécanique « écouter et toucher l'image »** n'existe pas dans la banque du CE1 : elle a été retirée lors de l'écriture de la banque, au motif qu'une mécanique déclarée et jamais employée est une promesse qu'on ne tient pas. Les trois images ne la rétablissent pas — un exercice « touche l'image du mot entendu » a besoin de plusieurs mots de la même famille, et chaque famille en compte un seul.
- **Les images de récit** des unités 14 et 37 : ces deux unités annoncent de « remettre des images dans l'ordre », et leurs exercices emploient des étapes **textuelles** faute d'images. Le manque n'était déclaré nulle part ; il l'est maintenant ici, et il demandera huit dessins de scène — un autre métier que l'icône, puisque la règle « un seul objet par image » ne s'y applique pas.
