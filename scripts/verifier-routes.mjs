/**
 * Contrôle des routes de l'application.
 *
 * POURQUOI CE FICHIER EXISTE
 * --------------------------
 * `app.json` déclare `experiments.typedRoutes: true`. On attendrait de cette
 * option qu'elle fasse refuser par `tsc` un `router.push` vers un écran qui
 * n'existe pas. **Elle ne le fait pas dans notre chaîne de vérification**, et
 * c'est mesuré : les types de routes sont écrits dans `.expo/types/`, que
 * `expo prebuild` et `expo start` engendrent — or `npm run typecheck` tourne
 * **avant** `expo prebuild`, dans le flux comme en local. Le dossier n'existe
 * donc jamais au moment du contrôle, et `Href` retombe sur un type permissif.
 *
 * Mesuré : `.expo/types/` absent, `expo-env.d.ts` absent, et `tsc` vert. Une
 * faute de frappe dans un `pathname` — « /lectur » au lieu de « /lecture » —
 * passerait le typage et n'apparaîtrait qu'à l'exécution, sur l'écran de
 * l'enfant, par un écran vide.
 *
 * Ce contrôle-ci ne dépend d'aucune génération : il lit `app/` sur le disque.
 * Il rend donc le service qu'on croyait rendu.
 *
 * TROIS DÉFAUTS, TOUS SILENCIEUX À L'EXÉCUTION
 * -------------------------------------------
 *   1. UNE CIBLE DE NAVIGATION QUI N'EXISTE PAS. L'application compile, et
 *      l'écran s'ouvre vide.
 *   2. UN ÉCRAN DÉCLARÉ DANS `_layout.tsx` QUI N'EXISTE PAS. expo-router
 *      **ignore** une déclaration orpheline sans rien dire : la pile est
 *      simplement amputée de la personnalisation prévue.
 *   3. UNE ROUTE QUI N'EST PAS DÉCLARÉE. expo-router la découvre quand même,
 *      mais lui donne le titre par défaut, c'est-à-dire **le nom du fichier**.
 *      L'en-tête de l'écran affiche alors « lecture » ou « niveau » — un nom de
 *      fichier, sous les yeux d'un enfant ou d'un parent.
 *
 * Le troisième est le plus coûteux : il ne casse rien, il enlaidit tout.
 *
 * Usage :
 *     node scripts/verifier-routes.mjs
 */

import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..');
const APP = join(RACINE, 'app');

/**
 * Le fichier de mise en page n'est pas une route : il décrit la pile. Il est le
 * seul à ne pas devoir figurer dans sa propre liste d'écrans déclarés.
 */
const MISE_EN_PAGE = '_layout.tsx';

let verifications = 0;
const defauts = [];

function defaut(marqueur, message) {
  defauts.push(`${marqueur} ${message}`);
}

/** Les fichiers `.tsx` de `app/`, hors mise en page. */
function fichiers(dossier) {
  return readdirSync(dossier)
    .filter((n) => n.endsWith('.tsx') && n !== MISE_EN_PAGE)
    .sort();
}

/** Les noms de routes : le nom du fichier sans son extension. */
function routes(dossier) {
  return fichiers(dossier).map((n) => n.replace(/\.tsx$/, ''));
}

/**
 * Les sous-dossiers de `app/`.
 *
 * Une route peut vivre dans un dossier — `app/niveau/index.tsx` répond à
 * `/niveau`. Sans cette liste, le contrôle refuserait une cible parfaitement
 * valide, et un contrôle qui crie au loup ne sert à rien.
 */
function dossiers(dossier) {
  return readdirSync(dossier)
    .filter((n) => statSync(join(dossier, n)).isDirectory())
    .sort();
}

/** Les écrans déclarés dans la mise en page, dans l'ordre du fichier. */
function ecransDeclares(texte) {
  return [...texte.matchAll(/<Stack\.Screen\s+name=["']([^"']+)["']/g)].map((m) => m[1]);
}

/** Les cibles de navigation, fichier par fichier. */
function ciblesDeNavigation(dossier) {
  const trouvees = [];
  for (const nom of readdirSync(dossier)) {
    if (!nom.endsWith('.tsx')) continue;
    const texte = readFileSync(join(dossier, nom), 'utf8');
    for (const m of texte.matchAll(/pathname:\s*['"]([^'"]+)['"]/g)) {
      trouvees.push({ fichier: nom, cible: m[1] });
    }
  }
  return trouvees;
}

export function main(dossier = APP, { silencieux = false } = {}) {
  // Les deux compteurs sont remis à zéro : le banc appelle `main` plusieurs
  // fois dans le même processus, et sans cela les défauts d'un cas
  // s'ajouteraient à ceux du suivant.
  verifications = 0;
  defauts.length = 0;

  if (!existsSync(dossier)) {
    defaut('[dossier-app-absent]', `${dossier} est introuvable`);
    if (!silencieux) console.error(defauts.join('\n'));
    return 1;
  }

  const noms = routes(dossier);
  const repertoires = dossiers(dossier);
  const connus = new Set([...noms, ...repertoires]);

  verifications += 1;
  if (noms.length === 0) {
    defaut('[aucune-route]', `${dossier} ne contient aucun fichier de route`);
  }

  // --- 1. La mise en page, et les deux sens de la déclaration --------------
  const cheminMiseEnPage = join(dossier, MISE_EN_PAGE);
  verifications += 1;
  if (!existsSync(cheminMiseEnPage)) {
    defaut(
      '[mise-en-page-absente]',
      `${MISE_EN_PAGE} est absent : aucune pile de navigation n'est décrite`
    );
  } else {
    const texte = readFileSync(cheminMiseEnPage, 'utf8');
    const declarees = ecransDeclares(texte);

    // 1a. Un écran déclaré qui n'existe pas : expo-router l'ignore en silence.
    for (const declaree of declarees) {
      verifications += 1;
      if (!noms.includes(declaree)) {
        defaut(
          '[ecran-inconnu]',
          `${MISE_EN_PAGE} déclare « ${declaree} », qu'aucun fichier ne porte — ` +
            'expo-router ignore une déclaration orpheline sans le dire'
        );
      }
    }

    // 1b. Une route non déclarée : elle s'affiche, mais sous son nom de fichier.
    for (const nom of noms) {
      verifications += 1;
      if (!declarees.includes(nom)) {
        defaut(
          '[route-non-declaree]',
          `${nom}.tsx n'est pas déclarée dans ${MISE_EN_PAGE} : l'en-tête de cet ` +
            `écran affichera « ${nom} », un nom de fichier`
        );
      }
    }

    // 1c. Un écran déclaré deux fois : la seconde ne sert à rien.
    const vues = new Set();
    for (const declaree of declarees) {
      verifications += 1;
      if (vues.has(declaree)) {
        defaut('[ecran-en-double]', `${MISE_EN_PAGE} déclare « ${declaree} » deux fois`);
      }
      vues.add(declaree);
    }
  }

  // --- 2. Les cibles de navigation ----------------------------------------
  for (const { fichier, cible } of ciblesDeNavigation(dossier)) {
    verifications += 1;
    const segment = cible.replace(/^\//, '').split('/')[0] ?? '';
    if (!connus.has(segment)) {
      defaut(
        '[cible-inconnue]',
        `${fichier} navigue vers « ${cible} », et aucune route « ${segment} » n'existe`
      );
    }
  }

  // --- Le rapport ----------------------------------------------------------
  const dire = silencieux ? () => {} : (l) => console.log(l);

  dire('Contrôle des routes de l’application');
  dire(`  routes                ${noms.length} (${noms.join(', ')})`);
  dire(`  vérifications         ${verifications}`);

  if (defauts.length > 0) {
    dire(`\nNON CONFORME — ${defauts.length} défaut(s) :`);
    for (const d of defauts) dire(`  ${d}`);
    return 1;
  }
  dire('\nRésultat : conforme');
  return 0;
}

export function defautsDe(dossier) {
  main(dossier, { silencieux: true });
  return [...defauts];
}

export { APP };

// Le contrôle ne s'exécute que si on le lance : importé par un banc, il rend
// ses fonctions sans rien lancer ni sortir du processus.
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exit(main(process.argv[2]));
}
