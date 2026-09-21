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
outils/                 les corpus (JSON) et les contrôles (Python)
  *.json                  les corpus : mots, progressions, exercices, images
  verifier-*.py           les contrôles
  tester-*.py             les bancs de falsification des contrôles
  generer-contenu-app.py  fabrique le contenu embarqué dans l'application
scripts/                les contrôles qui tournent sous Node, donc en intégration
tests/                  les bancs de ces contrôles
```

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

Cette commande enchaîne quatre contrôles :

| Contrôle | Ce qu'il vérifie |
| --- | --- |
| `check:workflows` | que les flux de travail GitHub sont bien formés, avant de les pousser |
| `contenu:verifier` | que le contenu embarqué est cohérent et que son empreinte correspond |
| `typecheck` | que le TypeScript compile |
| `test` | les deux bancs — 40 cas : le contrôle du contenu (23, dont 20 falsifications) et le contrôle des flux (17, dont 11 mutations) |

Le lanceur est appelé avec un **motif explicite** — `node --test
"tests/*.test.mjs"` — et non sans argument. Sans argument, Node découvre les
tests par convention, et cette convention descend dans `node_modules` : mesuré
sur ce dépôt, elle ramassait 76 fichiers `.js` rangés sous un dossier `test/`
d'appartenance à des paquets, plus un fichier de test d'un paquet. Le banc
passait de 40 à 277 cas, dont 201 en échec — tous imputables à des paquets
tiers. **Un contrôle qui ramasse ce qu'il n'a pas désigné ne dit rien de ce
qu'on lui demande de garder.**

Côté corpus, les contrôles du projet sont en Python :

```bash
python outils/verifier-exercices.py
python outils/verifier-textes-ce1.py --tous
python outils/verifier-pseudo-mots.py
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
- **parcourir** la progression du programme, étape par étape.

**Elle ne fait pas encore :**

- **aucun son.** Rien n'est enregistré à ce jour, et l'application le dit à
  l'écran plutôt que de proposer un bouton muet. Les activités du projet qui
  reposent sur la voix ne sont donc pas jouables — c'est le manque principal de
  cette version ;
- le CP n'a ni textes ni exercices : sa tranche n'est pas écrite. L'application
  affiche ce qui existe — ses 30 correspondances graphème-phonème — et rien de
  plus ;
- les 107 exercices des banques GS et CE1 ne sont pas encore rendus dans
  l'application. Le jeu du mot à trous est le premier.

---

## Licence

Projet interne aux écoles Frères Lumières. Voir `contenu/LICENCE-IMAGES.md`.
