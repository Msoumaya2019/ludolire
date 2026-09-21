# Ludo'Lire

**Apprendre à lire en jouant.**
Écoles maternelle et élémentaire Frères Lumières — Montmagny.

Ludo'Lire est une application de lecture pour trois tranches du cycle 1 et du
cycle 2 : la grande section, le cours préparatoire et le cours élémentaire
première année. Elle est **hors ligne** : elle ne parle à aucun serveur, ne
collecte aucune donnée et n'a pas de compte.

---

## Ce que contient ce dépôt

Le dépôt porte **deux choses**, et il est utile de les distinguer :

| | Quoi | Où |
| --- | --- | --- |
| **La spécification** | les corpus, les contrôles, les textes, les documents, les images | `outils/`, `contenu/` |
| **L'application** | l'application Expo qui les affiche | `app/`, `assets/`, `package.json` |

La spécification a été écrite **avant** l'application, et c'est délibéré : les
textes de lecture, les banques d'exercices, les découpes syllabiques et les
correspondances graphème-phonème ont été établis et vérifiés par des contrôles
avant qu'un seul écran n'existe. L'application ne décide de rien : elle affiche
ce que les corpus déclarent.

### L'arborescence

```
app/                    les écrans de l'application (expo-router)
assets/                 l'icône, l'écran de démarrage, et le contenu embarqué
contenu/                les textes de lecture et les documents du projet
  textes/                 les textes de la GS
  textes-ce1/             les textes du CE1
  textes-courts-ce1/      les textes courts du CE1
  planche-ecran-exercice.html   la planche de relecture de l'écran « S'entraîner »
outils/                 les corpus (JSON) et les contrôles (Python)
  *.json                  les corpus : mots, progressions, exercices, images
  formes-exercices.json   la DÉCISION : quelle interaction rend chaque mécanique
  verifier-*.py           les contrôles
  tester-*.py             les bancs de falsification des contrôles
  generer-contenu-app.py  fabrique le contenu embarqué dans l'application
scripts/                les contrôles qui tournent sous Node, donc en intégration
tests/                  les bancs de ces contrôles
```

---

## Une décision se range dans un fichier, pas dans une intention

`outils/formes-exercices.json` dit, pour chacune des 53 mécaniques des deux
banques d'exercices, **par quelle interaction l'application la rend** — ou
pourquoi elle n'en rend aucune. Les 95 exercices déclarés jouables par les
banques deviennent 11 réellement affichés, et les 81 autres sont comptés avec
leur raison.

C'est une décision, et non une déduction : la deviner en lisant la prose du champ
`geste` ferait exactement ce que ce projet refuse, une promesse que rien ne
vérifie. `outils/verifier-formes.py` tient donc trois choses ensemble — la table,
les deux banques, et les écrans réellement présents dans `app/` — et refuse
qu'une mécanique soit oubliée, qu'une forme nulle reste sans motif, ou qu'une
forme dise être rendue par un écran qui n'existe pas.

Une exception dit **de quel genre elle est**, parce que les deux ne se mesurent
pas de la même façon : `champs_manquants` quand il manque à l'exercice ce que sa
forme exige — un trou dans la donnée —, et `forme_inadaptee` quand l'exercice
porte tout mais que la forme ne sait pas montrer ce qu'il juge.

---

## Le contenu embarqué est FABRIQUÉ, jamais écrit à la main

`assets/contenu-app.json` n'est pas un fichier source. Il est produit par :

```bash
python outils/generer-contenu-app.py
```

à partir des corpus de `outils/` et des textes de `contenu/`. **Ne corrigez
jamais une faute dans `contenu-app.json`** : la correction disparaîtrait à la
fabrication suivante. Corrigez le corpus, puis relancez le générateur.

Le fichier porte une **empreinte de lui-même**, et l'application l'affiche en bas
de son accueil. C'est ce qui permet de savoir, en regardant l'application
installée, quel contenu elle embarque réellement.

---

## Vérifier

```bash
npm run verify
```

Cette commande enchaîne six contrôles :

| Contrôle | Ce qu'il vérifie |
| --- | --- |
| `check:workflows` | que les flux de travail GitHub sont bien formés, avant de les pousser |
| `routes:verifier` | que chaque navigation mène à un écran qui existe, et que chaque écran est déclaré |
| `contenu:verifier` | que le contenu embarqué est cohérent et que son empreinte correspond |
| `formes:verifier` | que chaque mécanique des banques a une forme déclarée, et que l'écran qui la rend existe |
| `typecheck` | que le TypeScript compile |
| `test` | les quatre bancs — 76 cas : le contenu (40, dont 35 falsifications), les flux (17, dont 11 mutations), le mélange des cartes (8, dont 4 implémentations fausses) et les routes (11, dont un faux positif) |

`formes:verifier` est le seul contrôle **Python** de cette liste. Il est appelé
par `python3` — le nom qui existe sur un exécuteur macOS comme sur cette machine
— et il tourne dans l'intégration continue comme les autres.

Le lanceur est appelé avec un **motif explicite** — `node --test
"tests/*.test.mjs"` — et non sans argument. Sans argument, Node découvre les
tests par convention, et cette convention descend dans `node_modules` : mesuré
sur ce dépôt, elle ramassait 76 fichiers `.js` rangés sous un dossier `test/`
d'appartenance à des paquets, plus un fichier de test d'un paquet. Le banc
passait de 40 à 277 cas, dont 201 en échec — tous imputables à des paquets
tiers. **Un contrôle qui ramasse ce qu'il n'a pas désigné ne dit rien de ce
qu'on lui demande de garder.**

Le banc du mélange importe `melange.ts` directement : Node 22 détache les types
et exécute le TypeScript sans transpileur. C'est la raison pour laquelle le
mélange vit dans son propre module plutôt que dans l'écran — `app/jeu.tsx`
importe React Native, donc un banc ne peut pas le charger, donc **rien** ne
vérifiait que le mélange déplace réellement la bonne carte.

Côté corpus, les contrôles du projet sont en Python :

```bash
python outils/verifier-exercices.py
python outils/verifier-textes-ce1.py --tous
python outils/verifier-pseudo-mots.py
python outils/verifier-formes.py
```

Leurs bancs de falsification ne tournent pas dans `npm run verify` — ils
éprouvent les contrôles, ils ne gardent pas le dépôt. On les lance à la main,
après avoir touché au contrôle correspondant :

```bash
python outils/tester-formes.py
python outils/tester-controle.py
```

---

## Obtenir l'application sur un iPhone

L'application n'est pas sur l'App Store. Elle se construit depuis GitHub, sans
Mac et sans compte Apple Developer.

1. Onglet **Actions** → **iOS — IPA non signé** → **Run workflow**.
2. La compilation prend un quart d'heure. Elle produit un IPA **non signé**,
   publié dans les *Releases* du dépôt.
3. Téléchargez l'IPA **depuis l'iPhone**, ouvrez-le dans **ESign**, et signez-le
   avec un certificat obtenu sur l'appareil.

**Un IPA non signé ne s'installe pas tel quel** : iOS vérifie la signature avant
d'exécuter une application, et refuse sans l'expliquer. La signature est faite
sur le téléphone, à l'installation.

Avec un identifiant Apple gratuit, l'application cesse de fonctionner au bout de
**sept jours** et doit être re-signée. Pour un usage réel par les familles, la
voie normale reste le magasin.

---

## Ce que fait la version 0.1.0, et ce qu'elle ne fait pas

**Elle fait :**

- choisir un niveau : GS, CP ou CE1 ;
- **lire** : 26 textes de lecture, affichés en grand sur un fond crème, chaque
  mot pouvant être touché ;
- **jouer** : le *mot à trous*, 42 mots dont une syllabe manque, avec des cartes
  à poser ;
- **s'entraîner** : 11 exercices du CE1, dont la consigne s'affiche et dont la
  réponse se donne en touchant une carte. Après une bonne réponse, la phrase du
  texte qui la prouve est montrée ;
- **parcourir** la progression du programme, étape par étape.

Pour relire l'écran « S'entraîner » sans installer l'application,
`contenu/planche-ecran-exercice.html` le montre dans ses six états, sur iPhone et
sur Android, avec les valeurs du thème et l'ordre des cartes **calculé par
`melange.ts`**. La planche s'ouvre hors ligne et ne dépend d'aucun fichier
extérieur.

**Elle ne fait pas encore :**

- **aucun son.** Rien n'est enregistré à ce jour, et l'application le dit à
  l'écran plutôt que de proposer un bouton muet. Les activités du projet qui
  reposent sur la voix ne sont donc pas jouables — c'est le manque principal de
  cette version. C'est aussi la raison pour laquelle **aucun exercice de la GS
  n'est rendu** : la règle du projet est que la consigne se donne par la voix, et
  un enfant de grande section ne lit pas encore une consigne écrite ;
- **81 exercices écrits et non rendus**, répartis sur **39 mécaniques** — 19 pour
  la GS, 20 pour le CE1. Ils ne sont pas cachés : l'écran du niveau les affiche,
  groupés par mécanique, avec leur nombre d'exercices et leur raison. Trois
  exercices déclarés jouables par la banque ne sont pas rendus non plus, et
  l'écran le dit aussi ;
- le CP n'a ni textes ni exercices : sa tranche n'est pas écrite. L'application
  affiche ce qui existe — ses 30 correspondances graphème-phonème — et rien de
  plus.

---

## Licence

Projet interne aux écoles Frères Lumières. Voir `contenu/LICENCE-IMAGES.md`.
