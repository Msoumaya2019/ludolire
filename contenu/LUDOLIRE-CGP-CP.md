# Ludo'Lire — Table de progression des CGP, tranche CP

**Statut :** proposition à valider. L'ordre est **notre choix**, dans un cadre officiel qui, lui, est vérifié.
**Source du cadre :** BO n° 41 du 31 octobre 2024, programme de français du cycle 2 (arrêté du 22 octobre 2024, application rentrée 2025-2026) ; guide Eduscol *Pour enseigner la lecture et l'écriture au CP*.
**Source de vérité de la table :** `outils/cgp-cp.json`. Le tableau ci-dessous en est le rendu, produit par `outils/generer-table.py`. Modifier le JSON, relancer la commande.

---

## 1. Ce qui vient du texte officiel, et ce qui vient de nous

Trois choses sont **imposées** :

- la **cadence** : « Il enseigne les CGP dès le début du CP selon une cadence soutenue : environ deux correspondances par semaine » ;
- les **paliers** : « En fin de période 1 : décoder et encoder 12 à 15 correspondances graphophonémiques (CGP) régulières, fréquentes et aisément prononçables » ; « En milieu d'année : décoder et encoder de 25 à 30 CGP » ;
- la **contrainte de lisibilité** : « Il ne donne à lire que des mots, des phrases puis des textes déchiffrables par l'élève, en fonction des CGP étudiées (l'usage des mots-outils doit être réduit au minimum). »

Une seule chose est **laissée au choix** : l'ordre. Le guide le dit explicitement — « La plupart des manuels syllabiques s'appuient sur ce type de progression avec des variantes concernant l'ordre d'étude. »

Nous nous donnons donc l'ordre, mais nous nous donnons aussi les critères, pour qu'il soit contestable.

## 2. Les huit paramètres d'ordonnancement

Recopiés du guide Eduscol, qui les énumère sous le titre « Paramètres pris en compte » :

1. la régularité des relations graphèmes-phonèmes ;
2. la fréquence des graphèmes et des phonèmes ;
3. la facilité de prononciation des consonnes isolées ;
4. la complexité de la structure syllabique ;
5. l'inséparabilité des graphèmes complexes ;
6. les lettres muettes ;
7. la fréquence des mots dans la langue française ;
8. le rôle des morphèmes.

Le guide ajoute la direction générale : « Globalement, elle va du plus simple au plus complexe, en prenant en compte la fréquence des graphèmes et des phonèmes en vue d'une lecture autonome. »

Ces huit paramètres expliquent trois choix qui surprennent au premier regard :

- **les consonnes continues avant les occlusives** (`l, m, r, n, s, v, f` avant `p, t, d, b`) — paramètre 3. Une consonne continue se tient, donc s'entend, donc se fusionne avec la voyelle. Une occlusive ne se tient pas.
- **les digrammes insécables traités comme des blocs** (`ou`, `oi`, `on`, `an`) — paramètre 5. On n'apprend pas `o` puis `u` pour lire `ou`.
- **`e` enseigné tôt malgré son instabilité** — paramètre 2. C'est la lettre la plus fréquente du français ; l'attendre coûterait plus cher que de l'enseigner avec vigilance.

## 3. La table

<!-- DEBUT TABLE GENEREE -->

| Rang | Semaine | CGP | Phonème | Graphies | Pourquoi ici |
|---|---|---|---|---|---|
| 1 | 1 | `a` | /a/ | `a` | régulier, très fréquent, prononçable |
| 2 | 1 | `i` | /i/ | `i` | régulier, très fréquent |
| 3 | 2 | `o` | /o/ | `o` | régulier, fréquent |
| 4 | 2 | `u` | /y/ | `u` | régulier, fréquent |
| 5 | 3 | `e` | /ə/ | `e` | fréquent — valeur instable, à enseigner tôt mais avec vigilance |
| 6 | 3 | `e-aigu` | /e/ | `é` | régulier, fréquent |
| 7 | 4 | `l` | /l/ | `l` | consonne continue, aisément prononçable isolément |
| 8 | 4 | `m` | /m/ | `m` | consonne continue, très fréquente |
| 9 | 5 | `r` | /ʁ/ | `r` | consonne continue, très fréquente |
| 10 | 5 | `n` | /n/ | `n` | consonne continue, fréquente |
| 11 | 6 | `s-sourd` | /s/ | `s` | consonne continue — valeur à surveiller entre deux voyelles |
| 12 | 6 | `v` | /v/ | `v` | consonne continue |
| 13 | 7 | `p` | /p/ | `p` | occlusive, fréquente — arrive après les continues |
| 14 | 7 | `t` | /t/ | `t` | occlusive, très fréquente |
| 15 | 8 | `f` | /f/ | `f` | consonne continue |
| 16 | 8 | `ch` | /ʃ/ | `ch` | graphème insécable, très fréquent |
| 17 | 9 | `d` | /d/ | `d` | occlusive, fréquente |
| 18 | 9 | `b` | /b/ | `b` | occlusive, fréquente |
| 19 | 10 | `ou` | /u/ | `ou` | graphème insécable, très fréquent — ouvre un grand nombre de mots |
| 20 | 10 | `oi` | /wa/ | `oi` | graphème insécable, fréquent |
| 21 | 11 | `on` | /ɔ̃/ | `on`, `om` | voyelle nasale — om devant m, b, p |
| 22 | 11 | `an` | /ɑ̃/ | `an`, `am` | voyelle nasale — am devant m, b, p |
| 23 | 12 | `c-dur` | /k/ | `c`, `qu` | valeur régulière devant a, o, u — qu pour la même valeur |
| 24 | 12 | `g-dur` | /g/ | `g`, `gu` | valeur régulière devant a, o, u — gu pour la même valeur |
| 25 | 13 | `j` | /ʒ/ | `j`, `ge` | ge devant a, o, u |
| 26 | 13 | `s-sonore` | /z/ | `s`, `z` | s entre deux voyelles |
| 27 | 14 | `in` | /ɛ̃/ | `in`, `im` | voyelle nasale — im devant m, b, p |
| 28 | 14 | `ain` | /ɛ̃/ | `ain`, `ein` | même phonème, autre graphie — la proximité avec in est le point de vigilance |
| 29 | 15 | `eu` | /ø/ | `eu`, `œu` | fréquent |
| 30 | 15 | `au` | /o/ | `au`, `eau` | fréquent — même phonème que o, déjà connu |

<!-- FIN TABLE GENEREE -->

## 4. L'alignement sur les paliers

| Repère officiel | Ce que la table donne | Écart |
|---|---|---|
| 12 à 15 CGP en fin de période 1 | 14 unités au rang 14 (semaine 7) | conforme |
| 25 à 30 CGP au milieu de l'année | 30 unités au rang 30 (semaine 15) | conforme |

**La tranche CP de la v1 s'arrête au rang 30.** Ce n'est pas un choix de confort : c'est le palier officiel de milieu d'année, et il a l'avantage d'être un objectif atteignable et vérifiable. Une tranche qui s'arrêterait à la semaine 15 parce que « c'est la moitié de l'année » serait arbitraire ; une tranche qui s'arrête à 30 CGP est adossée à un texte.

La semaine est une **indication de rythme**, pas une frontière. Le guide prévient que « le rythme d'acquisition des graphèmes sera différent au début de l'apprentissage, en cours d'apprentissage et en fin d'apprentissage », et que le calendrier des vacances module le nombre de semaines par période. **Ce qui borne la tranche est le compte des CGP, pas un numéro de semaine.**

## 5. Les brins parallèles

Trois apprentissages ne sont pas des CGP et progressent en parallèle. Ils sont déclarés dans le JSON, et le contrôle des textes les applique.

| Brin | Rang d'introduction | Règle |
|---|---|---|
| Muettes | 3 | le `e` final ne se prononce pas |
| Muettes | 11 | le `s` final marque le pluriel et ne se prononce pas |
| Muettes | 12 | `t`, `d` et `x` finaux muets |
| Accents | 3 | `é` est une CGP à part entière |
| Accents | 6 | accents grave et circonflexe sur les voyelles, sans changement de phonème |
| Doubles | 6 | `ss` entre deux voyelles vaut /s/ |
| Doubles | 14 | `ll` |

Le programme demande une présentation « progressive et structurée » des lettres muettes. C'est ce que fait ce tableau : une règle à la fois, à un rang daté.

## 6. Les mots-outils mémorisés

Le programme exige que « l'usage des mots-outils soit réduit au minimum », tout en prévoyant de « mémoriser les mots fréquents et réguliers ». La liste est donc **fermée**, et chaque entrée porte son rang.

| Rang | Mot | Raison |
|---|---|---|
| 6 | `et` | se lit /e/, irrégulier |
| 13 | `est` | se lit /ɛ/, irrégulier |
| 14 | `elle`, `elles` | contient `ll` |

**Quatre mots pour toute la tranche.** Tout le reste d'un texte doit être déchiffrable avec les CGP du rang — c'est la contrainte la plus dure du projet, et c'est elle qui rend les textes difficiles à écrire, pas l'inverse.

## 7. Ce qui est hors tranche

| Niveau | Contenu | Pourquoi |
|---|---|---|
| Fin du CP | `ai`, `ei`, `gn`, `ph`, `ill`, `un`, `tion`, lettres muettes lexicales, mots irréguliers fréquents | au-delà du rang 30 |
| CE1 | automatisation des CGP du CP, sons proches en encodage et décodage, fluence | tranche suivante |
| CE2 à CM2 | paliers 90, 110 et 120 mots par minute | hors périmètre v1 |

Ces éléments sont déclarés dans le JSON pour que la structure de contenu les accueille sans réécriture (§ 8 de la note de cadrage).

## 8. Comment on vérifie

```bash
python outils/generer-table.py                              # met la table à jour depuis le JSON
python outils/tester-controle.py                            # textes conformes + contrôle négatif
python outils/verifier-textes.py --rang 16 contenu/textes/T02-rang16.txt
python outils/verifier-textes.py --rang 10 --mots contenu/textes/T01-rang10.txt   # segmentation
```

## 9. Ce que cette table ne règle pas

- **L'ordre n'est pas validé en classe.** Il est cohérent avec les huit paramètres, il n'est pas certifié. La relecture pédagogique revient au porteur du projet, qui la fait en éprouvant l'application ; ce qui manque encore, c'est cette relecture, pas la cohérence.
- **Le compte des CGP dépend d'une convention** (§ 1 : une unité = un phonème et ses graphies). Le programme ne dit pas comment il compte ; nous comptons les unités d'enseignement, ce qui est la lecture la plus utile pour un logiciel.
- **Les textes ne sont pas encore écrits en nombre.** Trois existent, à titre de preuve du mécanisme.
