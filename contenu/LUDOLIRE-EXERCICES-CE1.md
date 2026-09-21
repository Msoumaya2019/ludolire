# Ludo'Lire — Les exercices de la tranche CE1

**Statut :** proposition. Banque de 57 exercices, 33 mécaniques, 33 consignes à enregistrer, 5 besoins déclarés, 4 corrections consignées. Version 0.1.0.
**Source de vérité :** `outils/exercices-ce1.json`. Les tableaux du § 7 en sont le rendu, produit par `outils/generer-table.py`.
**Dépend de :** `outils/progression-ce1.json` (les 42 unités, et leur champ `production`), `outils/cgp-ce1.json` (les graphies, dont dépend la déchiffrabilité de tout ce que l'enfant lit), `contenu/textes-ce1/` (les 18 textes du palier, et leur rang), `contenu/textes-courts-ce1/` (les 5 textes courts cités par les exercices), `outils/images-gs.json` (les 44 images de la GS) et `outils/images-ce1.json` (les 3 images du CE1, et les 22 mots déclarés non dessinables).

---

## 1. Ce que la banque règle, et ce qu'elle ne règle pas

La progression du CE1 dit **ce que** chaque unité vise. Elle ne dit pas **comment** on l'entraîne sur un écran sans micro, ni ce que l'application peut vérifier. C'est l'objet de cette banque.

Elle règle trois choses, et trois seulement :

1. **ce que la voix dit** — une consigne, dont le texte est ici le script de l'enregistrement à faire ;
2. **ce que l'enfant fait** — un geste, choisi pour être jugeable par la machine ;
3. **ce que l'application peut en conclure** — un verdict, `app` ou `hors app`.

Elle ne règle **ni** l'habillage graphique, **ni** l'ordre des exercices dans une séance, **ni** la difficulté relative de deux exercices.

### La règle qui gouverne tout le reste

> **Un exercice du CE1 n'emploie que des mots déchiffrables au rang de son unité — et il porte sur tout ce que l'enfant voit.**

À la GS, cette règle protégeait le découpage. Au CE1, elle protège la lecture, et elle s'étend : elle ne s'applique plus seulement aux mots de la série, mais **aussi aux questions et à leurs réponses**. Une option qu'on ne peut pas lire est une option qui n'existe pas ; un enfant qui choisit au hasard parce qu'il bute sur un mot n'apprend rien et la mesure ne dit rien de lui.

C'est le contrôle qui calcule cette déchiffrabilité, avec le décodeur du CE1 — celui-là même qui contrôle les textes. Une seule implémentation pour les deux, parce que deux implémentations divergeraient, et que la seconde serait celle qu'on oublie de corriger.

## 2. La consigne se dit, le geste répond

> Toute consigne se donne par la voix, et toute réponse se donne par le geste.

C'est la conséquence de l'absence de micro, et c'est elle qui a produit la liste des mécaniques.

**Ce qui change au CE1, c'est que l'enfant lit.** Le principe d'entrée de la tranche le dit : « toute consigne peut donc être écrite, et c'est la première tranche où c'est vrai ». Une consigne du CE1 est donc écrite **et** dite — et elle est courte, et autant que possible déchiffrable, parce qu'une consigne illisible est une consigne absente.

Le CE1 n'a pas de corpus de consignes enregistrées : le corpus audio est celui de la GS, et ses trente et une consignes ont été écrites pour des enfants qui ne lisent pas encore. Les trente-trois consignes de cette banque sont donc **déclarées ici, avec leur texte, qui est le script de l'enregistrement à faire** (§ 7). Le besoin est déclaré une fois (`B01a`) et porté par chaque consigne — de sorte qu'une consigne jamais employée se voie, au lieu de rester à enregistrer pour rien.

### Le retournement, et pourquoi il ne fait pas disparaître l'objectif

Une unité qui demande à l'enfant de **dire** quelque chose ne peut pas être vérifiée par la machine. Mais elle peut presque toujours être **retournée** :

| Le programme demande | L'exercice demande |
|---|---|
| de donner un titre au texte | l'enfant **touche**, parmi trois, le titre qui convient (E11, E47) |
| de justifier une réponse par un retour au texte | l'enfant **touche la phrase** qui prouve la réponse (E12) |
| de restituer les enchaînements du récit | l'enfant **remet les étapes dans l'ordre** (E19, E39, E45, E51) |
| d'expliciter les émotions des personnages | l'enfant **touche** ce que le texte dit du personnage (E20, E52) |
| de caractériser les personnages | l'enfant **apparie** chaque personnage à son trait (E30) |
| de résumer le texte | l'enfant **ordonne les moments** qui tiennent lieu de résumé (E45) |
| d'établir des liens entre ses lectures | l'enfant **touche** le texte qui ressemble au précédent (E55) |

Ce retournement déplace l'objectif, il ne l'abolit pas. C'est pourquoi chaque exercice retourné porte une **`inversion`** : ce que le geste reprend, et ce qui reste hors app.

## 3. Les trois façons de payer la dette d'une production

La progression déclare **dix unités dont l'objectif porte un acte de parole** — lire à voix haute, résumer, expliciter, donner un titre. Pour chacune, l'exercice qui la couvre doit dire ce qu'il fait de la production, et il n'a que trois façons de le faire :

| La situation | Ce que l'exercice déclare | Combien |
|---|---|---|
| l'unité a un geste possible dans l'app | une **`inversion`** — ce que le geste reprend | 7 |
| l'unité n'a aucun geste : l'enfant lit, un adulte valide | un **`pourquoi_hors_app`** | 4 |
| les deux, quand l'unité a une moitié réceptive et une moitié qui se dit | une `inversion` **et** un exercice hors app | 1 (l'unité 41) |

Les trois unités de lecture à voix haute (34, 39, 40) et la moitié « dire ce que ça t'a rappelé » de l'unité 41 sont **hors app** — et pour deux d'entre elles, la substitution vaut **« aucune »**. C'est une déclaration, pas un oubli : la fluence et l'expressivité n'ont pas de jumeau réceptif, et un exercice qui prétendrait les mesurer mesurerait autre chose en le faisant passer pour elles. C'est le seul endroit où la banque écrit qu'un objectif du programme n'est pas entraîné par l'application.

L'unité 42 — choisir un livre pour son plaisir — est hors app sans être une production : choisir n'est pas un acte de parole, c'est un goût, et une application qui aurait une bonne réponse jugerait un goût.

## 4. Les questions, et la phrase-preuve

> **Une question de compréhension ne vaut que si l'on peut montrer où le texte le dit.**

Le programme du CE1 demande de « justifier ses réponses par un retour au texte ». C'est ce qui rend la compréhension vérifiable par une machine : non pas « as-tu compris ? », mais **« où le texte le dit-il ? »**.

Chaque question porte donc sa **`phrase_preuve`**, citée du texte mot pour mot, et le contrôle vérifie qu'elle s'y trouve **littéralement**. Une phrase-preuve approximative est une réponse qu'on ne peut pas défendre — et, plus grave, elle apprend à l'enfant à justifier par une phrase qu'il n'a pas lue.

La banque compte **27 questions**, toutes avec leur preuve. Elles suivent une règle de distracteur :

> **Une mauvaise réponse doit être une lecture PLAUSIBLE du texte, pas une absurdité.**

C'est la règle des intruses du jeu de syllabes, transposée aux questions. Un intrus partage le plus possible avec la bonne réponse — le même personnage, le même lieu, la même action — et ne s'en écarte que par ce que la question demande. Une option écartée d'emblée n'apprend rien à l'enfant et ne mesure rien.

### Les textes courts, et pourquoi ils ont leur corpus

Quatre exercices ont besoin d'un texte qui n'est pas un texte du palier — trop court pour être lu seul, et fait pour être **comparé** :

- **E21** (distinguer le récit du documentaire, unité 16) demande **deux** textes à comparer ;
- **E55** (apparier deux lectures qui se ressemblent, unité 41) en demande **trois** ;
- **E32** et **E33** (la marque du pluriel, unité 27) jouent sur un même texte de quatre lignes.

Ces textes vivent dans leur propre corpus, `contenu/textes-courts-ce1/`, et l'exercice les **cite** par leur nom de fichier dans le champ `textes_courts`. Chacun déclare son rang, son **type** et son titre ; le contrôle les éprouve comme le reste — deux à six lignes de 34 signes, chaque mot déchiffrable au rang de l'unité — et refuse en plus un titre en collision avec celui d'un texte du palier, une phrase recopiée d'un texte du palier, et un texte que personne ne cite. Le corpus est documenté par `contenu/LUDOLIRE-TEXTES-COURTS-CE1.md`.

Il n'a pas été créé par goût de la symétrie : tant que ces textes étaient portés par l'exercice, **aucun contrôle ne les voyait ensemble**, et le travail a mesuré ce que cela coûtait — cinq phrases qui étaient déjà des lignes d'un texte du palier, un même texte porté par deux exercices chacun de son côté, trois phrases partagées entre deux autres, et cinq titres en collision avec ceux des textes du palier.

### Les pseudo-mots, et pourquoi ils ont leur corpus

Les cinq pseudo-mots que le programme donne en exemple étaient portés par **les deux** exercices de l'unité 35, chacun de son côté — la même liste, deux fois. Ils ont désormais leur corpus, `outils/pseudo-mots-ce1.json` → `contenu/LUDOLIRE-PSEUDO-MOTS-CE1.md`, et les deux exercices les **citent** par identifiant.

Le défaut n'était pas la duplication en elle-même : c'est ce qu'elle produisait. `E42` fait **entendre** les cinq suites et les fait retrouver parmi trois écrites ; `E43` les fait **lire** et demande de décider si c'est un mot. Avec la même liste, l'enfant qui venait de toucher `valin` dans le premier n'avait plus besoin de le décoder dans le second — alors que `E43` déclare entraîner « décoder d'abord, décider ensuite », et déclare ne pas vérifier « ce que l'enfant fait d'un mot qu'il croit reconnaître sans le lire ». L'exercice fabriquait la situation qu'il dit ne pas mesurer.

Le corpus porte donc **dix** suites : les cinq du programme pour `E42`, et cinq écrites pour `E43`, une par graphie que le CE1 ajoute et que les exemples ne couvraient pas. Le contrôle refuse qu'un même pseudo-mot soit cité par deux exercices de la même unité, qu'une suite soit déjà un mot de l'application — la crainte que B35 déclare —, ou qu'elle se lise comme un mot connu. Et sa lecture est **dérivée** des tables, graphie par graphie : c'est le script de l'enregistrement, et il n'est pas déclaré à la main.

## 5. Ce que la banque ne peut pas faire sans matériel

Cinq besoins sont déclarés, **aucun bloquant** — c'est-à-dire qu'aucun n'empêche la tranche d'être jouable, mais que chacun dit précisément ce qui manque. Deux concernent l'**audio**, trois les **images** :

- **B01a** (les consignes ne sont pas enregistrées) et **B02** (les mots du CE1 non plus) concernent l'**audio**. Les mécaniques qui font écouter un mot — écouter et toucher, écouter et décider — n'ont rien à jouer. Le texte de chaque consigne est le script de l'enregistrement à faire, et il est déclaré dans la banque ;

Les trois autres — B04, B13 et B30 — concernent les **images**, et depuis le 21 septembre 2026 ils ont leur réponse : `outils/images-ce1.json` et `contenu/LUDOLIRE-IMAGES-CE1.md` livrent **trois images** (`foin`, `parfum`, `œil`) et déclarent **vingt-deux mots non dessinables**, chacun avec sa raison. Le corpus dit aussi pourquoi il n'y en a que trois : les deux nasales rares et les mots irréguliers sont les endroits du français où le nom concret se raréfie, et l'action que la progression annonçait pour ces unités — « toucher l'image du mot entendu » — demande **plusieurs mots de la même famille**, alors que chaque famille en compte un seul. Le besoin n'était donc pas un manque d'illustrateur : il se solde par la **lecture**, ce que les exercices font déjà.

**Deux besoins ont été soldés**, et la liste est passée de sept à cinq. **B16** — « aucun texte informatif n'est lisible avant le rang 32 » — l'est par le corpus des textes courts : un texte informatif est lisible au rang 16, et les deux textes que `E21` compare sont désormais des textes qu'on peut relire. **B35** — « aucun pseudo-mot n'est enregistré » — l'est par le corpus des pseudo-mots, dont le § 4 dit ce qu'il demandait vraiment : sa seconde moitié, « un pseudo-mot enregistré par erreur comme un mot deviendrait un mot », est une crainte de **nommage**, et elle est désormais vérifiée par une règle. Ce qui reste de B35 est un enregistrement à faire, et il est déclaré dans la spécification du corpus, là où il se fera.

C'est pour cette raison que la mécanique `ecouter_et_toucher_image` **a été retirée de la liste** : une mécanique déclarée et jamais employée est une promesse qu'on ne tient pas. Le contrôle le vérifie désormais pour toutes.

## 6. Les corrections consignées

Quatre défauts trouvés **en écrivant la banque**, et consignés ici parce qu'ils disent quelque chose de la méthode. Le détail est au § 7.

1. **Les graphies `aille`, `eille` et `euille`** étaient écrites dans le code et rattachées à aucune CGP. Tout mot qui les contient — `oreille`, `taille`, `abeille` — était refusé ; `feuille` était lu /fœjl/. Aucun des dix-huit textes ne les contient, donc le contrôle des textes était vert : le défaut n'est apparu qu'en écrivant l'exercice de l'unité 18, c'est-à-dire **en demandant au décodeur un mot qu'aucun texte ne lui avait encore demandé**.

2. **Un contrôle d'atteignabilité qui ne pouvait pas échouer.** La première version cherchait chaque graphie dans la découpe d'une sonde construite autour d'elle — et la découpe prend toujours la plus longue correspondance, donc la graphie cherchée était toujours trouvée. Il a fallu le remplacer par un contrôle qui porte sur ce qui peut réellement se perdre.

3. **Trois unités dont l'action ne pouvait pas être exercée** (4, 13, 30), faute d'images. Un besoin tu se transforme en exercice faux. Le corpus d'images du CE1 a depuis répondu aux trois besoins : il livre ce qui se dessine, déclare ce qui ne se dessine pas, et **dit pourquoi** — les familles concernées comptent un seul mot illustrable chacune, et un exercice de discrimination n'en a pas assez.

4. **Des durées de GS recopiées au CE1.** Un exercice de compréhension demande de relire, de revenir au texte et de comparer trois réponses : ce n'est pas un exercice de 45 secondes.

Et un cinquième, trouvé par la falsification du contrôle lui-même : le **contrôle d'usage des mécaniques lisait les déclarations dans le contexte** au lieu de les lire dans la banque qu'il contrôlait — il ne pouvait donc pas voir une déclaration ajoutée. C'est en injectant la faute qu'on l'a su.

## 7. La banque

<!-- DEBUT TABLE GENEREE -->

### Les 33 mécaniques

| Mécanique | Ce que l'enfant fait | Ce que l'application fait | Verdict |
|---|---|---|---|
| `lire_mot_image` — Lire un mot et toucher son image | lire le mot écrit, puis toucher l'image correspondante parmi quatre | affiche quatre images et enregistre le toucher | app |
| `trier_graphies` — Trier des mots selon la graphie | ranger chaque mot dans la colonne de la graphie qui produit le son | affiche deux ou trois colonnes et range le mot touché | app |
| `trier_sons` — Trier des mots selon la voyelle entendue | ranger chaque mot dans la colonne de la voyelle qu'on entend, quand deux sons s'écrivent pareil | affiche deux colonnes et range le mot touché | app |
| `completer_mot` — Compléter un mot | toucher la carte-graphie qui complète le mot à trou | affiche le mot troué et les cartes, et enregistre la carte posée | app |
| `toucher_graphie_dans_mot` — Toucher la graphie dans le mot | toucher, dans le mot affiché, la graphie du son entendu | affiche le mot et enregistre la graphie touchée | app |
| `toucher_mot_dans_phrase` — Toucher un mot dans une phrase | toucher, dans la phrase affichée, le mot que la consigne désigne | affiche la phrase en mots touchables et enregistre le mot touché | app |
| `apparier_mot_image` — Apparier des mots et des images | toucher un mot puis son image, jusqu'à épuiser les paires | affiche les deux colonnes et vérifie les paires formées | app |
| `apparier_graphies` — Apparier deux mots qui partagent une graphie | toucher deux mots dont une graphie produit le même son | affiche les mots et vérifie les paires formées | app |
| `apparier_textes` — Apparier un texte à un autre qui lui ressemble | toucher, parmi trois textes courts, celui qui ressemble à celui qu'on vient de lire | affiche les trois textes et enregistre le toucher | app |
| `ecouter_et_choisir` — Écouter un mot et toucher sa graphie | écouter le mot dit par la voix, puis toucher le mot écrit qui correspond | joue le mot enregistré et enregistre le toucher | app |
| `lire_flash` — Lire un mot affiché brièvement | lire le mot avant qu'il disparaisse, puis toucher le même mot parmi quatre | affiche le mot un court instant, puis les quatre candidats | app |
| `lire_pseudo_mot` — Décider si une suite de lettres est un mot | toucher « oui » si la suite est un mot français, « non » sinon | affiche la suite et enregistre le choix binaire | app |
| `lire_et_choisir_son` — Lire et toucher le mot où le son s'entend | lire les mots affichés, puis toucher celui qui contient le son demandé | affiche les mots et enregistre le toucher | app |
| `classer_famille` — Classer des mots en familles | ranger les mots qui se ressemblent dans la même famille | affiche les mots et les familles, et vérifie le rangement | app |
| `choisir_forme` — Choisir la forme qui convient | toucher la forme du mot qui convient à la phrase | affiche la phrase et les formes, et enregistre le choix | app |
| `choisir_titre` — Choisir le titre du texte | toucher, parmi trois, le titre qui convient au texte lu | affiche les trois titres et enregistre le toucher | app |
| `choisir_resume` — Choisir le résumé qui convient | toucher, parmi trois, le résumé qui dit ce que le texte raconte | affiche les trois résumés et enregistre le toucher | app |
| `toucher_phrase_preuve` — Toucher la phrase qui prouve la réponse | toucher, dans le texte affiché, la phrase qui permet de répondre | affiche le texte en phrases touchables et enregistre la phrase choisie | app |
| `ordonner_recit` — Remettre le récit dans l'ordre | toucher les étapes du récit dans l'ordre où elles arrivent | affiche les étapes mélangées et vérifie l'ordre reconstruit | app |
| `toucher_referent` — Toucher le mot que remplace un pronom | toucher, plus haut dans le texte, le mot que désigne le pronom souligné | affiche le texte et enregistre le mot touché | app |
| `lever_ambiguite` — Choisir le sens qui convient | toucher, entre deux sens possibles d'un mot, celui que le texte retient | affiche les deux sens et enregistre le choix | app |
| `deviner_mot` — Trouver le sens d'un mot inconnu | toucher, parmi trois, ce que veut dire le mot en gras, d'après le texte | affiche les trois sens et enregistre le toucher | app |
| `inferer` — Répondre à une question dont la réponse n'est pas écrite | toucher la réponse qui se déduit du texte sans y être écrite | affiche les réponses et enregistre le toucher | app |
| `suivre_consigne_ecrite` — Exécuter une consigne lue | lire la consigne du texte et faire ce qu'elle dit, dans l'ordre | vérifie l'ordre et la conformité des gestes demandés | app |
| `prelever_info` — Trouver une information dans un texte | toucher, parmi les phrases du texte, celle qui porte l'information demandée | affiche le texte et enregistre la phrase touchée | app |
| `toucher_emotion` — Dire ce que ressent le personnage | toucher le mot qui dit ce que ressent le personnage à ce moment du texte | affiche les mots d'émotion et enregistre le toucher | app |
| `associer_personnage_trait` — Associer un personnage et un trait | toucher le trait qui va avec le personnage, pour chaque personnage | affiche les personnages et les traits, et vérifie les paires | app |
| `distinguer_type` — Dire si le texte raconte ou explique | toucher « il raconte une histoire » ou « il explique quelque chose » | affiche les deux étiquettes et enregistre le choix | app |
| `marquer_groupes` — Marquer les groupes de mots | toucher, entre deux mots, les endroits où le groupe se termine et où l'on respire | affiche le texte en mots touchables et enregistre les coupures | app |
| `lire_a_voix_haute` — Lire à voix haute | lire le texte à voix haute, devant l'adulte | ne fait rien : elle ne peut pas entendre | hors app |
| `lire_et_chronometrer` — Lire et se faire chronométrer | lire le texte pendant que l'adulte mesure le temps | affiche le texte et le nombre de mots, et laisse l'adulte saisir la durée | hors app |
| `choisir_son_livre` — Choisir un livre pour soi | parcourir les livres et en choisir un, pour le plaisir | ne fait rien : elle ne peut pas juger un choix personnel | hors app |
| `dire_sa_lecture` — Dire ce qu'une lecture a rappelé | dire à l'adulte ce que le texte a rappelé, ou à quoi il a fait penser | ne fait rien : elle ne peut pas entendre | hors app |

### Les 33 consignes — le script à enregistrer

| Consigne | Ce que la voix dit | Pictogramme | Employée par |
|---|---|---|---|
| `lis_le_mot_image` | « Lis le mot, puis touche son image. » | mot-et-image | `E01` |
| `trie_selon_graphie` | « Range chaque mot dans la colonne de la lettre qui fait le son. » | colonnes | `E04`, `E07`, `E16`, `E24`, `E25` |
| `trie_selon_son` | « Range chaque mot dans la colonne de la voyelle que tu entends. » | colonnes-sons | `E17` |
| `complete_le_mot` | « Touche la carte qui complète le mot. » | carte-a-poser | `E08` |
| `touche_la_graphie` | « Touche la lettre qui fait le son. » | graphie-a-toucher | `E05`, `E22`, `E34` |
| `touche_le_mot` | « Touche le mot demandé dans la phrase. » | mot-a-toucher | `E32`, `E35` |
| `apparie_mots_images` | « Touche un mot, puis son image. » | deux-colonnes | `E03` |
| `apparie_les_mots` | « Touche deux mots qui vont ensemble. » | deux-colonnes | `E15`, `E23` |
| `choisis_le_texte` | « Touche le texte qui ressemble à celui que tu viens de lire. » | trois-textes | `E55` |
| `ecoute_et_touche` | « Écoute le mot, puis touche-le. » | oreille | `E06`, `E14`, `E31`, `E42` |
| `lis_vite` | « Lis le mot, puis touche le même mot. » | eclair | `E02`, `E36` |
| `vrai_ou_faux_mot` | « Est-ce un vrai mot ? Touche oui ou non. » | oui-non | `E43` |
| `lis_et_touche_le_son` | « Lis les mots, puis touche celui où tu entends le son. » | loupe | `E09`, `E18`, `E26` |
| `classe_les_mots` | « Range ensemble les mots qui se ressemblent. » | paniers | `E44` |
| `choisis_la_forme` | « Touche la forme qui va dans la phrase. » | phrase-a-trou | `E33` |
| `choisis_le_titre` | « Touche le titre qui va avec le texte. » | trois-titres | `E11`, `E47` |
| `choisis_le_resume` | « Touche le résumé qui dit ce que raconte le texte. » | trois-resumes | `E10`, `E46` |
| `touche_la_phrase` | « Touche la phrase qui prouve ta réponse. » | phrase-a-toucher | `E12` |
| `remets_dans_ordre` | « Touche les étapes dans l'ordre de l'histoire. » | etapes | `E19`, `E39`, `E45`, `E51` |
| `touche_le_mot_remplace` | « Touche le mot que remplace le mot souligné. » | lien | `E27`, `E48` |
| `choisis_le_sens` | « Touche le sens qui va avec le texte. » | deux-sens | `E28` |
| `devine_le_mot` | « Touche ce que veut dire le mot en gras. » | loupe | `E29`, `E50` |
| `deduis_la_reponse` | « Touche ce que le texte permet de comprendre, même si ce n'est pas écrit. » | bulle | `E37`, `E49` |
| `cherche_dans_le_texte` | « Cherche la réponse dans le texte, puis touche la phrase. » | phrase-a-toucher | `E40` |
| `suis_la_consigne` | « Lis la consigne, puis fais ce qu'elle dit. » | liste-a-faire | `E38` |
| `touche_l_emotion` | « Touche ce que ressent le personnage. » | visages | `E20`, `E52` |
| `associe_personnage` | « Touche le personnage qui va avec le trait. » | deux-colonnes | `E30` |
| `raconte_ou_explique` | « Ce texte raconte une histoire, ou il explique quelque chose ? » | deux-etiquettes | `E21` |
| `marque_les_pauses` | « Touche les endroits où l'on respire. » | souffle | `E13` |
| `lis_a_voix_haute` | « Lis le texte à voix haute. » | voix | `E41`, `E54` |
| `lis_et_chronometre` | « Lis le texte, et l'adulte note le temps. » | chronometre | `E53` |
| `choisis_ton_livre` | « Choisis le livre que tu veux lire. » | etagere | `E57` |
| `dis_ce_que_tu_penses` | « Dis à l'adulte ce que ce texte t'a rappelé. » | bulle | `E56` |

### Les 57 exercices

| Item | Unité | Domaine | Mécanique | Titre | Ce que la voix dit | Ce que l'enfant fait | Verdict | Durée |
|---|---|---|---|---|---|---|---|---|
| `E01` | 1 | IDM | `lire_mot_image` | Le mot et son image | « Lis le mot, puis touche son image. » | lire le mot écrit, puis toucher l'image correspondante parmi quatre | app | 60 s |
| `E02` | 1 | IDM | `lire_flash` | L'éclair | « Lis le mot, puis touche le même mot. » | lire le mot avant qu'il disparaisse, puis toucher le même mot parmi quatre | app | 45 s |
| `E03` | 1 | IDM | `apparier_mot_image` | Les paires | « Touche un mot, puis son image. » | toucher un mot puis son image, jusqu'à épuiser les paires | app | 90 s |
| `E04` | 2 | IDM | `trier_graphies` | Les colonnes du è | « Range chaque mot dans la colonne de la lettre qui fait le son. » | ranger chaque mot dans la colonne de la graphie qui produit le son | app | 90 s |
| `E05` | 2 | IDM | `toucher_graphie_dans_mot` | Touche le è | « Touche la lettre qui fait le son. » | toucher, dans le mot affiché, la graphie du son entendu | app | 45 s |
| `E06` | 2 | IDM | `ecouter_et_choisir` | Écoute et touche | « Écoute le mot, puis touche-le. » | écouter le mot dit par la voix, puis toucher le mot écrit qui correspond | app | 60 s |
| `E07` | 3 | IDM | `trier_graphies` | Les deux nasales | « Range chaque mot dans la colonne de la lettre qui fait le son. » | ranger chaque mot dans la colonne de la graphie qui produit le son | app | 75 s |
| `E08` | 3 | IDM | `completer_mot` | La carte qui manque | « Touche la carte qui complète le mot. » | toucher la carte-graphie qui complète le mot à trou | app | 60 s |
| `E09` | 4 | IDM | `lire_et_choisir_son` | Où entend-on oin ? | « Lis les mots, puis touche celui où tu entends le son. » | lire les mots affichés, puis toucher celui qui contient le son demandé | app | 60 s |
| `E10` | 5 | CTX | `choisir_resume` | De quoi parle le texte ? | « Touche le résumé qui dit ce que raconte le texte. » | toucher, parmi trois, le résumé qui dit ce que raconte le texte | app | 90 s |
| `E11` | 6 | CTX | `choisir_titre` | Le titre du texte | « Touche le titre qui va avec le texte. » | toucher, parmi trois, le titre qui convient au texte lu | app | 90 s |
| `E12` | 7 | CTX | `toucher_phrase_preuve` | Prouve-le | « Touche la phrase qui prouve ta réponse. » | toucher, dans le texte affiché, la phrase qui permet de répondre | app | 90 s |
| `E13` | 8 | LVH | `marquer_groupes` | Où l'on respire | « Touche les endroits où l'on respire. » | toucher, entre deux mots, les endroits où le groupe se termine et où l'on respire | app | 90 s |
| `E14` | 9 | IDM | `ecouter_et_choisir` | Le son de la montagne | « Écoute le mot, puis touche-le. » | écouter le mot dit par la voix, puis toucher le mot écrit qui correspond | app | 60 s |
| `E15` | 10 | IDM | `apparier_graphies` | Deux mots pour un son | « Touche deux mots qui vont ensemble. » | toucher deux mots dont une graphie produit le même son | app | 60 s |
| `E16` | 11 | IDM | `trier_graphies` | Le f de la photo | « Range chaque mot dans la colonne de la lettre qui fait le son. » | ranger chaque mot dans la colonne de la graphie qui produit le son | app | 75 s |
| `E17` | 12 | IDM | `trier_sons` | Les deux eu | « Range chaque mot dans la colonne de la voyelle que tu entends. » | ranger chaque mot dans la colonne de la voyelle qu'on entend, quand deux sons s'écrivent pareil | app | 75 s |
| `E18` | 13 | IDM | `lire_et_choisir_son` | Lundi ou lune ? | « Lis les mots, puis touche celui où tu entends le son. » | lire les mots affichés, puis toucher celui qui contient le son demandé | app | 75 s |
| `E19` | 14 | CTX | `ordonner_recit` | Dans l'ordre | « Touche les étapes dans l'ordre de l'histoire. » | toucher les étapes du récit dans l'ordre où elles arrivent | app | 120 s |
| `E20` | 15 | CTX | `toucher_emotion` | Ce qu'elle ressent | « Touche ce que ressent le personnage. » | toucher le mot qui dit ce que ressent le personnage à ce moment du texte | app | 90 s |
| `E21` | 16 | DVL | `distinguer_type` | Ça raconte ou ça explique ? | « Ce texte raconte une histoire, ou il explique quelque chose ? » | toucher « il raconte une histoire » ou « il explique quelque chose » | app | 90 s |
| `E22` | 17 | IDM | `toucher_graphie_dans_mot` | La fin en tion | « Touche la lettre qui fait le son. » | toucher, dans le mot affiché, la graphie du son entendu | app | 60 s |
| `E23` | 18 | IDM | `apparier_graphies` | Les mots qui riment | « Touche deux mots qui vont ensemble. » | toucher deux mots dont une graphie produit le même son | app | 90 s |
| `E24` | 19 | IDM | `trier_graphies` | Le c de citron | « Range chaque mot dans la colonne de la lettre qui fait le son. » | ranger chaque mot dans la colonne de la valeur de la lettre | app | 90 s |
| `E25` | 20 | IDM | `trier_graphies` | Le g de girafe | « Range chaque mot dans la colonne de la lettre qui fait le son. » | ranger chaque mot dans la colonne de la valeur de la lettre | app | 75 s |
| `E26` | 21 | IDM | `lire_et_choisir_son` | Le s qui chante | « Lis les mots, puis touche celui où tu entends le son. » | lire les mots affichés, puis toucher celui qui contient le son demandé | app | 90 s |
| `E27` | 22 | CTX | `toucher_referent` | Qui est-il ? | « Touche le mot que remplace le mot souligné. » | toucher, plus haut dans le texte, le mot que désigne le pronom souligné | app | 90 s |
| `E28` | 23 | CTX | `lever_ambiguite` | Le chat est-il là ? | « Touche le sens qui va avec le texte. » | toucher, entre deux sens possibles, celui que le texte retient | app | 90 s |
| `E29` | 24 | CTX | `deviner_mot` | Que veut dire potion ? | « Touche ce que veut dire le mot en gras. » | toucher, parmi trois, ce que veut dire le mot en gras, d'après le texte | app | 90 s |
| `E30` | 25 | DVL | `associer_personnage_trait` | Qui aime quoi ? | « Touche le personnage qui va avec le trait. » | toucher le trait qui va avec le personnage, pour chaque personnage | app | 120 s |
| `E31` | 26 | IDM | `ecouter_et_choisir` | La lettre qu'on n'entend pas | « Écoute le mot, puis touche-le. » | écouter le mot dit par la voix, puis toucher le mot écrit qui correspond | app | 75 s |
| `E32` | 27 | IDM | `toucher_mot_dans_phrase` | La marque du pluriel | « Touche le mot demandé dans la phrase. » | toucher, dans la phrase affichée, le mot qui porte la marque du pluriel | app | 90 s |
| `E33` | 27 | IDM | `choisir_forme` | Le pluriel ou le singulier | « Touche la forme qui va dans la phrase. » | toucher la forme du mot qui convient à la phrase | app | 90 s |
| `E34` | 28 | IDM | `toucher_graphie_dans_mot` | Les lettres en double | « Touche la lettre qui fait le son. » | toucher, dans le mot affiché, la consonne doublée | app | 75 s |
| `E35` | 29 | IDM | `toucher_mot_dans_phrase` | Le mot qu'on connaît par cœur | « Touche le mot demandé dans la phrase. » | toucher, dans la phrase affichée, le mot-outil entendu | app | 90 s |
| `E36` | 30 | IDM | `lire_flash` | Les mots qui ne se déchiffrent pas | « Lis le mot, puis touche le même mot. » | lire le mot avant qu'il disparaisse, puis toucher le même mot parmi quatre | app | 75 s |
| `E37` | 31 | CTX | `inferer` | Ce que le texte ne dit pas | « Touche ce que le texte permet de comprendre, même si ce n'est pas écrit. » | toucher la réponse qui se déduit du texte sans y être écrite | app | 90 s |
| `E38` | 32 | CTX | `suivre_consigne_ecrite` | Fais la recette | « Lis la consigne, puis fais ce qu'elle dit. » | lire la consigne du texte et faire ce qu'elle dit, dans l'ordre | app | 120 s |
| `E39` | 32 | CTX | `ordonner_recit` | La recette dans l'ordre | « Touche les étapes dans l'ordre de l'histoire. » | toucher les étapes du texte dans l'ordre où elles arrivent | app | 120 s |
| `E40` | 33 | CTX | `prelever_info` | Que fait le chat la nuit ? | « Cherche la réponse dans le texte, puis touche la phrase. » | toucher, parmi les phrases du texte, celle qui porte l'information demandée | app | 120 s |
| `E45` | 37 | CTX | `ordonner_recit` | Le résumé en images | « Touche les étapes dans l'ordre de l'histoire. » | toucher les étapes du récit dans l'ordre où elles arrivent | app | 120 s |
| `E41` | 34 | LVH | `lire_a_voix_haute` | Lis pour quelqu'un | « Lis le texte à voix haute. » | aucun geste de réponse : l'enfant lit, un adulte valide | hors app | 180 s |
| `E53` | 39 | LVH | `lire_et_chronometrer` | Soixante-dix mots par minute | « Lis le texte, et l'adulte note le temps. » | lire le texte pendant que l'adulte mesure le temps | hors app | 180 s |
| `E54` | 40 | LVH | `lire_a_voix_haute` | Mets le ton | « Lis le texte à voix haute. » | aucun geste de réponse : l'enfant lit, un adulte valide | hors app | 180 s |
| `E42` | 35 | IDM | `ecouter_et_choisir` | Les mots qui n'existent pas | « Écoute le mot, puis touche-le. » | écouter la suite de lettres dite par la voix, puis toucher celle qui correspond | app | 75 s |
| `E43` | 35 | IDM | `lire_pseudo_mot` | Vrai mot ou pas ? | « Est-ce un vrai mot ? Touche oui ou non. » | toucher « oui » si la suite est un mot français, « non » sinon | app | 75 s |
| `E44` | 36 | IDM | `classer_famille` | Les familles de mots | « Range ensemble les mots qui se ressemblent. » | ranger les mots qui se ressemblent dans la même famille | app | 120 s |
| `E46` | 38 | CTX | `choisir_resume` | Le résumé de la pomme d'or | « Touche le résumé qui dit ce que raconte le texte. » | toucher, parmi trois, le résumé qui dit ce que raconte le texte | app | 180 s |
| `E47` | 38 | CTX | `choisir_titre` | Un titre pour la pomme d'or | « Touche le titre qui va avec le texte. » | toucher, parmi trois, le titre qui convient au texte lu | app | 120 s |
| `E48` | 38 | CTX | `toucher_referent` | Qui arrive ? | « Touche le mot que remplace le mot souligné. » | toucher, plus haut dans le texte, le mot que désigne le pronom souligné | app | 120 s |
| `E49` | 38 | CTX | `inferer` | Ce que le texte ne dit pas | « Touche ce que le texte permet de comprendre, même si ce n'est pas écrit. » | toucher la réponse qui se déduit du texte sans y être écrite | app | 120 s |
| `E50` | 38 | CTX | `deviner_mot` | Que veut dire pommier ? | « Touche ce que veut dire le mot en gras. » | toucher, parmi trois, ce que veut dire le mot en gras, d'après le texte | app | 120 s |
| `E51` | 38 | CTX | `ordonner_recit` | L'histoire dans l'ordre | « Touche les étapes dans l'ordre de l'histoire. » | toucher les étapes du récit dans l'ordre où elles arrivent | app | 150 s |
| `E52` | 38 | CTX | `toucher_emotion` | Ce que la reine ressent | « Touche ce que ressent le personnage. » | toucher le mot qui dit ce que ressent le personnage à ce moment du texte | app | 120 s |
| `E55` | 41 | DVL | `apparier_textes` | Le texte qui ressemble | « Touche le texte qui ressemble à celui que tu viens de lire. » | toucher, parmi trois textes courts, celui qui ressemble à celui qu'on vient de lire | app | 150 s |
| `E56` | 41 | DVL | `dire_sa_lecture` | Ce que ça t'a rappelé | « Dis à l'adulte ce que ce texte t'a rappelé. » | aucun geste de réponse : l'enfant parle à l'adulte | hors app | 180 s |
| `E57` | 42 | DVL | `choisir_son_livre` | Le livre que tu veux | « Choisis le livre que tu veux lire. » | aucun geste de réponse : l'enfant parcourt et choisit | hors app | 300 s |

### Le contenu et le matériel

| Item | Contenu de la série | Mots | Dont affichés en image | Phonèmes | Graphies | Texte adossé | Textes courts cités | Pseudo-mots |
|---|---|---|---|---|---|---|---|---|
| `E01` | chat ; rat ; sac ; main | `chat`, `rat`, `sac`, `main` | `chat`, `rat`, `sac`, `main` | — | — | — | — | — |
| `E02` | dix mots affichés un court instant, un par un, puis choisis parmi quatre | `chat`, `rat`, `sac`, `valise`, `moto`, `vélo`, `table`, `lune`, `tomate`, `banane` | — | — | — | — | — | — |
| `E03` | huit mots et leurs huit images, mélangés | `papa`, `maman`, `bébé`, `lune`, `jupe`, `café`, `vélo`, `moto` | `papa`, `maman`, `bébé`, `lune`, `jupe`, `café`, `vélo`, `moto` | — | — | — | — | — |
| `E04` | quatre colonnes : ai, ei, è, ê ; onze mots à ranger | `craie`, `reine`, `lait`, `maison`, `chaise`, `zèbre`, `père`, `mère`, `fête`, `tête`, `aime` | — | — | `ai`, `ei`, `è`, `ê` | — | — | — |
| `E05` | cinq mots, la graphie du son à toucher dans chacun | `craie`, `reine`, `père`, `fête`, `chaise` | — | — | `ai`, `ei`, `è`, `ê` | — | — | — |
| `E06` | six mots dits un par un, chacun à retrouver parmi quatre écrits | `craie`, `reine`, `père`, `tête`, `zèbre`, `lait` | — | `/ɛ/` | — | — | — | — |
| `E07` | deux colonnes : en, em ; huit mots à ranger | `vent`, `dent`, `tempête`, `emporte`, `entend`, `ensemble`, `content`, `moment` | — | — | `en`, `em` | — | — | — |
| `E08` | cinq mots à trou, les cartes en et em sous la main | `vent`, `dent`, `tempête`, `emporte`, `enfant` | — | — | `en`, `em` | — | — | — |
| `E09` | six mots affichés, un seul porte oin | `coin`, `point`, `loin`, `besoin`, `joint`, `rejoint` | — | — | — | — | — | — |
| `E10` | le texte « Le chat » affiché en entier ; une question, trois résumés | — | — | — | — | T01-rang01 | — | — |
| `E11` | le texte « La fête » affiché en entier ; une question, trois titres | — | — | — | — | T02-rang02 | — | — |
| `E12` | le texte « Le vent » affiché en phrases touchables ; une question, une phrase à trouver | — | — | — | — | T03-rang03 | — | — |
| `E13` | le texte « La maison de la reine » en mots touchables ; sept coupures à placer | — | — | — | — | T05-rang08 | — | — |
| `E14` | cinq mots dits un par un, chacun à retrouver parmi trois écrits | `agneau`, `montagne`, `vigne`, `signe`, `campagne` | — | `/ɲ/` | — | — | — | — |
| `E15` | fille et billet d'un côté, yeux et crayon de l'autre, mélangés | `fille`, `billet`, `yeux`, `crayon` | — | — | `ill`, `y` | — | — | — |
| `E16` | deux colonnes : ph et f ; six mots à ranger | `photo`, `téléphone`, `éléphant`, `phrase`, `fleur`, `fête` | — | `/f/` | `ph` | — | — | — |
| `E17` | deux colonnes : eu de fleur, eu de deux ; six mots à ranger | `fleur`, `peur`, `deux`, `peu`, `jeu`, `bleu` | — | `/œ/`, `/ø/` | — | — | — | — |
| `E18` | six mots affichés, dont trois portent la nasale un et trois le u suivi de n | `lundi`, `brun`, `chacun`, `aucun`, `lune`, `brune` | — | `/œ̃/` | — | — | — | — |
| `E19` | le texte « L'éléphant et le téléphone » lu d'abord ; quatre images de récit mélangées à remettre dans l'ordre | — | — | — | — | T07-rang11 | — | — |
| `E20` | le texte « La montagne » affiché ; une question, trois mots d'émotion | — | — | — | — | T06-rang09 | — | — |
| `E21` | deux textes courts affichés l'un sous l'autre ; trois étiquettes à toucher : le titre de chaque texte, et « ni l'un ni l'autre » | — | — | — | — | — | `C01-rang16`, `C02-rang16` | — |
| `E22` | six mots, la fin tion à toucher dans chacun | `potion`, `nation`, `station`, `action`, `direction`, `question` | — | — | `tion` | — | — | — |
| `E23` | six mots à apparier deux par deux, sur la fin qui sonne pareil | `soleil`, `fauteuil`, `grenouille`, `oreille`, `feuille`, `travail` | — | — | `ail`, `eil`, `euil`, `ouille`, `aille`, `eille`, `euille` | — | — | — |
| `E24` | deux colonnes : le c de citron, le c de café ; huit mots à ranger | `citron`, `place`, `cinéma`, `merci`, `café`, `cartable`, `canard`, `école` | — | `/s/`, `/k/` | `c` | — | — | — |
| `E25` | deux colonnes : le g de girafe, le g de gâteau ; cinq mots à ranger | `girafe`, `mange`, `mélange`, `rouge`, `gâteau` | — | `/ʒ/`, `/g/` | `g` | — | — | — |
| `E26` | neuf mots affichés, à partager entre le s qui fait /z/ et le s qui fait /s/ | `maison`, `chaise`, `oiseau`, `rose`, `valise`, `musique`, `chemise`, `tasse`, `poisson` | — | `/z/`, `/s/` | — | — | — | — |
| `E27` | le texte « Le chat de la reine » affiché ; trois pronoms soulignés, trois mots à toucher | — | — | — | — | T09-rang16 | — | — |
| `E28` | le texte « Le lundi brun » affiché ; une question, deux réponses contraires | — | — | — | — | T08-rang13 | — | — |
| `E29` | le texte « La station » affiché, le mot potion en gras ; une question, trois sens | — | — | — | — | T10-rang17 | — | — |
| `E30` | le texte « La valise de la reine » affiché ; trois personnages, trois traits | — | — | — | — | T12-rang21 | — | — |
| `E31` | six mots dits un par un, chacun à retrouver parmi trois écrits | `loup`, `nez`, `cheval`, `animal`, `tabac`, `fusil` | — | — | — | — | — | — |
| `E32` | un texte court de quatre lignes ; une phrase à la fois, un mot à toucher par phrase | — | — | — | — | — | `C03-rang27` | — |
| `E33` | deux phrases à trou, deux formes à chaque fois | — | — | — | — | — | `C03-rang27` | — |
| `E34` | le texte « La pomme » affiché ; cinq mots où la consonne doublée est à toucher | `pomme`, `échelle`, `appelle`, `arrive`, `attend` | — | — | — | T14-rang28 | — | — |
| `E35` | le texte « La pomme » affiché ; six mots-outils à retrouver dans les phrases | `et`, `est`, `elle`, `dans`, `avec`, `un` | — | — | — | T14-rang28 | — | — |
| `E36` | cinq mots affichés un court instant, un par un, puis choisis parmi quatre | `monsieur`, `femme`, `second`, `fils`, `œil` | — | — | — | — | — | — |
| `E37` | le texte « Monsieur le chat » affiché ; une question dont la réponse n'est pas écrite | — | — | — | — | T15-rang30 | — | — |
| `E38` | le texte « La recette de la reine » affiché en étapes ; six gestes à faire dans l'ordre | — | — | — | — | T16-rang32 | — | — |
| `E39` | six étapes de la recette mélangées, à remettre dans l'ordre | — | — | — | — | T16-rang32 | — | — |
| `E40` | le texte « Le chat » affiché en phrases touchables ; trois questions | — | — | — | — | T17-rang33 | — | — |
| `E45` | quatre images de récit : les moments du texte « Le chat » ; l'ordre à reconstruire | — | — | — | — | T17-rang33 | — | — |
| `E41` | le texte « Le chat » (T17-rang33), lu après préparation | — | — | — | — | T17-rang33 | — | — |
| `E53` | le texte « La pomme d'or » (T18-rang38), soixante-quinze mots | — | — | — | — | T18-rang38 | — | — |
| `E54` | le texte « La pomme d'or » (T18-rang38), relu avec un autre ton | — | — | — | — | T18-rang38 | — | — |
| `E42` | cinq suites de lettres dites une par une, chacune à retrouver parmi trois écrites | — | — | — | — | — | — | ``doir` (pm01)`, ``stag` (pm02)`, ``choust` (pm03)`, ``valin` (pm04)`, ``cagnou` (pm05)` |
| `E43` | dix suites affichées une par une, cinq mots et cinq pseudo-mots mêlés | `montagne`, `soleil`, `poisson`, `cartable`, `musique` | — | — | — | — | — | ``flaption` (pm06)`, ``trumpon` (pm07)`, ``pharmou` (pm08)`, ``girou` (pm09)`, ``poinche` (pm10)` |
| `E44` | trois familles à remplir : les mots en c de citron, en c de café, en tion | `citron`, `cinéma`, `place`, `face`, `café`, `cartable`, `école`, `flacon`, `flocon`, `potion`, `nation`, `station` | — | — | `c`, `tion` | — | — | — |
| `E46` | le texte « La pomme d'or » affiché en entier ; trois questions de compréhension | — | — | — | — | T18-rang38 | — | — |
| `E47` | le texte « La pomme d'or » affiché en entier ; trois titres | — | — | — | — | T18-rang38 | — | — |
| `E48` | le texte « La pomme d'or » affiché ; trois pronoms soulignés, trois mots à toucher | — | — | — | — | T18-rang38 | — | — |
| `E49` | le texte « La pomme d'or » affiché ; une question dont la réponse n'est pas écrite | — | — | — | — | T18-rang38 | — | — |
| `E50` | le texte « La pomme d'or » affiché, le mot pommier en gras ; une question, trois sens | — | — | — | — | T18-rang38 | — | — |
| `E51` | cinq étapes du texte « La pomme d'or » mélangées ; l'ordre à reconstruire | — | — | — | — | T18-rang38 | — | — |
| `E52` | le texte « La pomme d'or » affiché ; une question, trois mots d'émotion | — | — | — | — | T18-rang38 | — | — |
| `E55` | le texte « La pomme d'or » lu d'abord ; trois textes courts affichés | — | — | — | — | T18-rang38 | `C04-rang41`, `C02-rang16`, `C05-rang41` | — |
| `E56` | le texte « La pomme d'or » relu, puis un temps de parole | — | — | — | — | T18-rang38 | — | — |
| `E57` | une étagère de livres, à parcourir sans consigne de lecture | — | — | — | — | — | — | — |

### Ce que chaque exercice entraîne, et ce qu'il ne vérifie pas

| Item | Entraîne | Ne vérifie pas |
|---|---|---|
| `E01` | lire un mot entier sans le décomposer, et le rapprocher de ce qu'il désigne | le sens du mot hors de l'image : l'exercice demande de reconnaître, pas de définir |
| `E02` | reconnaître un mot d'un seul regard, sans passer par la syllabe | la vitesse de lecture à voix haute, qui ne se mesure pas à l'écran |
| `E03` | tenir un mot en mémoire le temps de trouver son image | l'ordre dans lequel les paires sont trouvées : il n'y a pas de bon ordre |
| `E04` | reconnaître la graphie qui produit le son, dans un mot entier | l'orthographe du mot : l'enfant range, il n'écrit pas |
| `E05` | isoler la graphie dans le mot, au lieu de la reconnaître de loin | la lecture du reste du mot : le doigt peut tomber juste sans que le mot soit lu |
| `E06` | faire correspondre ce qu'on entend et ce qu'on voit écrit | la production du son : l'enfant reconnaît, il ne prononce pas |
| `E07` | voir que la nasale change de lettre selon celle qui suit | le choix de la lettre dans un mot nouveau : l'enfant range des mots qu'il voit |
| `E08` | produire la graphie au lieu de la reconnaître, sans écrire | l'écriture du mot : l'enfant pose une carte, il ne trace pas les lettres |
| `E09` | entendre la nasale rare dans un mot qu'on lit | l'orthographe de oin : l'enfant choisit un mot, il ne l'écrit pas |
| `E10` | tenir le texte entier en tête, et non sa première phrase | le choix des mots du résumé : l'enfant choisit, il ne rédige pas |
| `E11` | décider de quoi le texte parle, et le reconnaître parmi d'autres | la formulation d'un titre par l'enfant : c'est elle qui est visée par l'unité, et elle se vérifie à l'oral |
| `E12` | retourner au texte, au lieu de répondre de mémoire | la formulation de la justification : l'enfant montre la phrase, il ne dit pas pourquoi elle prouve |
| `E13` | découper le texte en groupes de sens, et non mot à mot | la lecture qui suit : placer les coupures ne dit rien de la façon de lire à voix haute |
| `E14` | entendre /ɲ/ et le reconnaître dans deux lettres écrites | la prononciation de /ɲ/ par l'enfant : il choisit, il ne dit pas |
| `E15` | voir que deux graphies différentes portent le même son | le choix de la graphie dans un mot nouveau : l'enfant apparie ce qu'il voit |
| `E16` | distinguer les deux écritures du même son | le choix entre ph et f quand on écrit : l'enfant range des mots qu'il voit |
| `E17` | distinguer deux voyelles que l'écriture ne distingue pas | la règle qui décide, qui n'existe pas : c'est le mot qu'on connaît qui tranche, pas la graphie |
| `E18` | séparer une nasale de deux lettres qui se suivent sans former de son | la prononciation de la nasale : l'enfant lit, il ne dit pas à voix haute |
| `E19` | tenir la suite des événements, et non un seul moment | la mise en mots du récit : l'ordre est jugé, la narration ne l'est pas |
| `E20` | lire un état intérieur dans ce que le texte raconte | le mot que l'enfant emploierait lui-même pour dire l'émotion |
| `E21` | reconnaître ce qui arrive de ce qui est toujours vrai | la lecture de textes longs des deux types : les deux textes comparés sont courts, et le documentaire long n'arrive qu'au rang 33 |
| `E22` | isoler un suffixe insécable, où le t ne se lit pas comme un t | le sens du mot : l'exercice porte sur la fin, pas sur ce qu'elle veut dire |
| `E23` | entendre que le l de ces fins ne s'entend pas | l'écriture de ces fins : l'enfant apparie des mots qu'il voit |
| `E24` | décider de la valeur d'une lettre par la lettre qui suit | les mots où le c ne fait ni /s/ ni /k/ : il n'y en a pas dans la série |
| `E25` | décider de la valeur du g par la lettre qui suit, comme pour le c | la graphie ge devant a, o, u : la série ne la contient pas |
| `E26` | décider de la valeur du s par ce qui l'entoure | la règle écrite : c'est le voisinage qu'on voit, pas une règle qu'on récite |
| `E27` | remonter le texte pour retrouver qui un mot désigne | les reprises qui ne sont pas des pronoms : la série n'en contient pas |
| `E28` | trancher entre deux phrases du texte qui semblent se contredire | les ambiguïtés de sens d'un mot : la série porte sur une contradiction apparente |
| `E29` | se servir du texte pour comprendre un mot qu'on ne connaît pas | le sens exact du mot hors du texte : c'est le sens d'ici qui est demandé |
| `E30` | rattacher un trait à un personnage, et non au texte en général | le portrait que l'enfant ferait du personnage, qui est ce que l'unité vise |
| `E31` | voir une lettre à la fin d'un mot sans la faire sonner | l'explication de la lettre muette : elle ne se devine pas, elle s'apprend |
| `E32` | voir la marque du pluriel là où elle ne s'entend pas | la règle de l'accord : l'enfant repère la marque, il ne l'explique pas |
| `E33` | accorder le verbe au sujet, sur une marque qu'on ne prononce pas | la production écrite de la marque : l'enfant touche une forme, il ne l'écrit pas |
| `E34` | voir deux lettres pour un seul son | la prononciation de la double : elle ne s'entend pas, elle s'écrit |
| `E35` | reconnaître d'un seul regard les mots que le texte emploie partout | la lecture des autres mots de la phrase : l'exercice ne porte que sur les mots-outils |
| `E36` | reconnaître d'un seul regard les mots dont les lettres ne disent pas le son | la raison de l'irrégularité : ces mots ne s'expliquent pas, ils s'apprennent |
| `E37` | conclure ce que le texte permet de comprendre sans l'écrire | le raisonnement de l'enfant : seule la conclusion est jugée |
| `E38` | exécuter un texte qui dit quoi faire, et dans quel ordre | la réussite de la recette hors de l'écran : les gestes sont vérifiés, pas le gâteau |
| `E39` | suivre l'ordre d'un texte qui enchaîne des étapes | le temps de réalisation : l'ordre est jugé, pas la durée |
| `E40` | trouver une information précise dans un texte qu'on ne raconte pas | la mémorisation du texte : la question se traite en y retournant |
| `E45` | choisir les moments qui comptent, et les remettre dans l'ordre | ce qu'un résumé doit laisser de côté : la sélection est faite d'avance |
| `E41` | lire un texte préparé en marquant les pauses | tout ce qui s'entend : le ton, le rythme, la justesse des pauses |
| `E53` | lire un texte entier sans s'arrêter | la fluence elle-même : l'application mesure, elle n'évalue pas |
| `E54` | adapter sa voix au sens du texte | tout : cette unité ne passe pas par un écran |
| `E42` | décoder des suites de lettres qu'on n'a jamais vues | l'écriture de ces suites : l'enfant les reconnaît, il ne les écrit pas |
| `E43` | décoder d'abord, décider ensuite — un pseudo-mot se lit sans se reconnaître | ce que l'enfant fait d'un mot qu'il croit reconnaître sans le lire |
| `E44` | ranger des mots nouveaux par la graphie qu'ils partagent | la famille du sens : c'est la famille de l'écriture qui est demandée ici |
| `E46` | dégager le sens du texte entier, seul | la qualité du résumé que l'enfant ferait lui-même |
| `E47` | choisir ce qui dit le mieux le texte entier | le titre que l'enfant inventerait : il choisit parmi trois |
| `E48` | suivre qui fait quoi dans un texte qui nomme peu | les reprises par un nom : la série porte sur les pronoms |
| `E49` | conclure ce que le texte permet de comprendre sans l'écrire | le chemin du raisonnement : seule la conclusion est jugée |
| `E50` | se servir de la forme du mot et du texte pour le comprendre | le sens du mot hors du texte : c'est le sens d'ici qui est demandé |
| `E51` | restituer la suite du récit, du début à la fin | la mise en mots du récit : l'ordre est jugé, la narration ne l'est pas |
| `E52` | lire un sentiment dans ce que le texte dit du lien entre deux personnages | le mot que l'enfant emploierait lui-même : trois mots lui sont proposés |
| `E55` | reconnaître ce qu'une lecture a de commun avec une autre | le lien que l'enfant ferait avec sa propre expérience, qui ne se touche pas |
| `E56` | mettre en mots ce qu'une lecture a rappelé | tout ce qui se dit : l'application ne peut ni l'entendre ni le juger |
| `E57` | aller vers un livre de son propre mouvement | tout : cette unité se joue hors de l'application, et c'est son intérêt |

### Les 27 questions, et leur phrase-preuve

| Item | Texte | Question | Bonne réponse | Intrus | Phrase-preuve |
|---|---|---|---|---|---|
| `E10` | T01-rang01 | Quel résumé dit ce que raconte le texte ? | Le chat prend la noix, et la souris rit. | La souris prend la noix, et le chat rit. ; Le chat a une souris, et la souris a un chat. | « Le chat a la noix. » |
| `E12` | T03-rang03 | Qu'est-ce que le vent emporte ? | la craie | les pains ; la maison | « Le vent emporte la craie. » |
| `E19` | T07-rang11 | Que trouve-t-on sur la photo ? | un éléphant avec un téléphone | un éléphant dans la maison ; un téléphone sur la table | « Sur la photo, un éléphant a un téléphone. » |
| `E20` | T06-rang09 | Que veut la reine, dans ce texte ? | être avec l'agneau et la montagne | rejoindre le chat de la maison ; trouver une craie dans la vigne | « L'agneau a besoin de la reine. » |
| `E21` | `C01-rang16`, `C02-rang16` | Touche le texte qui raconte une histoire. | L'agneau de la reine | L'air qui va ; Ni l'un ni l'autre | « Un lundi, il a rejoint la maison. » |
| `E27` | T09-rang16 | Dans « Le chat a besoin de la reine », qui est « le chat » ? | le chat brun de la reine | l'agneau de la vigne ; le chat de la montagne | « La reine a un chat brun. » |
| `E28` | T08-rang13 | La reine a-t-elle un chat ? | Oui, elle a un chat brun. | Non, aucun chat n'est dans la maison. ; Non, le chat est dans la vigne. | « La reine a un chat brun. » |
| `E29` | T10-rang17 | Que veut dire « la potion », dans ce texte ? | quelque chose qui a une action sur le chat | une station sur la montagne ; une question de papa | « La potion a une action sur le chat. » |
| `E30` | T12-rang21 | Qu'aime l'oiseau ? | la musique | la chemise ; le poisson | « L'oiseau aime la musique. » |
| `E32` | `C03-rang27` | Quel mot porte la marque du pluriel dans « Ils dorment le jour » ? | dorment | jour ; Ils | « Ils dorment le jour. » |
| `E33` | `C03-rang27` | Les chats ___ la maison. | aiment | aime ; aimes | « Les chats aiment la maison. » |
| `E33` | `C03-rang27` | Ils ___ le jour. | dorment | dort ; dorme | « Ils dorment le jour. » |
| `E37` | T15-rang30 | Pourquoi monsieur le chat appelle-t-il la reine ? | parce qu'elle apporte une pomme | parce qu'elle a une question ; parce qu'elle a une valise | « La reine arrive avec une pomme. » |
| `E38` | T16-rang32 | Par quoi papa commence-t-il ? | il coupe la pomme | il ajoute le lait ; il mélange avec une cuillère | « Papa coupe la pomme. » |
| `E39` | T16-rang32 | Qu'est-ce qui vient juste après avoir mis la pomme dans la tasse ? | ajouter le lait | couper la pomme ; appeler la reine | « Il ajoute le lait. » |
| `E40` | T17-rang33 | Où le chat dort-il le jour ? | sur une chaise | dans le jardin ; sur l'échelle | « Le jour, il dort sur une chaise. » |
| `E40` | T17-rang33 | Que fait le chat la nuit ? | il sort dans le jardin | il dort sur une chaise ; il lave sa robe | « La nuit, il sort dans le jardin. » |
| `E40` | T17-rang33 | Avec quoi le chat lave-t-il sa robe ? | avec sa langue | avec ses griffes ; avec sa main | « Il lave sa robe avec sa langue. » |
| `E45` | T17-rang33 | Quel moment vient en dernier ? | le chat est un bon compagnon | le chat dort sur une chaise ; le chat lave sa robe | « Le chat est un bon compagnon. » |
| `E46` | T18-rang38 | Quel résumé dit ce que raconte le texte ? | Le chat trouve une pomme d'or et appelle la reine pour la manger avec lui. | La reine trouve une pomme d'or et la donne à son chat. ; Le chat monte sur une échelle et prend la pomme pour lui seul. | « Il appelle la reine. » |
| `E47` | T18-rang38 | Quel titre convient le mieux à ce texte ? | La pomme d'or | Le chat de la montagne ; La valise de la reine | « Sur le pommier, une pomme d'or. » |
| `E48` | T18-rang38 | Dans « Elle arrive avec une valise », qui est « elle » ? | la reine | la pomme ; la valise | « La reine a un chat brun. » |
| `E49` | T18-rang38 | Pourquoi le chat appelle-t-il la reine ? | parce qu'il veut partager la pomme avec elle | parce qu'il ne peut pas monter sur l'échelle ; parce qu'il a perdu sa valise | « Ils mangent la pomme ensemble. » |
| `E50` | T18-rang38 | Que veut dire « le pommier », dans ce texte ? | l'arbre où il y a une pomme | la valise de la reine ; le jardin de la maison | « Dans le jardin, il y a un pommier. » |
| `E51` | T18-rang38 | Que fait le chat en arrivant dans le jardin ? | il voit un pommier | il appelle la reine ; il monte sur une échelle | « Dans le jardin, il y a un pommier. » |
| `E52` | T18-rang38 | Que ressent la reine pour son chat, à la fin du texte ? | de l'affection | de la peur ; de la colère | « La reine aime son chat brun. » |
| `E55` | T18-rang38 | Quel texte ressemble le plus à celui que tu viens de lire ? | Une échelle, une pomme | L'air qui va ; Le téléphone de papa | « Il a grimpé sur une échelle. » |

### Les 7 inversions — ce que le geste reprend

| Item | Unité | Objectif de l'unité | Ce que le geste reprend |
|---|---|---|---|
| `E11` | 6 | Donner un titre au texte | Le programme demande de DONNER un titre au texte, et donner un titre est un acte de parole : la machine ne peut pas l'entendre. Le geste garde le jugement — reconnaître, parmi trois, celui qui convient — et perd la production. Les deux intrus sont des titres plausibles du même texte : « Les pains de maman » et « Le vent de la maison » parlent du même monde sans dire de quoi le texte parle. |
| `E12` | 7 | Justifier une réponse par un retour au texte | Le programme demande de JUSTIFIER une réponse par un retour au texte. Justifier est un acte de parole ; toucher la phrase qui le dit est le geste qui en garde la trace. L'enfant n'explique pas sa raison : il montre l'endroit, et c'est cet endroit qui est jugé. |
| `E19` | 14 | Restituer les enchaînements logiques et chronologiques d'un récit | Le programme demande de RESTITUER les enchaînements du récit, et restituer est un acte de parole. Le geste garde l'ordre — la seule chose qui s'y vérifie — et perd le récit. Un enfant qui remet les étapes dans l'ordre n'a pas dit l'histoire. |
| `E20` | 15 | Expliciter les émotions des personnages | Le programme demande d'EXPLICITER les émotions des personnages, et expliciter est un acte de parole — le palier de sortie range d'ailleurs cet objectif hors app. Le geste garde le repérage : le texte dit que l'agneau a besoin de la reine, et l'enfant touche ce que cela dit du lien. Il ne nomme pas l'émotion de lui-même. |
| `E30` | 25 | Caractériser les personnages et reconnaître des types récurrents | Le programme demande de CARACTÉRISER les personnages, et caractériser est un acte de parole. Le geste garde l'appariement — ce que le texte dit de chacun — et perd le portrait. Un enfant qui apparie juste n'a pas dit quel personnage est le chat. |
| `E45` | 37 | Résumer le texte | Le programme demande de RÉSUMER le texte, oralement — le palier de sortie range cet objectif hors app. Le geste garde la trame : remettre les moments dans l'ordre est ce qui reste d'un résumé quand on ne peut pas le dire. Le résumé lui-même, celui qui choisit ce qu'on garde et ce qu'on laisse, n'est pas jugé. |
| `E55` | 41 | Relier ses lectures à son expérience et à ses autres lectures | Le programme demande d'ÉTABLIR DES LIENS entre ses lectures, et dire ce lien est un acte de parole. Le geste garde le rapprochement — reconnaître ce qui se ressemble — et perd l'explication du lien. Un enfant qui touche le bon texte n'a pas dit pourquoi il ressemble. |

### Les 5 exercices hors app

| Item | Unité | Pourquoi l'application ne peut pas juger | Substitution |
|---|---|---|---|
| `E41` | 34 | l'application ne peut pas entendre. Réaliser les pauses adéquates se vérifie à l'oreille d'un adulte, et le palier de sortie déclare déjà cet objectif hors app. | le jumeau réceptif est E13 : l'enfant touche, dans le texte, les endroits où le groupe de mots se termine. Il vérifie le repérage des groupes de souffle, jamais la lecture qui les respecte. |
| `E53` | 39 | la vitesse de lecture ne se mesure pas sans micro : l'application ne peut pas compter les mots que l'enfant a lus. Elle affiche le texte et le nombre de mots, et laisse l'adulte saisir la durée — c'est un chronomètre, pas un juge. | aucune : la fluence n'a pas de jumeau réceptif. Un exercice qui ferait toucher des mots ne mesurerait pas une vitesse, et prétendre le contraire serait la faute la plus coûteuse de la banque. |
| `E54` | 40 | modifier sa voix et sa cadence selon le sens est un acte de parole, et l'application n'a pas de micro. Le palier de sortie range la lecture expressive hors app, au bilan. | aucune : rien dans l'application ne juge l'expressivité. Un jumeau réceptif qui prétendrait le faire mesurerait autre chose, et le ferait passer pour ce qu'il n'est pas. |
| `E56` | 41 | relier une lecture à sa propre expérience est un acte de parole, et l'application n'a pas de micro. C'est la moitié de l'objectif de l'unité, et c'est la moitié qui compte le plus. | le jumeau réceptif est E55 : l'enfant touche, parmi trois, le texte qui ressemble à celui qu'il vient de lire. Il vérifie le rapprochement entre deux lectures, jamais le lien avec l'expérience de l'enfant. |
| `E57` | 42 | choisir un livre pour son plaisir ne se vérifie pas : il n'y a pas de bonne réponse, et une application qui en aurait une jugerait un goût. Le programme demande d'aller vers les livres — c'est la seule unité de la tranche qui ne passe pas par un écran. | aucune : rien dans l'application ne juge un choix personnel, et rien ne doit le faire. L'étagère est là, elle ne mesure rien. |

### Les 5 besoins déclarés

| Id | Unité | Ce qui manque | Détail | Bloque ? |
|---|---|---|---|---|
| `B01a` | 1 | les trente-trois consignes du CE1 ne sont pas enregistrées | Le corpus audio est celui de la GS : trente et une consignes, écrites pour des enfants qui ne lisent pas encore. Les consignes du CE1 sont écrites ET dites, et aucune n'est enregistrée. Le texte de chaque consigne est le script de l'enregistrement à faire, et il est déclaré dans la banque. | non |
| `B02` | 2 | les mots du CE1 ne sont pas enregistrés | Le corpus audio de la GS contient des phonèmes et des mots de GS. Les mécaniques qui font écouter un mot — écouter et toucher, écouter et décider — ont besoin des mots du CE1 : craie, reine, agneau, montagne, loup, cheval, et les suites de lettres de l'unité 35. | non |
| `B04` | 4 | aucun mot contenant oin n'est illustré | L'unité 4 annonce « toucher l'image du mot entendu ». Les quarante-quatre mots illustrés sont ceux de la GS : aucun ne contient oin. L'exercice E09 demande donc de lire et de choisir le mot, ce qui entraîne la lecture mais pas le lien mot-image. | non |
| `B13` | 13 | aucun mot contenant la nasale un n'est illustré | Même défaut qu'à l'unité 4 : lundi, brun, chacun, aucun ne sont pas illustrés. L'exercice E18 sépare la nasale de deux lettres qui se suivent sans former de son — lundi contre lune — mais ne peut pas passer par l'image. | non |
| `B30` | 30 | aucun mot irrégulier n'est illustré | L'unité 30 annonce « toucher l'image du mot entendu ». monsieur, femme, second, fils, œil ne sont pas illustrés, et ce sont des mots qui ne se déchiffrent pas : ils s'apprennent d'un seul regard. L'exercice E36 les fait reconnaître en lecture flash, ce qui est bien l'objectif, mais sans le support de l'image. | non |

### Les 4 corrections consignées

**1. outils/cgp-ce1.json et outils/verifier-textes-ce1.py — les graphies aille, eille et euille**

- *Le défaut.* La liste des graphies du CE1 était écrite DEUX FOIS : dans la table (unité 18 : « ail, eil, euil, ouille ») et dans le code (qui en découpait quatre autres, dont « aille » et « eille », sans leur rattacher aucune CGP). Tout mot contenant « aille » ou « eille » — oreille, taille, bataille, abeille — était donc refusé comme « graphème non enseigné » ; et « feuille », découpé f \| euil \| l \| e, était lu /fœjl/ : accepté, et de travers.
- *La correction.* Les graphies sont désormais DÉRIVÉES de la table, avec leur identifiant de CGP, par `graphemes_et_identifiants`. Ajouter une graphie se fait dans le JSON, à l'unité qui l'enseigne ; le code suit. La table déclare les sept graphies de l'unité 18, et deux cas du harnais les éprouvent — un par le verdict, un par la lecture.
- *Pourquoi il était coûteux.* Le défaut était invisible : aucun des dix-huit textes de la tranche ne contient ces graphies, donc le contrôle des textes était vert. Il n'est apparu qu'en écrivant l'exercice de l'unité 18, c'est-à-dire en demandant au décodeur un mot qu'aucun texte ne lui avait encore demandé. Un contrôle vert sur un corpus ne dit rien d'un mot absent du corpus.

**2. outils/verifier-textes-ce1.py — le contrôle d'atteignabilité des graphies**

- *Le défaut.* La première version de ce contrôle cherchait chaque graphie déclarée dans la découpe d'une sonde construite autour d'elle (« a » + graphie + « t »). Elle ne pouvait pas échouer : la découpe prend toujours la plus longue correspondance, et la graphie cherchée était la plus longue de sa propre sonde. Le contrôle a d'ailleurs accusé deux graphies saines — « a » + « ill » donne « aill », lu ail puis l.
- *La correction.* Le contrôle porte maintenant sur ce qui peut réellement se perdre : les deux graphies positionnelles, c et g, que la dérivation écarte et que `resoudre_ce1` traite par un chemin à part. Il éprouve les deux contextes — le c de citron doit valoir c-doux, celui de cartable non — et il échoue si ce chemin est perdu.
- *Pourquoi il était coûteux.* Un contrôle qui ne peut pas échouer fait pire que rien : il rassure. Et un contrôle éprouvé sur des attentes fausses apprend à douter de lui-même au lieu de mesurer.

**3. outils/progression-ce1.json — l'action des unités 4, 13 et 30**

- *Le défaut.* Ces trois unités annoncent « toucher l'image du mot entendu ». Le corpus d'illustrations est celui de la GS : quarante-quatre mots, dont aucun ne contient oin, aucun ne contient la nasale un, et aucun n'est un mot irrégulier. L'action annoncée ne pouvait pas être exercée, et rien ne le disait.
- *La correction.* Les exercices E09, E18 et E36 emploient la mécanique qui reste possible — lire et choisir le mot, ou reconnaître le mot d'un seul regard — et le manque est déclaré dans les besoins B04, B13 et B30. La mécanique `ecouter_et_toucher_image` a été retirée de la liste : une mécanique déclarée et jamais employée est une promesse qu'on ne tient pas. Depuis, le corpus d'illustrations du CE1 existe (`outils/images-ce1.json`, `contenu/LUDOLIRE-IMAGES-CE1.md`) : trois images produites — `foin`, `parfum`, `œil` — et vingt-deux mots déclarés non dessinables, chacun avec sa raison. L'action annoncée n'est toujours pas exerçable, et le corpus dit POURQUOI : les deux nasales rares et les mots irréguliers sont les endroits du français où le nom concret se raréfie, et une famille qui compte un seul mot illustrable ne peut pas porter un exercice de discrimination. Le besoin n'est donc pas un manque d'illustrateur, c'est une propriété du lexique — et la réponse est la lecture, pas le dessin.
- *Pourquoi il était coûteux.* Un besoin tu se transforme en exercice faux : on écrit un exercice qui a l'air de faire ce que l'unité demande, et l'objectif n'est pas entraîné. C'est le mode d'échec le plus coûteux d'une banque — il fait croire qu'une unité est outillée quand elle ne l'est pas.

**4. outils/exercices-ce1.json — la longueur des séries**

- *Le défaut.* Les exercices adossés à un texte annonçaient une durée sans dire ce que l'enfant voyait. Un exercice de compréhension au CE1 demande de relire, de revenir au texte et de comparer trois réponses : la durée d'un exercice de GS ne pouvait pas être reprise telle quelle.
- *La correction.* Chaque exercice adossé à un texte déclare ce qu'il affiche, combien de questions il pose, et une durée de quatre-vingt-dix à cent quatre-vingts secondes. La durée totale de la banque est affichée par le contrôle, et c'est elle qui dira si une séance tient dans un temps d'attention de sept ans.
- *Pourquoi il était coûteux.* Une durée inventée ne se voit pas dans un tableau ; elle se voit dans une classe, quand l'enfant décroche au troisième exercice.

### Le décompte

| Point | Nombre |
|---|---|
| Unités de la progression | 42 |
| Unités servies par au moins un exercice | 42 |
| Unités dont l'objectif porte une production | 10 |
| Mécaniques | 33 |
| Mécaniques employées | 33 |
| Consignes déclarées | 33 |
| Consignes employées | 33 |
| Exercices | 57 |
| dont jugés par l'application | 52 |
| dont hors app | 5 |
| dont avec une inversion déclarée | 7 |
| dont adossés à un texte | 29 |
| Textes de la tranche employés | 15 |
| Questions avec leur phrase-preuve | 27 |
| Exercices citant des textes courts | 4 |
| Citations de textes courts | 7 |
| Exercices citant des pseudo-mots | 2 |
| Citations de pseudo-mots | 10 |
| Besoins déclarés | 5 |
| dont bloquants | 0 |
| Corrections consignées | 4 |
| Durée cumulée des exercices | 5820 s |

<!-- FIN TABLE GENEREE -->

## 8. Ce que la banque ne dit pas

- **Elle ne dit pas l'ordre des exercices.** Une séance, sa durée, ce qu'on reprend le lendemain : rien de tout cela n'est ici.
- **Elle ne dit pas l'habillage.** Ce que l'enfant voit — la disposition, la taille des lettres, la couleur des colonnes — n'est pas décrit.
- **Elle ne juge pas la plausibilité d'un intrus.** Le contrôle vérifie qu'un intrus existe, qu'il est distinct de la bonne réponse et qu'il est lisible. Qu'il soit *vraisemblable*, c'est une relecture humaine.
- **Elle ne dit pas la difficulté relative de deux exercices.** Deux exercices de 90 secondes ne sont pas de même difficulté parce qu'ils durent autant.
- **Elle n'évalue pas la lecture.** Les quatre exercices hors app le déclarent : l'application ne peut pas entendre, et elle ne prétend pas juger à la place de l'adulte.

## 9. Comment on vérifie

    python outils/verifier-exercices.py --ce1

Le contrôle vérifie que toutes les unités sont servies, que chaque mécanique et chaque consigne déclarées sont employées, que les mots, les phonèmes, les graphies et les textes existent et sont lisibles au rang de leur unité, que chaque phrase-preuve se trouve littéralement dans son texte, et que l'accord entre besoins déclarés et besoins consolidés tient dans les deux sens.

Il a été **falsifié**, et il l'est désormais **rejouable** : `outils/tester-exercices-ce1.py` injecte **vingt fautes** une par une sur une copie en mémoire — une phrase-preuve approximative, un mot trop difficile, un texte adossé trop haut, une bonne réponse recopiée parmi les intrus, une mécanique déclarée et jamais employée, une consigne déclarée et jamais employée, une question illisible à l'unité, un pseudo-mot qui ne se résout pas, un exercice dont aucun pseudo-mot n'est complexe — et le contrôle doit les nommer toutes. Un témoin est joué d'abord, sur la banque réelle : sans lui, un contrôle qui refuserait tout passerait le banc.

Ces vingt cas comprennent ceux d'une **première falsification, faite à la main**, qui avait trouvé un vrai défaut : le contrôle d'usage lisait les déclarations dans le fichier d'origine au lieu de la banque qu'on lui passait, et ne pouvait donc pas voir une mécanique **ajoutée** — précisément le cas qu'il doit attraper. Mais cette première falsification n'avait laissé **aucun banc** : rien ne pouvait la rejouer, et une falsification qu'on ne peut pas rejouer ne protège que le jour où elle a été faite. Les cas sont donc écrits, et ils le restent.

Les autres commandes de la tranche :

    python outils/tester-decodeur-ce1.py        # 110 essais sur le décodeur
    python outils/verifier-textes-ce1.py --tous # les 18 textes, mot à mot
    python outils/verifier-exercices.py         # la banque de la GS
    python outils/generer-table.py              # réécrit les tableaux de ce document
