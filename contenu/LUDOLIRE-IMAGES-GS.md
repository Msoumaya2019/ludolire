# Ludo'Lire — Les illustrations de la tranche GS

**Statut :** spécification complète et **images produites**, 21 septembre 2026. Les quarante-quatre SVG sont dans `contenu/images/`, engendrés par `outils/generer-images.py` — voir le § 0.
**Source de vérité :** `outils/images-gs.json` (le brief de dessin) et `outils/mots-gs.json` (le libellé). Le tableau du § 5 est engendré depuis les deux.
**Contrôle :** `outils/verifier-images.py`. Sortie non nulle si un mot n'a pas d'image, si deux mots reçoivent le même dessin, ou si un risque d'ambiguïté n'est déclaré que d'un côté.

---

## 0. Ce que ce document règle, et ce qu'il ne règle pas

Il règle **comment** dessiner les 44 images de la tranche GS : quel objet, dans quel cadre, et surtout ce qui doit être exclu de chaque dessin pour qu'aucun autre mot ne puisse être nommé à la place du mot visé.

**Les images sont produites.** Elles sont écrites **comme du code** — un SVG par mot, dans `contenu/images/`, engendré par `outils/generer-images.py`. Ce n'est pas un contournement : c'est la voie qui restait ouverte, et elle règle trois choses d'un coup.

1. **Aucun outil de génération d'image n'est disponible ici.** La connexion au service de génération a répondu `authenticated: false` — « aucun identifiant temporaire utilisable n'a été délivré » — et l'outil lui-même n'existe pas dans cette configuration. Deux tentatives, deux échecs attribuables.
2. **La licence est réglée par construction.** Les images appartiennent au projet parce qu'elles sont du code écrit pour lui. Rien à céder, rien à démontrer, aucun contrat à conserver. Voir `contenu/LICENCE-IMAGES.md`.
3. **Le contrôle devient possible.** Le brief impose une règle — « une image ne doit convenir à aucun autre mot ». Une image écrite comme du code est vérifiable par un script : palette fermée, aucun texte, cadrage constant, poids borné.

**Ce que ces images sont.** Des **icônes fonctionnelles**, dessinées pour être reconnues sans hésitation à la taille de l'application, dans un style plat à contour constant. Elles ne cherchent ni le charme ni la matière. Le brief ne demande pas la beauté, il demande l'absence d'ambiguïté. Une relecture par un illustrateur reste souhaitable avant publication ; elle n'est pas nécessaire pour valider la mécanique.

**Et le contrôle ne suffit pas.** Un SVG parfaitement conforme peut représenter un gribouillis, et aucun script ne le verra. La seule vérification qui vaille pour une image est de la **regarder**. Les 44 dessins ont donc été rastérisés en une planche unique, `contenu/images/planche.png`, et relus à l'œil. La première planche a fait tomber **sept** dessins ; la seconde, **deux** — dont le nez, raté deux fois de suite. Aucune de ces neuf fautes n'était visible dans le code.

Ce que cela n'a pas coûté, en revanche. Les vingt-quatre ambiguïtés déclarées au § 5 ont été trouvées en écrivant le brief, pas en regardant des images. Elles auraient été trouvées beaucoup plus tard — et beaucoup plus cher — si les images avaient été produites d'abord.

---

## 1. Pourquoi des images, et pourquoi elles ne peuvent pas être approximatives

La tranche GS est une tranche **orale**. Un enfant de cinq ans ne lit pas : tout ce qui doit lui parvenir passe par la voix et par l'image. Il n'y a pas de troisième voie.

Cela donne à l'illustration un statut qu'elle n'a pas dans un livre : **elle est la seule écriture disponible.** Dans le jeu de syllabes, c'est l'image qui dit de quel mot il s'agit ; les cases vides disent seulement combien de syllabes il contient. Une image fausse ne rend pas l'exercice plus difficile — elle le rend impossible, ou pire, elle le rend faisable par le mauvais chemin.

Et une image ambiguë ne se voit pas. Un dessin de lit convient aussi bien à `lit` qu'à `dodo`. Le brief est ce qui rend cette faute visible **avant** qu'elle ne coûte 44 dessins.

---

## 2. La règle qui produit tout le reste

> **Une image ne doit pas seulement convenir au mot visé. Elle ne doit convenir à aucun autre.**

C'est plus exigeant que « l'image doit être claire », et c'est ce qui se vérifie. Trois conséquences, qui expliquent la plupart des interdits du § 5 :

1. **Un seul objet.** Une scène invite à nommer la scène. Une image de plage ne dit pas `bateau`, elle dit « la mer ». La seule exception admise est un élément qui **lève** une ambiguïté — le ciel étoilé derrière la lune — et elle doit être justifiée dans le brief.
2. **Aucun personnage dont le nom n'est pas le mot visé.** Une jupe dessinée sur une fillette fait dire « fillette ». Un cartable porté par un enfant fait dire « enfant ».
3. **Rien à lire.** Pas de mot, pas de lettre, pas de chiffre. Une image qui contient le mot écrit contourne l'exercice au lieu de le servir — et à ce niveau, elle ne serait même pas lue.

---

## 3. Les ambiguïtés, qui sont le vrai travail

Vingt-quatre des quarante-quatre mots portent une ambiguïté **déclarée** : un autre mot, dans la banque ou hors de la banque, que l'image pourrait faire nommer à la place. Chacune est écrite avec sa parade.

Elles tombent en cinq classes. Les reconnaître est ce qui permet de les chercher sur les mots qui restent :

| Classe | Exemple | Ce qui la produit |
|---|---|---|
| **Même référent** | `lit` / `dodo` | Deux mots pour la même chose. Aucun dessin ne les sépare : il faut que les mots eux-mêmes se séparent, ou que l'un des deux sorte de la banque |
| **Même catégorie** | `pomme` / `tomate` / `cerise` | Trois fruits ronds et rouges. Le dessin doit porter le trait distinctif de chacun, et il doit être gros |
| **Silhouette** | `vélo` / `moto`, `zèbre` / `cheval` | Une silhouette réduite à une icône perd ce qui les distinguait |
| **Forme** | `lune` / `banane` | Le croissant de lune a exactement la forme d'une banane. La confusion la plus probable de toute la série |
| **Partie / tout** | `nez` | Un nez sur un visage fait nommer « visage ». Le nez doit être seul |
| **Contenant / contenu** | `café` | Ce qui se nomme est le breuvage, ce qui se voit est la tasse |

**La leçon du `nez`, qui vaut pour toute la série.** Trois versions ont été nécessaires. La première, de face, était une forme lisse et effilée, arrondie au bout : elle se lisait comme un **doigt**. La deuxième est passée de profil, en croyant que la vue sauverait la forme : elle a donné une **corne**, puis une **voile**. Le raisonnement était faux, et c'est ce qui est intéressant. Ce n'est pas la **vue** qui fait nommer un objet, ce sont ses **traits distinctifs** — pour un nez, la base large, les deux narines et les ailes en lobes. Tant que ces traits manquent, aucune vue ne sauve le dessin. La règle est désormais écrite dans le cadrage du brief (§ 5), et elle s'applique aux 43 autres mots.

**La leçon du `cheval`.** Sa crinière était dessinée en mèches perpendiculaires à l'encolure. Vues à la taille de l'application, ces mèches se lisent comme des **rayures** — c'est-à-dire comme le trait distinctif du **zèbre**, qui est dans la même banque. Une crinière doit donc être une crête **pleine** qui **déborde** de l'encolure : ce qui déborde se lit comme un poil, ce qui est posé sur le contour se lit comme une rayure. Deux mots d'une même banque peuvent se contaminer par un détail que personne n'avait regardé.

**Trois cas ne se règlent pas entièrement par le dessin**, et il faut le dire :

- **`lit` et `dodo` désignent le même objet.** La parade retenue est de séparer l'objet de l'action : `dodo` est un enfant endormi, `lit` est un lit vide. Cela fonctionne, mais c'est une convention, pas une évidence — et les deux images ne doivent jamais être montrées dans la même série.
- **`papa` et `maman` se distinguent par une convention sociale.** Le repère retenu — barbe courte pour l'un, cheveux attachés pour l'autre — est un stéréotype. Il n'y a pas de solution technique à ce problème : c'est une décision de contenu, à valider par le porteur du projet. Le brief la signale au lieu de la trancher en silence.
- **`café` est nommé par son contenant.** Aucune parade graphique n'existe : une tasse de café reste une tasse. Le dessin est retenu tel quel, et c'est le **mot** qui cédera si la relecture donne raison à l'enfant — on retire le mot de la banque d'images, on ne redessine pas. C'est la seule ambiguïté de la série dont la parade n'est pas dans le dessin.

---

## 4. La contrainte de licence, qui n'est pas une question de goût

L'application est publiée sur les stores en catégorie enfant, et le dépôt est public. Une image dont l'origine ne peut pas être démontrée n'est pas seulement une question d'esthétique : c'est un risque de retrait et un risque juridique.

**Il faut :** un auteur identifié, et un écrit qui cède les droits d'exploitation. Le contrat nominatif reste **hors du dépôt public** ; le dépôt porte une mention d'auteur, `contenu/LICENCE-IMAGES.md`.

**Il ne faut pas :** une image de banque sans licence explicite ; une image reconnaissable comme un personnage protégé ; une image dont l'origine ne peut pas être documentée — y compris une image produite par un outil automatique dont on ne peut pas nommer les conditions d'utilisation.

Cette dernière ligne mérite d'être dite franchement : **c'est une des raisons pour lesquelles l'absence d'outil de génération n'est pas entièrement une mauvaise nouvelle.** Une série de 44 images produites par un outil dont les conditions d'utilisation ne sont pas claires serait un passif, pas un actif, pour une application qui vise la catégorie enfant.

---

## 5. Les quarante-quatre images

<!-- DEBUT TABLE GENEREE -->

### Le cadrage technique

| Point | Règle |
|---|---|
| format master | SVG, un fichier par mot |
| export | PNG à 1x, 2x et 3x, fond transparent |
| taille logique | 512 × 512 points |
| occupation du cadre | le sujet tient dans 80 % du cadre, centré, avec une marge régulière |
| epaisseur du contour | 4 points à 512, constante sur toute la série |
| palette | palette fermée et déclarée, un seul jeu pour toute la série. Les couleurs doivent rester distinctes en niveaux de gris et pour les principaux types de daltonisme — un enfant daltonien doit pouvoir nommer l'objet. |
| poids cible | moins de 12 ko par SVG exporté, pour que les 44 images tiennent dans un chargement unique |

### Le nommage

| Point | Règle |
|---|---|
| motif | ill_<slug>.svg |
| slug | le mot en minuscules, sans accent et sans caractère hors a-z et 0-9 (zèbre donne zebre, gâteau donne gateau, école donne ecole) |
| pourquoi ascii | un nom de fichier accentué traverse mal les chaînes d'outils : il change d'octets selon l'encodage du shell, et une référence d'image qui ne correspond plus est une image qui ne s'affiche pas. Le slug est calculé, jamais tapé à la main. |

### Les quarante-quatre images

| Mot | Fichier | Libellé | Objet à dessiner | Interdit | Ambiguïté déclarée, et la parade |
|---|---|---|---|---|---|
| **papa** | `ill_papa.svg` | un papa | un homme adulte debout, cheveux courts, barbe courte | un enfant ; un bébé ; deux personnes | **maman** — un repère unique est FIXÉ pour toute la série et appliqué partout. Le repère retenu (barbe courte pour papa, cheveux attachés pour maman) est une convention, donc un stéréotype : c'est une décision de contenu, à valider par le porteur du projet, pas un choix technique |
| **maman** | `ill_maman.svg` | une maman | une femme adulte debout, cheveux attachés | un enfant ; un bébé ; deux personnes | **papa** — le même repère unique, appliqué partout |
| **bébé** | `ill_bebe.svg` | un bébé | un bébé assis, très petit, en grenouillère | un enfant qui marche ; un adulte qui le porte | — |
| **dodo** | `ill_dodo.svg` | un lit d'enfant | un enfant endormi sous une couverture, yeux fermés, dans un lit d'enfant | un lit vide ; un adulte | **lit** — `dodo` est l'ACTION — un enfant endormi — et `lit` est l'OBJET, vide et fait. Les deux images ne doivent jamais être montrées dans la même série |
| **lit** | `ill_lit.svg` | un lit | un lit vide, fait, vu de côté, sans dormeur | un dormeur ; une couverture froissée | **dodo** — l'absence de dormeur est ce qui distingue `lit` ; elle doit être visible, pas seulement vraie |
| **vélo** | `ill_velo.svg` | un vélo | un vélo vu de côté, cadre fin, pédalier et pédales visibles | un moteur ; un cycliste | **moto** — `vélo` montre le pédalier et la chaîne, `moto` montre le bloc moteur et un cadre épais. Le détail qui sépare doit être gros, pas un détail de spécialiste |
| **moto** | `ill_moto.svg` | une moto | une moto vue de côté, bloc moteur épais et visible | des pédales ; un pilote | **vélo** — le bloc moteur, dessiné gros |
| **café** | `ill_cafe.svg` | une tasse de café | une tasse de café pleine, brune, sur une soucoupe, vue de face | une cafetière ; une personne ; une cuillère ; de la mousse | hors banque : une tasse, un bol, un chocolat chaud — aucune parade graphique — une tasse de café reste une tasse. Le dessin est donc retenu tel quel, et c'est le mot qui cédera si la relecture montre qu'un enfant de GS nomme le contenant : on retire le mot de la banque d'images, on ne redessine pas |
| **gâteau** | `ill_gateau.svg` | un gâteau | un gâteau rond à étages, avec des bougies allumées | un texte sur le gâteau | — |
| **lune** | `ill_lune.svg` | la lune | la lune en disque plein, avec des cratères, dans un ciel étoilé | un croissant de lune | **banane** — la lune est dessinée en DISQUE PLEIN avec des cratères, jamais en croissant. C'est une contrainte de forme, pas de goût : le croissant est interdit |
| **jupe** | `ill_jupe.svg` | une jupe | une jupe seule, à plat, vue de face | une personne qui la porte ; un cintre | — |
| **pomme** | `ill_pomme.svg` | une pomme | une pomme rouge vue de face, pédoncule et feuille verte | un couteau ; une pomme coupée | **tomate** — la feuille verte et le pédoncule fin pour la pomme ; le calice vert en étoile, large et posé sur le dessus, pour la tomate ; **cerise** — la cerise n'est jamais seule : elle est par paire, avec deux queues |
| **tomate** | `ill_tomate.svg` | une tomate | une tomate rouge vue de face, calice vert en étoile bien visible sur le dessus | une tomate coupée ; un plan de tomate | **pomme** — le calice en étoile, large, est le trait qui sépare |
| **cerise** | `ill_cerise.svg` | des cerises | deux cerises rouges réunies par leurs queues, une feuille | une cerise seule ; un gâteau | **pomme** — la paire et les queues |
| **zèbre** | `ill_zebre.svg` | un zèbre | un zèbre entier vu de côté, rayures noires et blanches sur tout le corps | un cheval sans rayures ; une selle | **cheval** — les rayures couvrent le corps ENTIER, y compris l'encolure et les pattes. Des rayures partielles donnent un cheval |
| **cheval** | `ill_cheval.svg` | un cheval | un cheval entier vu de côté, robe unie brune, sans rayures | des rayures ; un cavalier | **zèbre** — la robe est unie, et l'image ne contient aucune rayure |
| **lapin** | `ill_lapin.svg` | un lapin | un lapin entier vu de côté, longues oreilles dressées | un chapeau ; un panier | — |
| **canard** | `ill_canard.svg` | un canard | un canard entier vu de côté, bec plat jaune, sur l'eau | une mare chargée ; un autre oiseau | — |
| **mouton** | `ill_mouton.svg` | un mouton | un mouton entier vu de côté, toison blanche bouclée | des cornes ; une tondeuse | — |
| **koala** | `ill_koala.svg` | un koala | un koala entier assis sur une branche, grandes oreilles rondes | un ours ; un arbre entier | — |
| **girafe** | `ill_girafe.svg` | une girafe | une girafe entière vue de côté, très long cou, taches | un arbre qui masque le cou | — |
| **éléphant** | `ill_elephant.svg` | un éléphant | un éléphant entier vu de côté, trompe visible, grandes oreilles | un autre animal | — |
| **crocodile** | `ill_crocodile.svg` | un crocodile | un crocodile entier vu de côté, long museau, dents visibles | un autre reptile | — |
| **loup** | `ill_loup.svg` | un loup | un loup entier vu de côté, gris, museau pointu, queue touffue | un collier ; une laisse | **chat** — le loup est gris et grand, la queue est longue et touffue ; le chat est petit et sa queue est fine. Aucun chien dans la banque, donc aucun troisième candidat |
| **chat** | `ill_chat.svg` | un chat | un chat entier vu de côté, petit, moustaches visibles, queue fine | des rayures de zèbre ; un collier | **loup** — la taille et l'épaisseur de la queue ; **rat** — le chat a des moustaches longues et des oreilles triangulaires ; le rat a un museau pointu et une queue sans poils, plus longue que son corps |
| **rat** | `ill_rat.svg` | un rat | un rat entier vu de côté, museau pointu, longue queue sans poils | des moustaches longues ; un fromage | **chat** — la queue sans poils, plus longue que le corps, est le trait qui sépare |
| **maison** | `ill_maison.svg` | une maison | une petite maison, toit à deux pentes, cheminée, une porte et une fenêtre | une horloge ; une cour de récréation ; un drapeau | **école** — la maison est PETITE, isolée, avec un toit à deux pentes et une cheminée ; l'école est un bâtiment LONG, à plusieurs fenêtres, avec une horloge et une cour. La taille et le nombre de fenêtres portent la différence |
| **école** | `ill_ecole.svg` | une école | un bâtiment long à plusieurs fenêtres, une horloge sur la façade, une cour devant | une cheminée ; un toit à deux pentes isolé | **maison** — la longueur, l'horloge et la cour |
| **valise** | `ill_valise.svg` | une valise | une valise rigide rectangulaire, poignée sur le dessus, deux fermoirs | des bretelles ; une personne | **cartable** — la valise est rigide, à angles droits, avec des fermoirs ; le cartable est souple, avec un rabat et deux bretelles ; **sac** — la valise est fermée par des fermoirs ; le sac est un cabas ouvert à deux anses |
| **cartable** | `ill_cartable.svg` | un cartable | un cartable d'écolier, rabat fermé, deux bretelles visibles, des cahiers qui dépassent | une valise ; un enfant qui le porte | **sac** — le cartable a un rabat et DEUX BRETELLES ; le sac a deux anses et reste ouvert ; **valise** — le cartable est souple avec un rabat ; la valise est rigide à angles droits avec des fermoirs |
| **sac** | `ill_sac.svg` | un sac | un cabas ouvert à deux anses, vide, posé | des bretelles ; des cahiers | **cartable** — les anses au lieu des bretelles, et l'ouverture béante ; **valise** — le sac est souple et ouvert ; la valise est rigide et fermée par des fermoirs |
| **téléphone** | `ill_telephone.svg` | un téléphone | un téléphone mobile vu de face, écran éteint, sans personne | une main ; un visage ; une icône sur l'écran | — |
| **parapluie** | `ill_parapluie.svg` | un parapluie | un parapluie OUVERT vu de côté, manche recourbé | un parapluie fermé ; une personne | hors banque : une canne — le parapluie est toujours ouvert et déployé |
| **avion** | `ill_avion.svg` | un avion | un avion entier vu de côté, ailes et hublots visibles | un aéroport ; des passagers | — |
| **bateau** | `ill_bateau.svg` | un bateau | un bateau entier vu de côté, coque et voile, sur l'eau | un port ; un marin | — |
| **soleil** | `ill_soleil.svg` | un soleil | un soleil en disque jaune avec des rayons réguliers | des lunettes de soleil ; un visage souriant | — |
| **fleur** | `ill_fleur.svg` | une fleur | une fleur à cinq pétales, tige et deux feuilles | un vase ; un bouquet | — |
| **banane** | `ill_banane.svg` | une banane | une banane jaune, courbée, avec sa tige brune | un croissant de lune ; un singe | **lune** — la banane est JAUNE avec une tige brune ; la lune est un disque plein, jamais un croissant |
| **ananas** | `ill_ananas.svg` | un ananas | un ananas entier, couronne de feuilles sur le dessus, motif en losanges | un ananas coupé ; un verre | — |
| **bonbon** | `ill_bonbon.svg` | un bonbon | un bonbon emballé, les deux papillotes torsadées visibles | un bonbon sans emballage | — |
| **chocolat** | `ill_chocolat.svg` | une tablette de chocolat | une tablette de chocolat, un carré détaché à côté | une boisson ; une tablette sans carré détaché | — |
| **pyjama** | `ill_pyjama.svg` | un pyjama | un pyjama complet — haut et pantalon — posé à plat | un enfant qui le porte ; un lit | — |
| **nez** | `ill_nez.svg` | un nez | un nez seul, vu de face : base large, deux narines, ailes en lobes, columelle | un visage entier ; des yeux ; une main ; un doigt | hors banque : un visage, une tête, un doigt, une corne — le nez est seul, sans aucun autre trait du visage, et porte ses trois traits distinctifs : base large, deux narines, ailes en lobes. C'est la silhouette qui fait le mot, pas la vue — un nez de profil dépourvu de ces traits a donné une corne, puis une voile |
| **main** | `ill_main.svg` | une main | une main ouverte, paume visible, cinq doigts écartés | un bras ; un poignet avec manche | — |

### Le décompte

| Point | Nombre |
|---|---|
| Mots de la banque GS | 44 |
| Images à produire | 44 |
| Mots dont l'image porte une ambiguïté déclarée | 24 |
| Mots dont l'image n'en porte aucune | 20 |

<!-- FIN TABLE GENEREE -->

---

## 6. Ce qui reste

1. **Relire les 44 images une par une**, contre le brief et contre l'usage réel. Le contrôle automatique vérifie que le brief est complet, que les fichiers sont conformes et que les risques sont déclarés des deux côtés ; il ne peut pas juger si un dessin est **reconnaissable** par un enfant de cinq ans. C'est le porteur du projet qui le fait, en éprouvant l'application. La planche `contenu/images/planche.html` est faite pour ça : les 44 images en une page, à la taille de l'application.
2. **Valider les deux conventions** du § 3 : le repère `papa`/`maman` — un stéréotype, donc une décision de contenu — et la séparation `lit`/`dodo`.
3. **Trancher le cas `café`** : seul mot dont la parade n'est pas graphique.
4. **Faire passer un illustrateur** sur la série, si l'apparence doit être soignée. Le brief est fait pour être envoyé tel quel, et les images produites ici peuvent lui servir de chemin de fer. Le § 4 dit ce qu'il faudra alors exiger : un auteur identifié et un écrit qui cède les droits, conservé hors du dépôt public.
5. **Décider du sort des PNG.** L'export 1x/2x/3x transparent existe et fonctionne — `outils/exporter-images.mjs`, 132 fichiers vérifiés. Il n'est **pas versionné**, et c'est délibéré : c'est un artefact dérivé de 4,5 Mo qui périmerait à chaque correction d'un dessin. Il se régénère en une commande, au moment de la construction de l'application.

`contenu/LICENCE-IMAGES.md` est écrit et versionné avec les images (§ 4).

---

## 7. Comment vérifier ce document

```bash
python outils/generer-images.py      # écrit les 44 SVG et la planche de contrôle
python outils/verifier-images.py     # briefs complets, risques réciproques, fichiers conformes
python outils/generer-table.py       # le tableau du § 5 est-il à jour ?

# regarder le résultat — la seule vérification qui vaille pour une image
NODE_PATH=<espace node>/node_modules node <espace node>/rasteriser-svg.mjs \
    contenu/images/planche.svg contenu/images/planche.png 1400

# l'export livré à l'application — facultatif, non versionné
NODE_PATH=<espace node>/node_modules node outils/exporter-images.mjs
```

`verifier-images.py` refuse, entre autres :

- un mot de la banque GS sans brief — un mot sans image est un exercice impossible, pas un oubli ;
- deux mots qui reçoivent le même objet — deux fois le même dessin, c'est deux réponses possibles pour une seule image ;
- un risque d'ambiguïté déclaré d'un seul côté. Si `dodo` craint `lit`, `lit` craint `dodo` : la crainte est réciproque par nature, et ne l'écrire qu'une fois est exactement la façon dont on oublie la moitié. Ce contrôle a attrapé deux déclarations à sens unique lors de sa première exécution ;
- deux mots qui donnent le même slug une fois les accents retirés — deux images s'écraseraient l'une l'autre en silence ;
- un champ vide dans le cadrage technique ou dans la licence — un format manquant est une image qu'on ne sait pas exporter ;
- **et, sur les fichiers eux-mêmes** : un `viewBox` qui n'est pas `0 0 512 512`, un élément texte, une couleur hors de la palette fermée, un contour absent, un fichier de plus de 12 ko.

**Ce qu'il ne vérifie pas, et qu'il faut savoir.** Il ne juge pas si un dessin est reconnaissable, et il n'en a pas les moyens. Un SVG parfaitement conforme peut représenter un gribouillis. C'est pourquoi la planche se **regarde** — c'est la seule étape du contrôle qui a trouvé de vraies fautes.
