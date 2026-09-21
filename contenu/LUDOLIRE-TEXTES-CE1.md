# Ludo'Lire — Les textes du CE1

**Statut :** proposition à valider. Les textes sont écrits et contrôlés ; leur intérêt pédagogique se jugera en éprouvant l'application, pas à la lecture de ce document.
**Dépend de :** `contenu/LUDOLIRE-PROGRESSION-CE1.md` (les 42 unités et leurs rangs), `outils/cgp-ce1.json` (les correspondances du CE1), `outils/verifier-textes-ce1.py` (le contrôle).
**Suite de :** `contenu/LUDOLIRE-REGLES-TEXTES.md`, qui pose la règle de rédaction pour le CP. Ce document ne la répète pas : il dit **ce que le CE1 y change**.

---

## 1. La règle unique, et ce qui change au CE1

**Un texte au rang N n'emploie que des graphèmes enseignés au rang N ou avant.**

Au CE1, l'ensemble des graphèmes autorisés n'est pas « les trente CGP du CP plus les unités du CE1 jusqu'au rang N » par hasard : c'est que **tout le CP est acquis**. Le programme le demande explicitement — l'automatisation du décodage « tout au long de l'année ». Les trente correspondances du CP ne sont donc pas réenseignées, elles sont **autorisées partout**, dès le rang 1.

Trois règles du CP tombent, chacune à un rang précis. C'est la raison d'être de la table du CE1 :

| Ce qui tombe | Au CP | Au CE1 |
|---|---|---|
| La terminaison `-ent` | **interdite dans toute la tranche**, à tout rang | lisible au **rang 27** — le programme donne l'exemple « ils chantent » |
| Les consonnes doubles | `ss` et `ll` seulement | **toutes**, au **rang 28** |
| Les lettres finales muettes | `e`, `s`, `t`, `d`, `x` | s'étendent aux **muettes lexicales** au **rang 26** — « le lait », « le loup » |

## 2. La longueur : une décision de produit, et elle est prise

Le programme du CE1 fixe la longueur d'un texte **en lignes** — « une quinzaine de lignes » — et pas en mots. Une ligne n'a de sens qu'avec la largeur de ligne de l'application.

Tant que cette largeur n'était pas fixée, « une quinzaine de lignes » n'était **vérifiable par rien** : le contrôle ne pouvait que rapporter un nombre de mots en disant qu'il ne savait pas conclure. Et un texte de quinze **phrases** passait pour un texte de quinze **lignes** — il en fait vingt.

**La largeur de ligne de Ludo'Lire est donc fixée à 34 signes, espaces comprises.** Elle est déclarée dans `outils/verifier-textes-ce1.py` (`LARGEUR_LIGNE`), le texte y est plié, et le compte de lignes est **contrôlé**.

Le chiffre n'est pas choisi pour arranger les textes. Un enfant qui apprend à lire a un empan de lecture court, et au-delà d'une trentaine de signes le retour à la ligne devient une source d'erreur : l'œil saute la ligne ou revient au début de la même. Trente-quatre signes est le haut de cette fourchette, et il vaut pour le téléphone, qui est le support le plus contraint.

Conséquence, et elle se vérifie : une ligne de Ludo'Lire porte **quatre à cinq mots courants**. « Une quinzaine de lignes » vaut donc une **soixantaine à une quatre-vingtaine de mots**. La borne basse de la tranche, six lignes, en vaut une trentaine.

## 3. La forme d'écriture, et pourquoi elle n'est pas la forme de lecture

Un fichier de texte met **une phrase par ligne**. C'est la forme d'écriture : elle rend la relecture possible, et elle permet de corriger une phrase sans toucher aux autres.

Ce n'est **pas** la forme de lecture. L'application plie le texte à 34 signes, et un paragraphe de trois phrases fait quatre ou cinq lignes. Le contrôle compte les lignes **pliées**, parce que ce sont celles que l'enfant lit.

Le pliage est glouton et coupe aux espaces : un mot ne se coupe pas. C'est la règle la plus simple, et la seule qu'on puisse vérifier sans connaître la police de l'application.

## 4. Les textes écrits

<!-- DEBUT TABLE GENEREE -->

| Texte | Rang | Période | Titre | Lignes de 34 signes | Mots | CGP nouvelle du rang |
|---|---|---|---|---|---|---|
| `T01-rang01.txt` | 1 | 1 | Le chat | 6 | 28 | — |
| `T02-rang02.txt` | 2 | 1 | La fête | 7 | 33 | e-ouvert |
| `T03-rang03.txt` | 3 | 1 | Le vent | 8 | 35 | en |
| `T04-rang04.txt` | 4 | 1 | Le coin de la reine | 9 | 56 | oin |
| `T05-rang08.txt` | 8 | 1 | La maison de la reine | 9 | 52 | — |
| `T06-rang09.txt` | 9 | 2 | La montagne | 10 | 55 | gn |
| `T07-rang11.txt` | 11 | 2 | L'éléphant et le téléphone | 11 | 50 | ph |
| `T08-rang13.txt` | 13 | 2 | Le lundi brun | 11 | 64 | un |
| `T09-rang16.txt` | 16 | 2 | Le chat de la reine | 11 | 60 | — |
| `T10-rang17.txt` | 17 | 3 | La station | 12 | 54 | tion |
| `T11-rang19.txt` | 19 | 3 | Merci la reine | 12 | 63 | c-doux |
| `T12-rang21.txt` | 21 | 3 | La valise de la reine | 13 | 61 | — |
| `T13-rang25.txt` | 25 | 3 | Le poisson de la reine | 13 | 66 | — |
| `T14-rang28.txt` | 28 | 4 | La pomme | 13 | 61 | — |
| `T15-rang30.txt` | 30 | 4 | Monsieur le chat | 13 | 72 | — |
| `T16-rang32.txt` | 32 | 4 | La recette de la reine | 14 | 59 | — |
| `T17-rang33.txt` | 33 | 4 | Le chat | 14 | 75 | — |
| `T18-rang38.txt` | 38 | 5 | La pomme d'or | 15 | 75 | — |

<!-- FIN TABLE GENEREE -->

**La montée est réelle, et elle est contrôlée.** Les textes vont de six à quinze lignes de 34 signes, sans décroissance d'un texte au suivant. Le dernier texte, au rang 38, atteint la quinzaine : c'est le palier de la tranche.

## 5. Ce que le contrôle ne voit pas

Un contrôle qui ne dit pas ses limites fait plus de mal que de bien.

- **Le sens et l'intérêt.** Un texte conforme peut être plat. Aucun script ne mesure ce qui fait revenir un enfant le lendemain.
- **Le niveau de vocabulaire.** Un mot déchiffrable peut être inconnu d'un enfant de sept ans. Le vocabulaire employé ici est celui de la vie courante — chat, reine, pomme, valise, jardin — mais rien ne le garantit mécaniquement.
- **Les liaisons et la prosodie**, qui ne s'écrivent pas.
- **La phrase-preuve d'une question de compréhension.** Le contrôle des textes ne vérifie pas qu'une phrase citée par une question existe réellement dans le texte. Cette vérification appartient au contrôle des exercices, et elle y est faite depuis : `outils/verifier-exercices.py --ce1` refuse une question dont la phrase citée n'est pas **littéralement** présente dans le texte qu'elle nomme.

### 5.1 La limite la plus sérieuse : la lecture interne du contrôle après le rang 26

À partir du rang 26, le contrôle traite **toute consonne finale** hors de `e`, `s`, `t`, `d`, `x` comme muette — c'est la règle des muettes lexicales. C'est ce qui ouvre « loup », « tabac », « fusil », et c'est correct pour ces mots.

Mais la règle est **trop large**, et il faut le dire : dans « animal », « mal », « fil », « sel », le `l` final **se prononce**. Le contrôle accepte ces mots — ce qui est juste, ils sont lisibles au rang 26 — mais il les lit intérieurement **sans leur `l`**.

Ce défaut ne fausse pas les textes : un mot accepté au rang 26 est un mot qu'un enfant de CE1 sait lire. Il fausserait tout ce qui serait **dérivé** de cette lecture — un découpage syllabique, une synthèse vocale, une mesure de longueur phonétique. C'est pourquoi il est écrit ici plutôt que tu, et pourquoi tout ce qui dérivera de la prononciation devra passer par une table de prononciation, pas par ce décodeur.

**La direction de l'erreur est la bonne** : avant le rang 26, la même consonne est *indécidable* et le mot est **refusé**. Un texte refusé se voit et se réécrit ; un texte accepté de travers ne se voit pas. C'est la raison pour laquelle le contrôle refuse plutôt que de deviner.

## 6. Ce qui reste à faire pour la tranche CE1

- **La banque d'exercices** — *faite* : `outils/exercices-ce1.json` et `contenu/LUDOLIRE-EXERCICES-CE1.md`, **57 exercices couvrant les 42 unités**. Les **dix unités de production** y soldent leur dette — sept par une `inversion`, trois par un `pourquoi_hors_app`, l'unité 41 par les deux — et les **27 questions de compréhension** y portent leur **phrase-preuve**, vérifiée littéralement dans le texte nommé.
- **Les illustrations** — *faites* : `outils/images-ce1.json` → `contenu/LUDOLIRE-IMAGES-CE1.md`, **3 images** (`foin`, `parfum`, `œil`) et **22 mots déclarés non dessinables**, chacun avec sa raison. Les trois besoins B04, B13 et B30 ont leur réponse, et la réponse dit aussi ce qui reste impossible : les deux nasales rares et les mots irréguliers sont les endroits du français où le nom concret se raréfie, et une famille qui compte un seul mot illustrable ne peut pas porter un exercice de discrimination. Ces besoins se soldent par la **lecture**, pas par un dessin. Les **images de récit** des unités 14 et 37 sont faites elles aussi : `outils/images-recit-ce1.json` → `contenu/LUDOLIRE-IMAGES-RECIT-CE1.md`, **8 scènes** pour les deux exercices de remise en ordre dont l'unité annonce un geste d'image.
- **Les textes courts** — *faits* : `contenu/textes-courts-ce1/` → `contenu/LUDOLIRE-TEXTES-COURTS-CE1.md`, **5 textes** de deux à six lignes, chacun déclarant son rang, son **type** et son titre, et **cités** par les quatre exercices qui en ont besoin. Le corpus existe parce que ces textes, portés par l'exercice, n'étaient vus par aucun contrôle : cinq de leurs phrases étaient déjà des lignes d'un texte du palier, `E32` et `E33` portaient le même texte chacun de son côté, et cinq titres entraient en collision avec ceux des textes du palier. Il solde le besoin **B16** — un texte informatif est désormais lisible au rang 16, et l'unité 16 peut opposer les deux types.
- **Le corpus audio** : les textes du CE1 ne sont pas enregistrés à ce jour, ni les 33 consignes (B01a). Les pseudo-mots que le programme donne en exemple ont, eux, leur corpus et le script de leur enregistrement (`contenu/LUDOLIRE-PSEUDO-MOTS-CE1.md`) : B35 est soldé, et ce qui manque est la prise de son.
