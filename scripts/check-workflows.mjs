/**
 * Contrôle statique des flux de travail GitHub Actions.
 *
 * POURQUOI CE FICHIER EXISTE
 * --------------------------
 * Un flux de travail se teste normalement en le poussant, et c'est le pire
 * moment pour découvrir une faute de frappe : sur une application mobile, la
 * compilation iOS prend un quart d'heure et consomme un exécuteur macOS. Deux
 * allers-retours suffisent à perdre une heure.
 *
 * Deux familles de défauts, très inégales en coût :
 *
 *   - YAML MAL FORMÉ : le flux ne démarre pas, GitHub le dit. Immédiat.
 *   - SCRIPT `run:` INVALIDE : le flux démarre, installe tout, puis échoue.
 *     Un quart d'heure, et le message ne nomme pas la cause.
 *
 * C'est la seconde qui justifie ce fichier.
 *
 * PORTÉE DU CONTRÔLE, ET OÙ IL S'ARRÊTE
 * -------------------------------------
 * `bash -n` analyse SANS ÉVALUER les expansions. Il attrape donc un `then`
 * manquant, un `fi` orphelin, une quote non fermée — et il ne voit PAS une
 * expansion fautive : `echo ${x` est refusé, mais `echo ${a b}` est accepté et
 * échoue à l'exécution en `bad substitution`. Une faute de frappe dans
 * `${CHEMIN}` ne sera signalée ni ici, ni par `tsc`, ni par ESLint.
 *
 * Ce contrôle ne dit rien non plus de la JUSTESSE : un flux parfaitement formé
 * peut compiler la mauvaise application.
 *
 * LA LISTE DES FLUX EST FERMÉE, DANS LES DEUX SENS
 * ------------------------------------------------
 * C'est le seul contrôle du projet dont l'absence d'un sujet produirait un
 * vert : il découvre ses sujets par `readdir`, donc il mesure ce qui RESTE,
 * jamais ce qui MANQUE. Rien d'autre dans la chaîne ne lit `.github/workflows`.
 * Un fichier écarté ne produirait donc aucun signal.
 *
 * Fermer la liste coûte une friction à chaque ajout, et cette friction est
 * utile : elle force à se demander si le nouveau flux doit tourner partout.
 *
 * Usage :
 *     node scripts/check-workflows.mjs
 */

import { spawnSync } from 'node:child_process';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Ce fichier est un module ESM, où `require` n'existe pas. `createRequire`
// rétablit la résolution des paquets CommonJS — c'est le moyen prévu, et il
// évite d'écrire un `import` statique de `yaml`, qui ferait échouer le fichier
// entier si le paquet n'était pas installé.
const require = createRequire(import.meta.url);

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..');
const DOSSIER = join(RACINE, '.github', 'workflows');

/** La liste FERMÉE des flux attendus. Ajouter un flux, c'est l'ajouter ici. */
const FLUX_ATTENDUS = ['ios-unsigned.yml'];

/**
 * Les actions dont le MOTEUR est connu bon.
 *
 * Le moteur se lit dans le manifeste de l'action, pas dans son numéro de
 * version : `upload-artifact@v5` annonce « supports Node 24 » et tourne
 * pourtant encore sous Node 20 — seul `v6` bascule. Ces versions-ci ont été
 * vérifiées.
 */
const ACTIONS_EPINGLEES = {
  'actions/checkout': ['v5', 'v6', 'v7'],
  'actions/setup-node': ['v5', 'v6', 'v7'],
  'actions/upload-artifact': ['v7'],
};

let verifications = 0;
const defauts = [];

function defaut(marqueur, message) {
  defauts.push(`${marqueur} ${message}`);
}

/** Neutralise les expressions GitHub : on analyse ce que le shell verra. */
function neutraliser(script) {
  return script.replace(/\$\{\{[^}]*\}\}/g, 'VALEUR');
}

function chargerYaml() {
  for (const nom of ['yaml', 'js-yaml']) {
    try {
      const module = require(nom);
      return { nom, lire: nom === 'yaml' ? (t) => module.parse(t) : (t) => module.load(t) };
    } catch {
      // on essaie le suivant
    }
  }
  return null;
}

function* etapesDe(flux) {
  for (const [nomTravail, travail] of Object.entries(flux.jobs ?? {})) {
    const etapes = travail?.steps ?? [];
    for (let i = 0; i < etapes.length; i += 1) {
      yield { nomTravail, index: i, etape: etapes[i] ?? {} };
    }
  }
}

export function main(dossier = DOSSIER, { silencieux = false } = {}) {
  // Les deux compteurs sont remis à zéro : le banc appelle `main` plusieurs
  // fois dans le même processus, et sans cela les défauts d'un cas
  // s'ajouteraient à ceux du suivant.
  verifications = 0;
  defauts.length = 0;

  const yaml = chargerYaml();
  if (!yaml) {
    console.error(
      "REFUS : ni « yaml » ni « js-yaml » n'est installé. Le contrôle ne peut pas analyser un flux\n" +
        '         sans analyseur YAML, et deviner serait pire que refuser.\n' +
        '         Remède : npm install yaml --save-dev'
    );
    return 1;
  }

  // --- La liste fermée, dans les deux sens -------------------------------
  if (!existsSync(dossier)) {
    defaut('[dossier-absent]', `${dossier} est introuvable`);
    console.error(defauts.join('\n'));
    return 1;
  }

  const fichiers = readdirSync(dossier)
    .filter((n) => n.endsWith('.yml') || n.endsWith('.yaml'))
    .sort();
  verifications += 1;

  for (const attendu of FLUX_ATTENDUS) {
    verifications += 1;
    if (!fichiers.includes(attendu)) {
      defaut('[flux-absent]', `${attendu} — flux attendu, absent du dossier`);
    }
  }
  for (const trouve of fichiers) {
    verifications += 1;
    if (!FLUX_ATTENDUS.includes(trouve)) {
      defaut(
        '[flux-non-declare]',
        `${trouve} — présent dans le dossier et absent de FLUX_ATTENDUS. ` +
          'Déclarez-le, ou retirez-le : un flux non déclaré n’est surveillé par personne'
      );
    }
  }

  // --- Chaque flux -------------------------------------------------------
  for (const nom of fichiers) {
    const chemin = join(dossier, nom);
    let flux;
    try {
      flux = yaml.lire(readFileSync(chemin, 'utf8'));
    } catch (erreur) {
      defaut('[yaml-invalide]', `${nom} — le YAML est refusé par ${yaml.nom} : ${erreur.message}`);
      continue;
    }
    verifications += 1;

    // Le déclencheur. `on:` est lu comme la clé booléenne `true` par un
    // analyseur en schéma YAML 1.1 — le flux ne se déclencherait alors jamais.
    if (!('on' in (flux ?? {}))) {
      defaut('[declencheur-absent]', `${nom} — aucune clé « on »`);
    } else if (typeof flux.on === 'boolean') {
      defaut(
        '[declencheur-booleen]',
        `${nom} — « on » est lu comme un booléen : l’analyseur emploie un schéma YAML 1.1`
      );
    }
    verifications += 1;

    if (!('permissions' in (flux ?? {}))) {
      defaut('[permissions-absentes]', `${nom} — aucun bloc « permissions »`);
    }
    verifications += 1;

    for (const [nomTravail, travail] of Object.entries(flux?.jobs ?? {})) {
      verifications += 1;
      if (!travail?.['runs-on']) {
        defaut('[runs-on-absent]', `${nom} › ${nomTravail} — aucun « runs-on »`);
      }
    }

    // --- Les sorties référencées -----------------------------------------
    const identifiants = new Map(); // id d'étape -> index d'apparition
    const ecrites = new Map(); // id d'étape -> noms de sorties écrites
    let rang = 0;
    for (const { etape } of etapesDe(flux)) {
      rang += 1;
      if (typeof etape.id === 'string') {
        identifiants.set(etape.id, rang);
        const texte = typeof etape.run === 'string' ? etape.run : '';
        const noms = new Set();
        for (const m of texte.matchAll(
          /^\s*(?:echo|printf)\s+["']?([A-Za-z_][A-Za-z0-9_]*)=/gm
        )) {
          noms.add(m[1]);
        }
        ecrites.set(etape.id, noms);
      }
    }

    // --- Chaque étape ------------------------------------------------------
    rang = 0;
    for (const { nomTravail, index, etape } of etapesDe(flux)) {
      rang += 1;
      verifications += 1;
      const ou = `${nom} › ${nomTravail} › étape ${index + 1}`;

      if (!etape.uses && !etape.run) {
        defaut('[etape-vide]', `${ou} — ni « uses » ni « run » : l’étape ne fait rien`);
      }

      // Les expressions sont vérifiées pour TOUTES les étapes, y compris celles
      // qui n'ont qu'un `uses:` : un contrôle écrit dans la branche `run:` ne
      // les verrait pas, et c'est exactement là que se cachait un défaut mesuré
      // sur un autre dépôt.
      const complet = JSON.stringify(etape);
      for (const m of complet.matchAll(/steps\.([A-Za-z_][A-Za-z0-9_]*)\.outputs\.([A-Za-z_][A-Za-z0-9_]*)/g)) {
        verifications += 1;
        const [, id, sortie] = m;
        if (!identifiants.has(id)) {
          defaut('[sortie-inconnue]', `${ou} — steps.${id}.outputs.${sortie} : aucune étape « ${id} »`);
        } else if (identifiants.get(id) > rang) {
          defaut(
            '[sortie-avant-producteur]',
            `${ou} — steps.${id}.outputs.${sortie} : l’étape « ${id} » vient plus bas`
          );
        } else if (ecrites.has(id) && ecrites.get(id).size > 0 && !ecrites.get(id).has(sortie)) {
          defaut(
            '[sortie-non-declaree]',
            `${ou} — steps.${id}.outputs.${sortie} : l’étape « ${id} » n’écrit pas « ${sortie} » ` +
              `(elle écrit : ${[...ecrites.get(id)].join(', ')})`
          );
        }
      }

      if (etape.uses) {
        verifications += 1;
        const [action, version] = String(etape.uses).split('@');
        if (!version) {
          defaut('[action-non-epinglee]', `${ou} — uses: ${etape.uses} sans version`);
        } else if (action in ACTIONS_EPINGLEES && !ACTIONS_EPINGLEES[action].includes(version)) {
          defaut(
            '[action-version-inconnue]',
            `${ou} — ${action}@${version} : versions connues bonnes ${ACTIONS_EPINGLEES[action].join(', ')}`
          );
        }
      }

      if (typeof etape.run === 'string') {
        // 1. La syntaxe.
        verifications += 1;
        const analyse = spawnSync('bash', ['-n'], {
          input: neutraliser(etape.run),
          encoding: 'utf8',
        });
        if (analyse.status !== 0) {
          defaut(
            '[script-invalide]',
            `${ou} — le script est refusé par « bash -n » : ` +
              `${(analyse.stderr || '').trim().split('\n')[0] ?? 'sans message'}`
          );
        }

        // 2. Un `run:` qui enchaîne plusieurs contrôles doit les exécuter TOUS.
        //    Sous `bash -e`, la première commande en échec termine le script et
        //    les suivantes ne tournent jamais — en silence, puisque le pas est
        //    déjà rouge pour une autre raison.
        const lignes = etape.run
          .split('\n')
          .map((l) => l.trim())
          .filter((l) => l.startsWith('npm run ') || l.startsWith('npm test') || l.startsWith('npm ci'));
        if (lignes.length >= 2) {
          verifications += 1;
          const gardees = lignes.filter((l) => l.includes('|| code=1')).length;
          const final = etape.run.trimEnd().split('\n').at(-1)?.trim();
          if (gardees !== lignes.length || final !== 'exit "$code"') {
            defaut(
              '[controle-agrege]',
              `${ou} — ${lignes.length} commandes enchaînées : ${gardees} portent « || code=1 » ` +
                `et la dernière ligne est « ${final} ». Sous « bash -e », l’échec du premier ` +
                'contrôle supprimerait les suivants sans un mot.'
            );
          }
        }
      }
    }
  }

  // --- Le rapport --------------------------------------------------------
  const dire = silencieux ? () => {} : (l) => console.log(l);

  dire(`Contrôle statique des flux de travail`);
  dire(`  analyseur YAML        ${yaml.nom}`);
  dire(`  flux analysés         ${fichiers.length} (${fichiers.join(', ')})`);
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

export { DOSSIER, FLUX_ATTENDUS };

// Le contrôle ne s'exécute que si on le lance : importé par un banc, il rend
// ses fonctions sans rien lancer ni sortir du processus.
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exit(main(process.argv[2]));
}
