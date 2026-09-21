# Ludo'Lire — Règles de rédaction des textes de lecture

**Statut :** proposition à valider, applicable dès le premier texte.
**Dépend de :** `contenu/LUDOLIRE-CGP-CP.md` (la table des rangs) et `outils/verifier-textes.py` (le contrôle).
**Rappel du cadre officiel :** « Il ne donne à lire que des mots, des phrases puis des textes déchiffrables par l'élève, en fonction des CGP étudiées (l'usage des mots-outils doit être réduit au minimum). »

---

## 1. La règle unique

**Un texte au rang N ne contient que des graphèmes enseignés au rang N ou avant.**

Tout le reste en découle. Un texte qui emploie `ch` au rang 12 n'est pas « un peu trop difficile » : il est **indéchiffrable**, et l'enfant qui bute n'apprend rien — il devine. Un exercice dont on peut trouver la réponse sans lire est un exercice raté.

Trois exceptions, et trois seulement :

1. les **mots-outils mémorisés** de la liste fermée (§ 2) ;
2. les **lettres muettes** dont la règle est introduite (§ 3) ;
3. les **accents** sur voyelle, admis à partir du rang 6 (le phonème ne change pas).

## 2. Les mots-outils

Liste **fermée**, portée par `outils/cgp-cp.json`. Pour toute la tranche CP :

| Rang | Mot |
|---|---|
| 6 | `et` |
| 13 | `est` |
| 14 | `elle`, `elles` |

**On n'ajoute pas un mot-outil pour sauver une phrase.** Si un texte a besoin d'un cinquième mot-outil, c'est le texte qu'il faut réécrire. C'est la règle la plus souvent contournée, et c'est celle qui distingue un texte déchiffrable d'un texte qui a l'air déchiffrable.

Les mots-outils **réguliers et transparents** (`le`, `la`, `un`, `une`, `il`, `lui`, `lune`) ne sont pas des exceptions : ils sont déchiffrables, donc ils s'emploient librement dès que leurs graphèmes sont enseignés.

## 3. Les lettres muettes

Elles suivent le tableau du § 5 de la table des rangs. En pratique :

- `e` final muet : dès le rang 3 ;
- `s` final du pluriel : dès le rang 11 ;
- `t`, `d`, `x` finaux : dès le rang 12.

Une lettre muette qui n'a pas encore sa règle interdit le mot. C'est ce qui rend `loup` impossible avant l'introduction du `p` final muet — et le contrôle le signale, ce qui évite de le découvrir à la relecture.

Un cas voisin mérite d'être connu : **la nasale en fin de mot**. `son`, `bon`, `nom` se terminent par une voyelle nasale, pas par une voyelle suivie d'une consonne. Une première version du contrôle les segmentait `s | o | n` et les acceptait au rang 20, alors que la CGP `on` n'est enseignée qu'au rang 21 — elle **acceptait à tort**, ce qui est le sens d'erreur le plus dangereux : un texte refusé se voit, un texte accepté par erreur ne se voit pas. Le défaut est corrigé, et `outils/tests/controle-negatif-nasale.txt` le surveille.

## 4. Longueur et forme

| Rang | Forme attendue | Volume |
|---|---|---|
| 1 à 10 | mots isolés, puis une phrase courte | 3 à 5 mots par phrase |
| 11 à 20 | 2 à 4 phrases | 4 à 7 mots par phrase |
| 21 à 30 | 4 à 6 phrases, un début de récit | 5 à 9 mots par phrase |

Un texte de la tranche CP se lit **en une minute**, pas plus. La lecture est un exercice, pas une épreuve d'endurance.

## 5. Ce qu'un texte doit apporter

Un texte n'est pas un prétexte à graphèmes. Trois exigences, toutes tirées du guide :

1. **Il doit être compréhensible une fois déchiffré.** Le vocabulaire employé doit être connu de l'enfant à l'oral. Un texte déchiffrable mais incompréhensible n'entraîne rien.
2. **Il doit contenir au moins une phrase résistante.** Le guide le demande : « Au-delà de phrases simples, il faut donc proposer des phrases résistantes qui permettent d'exercer la compréhension immédiatement après le déchiffrage. Exemple : *Rassasié, le chat s'assoupit sur le tapis.* » Le déchiffrage et la compréhension s'exercent dans le même geste.
3. **Il ne doit pas être résoluble sans lire.** Pas d'image qui donne la réponse, pas de mot devinable par le contexte seul. L'illustration accompagne, elle ne répond pas.

## 6. Les prénoms et les noms propres

Ils sont soumis à la même règle. Un prénom contenant un graphème non enseigné est interdit — `Sophie` avant le rang 16, `Nathan` avant le rang 22.

C'est une contrainte réelle : à bas rang, le choix se réduit à des prénoms déchiffrables. `Lina`, `Lola`, `Nino`, `Rémi`, `Mila` fonctionnent tôt ; c'est pour cela qu'ils apparaissent dans les premiers textes, et c'est un critère de sélection, pas un hasard.

## 7. Les formes interdites dans la tranche

| Forme | Pourquoi | Ce que ça implique |
|---|---|---|
| Terminaison `-ent` (`ils dorment`, `dent`, `volent`) | morphème muet, ou nasale suivie d'un t muet — la segmentation la lit de travers dans les deux cas | **interdite dans toute la tranche** : le contrôle la refuse, à tout rang. Voir § 7.1 |
| `sens`, `ours`, `fils`, `mars`, `os` | lettre finale muette qui se prononce | hors contrôle automatique, à éviter |
| Digrammes nasaux détournés (`an` devant voyelle, `om` hors `m/p/b`) | le contrôle les traite par contexte | rien à faire, mais savoir que le contrôle les distingue |

### 7.1 La terminaison `-ent`, interdite

La terminaison `-ent` est **refusée dans toute la tranche CP, à tout rang**, et le refus est prononcé **avant** toute autre analyse : le contrôle s'arrête là pour le mot.

La raison est double, et c'est ce qui justifie une interdiction plutôt qu'un simple signalement :

- dans un **verbe** (`ils dorment`, `elles volent`), `-ent` n'est pas un `/e/` suivi d'un `/t/` : c'est un morphème muet, entièrement silencieux ;
- dans un **nom** (`dent`, `vent`), c'est une voyelle nasale suivie d'un `t` muet.

Dans les deux cas, la segmentation lit de travers, et l'enfant de CP n'a la règle ni dans un cas ni dans l'autre. Un mot refusé doit se **remplacer**, pas s'autoriser.

Une liste blanche existe dans le code (`MOTS_ENT_AUTORISES`), vide à dessein. Y ajouter un mot est une décision pédagogique, pas un ajustement technique — et aucun nom en `-ent` n'est déchiffrable avant le rang 30 de toute façon.

Le refus est **attribuable** : le contrôle ne rapporte que la terminaison, jamais un autre motif à sa place. C'est ce que vérifie `outils/tests/controle-negatif-ent.txt`.

## 8. Le processus

1. **Choisir le rang** d'implantation du texte.
2. **Écrire** en respectant les contraintes — c'est la partie difficile, et elle se fait en écrivant court.
3. **Contrôler** :

```bash
python outils/verifier-textes.py --rang 16 contenu/textes/T02-rang16.txt
python outils/verifier-textes.py --rang 16 --mots contenu/textes/T02-rang16.txt
```

4. **Corriger** jusqu'à `conforme`, sans jamais assouplir la règle. Un mot qui ne passe pas se remplace ; il ne s'autorise pas.
5. **Faire relire par le porteur du projet** — le contrôle ne juge ni le sens, ni l'intérêt, ni l'âge. La relecture se fait en éprouvant l'application, et non par un relecteur externe.

## 9. Où le contrôle s'arrête

Un contrôle qui ne dit pas ses limites fait plus de mal que de bien. Ce qu'il **ne** voit pas :

- **le sens** : un texte conforme peut être idiot, incohérent ou incompréhensible ;
- **le niveau de vocabulaire** : un mot déchiffrable peut être inconnu d'un enfant de 6 ans ;
- **les liaisons et la prosodie**, qui ne s'écrivent pas ;
- **les mots pièges** de la liste, signalés mais non tranchés ;
- **l'intérêt** du texte. C'est le seul point qui décide vraiment qu'un enfant revienne le lendemain, et aucun script ne le mesure.

## 10. Les textes produits à ce jour

Trois textes, à titre de preuve du mécanisme. Ils sont courts, et c'est normal : aux rangs bas, le vocabulaire disponible est minuscule — au rang 10, seuls quelques noms et le verbe `a` sont accessibles.

| Fichier | Rang | Contenu |
|---|---|---|
| `contenu/textes/T01-rang10.txt` | 10 | `La lune` — 4 phrases, 18 mots |
| `contenu/textes/T02-rang16.txt` | 16 | `Le cheval` — 4 phrases, 24 mots |
| `contenu/textes/T03-rang23.txt` | 23 | `Le mouton et le canard` — 3 phrases, 18 mots |

Le harnais `outils/tester-controle.py` les éprouve, et éprouve **trois contrôles négatifs** qui doivent être refusés : une CGP non enseignée, la terminaison `-ent`, et une nasale finale avant son rang. Chaque contrôle négatif porte un **motif attendu** dans la sortie : un refus n'est probant que si l'on sait sur quoi il porte, et un texte refusé pour une autre raison que celle qu'on veut éprouver ne prouve rien.
