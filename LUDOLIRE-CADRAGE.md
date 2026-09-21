# Ludo'Lire — Note de cadrage produit et pédagogique

**Statut :** décisions de cadrage du 21 septembre 2026 intégrées. Document de référence pour la v1.
**Périmètre :** application iOS et Android, trois niveaux (GS, CP, CE1), publication sur les stores grand public, catégorie enfant.
**Ce que ce document n'est pas :** ni une spécification fonctionnelle, ni un choix d'architecture. Il fixe le *quoi* et le *pourquoi*. Le *comment* vient après.

---

## 0. Décisions tranchées le 21 septembre 2026

| # | Décision |
|---|---|
| 1 | **Trois niveaux superficiels** en v1, plutôt qu'un niveau mené à son terme |
| 2 | **Niveau 1 = GS**, niveau 2 = **CP**, niveau 3 = **CE1** |
| 3 | **Pas de reconnaissance vocale** en v1 — la lecture à voix haute n'est pas évaluée automatiquement |
| 4 | **Une seule porte parentale**, devant la politique de confidentialité |
| 5 | **v1 gratuite**, sans achat. Par la suite, **abonnement mensuel avec 7 jours d'essai** |
| 6 | **Catégorie enfant** assumée (Apple Kids Category, Google Play Familles) |
| 7 | **Les textes de lecture sont écrits par l'assistant** pour le moment |

Les conséquences de ces sept décisions sont développées ci-dessous, et elles sont nombreuses : deux d'entre elles changent la promesse du produit et la façon de mesurer sa réussite.

---

## 1. Le problème

Apprendre à lire ne s'improvise pas. C'est la seule compétence scolaire dont l'échec se paie pendant toute la scolarité, et c'est aussi celle où l'écart se creuse le plus vite : un enfant qui décode mal en fin de CP lit moins, donc lit moins bien, et la boucle est verrouillée dès le CE1.

Trois constats structurent le projet :

1. **L'entraînement manque, pas la méthode.** L'école enseigne bien le décodage. Ce qui manque, c'est le volume de répétitions courtes et régulières, avec une correction immédiate. Un adulte peut faire cela ; il ne peut pas le faire tous les jours, ni savoir précisément quel graphème coince.
2. **Les parents ne savent pas où en est leur enfant.** « Il lit mal » n'est pas une information actionnable. « Il confond ou / on et il rate un mot sur cinq depuis deux semaines » l'est.
3. **Les apps existantes sont soit des jeux déguisés, soit des cahiers d'exercices.** Les premières amusent sans enseigner, les secondes enseignent sans qu'on ait envie d'y revenir.

**La promesse de Ludo'Lire, révisée après la décision 3 :** dix minutes par jour, un entraînement qui suit l'ordre officiel d'apprentissage du code, une correction immédiate qui dit *quel* son coince, et un tableau de bord qui montre au parent ce que son enfant sait faire maintenant qu'il ne savait pas faire il y a un mois.

La mesure de la fluence n'est plus dans la promesse de la v1 — c'est la conséquence la plus lourde de la décision 3, et elle est traitée au § 10.

---

## 2. Les trois niveaux de la v1

Le public visé couvre le corridor où tout se joue : de la maternelle au CE1. Trois tranches, chacune correspondant à un palier officiel identifiable.

| Niveau | Âge | Périmètre de la tranche | Palier de sortie | Hors périmètre |
|---|---|---|---|---|
| **1 — GS** | 4-6 ans | Conscience phonologique (syllabes, attaques, rimes, phonèmes) ; principe alphabétique ; lettres dans les trois graphies | Nommer les 26 lettres dans les trois graphies ; connaître le nom des lettres et leur valeur sonore hormis les occlusives ; repérer une rime, localiser un phonème, trouver l'intrus à l'initiale ; épeler un mot connu ; prononcer les 36 phonèmes | Vocabulaire (2 500 mots), oral complexe, écriture, manipulation des phonèmes (CP) |
| **2 — CP** | 6-7 ans | Les CGP du CP, dans l'ordre ; décodage syllabes → mots → phrases courtes | Décoder sans erreur des mots réguliers construits sur les CGP couvertes ; lire une phrase courte | CGP complexes, lettres muettes, mots irréguliers, fluence |
| **3 — CE1** | 7-8 ans | Lecture de textes courts déchiffrables ; compréhension littérale et première inférence | Lire un texte court et répondre à des questions de compréhension | Orthographe, production d'écrit, expressivité |

**Ce que « superficiel » signifie exactement :** chaque tranche couvre une partie de son programme, mais elle est **cohérente et se termine sur un palier mesurable**. L'alternative — trois tranches inachevées et sans fin identifiable — produirait un produit qu'on juge « démo ». Une tranche superficielle qui a une sortie claire est un produit ; une tranche superficielle sans sortie est une démo.

**L'adulte est un utilisateur de plein droit.** Il lui faut un écran séparé, qui ne s'adresse jamais à l'enfant. Mais cet écran **n'est pas protégé** (décision 4) : voir § 6.4.

**Conséquence de conception la plus lourde :** un enfant de 5 ans ne lit pas les consignes. Toute navigation du niveau GS doit être orale et iconographique. Un enfant de 7 ans doit pouvoir lire seul. Ce sont deux interfaces, pas une interface simplifiée.

**Conséquence de la réattribution des colonnes d'âge (21 septembre 2026) :** la tranche GS compte 45 unités, dont **27 relèvent du préparatoire** — les colonnes « avant 4 ans » et « à partir de 4 ans » — et 18 seulement de la colonne « à partir de 5 ans ». C'est ce que dit le programme, et c'est ce dont un enfant de GS en difficulté a besoin. Mais une tranche « GS » aux deux tiers préparatoire ne se présente pas comme une tranche de GS : la fiche de store doit le dire, plutôt que de laisser le parent découvrir qu'on compte les syllabes en grande section.

**Conséquence de la décision 2 :** le public s'arrête à 8 ans. Les niveaux CE2 à CM2, et donc les paliers 90, 110 et 120 mots par minute, sont hors périmètre de la v1 — mais la structure de contenu doit les accueillir sans réécriture (§ 8).

---

## 3. L'ancrage institutionnel

Ce n'est pas un supplément d'âme : c'est ce qui rend l'app crédible auprès des parents, des enseignants, et ce qui la protège du reproche le plus fréquent fait aux apps éducatives — enseigner dans le désordre.

### 3.1 Les trois entrées de l'apprentissage, dès le CP

Le programme de français du cycle 2 pose trois entrées « non pas à envisager successivement, mais de manière parallèle et complémentaire » :

- l'apprentissage puis l'automatisation du **décodage** ;
- la **lecture à voix haute** ;
- la **compréhension** de textes dans toutes les disciplines.

Il ajoute que « la compréhension est la finalité de l'apprentissage de la lecture ».

**Point de vigilance né de la décision 3 :** la v1 entraîne la première et la troisième entrée. La deuxième — la lecture à voix haute — est une entrée **officiellement obligatoire** et c'est celle qui construit la fluence. L'app doit donc continuer à **faire lire l'enfant à voix haute** ; ce qu'elle abandonne en v1, c'est de *vérifier* cette lecture par la machine. Une étape de lecture non évaluée, validée par le parent, préserverait l'entrée sans le risque technique (voir § 5).

### 3.2 L'échelle de fluence officielle

| Niveau | Fin d'année — vitesse cible | Précision du texte officiel |
|---|---|---|
| CP | **30 mots/min sans préparation, 50 après préparation** | « Décoder 30 mots par minute au minimum fin CP, sans préparation, 50 après préparation » |
| CE1 | **70 mots/min** | « Lire un texte adapté à son niveau de lecture avec une vitesse de 70 mots par minute » |
| CE2 | 90 mots/min | hors v1 |
| CM1 | 110 mots/min | hors v1 |
| CM2 | 120 mots/min | hors v1 |
| 6e | 130 mots/min | hors v1 |

La distinction « sans préparation / après préparation » n'est pas un détail de rédaction : elle définit le régime de l'exercice. Un texte relu est un texte préparé, et le repère applicable est le second chiffre. Toute mesure de fluence devra **distinguer les deux régimes**, et ne jamais comparer une première lecture à une cible de lecture préparée.

### 3.3 Les étapes intermédiaires du CP, déjà écrites

Le programme ne se contente pas d'un objectif de fin d'année, il fournit les paliers — et ces paliers sont directement implémentables :

- **milieu d'année :** décoder et encoder **25 à 30 CGP** ; déchiffrer entre **15 et 30 mots par minute** ; avoir pris conscience des lettres finales muettes ; mémoriser les mots fréquents et réguliers ;
- **fin d'année :** décoder 30 mots/min sans préparation, 50 après préparation.

C'est ce palier de milieu d'année qui borne la tranche 2 : **environ 30 CGP** est un objectif de tranche, pas un objectif de fin d'année déguisé.

### 3.4 Ce que la maternelle doit avoir installé

Le programme de cycle 1 distingue deux acquisitions préalables à l'entrée dans l'écrit :

- la **conscience phonologique** — « manipuler et isoler de façon intentionnelle les unités phonologiques d'un mot (syllabe, attaque, rime, phonème) » ;
- le **principe alphabétique** — « un lien entre les signes que sont les lettres et groupes de lettres et les sons ».

Attendus de fin de maternelle utiles au produit : nommer toutes les lettres d'un mot dans les **trois graphies** ; prononcer correctement l'ensemble des **trente-six phonèmes** du français ; un vocabulaire de l'ordre de **2 500 mots** en fin de GS ; mémoriser en moyenne un texte par semaine en moyenne et grande section.

La tranche 1 de Ludo'Lire retient les deux premières lignes et laisse le vocabulaire de côté : c'est le choix qui rend la tranche faisable, et il doit être dit.

### 3.5 Le calendrier des programmes

- **cycles 1 et 2** (français et mathématiques) : arrêté du 22 octobre 2024, JO du 25 octobre, BO n° 41 du 31 octobre 2024. En application depuis la **rentrée 2025-2026**.
- **cycle 3** (français et mathématiques) : arrêté du 10 avril 2025, BO n° 16 du 17 avril 2025. En application **en CM1 et en 6e depuis la rentrée 2025-2026**, et **en CM2 à partir de la rentrée 2026-2027**.

Les trois niveaux de la v1 relèvent des deux premiers textes, tous deux en vigueur depuis un an. Le contenu pédagogique doit néanmoins être **versionné par programme**, comme on versionne une API.

---

## 4. Le modèle d'apprentissage

Sept principes, qui sont des contraintes de conception et non des intentions.

1. **Le décodage d'abord, dans l'ordre des CGP.** Pas de mots « devinés » par l'image ou le contexte. Un exercice dont on peut trouver la réponse sans lire est un exercice raté.
2. **La progression est graphémique, pas thématique.** On n'organise pas par « les animaux » ou « la maison », mais par « a, i, o, u, é, l, m, p, r, s, t, v, d, n, ch, ou, on… ». Le thème est un habillage, jamais la structure.
3. **Court et quotidien plutôt que long et hebdomadaire.** Cible : 5 à 10 minutes par jour.
4. **Correction immédiate et locale.** L'enfant doit savoir *quel* son il a raté, dans la seconde, sans quitter l'exercice. C'est le cœur de la valeur, et c'est aussi ce qui rend le tableau de bord adulte possible : les erreurs sont enregistrées par CGP, pas par exercice.
5. **L'app fait lire à voix haute, même quand elle ne l'évalue pas.** La lecture à voix haute est une entrée du programme et le seul exercice qui entraîne la prosodie. Sans reconnaissance vocale, l'étape devient une lecture non évaluée — mais elle reste dans la séance.
6. **La précision compte plus que la vitesse.** Un enfant rapide et imprécis n'est pas en avance. En v1, la précision est mesurée sur les exercices de décodage : c'est le seul indicateur fiable dont on dispose, et il est bon.
7. **Pas de récompense qui se substitue à l'apprentissage.** Les mécaniques de jeu servent à faire revenir ; elles ne doivent jamais récompenser le clic plutôt que la lecture. C'est aussi une exigence des politiques de store (§ 6).

---

## 5. Le parcours

Trois boucles, plus une étape à confirmer.

**Boucle A — Diagnostic initial (une fois, ~10 min).**
L'enfant est placé, pas interrogé. Niveau GS : reconnaissance des lettres, conscience phonologique. Niveaux CP et CE1 : lecture de mots et de pseudo-mots, puis de phrases. Un placement faux coûte des semaines d'ennui ou de découragement — et avec des tranches superficielles, il coûte plus cher encore, parce qu'un enfant mal placé sort de sa tranche par le haut ou par le bas.

**Boucle B — Séance quotidienne (~7 min).**
Trois à quatre exercices, toujours dans le même ordre : échauffement (révision espacée de ce qui a été vu), apprentissage (une CGP nouvelle ou une difficulté ciblée), application (mots puis phrases), clôture (une lecture courte, réussie). La séance se termine sur une réussite : c'est ce qui fait revenir le lendemain.

**Boucle C — Lecture à voix haute, non évaluée (~2 min). — à confirmer.**
L'enfant lit un texte court à l'écran, à voix haute. L'app ne l'écoute pas : soit l'enfant s'auto-évalue, soit le parent valide d'un geste. Le texte est choisi pour ne contenir que des CGP déjà vues, ce qui garantit qu'il est déchiffrable — et c'est cette contrainte-là qui coûte du travail de rédaction, pas l'évaluation.

Cette étape est proposée parce qu'elle préserve une entrée officielle du programme à coût quasi nul, et parce qu'elle prépare la v2 : le jour où la mesure automatique arrive, l'étape existe déjà, il n'y a qu'à brancher le micro.

**Boucle D — Bilan (~1 fois par mois).**
Un texte jamais vu, une lecture, un résultat. En v1, sans mesure automatique, le bilan porte sur **la précision et la couverture** : quelles CGP sont acquises, lesquelles résistent, avec quelle régularité. Le parent voit une courbe et une phrase : « 12 CGP sur 30 acquises, dont 3 fragiles : ou, on, ch ».

---

## 6. Contraintes de publication — les politiques de store

Ces règles ne sont pas des recommandations : elles décident de l'architecture et du modèle économique. Les deux stores encadrent les apps destinées aux enfants de façon stricte et convergente.

### 6.1 Apple — Kids Category

Règles applicables (App Store Review Guidelines, sections 1.3 et 5.1.4, consultées le 21 septembre 2026) :

- les apps de la catégorie **ne doivent pas** comporter de liens sortants, d'occasions d'achat ni d'autres distractions **sauf dans une zone dédiée derrière un contrôle parental** (« parental gate ») ;
- les apps de la Kids Category **ne peuvent pas envoyer d'informations personnelles identifiantes ni de données d'appareil à des tiers** ;
- elles **ne doivent pas inclure d'analytique ni de publicité tierces**. Des exceptions limitées existent : analytique tierce uniquement si le service ne collecte ni IDFA, ni information identifiante sur l'enfant, ni localisation, ni donnée d'appareil ; publicité **contextuelle** tierce uniquement si le service documente publiquement des pratiques adaptées aux apps enfants, avec **revue humaine des créations publicitaires** ;
- toute app de la catégorie **ou** qui collecte des données personnelles d'un mineur **doit** avoir une politique de confidentialité et respecter les lois applicables (COPPA, RGPD) ;
- l'usage des termes « For Kids » / « For Children » dans les métadonnées est **réservé** à la Kids Category.

### 6.2 Google Play — Families

Obligations principales (politique Familles, consultée le 21 septembre 2026) :

- déclarer le public cible **avant publication**, et le déclarer exactement — la déclaration inexacte expose au retrait ;
- une app **ciblant uniquement des enfants** ne doit **pas** transmettre l'identifiant publicitaire Android (AAID), le numéro de série SIM, le Build Serial, BSSID, MAC, SSID, IMEI, IMSI — et ne doit pas demander la permission `AD_ID` à partir de l'API 33 ;
- pas de **permission de localisation** ni de collecte de localisation précise pour une app ciblant uniquement des enfants ;
- pas d'**API ou SDK non approuvé pour les services destinés aux enfants** ;
- si des publicités sont affichées à des enfants : uniquement via des **SDK publicitaires auto-certifiés Familles**, sans ciblage comportemental ni remarketing, avec des formats conformes ;
- pour une app à public mixte : **écran d'âge neutre** obligatoire ;
- les formulaires **Data safety** et **IARC** doivent refléter la réalité de l'app.

### 6.3 Ce que ces règles imposent au produit

| Règle | Conséquence directe |
|---|---|
| Pas d'analytique tierce par défaut | Mesurer l'usage soi-même, ou renoncer à le mesurer. Pas de Firebase Analytics, pas de SDK d'attribution. |
| Pas de publicité pour les enfants | Modèle sans publicité. Ce n'est pas un choix esthétique, c'est une contrainte. |
| Pas d'identifiant publicitaire | Ne jamais lier le SDK publicitaire d'Android ; ne pas déclarer `AD_ID`. |
| Public mixte = écran d'âge neutre | À éviter : Ludo'Lire est **exclusivement** enfant, donc une seule déclaration. |
| Déclaration du public cible | GS + CP + CE1 couvrent 4 à 8 ans, soit **deux tranches d'âge** chez les deux stores (5 ans et moins, puis 6-8 ans). À déclarer toutes les deux, et à assumer dans la fiche. |
| Politique de confidentialité obligatoire | Rédigée dès le premier jour, pas à la veille de la soumission. |

### 6.4 Ce que change la décision 4 — une seule porte parentale

La porte parentale protège **la politique de confidentialité, et rien d'autre**. Conséquences :

- **aucun autre lien sortant n'est possible.** Pas de « noter l'app », pas de « partager », pas de lien vers un site, pas de réseau social. C'est une contrainte de contenu, pas seulement de code ;
- **aucun achat** en v1 : il n'y a rien à acheter, donc rien à protéger. La décision est cohérente avec la gratuité de la v1 ;
- **le tableau de bord du parent n'est pas protégé.** Un enfant peut y arriver. Il ne doit donc contenir **aucune action irréversible** — ou bien ces actions passent par la même porte, ce qui reste à trancher (§ 12) ;
- **la décision devra être révisée au moment de l'abonnement.** Apple exige que toute occasion d'achat soit derrière une porte parentale. Le passage à l'abonnement ajoutera donc une seconde zone protégée — ce n'est pas un défaut de conception, c'est la règle.

### 6.5 Ce que la fiche de store doit dire — les trois annonces honnêtes

Décision prise le 21 septembre 2026 : **la fiche de store annonce les trois choses suivantes, explicitement.**

| Ce qu'on annonce | Pourquoi ce n'est pas de la communication |
|---|---|
| **« Gratuit pendant la phase de lancement »**, et non « gratuit » | La décision 5 prévoit un abonnement. Promettre « gratuit » puis facturer est le chemin le plus court vers les avis à une étoile (§ 9). |
| **Le palier de sortie de chaque tranche** — ce que l'enfant saura faire à la fin, écrit noir sur blanc | C'est la parade au risque « l'app est une démo » (§ 11). Une tranche dont le terme est annoncé n'est pas une tranche inachevée. |
| **La part préparatoire de la tranche GS** — « les deux tiers du contenu de la grande section préparent à la lecture plutôt qu'ils n'apprennent à lire » | C'est la conséquence directe de la réattribution des colonnes d'âge du programme de cycle 1 (§ 2). Le contenu est juste ; c'est la façon de le vendre qui serait fausse si on la taisait. Un parent qui découvre seul qu'on compte les syllabes en grande section se sent trompé, et il l'est. |

**Ce que la fiche ne doit pas faire :** nommer la tranche GS « niveau lecture » ou la présenter comme l'équivalent du CP. Le palier de sortie de la GS est un palier **oral** — nommer les lettres, entendre un phonème, repérer une rime. Le dire est ce qui rend le reste crédible.

**Conséquence de forme :** la troisième annonce tient en une phrase et doit apparaître dans les **métadonnées**, pas seulement dans la politique de confidentialité ou un écran interne. Une phrase qui ne se lit qu'après installation ne corrige pas une attente créée avant.

---

## 7. Données des enfants et RGPD

**Le principe : collecter le moins possible, et si possible rien.**

Le RGPD fixe à **15 ans** l'âge à partir duquel un mineur peut consentir seul au traitement de ses données pour un service de la société de l'information (article 8 du RGPD, transposé à l'article 45 de la loi Informatique et Libertés). En dessous, le consentement parental est requis. La CNIL recommande en outre de vérifier l'âge de façon proportionnée et de ne pas collecter plus que nécessaire.

Notre public va de 4 à 8 ans : **tout utilisateur est sous le seuil**. Le consentement parental serait donc requis pour la moindre collecte identifiante — sauf à ne rien collecter.

**Position pour la v1 :**

- **aucun compte enfant**, aucun nom, aucune date de naissance stockée, aucune photo, aucun e-mail ;
- **stockage local** de la progression sur l'appareil, effaçable ;
- **aucun identifiant persistant** transmis à un tiers ;
- **aucun micro** : la décision 3 supprime le seul capteur dont l'app aurait eu besoin ;
- politique de confidentialité et **registre de traitement** tenus dès le début.

Une app qui ne collecte rien n'a presque rien à déclarer. C'est un avantage concurrentiel décisif pour un produit destiné aux enfants, et c'est la voie la plus simple à défendre.

**Ce que l'abonnement changera.** Un abonnement suppose un compte, donc un identifiant et une adresse de paiement. La position « rien ne se collecte » deviendra « **rien côté enfant, le minimum côté parent** ». C'est tenable, mais il faut le concevoir maintenant : la frontière entre les deux doit exister dans le modèle de données **avant** qu'on y mette quoi que ce soit. Un compte créé plus tard sur une base qui n'a jamais distingué l'enfant de l'adulte est une reprise complète.

---

## 8. Ce que ces contraintes décident déjà pour la technique

Sans choisir la pile, on peut verrouiller six propriétés non négociables.

1. **Fonctionnement hors ligne complet.** Une salle de classe ou une voiture n'a pas de réseau. Le réseau ne doit servir qu'à la synchronisation optionnelle et aux mises à jour de contenu.
2. **Aucun SDK tiers non maîtrisé dans le binaire.** Chaque dépendance doit être justifiée, et son comportement réseau connu. C'est une exigence de conformité, pas d'hygiène.
3. **Contenu séparé du code.** Les corpus, les listes de CGP et les textes sont des données versionnées, modifiables sans publier une nouvelle version de l'app.
4. **Un moteur, trois jeux de données.** Les trois niveaux partagent la même mécanique de séance et de suivi ; ce qui change est le contenu et l'interface. Si les trois niveaux deviennent trois logiques, le projet devient trois projets.
5. **La structure doit accueillir CE2, CM1 et CM2 sans réécriture.** La décision 2 borne la v1, elle ne borne pas le produit.
6. **La frontière gratuit / payant est posée dès la v1.** Tout est ouvert en v1, mais le contenu doit déjà savoir s'il est libre ou payant. Le jour de l'abonnement, le changement est une configuration, pas une reprise — et la coupure choisie (§ 9) peut être annoncée dès la fiche de store.

---

## 9. Modèle économique

**v1 : gratuite, sans achat, sans abonnement, sans publicité.** C'est la décision 5, et elle est cohérente : la v1 n'a rien à vendre tant que les trois tranches sont superficielles.

**Ensuite : abonnement mensuel avec 7 jours d'essai.**

| Option | Compatible catégorie enfant | Avantages | Risques |
|---|---|---|---|
| **Abonnement mensuel, 7 jours d'essai** (décision 5) | Oui, derrière une porte parentale | Revenu récurrent ; finance le contenu des tranches suivantes | Suppose un compte et donc des données ; exige une infrastructure d'abonnement ; le passage du gratuit au payant est la transition la plus risquée d'une application grand public |
| Achat unique | Oui, derrière une porte parentale | Aucun compte, aucune donnée | Revenus plafonnés |
| Gratuit avec publicité | **Non** | — | Rédhibitoire pour un public enfant |

**La difficulté n'est pas l'abonnement, c'est le passage.** Des familles auront installé l'app gratuitement, s'y seront attachées, et se verront demander un paiement. Deux parades, à retenir maintenant parce qu'elles se préparent avant, pas après :

1. **Annoncer la gratuité comme temporaire dès la fiche de store.** « Gratuit pendant la phase de lancement » n'est pas la même promesse que « gratuit ». Ce n'est pas de la communication, c'est de l'honnêteté — et c'est ce qui évite les avis à une étoile.
2. **Garder un socle gratuit.** Le niveau 1 (GS) reste ouvert ; les niveaux CP et CE1 passent à l'abonnement. La coupure devient une frontière de contenu plutôt qu'un retrait, et le parent peut essayer l'app avec son enfant avant de payer.

**Deux points techniques à ne pas découvrir au moment du passage :** l'abonnement passe par StoreKit et Play Billing (des mécanismes de première partie, donc conformes) ; un prestataire tiers de gestion d'abonnements doit être vérifié au regard des règles du § 6 avant d'entrer dans le binaire.

---

## 10. Indicateurs de réussite

**La décision 3 change l'indicateur principal.** Sans reconnaissance vocale, il n'y a pas de mots correctement lus par minute — donc pas de mesure de fluence. Le prétendre serait malhonnête ; il faut un autre indicateur, et il existe.

**Indicateur principal : le franchissement du palier de sortie de la tranche.** Pour le niveau CP, par exemple : part des enfants ayant atteint 30 CGP sur 30 avec une précision supérieure à 95 % sur les mots réguliers. C'est mesurable, comparable d'un enfant à l'autre, et c'est aligné sur le palier officiel de milieu d'année.

Indicateurs secondaires :

- **Précision par CGP** : quelles correspondances résistent, et pendant combien de temps. C'est la donnée qui alimente le tableau de bord adulte, et la plus utile au parent comme à l'enseignant.
- **Régularité** : nombre de séances par semaine (cible : 4 ou plus).
- **Couverture** : part du contenu de la tranche effectivement parcourue.
- **Temps de réponse par item** : un proxy honnête de l'automatisation du décodage, à défaut de fluence. À utiliser comme tendance, jamais comme note.
- **Rétention à 30 et 90 jours.**
- **Côté store** : note moyenne, volume d'avis, taux de conversion vers l'abonnement le jour venu.
- **Côté adulte** : part des parents qui ouvrent le tableau de bord au moins une fois par mois.

À noter : **sans analytique tierce, ces mesures coûtent cher à obtenir.** Il faut soit une télémétrie maison respectueuse (agrégée, sans identifiant), soit des mesures déclaratives via des tests utilisateurs. C'est un coût réel du modèle retenu, à assumer dès maintenant.

---

## 11. Risques

| Risque | Gravité | Parade |
|---|---|---|
| Trois tranches superficielles, aucune menée à son terme : l'app est jugée « démo » | **Élevée** — c'est le risque né de la décision 1 | Chaque tranche a un palier de sortie explicite, affiché dans l'app et dans la fiche de store. Une tranche finie et annoncée comme telle n'est pas une démo. |
| Le passage du gratuit à l'abonnement fait fuir les familles acquises | **Élevée** — c'est le risque né de la décision 5 | Annoncer la gratuité comme temporaire dès le premier jour ; garder le niveau GS gratuit ; annoncer la frontière à l'avance. |
| La lecture à voix haute n'étant pas évaluée, la fluence n'est pas mesurée | Moyenne — assumée par la décision 3 | Mesurer la précision et le temps de réponse ; proposer une lecture non évaluée validée par le parent ; traiter la mesure vocale en v2. |
| Le contenu de trois tranches coûte plus cher que le code | Moyenne à élevée | Les textes sont écrits en interne (décision 7). Le goulot d'étranglement n'est plus l'écriture mais **le temps de relecture** : la relecture pédagogique est faite par le porteur du projet, en éprouvant l'application de bout en bout. Ce qui reste à organiser, c'est ce temps de test, pas le recrutement d'un relecteur. |
| Un texte de lecture contient une CGP non encore enseignée, et devient indéchiffrable | Moyenne, et insidieuse | Contrôle automatique de chaque texte contre la liste des CGP déjà vues pour le rang considéré. Un texte non conforme est un exercice raté qui ne se voit pas. |
| Rejet à la revue Apple ou Google | Moyenne | Conformité intégrée dès la conception (§ 6), pas corrigée après coup. |
| L'enfant s'ennuie au bout de deux semaines | Moyenne | Variété des exercices à progression constante ; séance courte ; fin systématiquement réussie. |
| Un concurrent bien financé occupe le terrain | Moyenne | La niche défendable n'est pas « apprendre à lire » mais « montrer au parent ce que l'enfant sait faire » — le tableau de bord. |
| Un parent trouve l'app « trop scolaire » | Faible | C'est le prix de l'efficacité ; l'assumer dans le positionnement. |

---

## 12. Décisions ouvertes

Les sept décisions de cadrage sont prises (§ 0). Ce qui reste :

1. **L'étape de lecture à voix haute non évaluée est-elle retenue ?** → Recommandation : oui. Elle préserve une entrée officielle du programme et prépare la v2 à coût quasi nul.
2. **Les actions irréversibles du tableau de bord (effacer la progression) passent-elles par la porte parentale ?** → Recommandation : oui, la même porte. Un enfant qui efface six mois de progression est un incident qui ne se répare pas.
3. **Que fait l'enseignant, que ne fait pas le parent ?** → Les deux rôles ne doivent pas se mélanger dans la même interface.
4. **La coupure gratuit / payant se fera-t-elle sur le niveau, ou sur le contenu ?** → Recommandation : sur le niveau (GS gratuit, CP et CE1 payants), pour que la frontière soit lisible.

---

## 13. Prochaines étapes

État au 21 septembre 2026 : les étapes 1 et 2 sont faites ; la 3 est amorcée (trois textes, à titre de preuve du mécanisme) ; le corpus audio de la GS est inventorié, le jeu de syllabes est spécifié et dérivé, les 44 illustrations de la GS sont produites et contrôlées, et la **banque d'exercices de la GS est écrite et contrôlée** — 50 exercices couvrant les 45 unités. La tranche GS est donc complète sur le papier. Pour le CE1, la **table de progression est écrite, sourcée et contrôlée** (42 unités), la **table des correspondances** qui la rend déchiffrable est écrite, le **décodeur du CE1 est éprouvé** — **129 essais** de part et d'autre de chaque seuil : 99 qui éprouvent le *verdict*, 20 la *lecture* — c'est-à-dire quels graphèmes sont muets — et 10 la *découpe* — quels graphèmes sont reconnus, et dans quel ordre — les **18 textes du CE1 sont écrits et conformes**, de six à quinze lignes de 34 signes, et la **banque d'exercices du CE1 est écrite et contrôlée** — 57 exercices couvrant les 42 unités, où les dix unités de production soldent leur dette. La largeur de ligne de l'application est **fixée**, sans quoi « une quinzaine de lignes » n'était vérifiable par rien, et le **corpus d'images du CE1 est écrit et contrôlé** — 3 images produites, 22 mots déclarés non dessinables avec leur raison, qui répondent aux besoins B04, B13 et B30 en disant aussi ce qui reste impossible —, et les **images de récit du CE1 sont écrites et contrôlées** — **8 scènes** pour les deux exercices de remise en ordre dont l'unité annonce un geste d'image, et la déclaration des deux autres, qui jouent sur le texte —, et les **textes courts du CE1 sont écrits et contrôlés** — **5 textes** de deux à six lignes, chacun déclarant son rang, son **type** et son titre, cités par les quatre exercices qui en ont besoin, ce qui solde le besoin B16 —, et les **pseudo-mots du CE1 sont écrits et contrôlés** — **10 suites**, les cinq du programme et cinq écrites, citées par les deux exercices de l'unité 35 qui les portaient tous deux, avec une prononciation **dérivée** des tables et non déclarée, ce qui solde le besoin B35. La tranche CE1 est donc complète sur le papier, comme l'était la GS avant elle.

1. **Table de progression des CGP du niveau CP** — *fait* : `outils/cgp-cp.json` → `contenu/LUDOLIRE-CGP-CP.md`, 30 unités bornant la tranche au palier de milieu d'année.
   **Table de progression de la tranche GS** — *fait* : `outils/progression-gs.json` → `contenu/LUDOLIRE-PROGRESSION-GS.md`, 45 unités sur cinq périodes (27 préparatoires, 18 GS), chacune rattachée à sa colonne d'âge du programme.
   **Corpus audio de la GS** — *fait* : `outils/corpus-gs.json` → `contenu/LUDOLIRE-CORPUS-AUDIO-GS.md`, 218 fichiers inventoriés (la banque d'exercices en a fait apparaître douze de plus que l'inventaire initial).
   **Jeu de syllabes manquantes** — *fait* : `outils/jeu-syllabes.json` → `contenu/LUDOLIRE-JEU-SYLLABES.md`, 42 items (30 oraux GS, 12 écrits CP), **84 intruses** dont 76 consonantiques. La banque est dérivée puis figée par `outils/proposer-intruses.py`, et vérifiée par `outils/verifier-corpus.py`.
   **Banque d'exercices de la GS** — *fait* : `outils/exercices-gs.json` → `contenu/LUDOLIRE-EXERCICES-GS.md`, **50 exercices couvrant les 45 unités**, 20 mécaniques, 7 besoins déclarés dont 2 bloquants, 5 corrections consignées. Contrôlée par `outils/verifier-exercices.py`, qui refuse une unité sans exercice, un verdict que la mécanique ne peut pas tenir, un besoin déclaré sans entrée consolidée — et réciproquement. La conception tient en une règle : *toute consigne se donne par la voix, toute réponse se donne par le geste*. Là où le programme demande une production que la machine ne peut pas entendre, la charge est **inversée** — la voix nomme et l'enfant touche — et l'exercice déclare ce que le geste reprend.
   **Illustrations de la GS** — *fait* : `outils/images-gs.json` → `contenu/LUDOLIRE-IMAGES-GS.md`, 44 briefs de dessin avec les ambiguïtés déclarées et leur parade, et **44 SVG produits** dans `contenu/images/` par `outils/generer-images.py`. **Aucun outil de génération d'image n'est disponible dans l'environnement actuel** : les images sont donc écrites comme du code, ce qui règle la licence par construction et les rend vérifiables par script (`outils/verifier-images.py`). L'export PNG 1x/2x/3x transparent existe (`outils/exporter-images.mjs`) et n'est pas versionné — artefact dérivé, régénérable. Reste à relire les images une par une, et à trancher le cas `café`.
2. **Règles de rédaction des textes de lecture** — *fait* : `contenu/LUDOLIRE-REGLES-TEXTES.md`, avec un contrôle automatique de conformité (`outils/verifier-textes.py`).
3. **Premiers textes de lecture** — amorcé : trois textes conformes (`contenu/textes/`). La suite s'écrit rang par rang.
4. **Veille concurrentielle ciblée** — établir ce que font les apps existantes (méthode, progression, modèle, confidentialité) avant de figer le positionnement.
5. **Maquettes des deux interfaces** — enfant (orale et iconographique pour la GS, lisible pour le CP) et adulte (tableau de bord).
6. **Note de conformité store** — public cible déclaré (deux tranches d'âge), Data safety, politique de confidentialité, et les trois annonces honnêtes du § 6.5.
7. **Relire les 44 illustrations, une par une** — les images existent, elles sont conformes au brief et contrôlées par script, mais aucun script ne juge si un dessin est *reconnaissable* par un enfant de cinq ans. La planche `contenu/images/planche.html` les montre toutes à la taille de l'application. Resteront ensuite : trancher le cas `café`, valider les deux conventions (`papa`/`maman`, `lit`/`dodo`), et faire passer un illustrateur si l'apparence doit être soignée.
8. **Tranche CE1** — *faite* : table de progression, table des correspondances, décodeur éprouvé, textes, **la banque d'exercices** — 57 exercices couvrant les 42 unités, la dette des dix unités de production soldée —, **le corpus d'images lexicales**, **les images de récit**, **les textes courts** et **les pseudo-mots**. La tranche est complète sur le papier, comme la GS avant elle.
   **Table de progression du CE1** — *fait* : `outils/progression-ce1.json` → `contenu/LUDOLIRE-PROGRESSION-CE1.md`, **42 unités** sur cinq périodes, réparties dans les **quatre ensembles officiels** de la section « Lecture » du programme — Identifier les mots (21), Lire à voix haute (4), Comprendre un texte (13), Devenir lecteur (4). Chaque unité déclare d'où vient son objectif (`objectif`, `exemple`, `choix`) et si son exemple est repris du programme ou de notre main : **24 exemples repris, 18 de notre main**, adossés à **8 citations officielles** de l'Annexe 3 que le contrôle relit. Contrôlée par `outils/verifier-progression.py`, qui refuse une unité hors des quatre domaines officiels, un exemple annoncé « programme » absent des citations, et — c'est le contrôle qui garde l'axe honnête — un objectif qui porte un **acte de parole** sans être marqué de production.
   **Table des correspondances du CE1** — *fait* : `outils/cgp-ce1.json`, **11 correspondances nouvelles** au-delà des 30 du CP, 34 mots-outils mémorisés, 7 mots irréguliers, 6 familles de règles. Elle ne redéclare ni les CGP du CP ni ses mots-outils : les redéclarer serait deux listes de la même chose, et le contrôle vérifie qu'elles sont **disjointes** au lieu d'exiger que la seconde n'existe pas.
   **Décodeur du CE1** — *fait* : `outils/verifier-textes-ce1.py`, éprouvé par `outils/tester-decodeur-ce1.py` (**129 essais**, chacun de part et d'autre d'un seuil). Trois règles du CP tombent au CE1 à un rang précis : la terminaison `-ent`, interdite dans toute la tranche CP, s'ouvre au rang 27 ; les consonnes doubles deviennent générales au rang 28 ; les lettres finales muettes s'étendent aux **muettes lexicales** au rang 26. La segmentation est **importée** du contrôle du CP, pas réécrite : deux découpures divergeraient. Le décodeur déclare ses limites plutôt que de deviner — le `r` final, les mots en `-ent` dont le `en` est nasal, les finales prononcées — et **dit toujours où il s'arrête**.
   Ce chantier a fait apparaître un défaut **dans la tranche CP déjà livrée** : `verifier-textes.py` lisait `pomme` comme `p | om | m | e`, c'est-à-dire /pɔ̃m/, et acceptait le mot au CP où `mm` n'est pas enseigné. Le défaut est corrigé, le harnais du CP reste vert (6 cas), et il n'était visible ni à la lecture du code ni à celle des textes.
   **Les textes du CE1** — *fait* : `contenu/textes-ce1/`, **18 textes**, de **six à quinze lignes**, un par palier de la progression, chacun déclarant son rang dans son propre en-tête (`# rang: N`) — le redonner sur la ligne de commande serait une seconde source de la même vérité. Ils sont contrôlés par `verifier-textes-ce1.py --tous`, et documentés par `contenu/LUDOLIRE-TEXTES-CE1.md`, dont le tableau des longueurs est **engendré** à partir des fichiers eux-mêmes — un fichier de texte *est* la donnée, et la recopier dans un JSON créerait une seconde source qui divergerait en silence.
   **La largeur de ligne, et pourquoi elle est une décision de produit** — *fait* : le programme du CE1 fixe la longueur d'un texte **en lignes** (« une quinzaine de lignes »), et une ligne n'a de sens qu'avec la largeur de ligne de l'application. Tant qu'elle n'était pas fixée, « une quinzaine de lignes » n'était **vérifiable par rien**, et un texte de quinze **phrases** passait pour un texte de quinze **lignes** — il en fait vingt. La largeur est donc **fixée à 34 signes espaces comprises** (`LARGEUR_LIGNE` dans le contrôle), le texte y est plié, et le compte de lignes est **contrôlé** : la tranche va de 6 à 16 lignes, et le profil des 18 textes monte sans jamais décroître. Le chiffre n'a pas été choisi pour arranger les textes : au-delà d'une trentaine de signes, le retour à la ligne devient une source d'erreur pour un enfant qui apprend à lire.
   Ce compteur a fait apparaître que **les textes écrits d'abord étaient trop longs** — jusqu'à vingt lignes pour le palier — et les 18 textes ont été recalibrés. Un contrôle qui se contente de rapporter ne corrige rien ; c'est le seuil qui a rendu la faute visible.
   **Deux défauts de plus dans le décodeur, tous deux trouvés en écrivant les textes** — *corrigés*. D'abord, la moitié « muette » de la **règle du `r` final** n'était pas implémentée : elle était écrite dans la table, mais le `r` après un `e` tombait dans la barrière du rang 26, et « chanter » au rang 1 était rapporté comme « consonne finale qu'aucune règle ne couvre » — un refus qui portait à côté, puisque la règle était dans le même fichier. Le harnais ne l'avait pas vu parce qu'il ne testait « chanter » **qu'au rang 26**, le seul rang où la barrière masque exactement ce défaut. Ensuite, les **formes élidées** étaient refusées : la découpe jette l'apostrophe, et `l'agneau`, `n'est`, `j'aime`, `d'un` arrivaient au contrôle comme des mots d'une lettre dont la consonne finale serait muette. Une consonne en tête de mot est une **attaque** : elle se prononce toujours, et un mot ne peut pas être entièrement muet. Le même défaut existait dans le contrôle du CP, où il faisait lire `d'un` avec un `d` muet — **accepté, mais mal lu**, le sens d'erreur le plus dangereux. Les deux harnais ont donc reçu une section qui éprouve la **lecture** (quels graphèmes sont muets) et pas seulement le verdict : le harnais du CE1 est passé de 64 à **110 essais** — 93 verdicts et 17 lectures —, puis à **129** avec sa troisième section (voir plus bas), celui du CP de 6 cas à **6 cas et 8 lectures**. Le correctif a été **falsifié** avant d'être cru — la version d'avant est jouée à côté de la nouvelle, et `d`, `s`, `t` changent bien de lecture.
   **Deux défauts de plus dans le décodeur, tous deux trouvés en écrivant la banque d'exercices** — *corrigés*. Le premier est un cas d'école : les graphies `aille`, `eille`, `euille` étaient **déclarées deux fois** — dans la table des correspondances, et dans une liste recopiée dans le code — et les deux listes avaient divergé. La table portait les sept graphies de l'unité 18 ; le code en découpait quatre, et pas les mêmes. `oreille`, `taille`, `bataille`, `abeille` étaient donc **refusés** comme « graphème non enseigné », et `feuille` était lu `f | euil | l | e`, c'est-à-dire /fœjl/ — **accepté, et mal lu**, le sens d'erreur le plus dangereux. Le défaut était invisible dans les dix-huit textes : aucun ne contient ces graphies. Il n'est apparu qu'en écrivant l'exercice de l'unité 18 — **un contrôle vert sur un corpus ne dit rien d'un mot absent du corpus**. Le remède n'est pas de recopier la liste correctement, c'est de ne plus la recopier du tout : les graphies sont désormais **dérivées de la table**, avec leur identifiant de CGP, et deux essais du harnais les éprouvent, un par le verdict et un par la lecture. Le second défaut tient à une subtilité de Python : `"" in "eiéèê"` est **vrai** — la chaîne vide est sous-chaîne de toute chaîne. Quand `c` est la dernière lettre d'un mot, la lettre suivante est `""`, donc `c` était résolu `c-doux` et lu /s/ : `sac` était **refusé** avant le rang 19, et `avec` — présent dans deux textes déjà tenus pour conformes — était **accepté mais lu /avɛs/**. Le garde-fou `suivant and suivant in …` a été posé sur `c` et sur `g`, six essais ajoutés au harnais, et le contrôle des positions rendu **falsifiable** : il sonde `cit`/`cat` et `git`/`gat`, et échoue si le chemin positionnel disparaît. Le contrôle d'atteignabilité qui l'avait précédé, lui, ne pouvait pas échouer — il cherchait chaque graphie dans la découpe d'une sonde construite autour d'elle, où elle était forcément la plus longue correspondance — et il accusait deux graphies saines. Un contrôle qui ne peut pas échouer fait pire que rien : il rassure.
   **La banque d'exercices du CE1** — *fait* : `outils/exercices-ce1.json` → `contenu/LUDOLIRE-EXERCICES-CE1.md`, **57 exercices couvrant les 42 unités**, **33 mécaniques** (29 tenues par l'application, 4 déclarées **hors app** : lire à voix haute, se faire chronométrer, choisir un livre, dire ce qu'une lecture a rappelé), **33 consignes** — toutes enregistrées à la voix, chacune portant son pictogramme —, **5 besoins** déclarés dont aucun bloquant, et **4 corrections** consignées. Elle tient la règle de la GS — *toute consigne se donne par la voix, toute réponse se donne par le geste* — et la pousse plus loin : **dix unités demandent une production que la machine ne peut pas entendre**, et chacune doit dire comment elle s'en acquitte. Sept la paient par une `inversion` — la voix nomme, l'enfant touche, et l'exercice déclare ce que le geste reprend : donner un titre (unité 6), justifier une réponse (7), restituer les étapes (14), expliciter une émotion (15), caractériser un personnage (25), résumer (37), établir des liens entre deux textes (41). Trois la paient par un `pourquoi_hors_app` : lire à voix haute (34), la vitesse de lecture, qui ne se mesure pas sans oreille (39), adapter sa voix et sa cadence (40). L'unité 41 paie **les deux**, parce qu'elle demande à la fois d'établir des liens et de dire ce qu'une lecture a rappelé ; et l'unité 42, qui n'est pas une unité de production mais relève de « Devenir lecteur », est hors app par nature — choisir un livre pour son plaisir ne s'évalue pas. Le contrôle refuse une unité de production dont l'exercice ne déclare ni `inversion` ni `pourquoi_hors_app` : **aucune ne reste sans réponse**. **27 questions de compréhension**, réparties sur 24 exercices, portent chacune sa **phrase-preuve**, et le contrôle refuse une question dont la phrase citée n'est pas **littéralement** présente dans le texte qu'elle nomme — c'est la vérification que le contrôle des textes annonçait sans pouvoir la faire. Quatre exercices ont besoin de textes **plus courts que ceux de la tranche** — unité 16, pour opposer un récit à un documentaire ; unité 27, pour départager deux phrases ; unité 41, pour apparier trois lectures proches : ils les portent eux-mêmes, de deux à six lignes, et le contrôle vérifie que chaque mot y est lisible au rang de l'unité. Onze exercices déclarent leurs `graphies` et deux leurs `pseudo_mots`, deux champs que le CE1 ajoute à ceux de la GS parce qu'une graphie de plusieurs lettres ne tient pas dans `lettres`. La banque est contrôlée par `outils/verifier-exercices.py --ce1`. Elle a été **falsifiée une première fois à la main** — dix-sept fautes injectées une par une —, et cela a fait apparaître un vrai défaut, de la même famille que dans le décodeur : le contrôle d'usage lisait les déclarations dans le fichier d'origine au lieu de la banque qu'on lui passait, si bien qu'une mécanique **ajoutée** lui échappait, précisément le cas qu'il doit attraper. Mais cette falsification n'avait laissé **aucun banc** : rien ne pouvait la rejouer, et une falsification qu'on ne peut pas rejouer ne protège que le jour où elle a été faite. Les cas sont donc écrits, et ils le restent — `outils/tester-exercices-ce1.py` injecte **vingt fautes** sur une copie en mémoire, avec un témoin joué d'abord sur la banque réelle.
   **Le `um` de la nasale `un`, et la troisième section du harnais** — *corrigé*. La table déclare `on/om`, `an/am`, `in/im`, `ain/ein` — une nasale devant `p` ou `b` s'écrit avec un `m` — mais l'unité 13 ne déclarait que `un`. `parfum` était donc **refusé**, son `m` final n'étant couvert par aucune règle avant le rang 26, et `humble`, découpé `h | u | m | b | l | e`, était lu /ymbl/ pour /œ̃bl/ — **accepté, et de travers**. Le défaut est apparu en cherchant l'image d'un mot porteur de la nasale, donc **en dehors des dix-huit textes** : aucun ne contient de `um`. Le correctif a été **falsifié**, et la falsification a montré que le harnais ne pouvait pas le voir : retirer le `um` du garde-fou des nasales ne changeait **aucun** essai, parce que `humide` découpé `h | um | i | d | e` donne le même verdict et la même liste de muets que `h | u | m | i | d | e`. Le harnais a donc une **troisième section**, qui éprouve la **découpe** — quels graphèmes sont reconnus, dans quel ordre —, et il passe de 110 à **129 essais** : 99 verdicts, 20 lectures et 10 découpes. *Un contrôle ne prouve que ce qu'il regarde, et il faut le falsifier pour savoir ce qu'il regarde vraiment.*
   **Les illustrations du CE1** — *fait* : `outils/images-ce1.json` → `contenu/LUDOLIRE-IMAGES-CE1.md`, **3 images** produites dans `contenu/images-ce1/` par `outils/generer-images.py --ce1` (`foin`, `parfum`, `œil`) et **22 mots déclarés non dessinables**, chacun avec sa raison et son motif, pris dans une liste fermée. Le corpus répond aux trois besoins B04, B13 et B30, et sa réponse dit aussi ce qui reste impossible : sur **vingt-cinq mots examinés**, trois sont illustrables, parce que les deux nasales rares et les mots irréguliers sont les endroits du français où le nom concret se raréfie. **Ce n'est donc pas un manque d'illustrateur** : ces besoins se soldent par la **lecture**, ce que les exercices font déjà. Le corpus ne recopie pas le cadrage de la GS, il le reprend **par référence** — deux copies d'une même règle divergent, et c'est ce qui a valu quatre mots refusés et un mot lu de travers. Il dit la **vérité** sur son emploi (`present_dans_la_serie` est comparé à la série réelle de l'exercice), il refuse un mot illisible au rang de l'unité qui l'affiche, et il porte un datum — `reponse_aux_besoins` — qui **réclame** chaque image : sans lui, un mot illustré qui disparaît du corpus ne faisait échouer aucun contrôle, et c'est la falsification qui l'a montré, pas la lecture du code. Contrôlé par `outils/verifier-images.py --ce1`, éprouvé par `outils/tester-images-ce1.py` — **23 corpus faux et 4 fichiers faux, tous vus**. Le travail a mis au jour deux écarts dans la banque, consignés et **non corrigés** parce que la relecture pédagogique appartient au porteur du projet : l'énoncé de E09 annonce « six mots affichés, un seul porte `oin` » là où sa série en compte six qui portent tous la graphie, et celui de E18 annonce « trois et trois » là où elle en compte quatre et deux.
   **Les images de récit du CE1** — *fait* : `outils/images-recit-ce1.json` → `contenu/LUDOLIRE-IMAGES-RECIT-CE1.md`, **8 scènes** produites dans `contenu/images-recit-ce1/` par `outils/generer-images.py --recit` — quatre moments pour chacun des deux exercices de remise en ordre qui jouent sur des images, E19 (unité 14) et E45 (unité 37). Une icône porte un mot et se vérifie seule ; une image de récit porte un **moment** et ne se vérifie que **dans son ordre** : c'est ce qui justifie un corpus à part et un contrôle à part. Le contrôle central cherche la ligne citée par chaque étape **littéralement** dans le fichier du texte et refuse un ordre que le texte ne porte pas — c'est le seul défaut de ce corpus qui ne se voie ni dans le code ni dans un fichier. Chaque étape déclare le **repère** sur lequel le dessin s'appuie pour être reconnu — le personnage, le cadre, le moment du jour, le décor, le geste du corps —, deux étapes d'un même récit ne peuvent pas s'appuyer sur le même, et les craintes de confusion sont **réciproques** : si une étape en craint une autre, l'autre la craint aussi. Les figures ne sont pas redessinées, elles sont **réemployées** — le même papa, le même éléphant, le même chat — et le trait est **compensé**, parce que le moteur de rendu **ignore** `vector-effect="non-scaling-stroke"` : mesuré, pas supposé — à l'échelle 0,25 le contour rendu fait 1 px, que l'attribut soit posé sur le groupe, sur la forme, ou nulle part. La compensation est donc écrite dans le fichier, et le contrôle relit le produit de l'échelle et de l'épaisseur : il refuse une figure dont le trait ne rend pas 4 px. Éprouvé par `outils/tester-images-recit.py` — **32 corpus faux et 6 fichiers faux, tous vus**. Le contrôle de couverture a fait apparaître ce que ce cadrage ne mentionnait pas : **quatre** exercices remettent un récit dans l'ordre, et c'est la progression qui dit lesquels jouent sur des images — E39 (unité 32, une recette) et E51 (unité 38, un texte entier) demandent de **lire**, et le corpus les déclare au lieu de les ignorer. La référence de cadrage s'est révélée **transitive** — le corpus du récit renvoie au corpus lexical du CE1, qui renvoie à la GS —, et la résolution est désormais unique et partagée par les deux modes.
   **Les textes courts du CE1** — *fait* : `contenu/textes-courts-ce1/` → `contenu/LUDOLIRE-TEXTES-COURTS-CE1.md`, **5 textes** de deux à six lignes, chacun déclarant son rang, son **type** et son titre, et **cités** par les quatre exercices qui en ont besoin. Un texte du palier est la donnée d'un rang ; un texte court est un texte qu'on **compare**, et tant qu'il était porté par l'exercice il n'existait que dans le corps d'un JSON, où rien ne le voyait. Le travail a mesuré ce que cela coûtait : **cinq phrases des textes courts étaient déjà des lignes d'un texte du palier**, `E32` et `E33` portaient le **même texte** chacun de son côté, `E21` et `E55` partageaient **trois phrases**, et **cinq titres** entraient en collision avec ceux des textes du palier — deux « Le vent », deux « Le chat » sous des formes voisines. Aucun de ces défauts n'était visible dans le code : les textes étaient conformes mot à mot. **Le type déclaré est ce qui rend la clé de réponse vérifiable** — une question qui demande « le texte qui raconte » et dont la bonne réponse est déclarée `informatif` apprend l'inverse de ce qu'elle annonce ; le contrôle lit la direction dans la question, « raconte » ou « explique », et refuse une clé qui ne va pas dans ce sens ; quand la question ne dit ni l'un ni l'autre, il **ne conclut pas** et le déclare. Le corpus est contrôlé par `outils/verifier-textes-courts-ce1.py`, éprouvé par `outils/tester-textes-courts-ce1.py` — **15 corpus faux et 1 témoin, tous vus** —, et les contrôles de la banque ont reçu leur banc le même jour, `outils/tester-exercices-ce1.py` — **20 banques fausses et 1 témoin, tous vus**. Ce travail solde le besoin **B16**, et il a montré que le besoin disait moins que son propre détail : le manque n'était pas l'absence d'un texte informatif — il y en avait un, écrit dans `E21` — mais le fait qu'il n'existait **nulle part ailleurs que dans cet exercice**.
   **Les pseudo-mots du CE1** — *fait* : `outils/pseudo-mots-ce1.json` → `contenu/LUDOLIRE-PSEUDO-MOTS-CE1.md`, **10 suites** — les **cinq** exemples du programme et **cinq** écrites pour l'exercice qui en manquait —, chacune déclarant ses graphies, sa complexité et son origine, et **citées** par les deux exercices de l'unité 35. Le défaut mesuré est le même que celui des textes courts, poussé plus loin : `E42` et `E43` **portaient la même liste de cinq**, chacun de son côté. Or `E42` fait **entendre** les suites et les fait retrouver parmi trois écrites, et `E43` les fait **lire** en demandant de décider si c'est un mot. Avec la même liste, l'enfant qui venait de toucher `valin` dans le premier n'avait plus besoin de le décoder dans le second — alors que `E43` déclare entraîner « décoder d'abord, décider ensuite » et déclare ne pas vérifier « ce que l'enfant fait d'un mot qu'il croit reconnaître sans le lire ». **L'exercice fabriquait la situation qu'il dit ne pas mesurer.** La parade n'est pas de recopier mieux, c'est de ne plus recopier : le corpus est la seule copie, et le contrôle refuse qu'un même pseudo-mot soit cité par deux exercices de la même unité. **La prononciation n'est pas déclarée, elle est dérivée** — graphie par graphie, avec le décodeur et les tables du projet —, et c'est le script de l'enregistrement : dix valeurs écrites à la main auraient été invérifiables. Deux règles sont nées de la mesure. D'abord, **le rang minimal ne dit rien ici** : au CE1 tout le CP est acquis dès le rang 1, donc `doir`, `choust` et `valin` — trois des cinq exemples du programme — sont déchiffrables au rang 1 et ne portent **aucune** graphie du CE1 ; la règle qui les remplace est celle de la **complexité**, et le contrôle refuse un exercice dont aucune suite citée n'est complexe. Ensuite, et c'est la découverte de ce travail : **neuf graphies de la table** — `ill`, `y`, `ail`, `eil`, `euil`, `ouille`, `aille`, `eille`, `euille` — **n'ont pas de lecture dérivable**. La table leur donne `/j/`, qui est une **semi-consonne** et ne fait pas une syllabe : c'est l'**étiquette de la classe** des graphies du /j/ en fin de mot, pas leur lecture, qui se compose (`ail` vaut /aj/, `euille` /œj/, `ill` /ij/). Le défaut a été trouvé par un refus — une suite écrite avec `ail` se lisait /bʁɔ̃dj/ —, et la distinction avec `qu`, `gu`, `ge` n'est pas arbitraire : ces trois-là contiennent aussi une voyelle et rendent des consonnes pleines, donc des lectures complètes. Aucune suite bâtie sur ces neuf graphies ne peut donc entrer dans le corpus, faute d'une prononciation fondée ; le décodeur, lui, n'en souffre pas — il n'a jamais besoin du phonème pour dire si un texte est déchiffrable. Le corpus est contrôlé par `outils/verifier-pseudo-mots.py`, éprouvé par `outils/tester-pseudo-mots.py` — **20 corpus faux, 1 témoin, 12 mots réels dont la lecture est éprouvée et 5 divergences assumées, tous vus**. Ce travail solde **B35**, et il confirme la leçon de B16 : le besoin disait moins que son propre détail. Son manque — « aucun pseudo-mot n'est enregistré » — est un enregistrement à faire ; son détail — « un pseudo-mot enregistré par erreur comme un mot deviendrait un mot » — est une crainte de **nommage**, et c'est la seule partie qui se solde par une règle : la famille d'enregistrement s'appelle `pm`, et une suite qui est déjà un mot de l'application est refusée.
   Restent, pour la tranche CE1 : **l'enregistrement** — les 18 textes du palier, les 5 textes courts, les 10 pseudo-mots et les 33 consignes, que le corpus audio de la GS ne couvre pas (B01a), et les mots du CE1 (B02) ; les pseudo-mots ont désormais leur spécification et le script de leur prise de son, ce qui manque est la prise de son elle-même. S'y ajoutent des manques que le travail sur les images, sur les textes courts et sur les pseudo-mots a fait apparaître sans qu'aucun besoin ne les déclare : la **relecture des huit scènes de récit**, celle des **cinq textes courts** et celle des **dix pseudo-mots**, un par un — les uns et les autres sont conformes au brief et contrôlés par script, mais aucun script ne juge si un dessin se reconnaît, si le type déclaré d'un texte est le bon, ni si un pseudo-mot est un **bon** pseudo-mot pour un enfant de CE1 —, l'**emploi de deux des trois images** du corpus lexical — `foin` et `parfum` ne sont pas encore dans la série de leur exercice, ce que le corpus déclare au lieu de le taire —, et **les trois écritures que `E42` promet sans les nommer** : son énoncé dit « chacune à retrouver parmi trois écrites », et ces deux autres écritures ne sont déclarées nulle part. **Mesuré, puis tranché** : le vivier est large — une substitution d'une seule graphie laisse **187 à 263** candidates lisibles par suite —, l'enveloppe le resserre à **80 à 136**, et ce qui reste ne se sépare par aucune règle mais par la **nature du phonème** : `dchr`, `dgnr`, `chgust`, une consonne posée là où la suite porte une voyelle, sont du bruit, quand `valan`, `valon`, `valun` autour de `valin` et `trampon`, `trenpon` autour de `trumpon` sont de vrais leurres. **Le choix n'est donc pas dérivable** : c'est un jugement pédagogique, et il rejoint `foin`/`parfum` dans la liste des arrêts **déclarés** plutôt que d'être habillé en règle. Aucun de ces manques n'est bloquant : la banque est jouable telle quelle, et chacun se solde par un enregistrement, une relecture ou une décision pédagogique.

   **L'application, et l'IPA non signé** — *fait* : Ludo'Lire est désormais une **application Expo** (SDK 57, `expo-router`), dans `app/`, et non plus seulement une spécification. Elle est **hors ligne** — elle ne parle à aucun serveur, donc elle n'a aucune variable `EXPO_PUBLIC_*` à perdre au regroupement —, mais elle a un défaut qui lui est propre, et c'est celui-là que le flux surveille. Le contenu qu'elle affiche est **fabriqué**, jamais écrit à la main : `outils/generer-contenu-app.py` le tire des corpus vers `assets/contenu-app.json` — 3 niveaux, 26 textes, 42 items, 87 unités, 30 correspondances —, il est **déterministe au bit près** (mesuré : SHA-256 identique après refabrication), et il porte une **empreinte de lui-même** (`97668bdf9b636299`) que l'écran d'accueil affiche. Ce travail a mis au jour une contradiction **dans une banque déjà livrée** : `jeu-syllabes.json` déclarait ne lire que `mots-gs.json`, alors que huit de ses douze items écrits — `lama`, `mule`, `rame`, `lime`, `lilas`, `tapis`, `dodu`, `poisson` — viennent de `mots-cp.json`. Le contrôle, lui, lisait bien les deux banques : c'est la **déclaration** qui était fausse. Un générateur qui suit la déclaration plutôt que le contrôle perdait **huit items en silence** — 42 annoncés, 34 écrits, aucune erreur. Corrigé des deux côtés : la déclaration nomme maintenant les deux banques, et le générateur **refuse** un item qu'il ne sait pas résoudre au lieu de le laisser tomber. Le flux `.github/workflows/ios-unsigned.yml` compile l'IPA **non signé** sur `macos-26` et le publie dans une *release*, seul chemin qu'un iPhone peut suivre sans compte GitHub — l'artefact d'un flux répond 401 à un visiteur anonyme, un fichier attaché à une release répond 302. Il vérifie deux choses, et ce sont les deux qui comptent ici : que `assets/contenu-app.json` est bien ce que les corpus produisent (refabrication, puis `git diff --exit-code`), et que le paquet JavaScript **livré** contient l'empreinte du dépôt — sans quoi une compilation verte cacherait un contenu périmé. Trois contrôles de plus sont nés en poursuivant, et tous les trois d'une promesse non tenue. Le **mélange des cartes** — le corpus déclare la bonne carte en tête, et l'application la déplace — vivait dans l'écran, qu'aucun banc ne peut charger puisqu'il importe React Native : il est passé dans `melange.ts`, éprouvé par huit cas dont quatre implémentations fausses. Sa graine dépend désormais de la **partie** et non du seul item, car l'ordre était figé pour toujours : l'enfant qui touchait « Recommencer » retrouvait la disposition qu'il venait de mémoriser, et gagnait sans lire au troisième passage — précisément ce que le mélange existe pour empêcher. Mesuré après correction : **chaque item atteint les trois positions** sur quinze parties, et la répartition reste équilibrée (15 / 14 / 13 à la première). Enfin, `experiments.typedRoutes` était déclaré mais **ne gardait rien** : les types de routes sont écrits par `expo prebuild`, qui tourne *après* `typecheck`, dans le flux comme en local — donc une faute de frappe dans un `pathname` aurait traversé tout le typage et serait apparue à l'exécution, sur l'écran de l'enfant. `scripts/verifier-routes.mjs` lit `app/` sur le disque et ne dépend d'aucune génération : il vérifie que chaque navigation mène à un écran qui existe, que chaque écran est déclaré dans la pile, et qu'aucune déclaration n'est orpheline — expo-router ignorant ces deux dernières fautes en silence. L'application **ne fait pas** ce que les corpus ne portent pas encore : elle n'a **aucun son** — l'écran le dit lui-même plutôt que de laisser croire à une panne —, le CP n'a **pas de textes**, et les 107 exercices des deux banques ne sont pas encore rendus à l'écran. La v1 jouable se limite donc aux trois textes de GS, au jeu du mot à trous (42 items), aux textes et unités du CE1 et aux correspondances du CP. Le dépôt est public — **`github.com/Msoumaya2019/ludolire`** — et l'IPA se récupère dans ses *versions* : il est **non signé**, donc à re-signer sur l'appareil avec ESign ou Sideloadly, et une signature par certificat Apple gratuit ne tient que **sept jours**. Que la version téléchargeable porte bien le correctif du mélange a été **prouvé, et non supposé** : le paquet publié a été retéléchargé, et l'en-tête de son bytecode Hermes livre un `sourceHash` — l'empreinte du source JS compilé, indépendante de la machine. Il est identique à celui de l'export local du commit corrigé (`55a81e2c…`), et **différent** de celui du commit parent (`5828e32b…`) : c'est ce second essai qui donne sa valeur au premier, sans quoi un champ constant passerait pour une preuve. Comparer les deux fichiers octet à octet, lui, ne dit rien — l'URL source embarquée contient le chemin de la machine et décale tout ce qui suit. C'est un artefact pour **essayer** l'application, pas pour la distribuer : la distribution aux familles passe par le magasin.

---

## Sources

- Arrêté du 22 octobre 2024 (JO du 25 octobre 2024), BO n° 41 du 31 octobre 2024 — programmes de cycle 1 (langage oral et écrit) et de cycle 2 (français, mathématiques). Application : rentrée 2025-2026. Les chiffres de fluence CP (30 sans préparation / 50 après préparation), CE1 (70) et CE2 (90), ainsi que les paliers de milieu d'année du CP, sont extraits du texte publié.
- Arrêté du 10 avril 2025 (JO du 16 avril 2025), BO n° 16 du 17 avril 2025 — programmes de français et de mathématiques du cycle 3. Application : CM1 et 6e à la rentrée 2025-2026, CM2 à la rentrée 2026-2027. Cibles de fluence : CM1 110, CM2 120, 6e 130 mots par minute.
- App Store Review Guidelines, sections 1.3 (Kids Category) et 5.1.4 (Kids) — consultées le 21 septembre 2026.
- Google Play, politique Familles (support.google.com/googleplay/android-developer) — consultée le 21 septembre 2026.
- RGPD, article 8 ; loi Informatique et Libertés, article 45 (âge du consentement numérique fixé à 15 ans en France) ; recommandations de la CNIL relatives aux droits numériques des mineurs.
