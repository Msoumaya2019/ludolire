/**
 * Contrôle du contenu embarqué.
 *
 * CE QU'IL VÉRIFIE, ET POURQUOI CES CHOSES-LÀ
 * -------------------------------------------
 * `assets/contenu-app.json` est fabriqué par `outils/generer-contenu-app.py`.
 * Rien n'empêche de le modifier à la main — et c'est exactement le risque : une
 * correction faite ici disparaîtrait à la fabrication suivante, sans que
 * personne ne s'en aperçoive avant qu'un enfant ne voie l'ancienne version.
 *
 * Deux protections, et elles se complètent :
 *
 *   - L'EMPREINTE. Le générateur inscrit dans le contenu une empreinte de ce
 *     contenu, calculée sans elle. Si quelqu'un touche au fichier, l'empreinte
 *     ne correspond plus. C'est ce qui rend une retouche manuelle impossible à
 *     taire.
 *   - LA COHÉRENCE. Un contenu bien formé mais faux passe l'empreinte — une
 *     empreinte ne dit rien de la vérité, seulement de l'identité. On vérifie
 *     donc aussi ce que le contenu doit être : chaque item du jeu porte sa
 *     bonne réponse parmi ses cartes, aucune carte ne se répète, chaque texte
 *     a un titre et au moins une ligne, chaque niveau a un identifiant unique.
 *
 * CE QU'IL NE PEUT PAS VÉRIFIER
 * -----------------------------
 * Que le contenu soit FIDÈLE aux corpus. Cela demanderait de lire les corpus,
 * qui sont en JSON et en Python, et le contrôle tourne sur un exécuteur Node
 * sans Python. La fidélité est garantie par la fabrication, pas par ce
 * contrôle : c'est une limite, et elle est écrite ici plutôt que tue.
 *
 * Usage :
 *     node scripts/verifier-contenu.mjs
 */

import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ICI = dirname(fileURLToPath(import.meta.url));
export const CHEMIN = join(ICI, '..', 'assets', 'contenu-app.json');

/**
 * Le même calcul que le générateur : clés triées, séparateurs serrés, UTF-8.
 *
 * C'est une RÉ-IMPLÉMENTATION, et c'est assumé : elle doit donner le même
 * résultat que `json.dumps(..., sort_keys=True, separators=(",", ":"))` de
 * Python. Si les deux divergeaient, ce contrôle signalerait une faute qui
 * n'existe pas — c'est pourquoi `tests/contenu.test.mjs` compare les deux
 * valeurs sur le contenu réel, et pas seulement sur un cas fabriqué.
 */
function canonique(valeur) {
  if (valeur === null || typeof valeur !== 'object') {
    return JSON.stringify(valeur);
  }
  if (Array.isArray(valeur)) {
    return '[' + valeur.map(canonique).join(',') + ']';
  }
  const cles = Object.keys(valeur).sort();
  return '{' + cles.map((c) => JSON.stringify(c) + ':' + canonique(valeur[c])).join(',') + '}';
}

export function empreinteDe(contenu) {
  const nu = JSON.parse(JSON.stringify(contenu));
  delete nu.meta.empreinte;
  return createHash('sha256').update(canonique(nu), 'utf8').digest('hex').slice(0, 16);
}

export function controler(contenu) {
  const erreurs = [];
  const detail = {};

  if (!contenu || typeof contenu !== 'object') {
    return { erreurs: ['le contenu n\'est pas un objet'], detail };
  }
  if (!contenu.meta || typeof contenu.meta !== 'object') {
    erreurs.push('meta manquant');
    return { erreurs, detail };
  }
  if (!Array.isArray(contenu.niveaux) || contenu.niveaux.length === 0) {
    erreurs.push('aucun niveau');
    return { erreurs, detail };
  }

  // --- L'empreinte -------------------------------------------------------
  const attendue = contenu.meta.empreinte;
  if (typeof attendue !== 'string' || attendue.length === 0) {
    erreurs.push("meta.empreinte est absente : rien ne dit de quelle fabrication vient ce fichier");
  } else {
    const calculee = empreinteDe(contenu);
    if (calculee !== attendue) {
      erreurs.push(
        `empreinte : le contenu déclare ${attendue} et vaut ${calculee} — ` +
          'le fichier a été retouché à la main, ou fabriqué avant une modification des corpus'
      );
    }
    detail.empreinte = attendue;
  }

  // --- Les niveaux -------------------------------------------------------
  const ids = new Set();
  let textes = 0;
  let items = 0;
  let unites = 0;
  let correspondances = 0;

  for (const n of contenu.niveaux) {
    const ou = `niveau ${n?.id ?? '?'}`;
    if (typeof n?.id !== 'string' || n.id.length === 0) {
      erreurs.push(`${ou} : identifiant manquant`);
      continue;
    }
    if (ids.has(n.id)) {
      erreurs.push(`${ou} : identifiant en double`);
    }
    ids.add(n.id);
    for (const champ of ['nom', 'court', 'sous_titre', 'couleur']) {
      if (typeof n[champ] !== 'string' || n[champ].length === 0) {
        erreurs.push(`${ou} : champ « ${champ} » manquant ou vide`);
      }
    }
    for (const champ of ['textes', 'jeu_syllabes', 'unites', 'correspondances']) {
      if (!Array.isArray(n[champ])) {
        erreurs.push(`${ou} : champ « ${champ} » n'est pas une liste`);
      }
    }

    // --- Les textes ------------------------------------------------------
    for (const t of n.textes ?? []) {
      textes += 1;
      if (typeof t.titre !== 'string' || t.titre.length === 0) {
        erreurs.push(`${ou} : un texte sans titre (${t.id})`);
      }
      if (!Array.isArray(t.lignes) || t.lignes.length === 0) {
        erreurs.push(`${ou} : le texte « ${t.id} » n'a aucune ligne`);
      }
      for (const ligne of t.lignes ?? []) {
        if (typeof ligne !== 'string' || ligne.trim().length === 0) {
          erreurs.push(`${ou} : le texte « ${t.id} » porte une ligne vide`);
        }
      }
    }

    // --- Le jeu des syllabes ---------------------------------------------
    const vus = new Set();
    for (const it of n.jeu_syllabes ?? []) {
      items += 1;
      if (vus.has(it.id)) {
        erreurs.push(`${ou} : item « ${it.id} » en double`);
      }
      vus.add(it.id);

      const ouItem = `${ou} item ${it.id}`;
      if (!Array.isArray(it.syllabes) || it.syllabes.length < 2) {
        erreurs.push(`${ouItem} : moins de deux syllabes — il n'y a pas de mot à trous`);
        continue;
      }
      if (typeof it.trou !== 'number' || it.trou < 0 || it.trou >= it.syllabes.length) {
        erreurs.push(`${ouItem} : le trou ${it.trou} est hors de la découpe`);
        continue;
      }
      if (it.syllabes.join('') !== it.mot) {
        erreurs.push(
          `${ouItem} : la découpe « ${it.syllabes.join('-')} » ne recompose pas « ${it.mot} »`
        );
      }
      if (!Array.isArray(it.cartes) || it.cartes.length < 2) {
        erreurs.push(`${ouItem} : moins de deux cartes — le jeu n'a pas de choix`);
        continue;
      }
      const bonne = it.syllabes[it.trou];
      if (!it.cartes.includes(bonne)) {
        erreurs.push(
          `${ouItem} : la bonne syllabe « ${bonne} » n'est pas parmi les cartes ` +
            `[${it.cartes.join(', ')}] — l'item est injouable`
        );
      }
      if (new Set(it.cartes).size !== it.cartes.length) {
        erreurs.push(`${ouItem} : deux cartes identiques dans [${it.cartes.join(', ')}]`);
      }
      // IL N'Y A PAS DE CONTRÔLE « une intruse qui recomposerait le mot ».
      //
      // Ce contrôle a existé, puis a été retiré : il ne pouvait pas se
      // déclencher. La découpe recompose déjà le mot (`syllabes.join('') === mot`),
      // donc remplacer la syllabe du trou par une autre chaîne donne forcément
      // une autre chaîne — la seule carte qui recompose le mot est la bonne.
      // Un contrôle inatteignable fait paraître le contrôle plus fort qu'il
      // n'est ; c'est pire que de ne pas l'avoir.
      //
      // La propriété qu'il visait — une seule façon de gagner — est garantie par
      // les deux contrôles ci-dessus : la bonne carte est là, et aucune carte ne
      // se répète. `tests/contenu.test.mjs` l'éprouve sur le contenu réel.
      //
      // Ce qui n'est PAS vérifié ici, et qui reste un risque réel : qu'une
      // intruse forme un AUTRE mot de l'application. « banane » privé de « na »
      // et complété par une intruse ne doit pas donner un mot connu, sans quoi
      // l'enfant hésite entre deux mots au lieu de discriminer deux syllabes.
      // Ce contrôle demande le lexique de l'application, qui vit dans
      // `outils/` et n'est pas embarqué : il appartient au contrôle du corpus,
      // qui l'a.
    }

    // --- Les unités et les correspondances -------------------------------
    const rangs = new Set();
    for (const u of n.unites ?? []) {
      unites += 1;
      if (rangs.has(u.rang)) {
        erreurs.push(`${ou} : deux unités portent le rang ${u.rang}`);
      }
      rangs.add(u.rang);
      if (typeof u.objectif !== 'string' || u.objectif.length === 0) {
        erreurs.push(`${ou} : l'unité ${u.rang} n'a pas d'objectif`);
      }
    }
    for (const c of n.correspondances ?? []) {
      correspondances += 1;
      if (!Array.isArray(c.graphies) || c.graphies.length === 0) {
        erreurs.push(`${ou} : la correspondance ${c.rang} n'a aucune graphie`);
      }
      if (typeof c.phoneme !== 'string' || c.phoneme.length === 0) {
        erreurs.push(`${ou} : la correspondance ${c.rang} n'a pas de phonème`);
      }
    }
  }

  detail.niveaux = contenu.niveaux.length;
  detail.textes = textes;
  detail.items = items;
  detail.unites = unites;
  detail.correspondances = correspondances;
  return { erreurs, detail };
}

export function lire() {
  return JSON.parse(readFileSync(CHEMIN, 'utf8'));
}

const estLance = process.argv[1] && import.meta.url === new URL(`file://${process.argv[1]}`).href;

if (estLance || process.argv[1]?.endsWith('verifier-contenu.mjs')) {
  const { erreurs, detail } = controler(lire());
  console.log("Le contenu embarqué dans l'application");
  for (const [cle, valeur] of Object.entries(detail)) {
    console.log(`  ${cle.padEnd(18)} ${valeur}`);
  }
  if (erreurs.length > 0) {
    console.log(`\nNON CONFORME — ${erreurs.length} problème(s) :`);
    for (const e of erreurs) console.log(`  ${e}`);
    process.exit(1);
  }
  console.log('\nRésultat : conforme');
}
