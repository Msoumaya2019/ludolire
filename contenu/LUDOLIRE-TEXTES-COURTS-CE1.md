# Ludo'Lire — Les textes courts du CE1

**Statut :** proposition à valider. Les textes sont écrits et contrôlés ; leur intérêt pédagogique se jugera en éprouvant l'application.
**Dépend de :** `contenu/LUDOLIRE-TEXTES-CE1.md` (les textes du palier, dont ce corpus se distingue), `outils/cgp-ce1.json` (les correspondances), `outils/verifier-textes-courts-ce1.py` (le contrôle).

---

## 1. Pourquoi un corpus à part

Un texte du palier et un texte court ne sont pas le même objet.

Le texte du palier est **la donnée d'un rang** : il fait de six à seize lignes de 34 signes, il est lu seul, il porte l'objectif de lecture de son unité, et sa longueur suit une montée qui ne redescend pas. Le texte court fait de **deux à six lignes** : il n'est pas lu seul, il est **cité par un exercice**, et il sert à comparer — deux textes dont l'un raconte et l'autre explique (unité 16), trois textes dont l'un ressemble à celui qu'on vient de lire (unité 41).

Tant qu'ils étaient portés par l'exercice, ces textes n'existaient que dans le corps d'un JSON. Rien ne les voyait : ni le rang, ni le titre, ni le type. Le travail a mesuré ce que cela coûtait :

- **cinq phrases des textes courts étaient déjà des lignes d'un texte du palier** — « La reine a un chat brun. » se lit dans `T08`, `T09` et `T18`, « Le chat monte sur une échelle. » dans `T18`, « Le téléphone est dans la maison. » dans `T07` ;
- **deux exercices portaient le même texte**, chacun de son côté : `E32` et `E33` avaient quatre phrases identiques ;
- **`E21` et `E55` partageaient trois phrases**, dont deux d'un même texte sur le vent ;
- **cinq titres entraient en collision** avec ceux des textes du palier — deux « Le vent », et deux « Le chat » sous des formes voisines.

Aucun de ces défauts n'était visible dans le code : les textes étaient conformes mot à mot, et le contrôle des exercices vérifiait leur lisibilité. Ce qui manquait était un **lieu** où les voir ensemble.

## 2. Le rang, le type, le titre

Un texte court déclare trois choses dans son en-tête, et chacune sert :

| Ce qu'il déclare | À quoi ça sert |
|---|---|
| `# rang: N` | la lisibilité se contrôle à ce rang — la règle du palier vaut aussi ici |
| `# type: ...` | le type est **comparé** à la réponse de l'exercice |
| `# titre: ...` | le titre est ce que l'enfant touche, et ce que la clé de réponse nomme |

**Le type est ce qui rend la clé de réponse vérifiable.** Une question qui demande « le texte qui raconte une histoire » et dont la bonne réponse est un texte déclaré `informatif` apprend l'inverse de ce qu'elle annonce — et aucun contrôle ne pouvait le voir, puisque le type n'était écrit nulle part. Le contrôle lit maintenant la **direction** dans la question (« raconte » ou « explique ») et refuse une clé qui ne va pas dans ce sens. Quand la question ne dit ni l'un ni l'autre, il **ne conclut pas** et le déclare au lieu de laisser croire qu'il a vérifié.

La liste des types est **fermée** : `recit`, `informatif`, `prescriptif`.

## 3. Les textes courts

<!-- DEBUT TABLE GENEREE -->

### Les 5 textes courts

| Texte | Rang | Type | Titre | Lignes de 34 signes | Cité par |
|---|---|---|---|---|---|
| `C01-rang16.txt` | 16 | recit | L'agneau de la reine | 5 | `E21` |
| `C02-rang16.txt` | 16 | informatif | L'air qui va | 5 | `E21`, `E55` |
| `C03-rang27.txt` | 27 | informatif | Les chats | 4 | `E32`, `E33` |
| `C04-rang41.txt` | 41 | recit | Une échelle, une pomme | 4 | `E55` |
| `C05-rang41.txt` | 41 | recit | Le téléphone de papa | 4 | `E55` |

### Ce que disent les 5 textes courts

| Texte | Titre | Le texte |
|---|---|---|
| `C01-rang16.txt` | L'agneau de la reine | La reine a un agneau. / L'agneau aime la montagne. / Un lundi, il a rejoint la maison. / La reine rit. / La reine aime son agneau. |
| `C02-rang16.txt` | L'air qui va | Le vent est de l'air qui va. / Quand le vent est fort, il emporte la craie. / Sans le vent, les bateaux ne vont pas. |
| `C03-rang27.txt` | Les chats | Les chats aiment la maison. / Ils dorment le jour. / Ils mangent le soir. / La reine les aime. |
| `C04-rang41.txt` | Une échelle, une pomme | Le chat a vu une pomme. / Il a grimpé sur une échelle. / La reine a ri. / Ils ont mangé la pomme. |
| `C05-rang41.txt` | Le téléphone de papa | Papa a un téléphone. / Il le pose sur la table. / Papa a une question. / Maman a une réponse. |

<!-- FIN TABLE GENEREE -->

## 4. Ce que le contrôle refuse

- un texte illisible au rang qu'il déclare ;
- une longueur hors de deux à six lignes de 34 signes ;
- un type inconnu, ou absent ;
- un titre égal à celui d'un texte du palier, ou qui le **contient** ;
- une phrase qui est déjà une ligne d'un texte du palier ;
- deux textes courts qui partagent une phrase ;
- un texte court que **aucun** exercice ne cite — un texte écrit pour rien ;
- une citation qui ne résout pas, ou qui nomme un texte d'un rang au-delà de l'unité.

Le contrôle du corpus est éprouvé par `outils/tester-textes-courts-ce1.py` — **15 corpus faux et 1 témoin, 16 essais, tous vus** —, et les contrôles de la banque par `outils/tester-exercices-ce1.py` — **10 banques fausses et 1 témoin, 11 essais, tous vus**.

## 5. Ce que le contrôle ne voit pas

- **Le type déclaré est-il le bon ?** Le contrôle lit le type, il ne juge pas le texte. Un récit déclaré `informatif` passerait tous les contrôles et tromperait l'exercice. C'est la vérification qui reste à l'œil.
- **L'intérêt du texte.** Un texte court conforme peut être plat.
- **La plausibilité d'un intrus.** Le contrôle ne voit que la forme : non vide, distinct de la bonne réponse et — pour une question de type — d'un type différent.

## 6. Le besoin B16, et ce qu'il demandait vraiment

Le besoin B16 déclarait « aucun texte informatif n'est lisible avant le rang 32 », et son détail ajoutait que `E21` portait donc deux textes courts, « qu'il porte lui-même : ils sont contrôlés mot à mot, mais ils ne sont pas des textes qu'on peut relire seul ».

**Le détail était la bonne formulation, et il disait plus que le manque.** Le problème n'était pas l'absence d'un texte informatif — il y en avait un, écrit dans `E21` — mais le fait qu'il n'existait **nulle part ailleurs que dans cet exercice**.

Le besoin est donc soldé par le corpus : un texte informatif est désormais lisible au rang 16 (`C02`), et les textes courts sont des textes qu'on cite et qu'on contrôle. Le documentaire **long** reste au rang 33 (`T17`, « Le chat »), et c'est sa place : l'unité 16 demande deux textes **courts**, parce qu'elle demande de les comparer.

## 7. Ce qui reste

- **La relecture des textes courts, un par un** — ils sont conformes au brief et contrôlés par script, mais aucun script ne juge si un texte se comprend, ni si son type déclaré est le bon.
- L'enregistrement des textes et des consignes (B01a). Les pseudo-mots ont leur corpus et leur spécification d'enregistrement depuis le même jour — B35 est soldé —, et ce qui reste est la prise de son.
