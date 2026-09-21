/**
 * Banc du contrôle statique des flux de travail.
 *
 * POURQUOI CE BANC EXISTE
 * -----------------------
 * Un contrôle qui n'a jamais échoué n'est pas un contrôle : c'est une fonction
 * qui renvoie 0. On introduit donc ici chaque défaut que le contrôle prétend
 * attraper, et on exige qu'il l'attrape — EN LE NOMMANT, par son marqueur.
 *
 * LE MARQUEUR, ET NON LA PHRASE
 * -----------------------------
 * Les défauts portent des marqueurs ASCII (`[flux-absent]`, `[script-invalide]`)
 * et le banc s'accroche à eux. Un fragment de prose française est un contrat
 * fragile : il se reformule, et il traverse parfois mal un encodage. Un marqueur
 * est un identifiant.
 *
 * LE BANC DISTINGUE « MOTIF INTROUVABLE » DE « RESTÉ VERT »
 * ---------------------------------------------------------
 * Une mutation dont le texte à remplacer a disparu laisse le contrôle vert, et
 * on conclut alors à un défaut du contrôle alors que la mutation n'a pas eu
 * lieu. Chaque mutation est donc VÉRIFIÉE : `remplacer` refuse si le motif
 * n'apparaît pas exactement une fois.
 */

import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';

import { DOSSIER, FLUX_ATTENDUS, defautsDe, main } from '../scripts/check-workflows.mjs';

const REEL = readFileSync(join(DOSSIER, FLUX_ATTENDUS[0]), 'utf8');
const NOM = FLUX_ATTENDUS[0];

function bac() {
  return mkdtempSync(join(tmpdir(), 'ludolire-flux-'));
}

function ecrire(dossier, contenu, nom = NOM) {
  mkdirSync(dossier, { recursive: true });
  writeFileSync(join(dossier, nom), contenu, 'utf8');
}

/** Remplace, et REFUSE si le motif n'est pas là : sinon on croirait avoir muté. */
function remplacer(texte, motif, par) {
  const occurrences = texte.split(motif).length - 1;
  assert.equal(
    occurrences,
    1,
    `la mutation ne peut pas avoir lieu : le motif « ${motif.slice(0, 60)}… » ` +
      `apparaît ${occurrences} fois, 1 attendue`
  );
  return texte.replace(motif, par);
}

function attrape(dossier, marqueur) {
  const defauts = defautsDe(dossier);
  assert.ok(
    defauts.some((d) => d.includes(marqueur)),
    `le contrôle n'a pas vu ${marqueur}.\nDéfauts rendus :\n  ${defauts.join('\n  ') || '(aucun)'}`
  );
}

// ---------------------------------------------------------------------------
//  Le témoin
// ---------------------------------------------------------------------------

test('témoin : les flux du dépôt sont conformes', () => {
  assert.equal(main(undefined, { silencieux: true }), 0);
});

test('témoin : un flux minimal et valide passe', () => {
  const d = bac();
  try {
    ecrire(
      d,
      [
        'name: Minimal',
        'on:',
        '  workflow_dispatch:',
        'permissions:',
        '  contents: read',
        'jobs:',
        '  a:',
        '    runs-on: ubuntu-latest',
        '    steps:',
        '      - run: echo bonjour',
        '',
      ].join('\n')
    );
    assert.deepEqual(defautsDe(d), []);
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

// ---------------------------------------------------------------------------
//  La liste fermée, dans les deux sens — le seul contrôle qu'aucune mutation
//  des vrais fichiers ne peut atteindre
// ---------------------------------------------------------------------------

test('un flux attendu absent est signalé', () => {
  const d = bac();
  try {
    // Un dossier vide, mais le contrôle doit refuser sur l'absence, pas sur le vide.
    assert.ok(defautsDe(d).some((x) => x.includes('[flux-absent]')));
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

test('un flux présent mais non déclaré est signalé', () => {
  const d = bac();
  try {
    ecrire(d, REEL);
    ecrire(d, REEL, 'un-flux-en-trop.yml');
    const defauts = defautsDe(d);
    assert.ok(
      defauts.some((x) => x.includes('[flux-non-declare]') && x.includes('un-flux-en-trop.yml')),
      `défauts rendus : ${defauts.join(' | ') || '(aucun)'}`
    );
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

test('un dossier de flux absent est signalé', () => {
  const defauts = defautsDe(join(tmpdir(), 'ludolire-dossier-qui-nexiste-pas'));
  assert.ok(defauts.some((x) => x.includes('[dossier-absent]')));
});

// ---------------------------------------------------------------------------
//  Les mutations
// ---------------------------------------------------------------------------

const MUTATIONS = [
  {
    nom: 'un YAML mal formé',
    marqueur: '[yaml-invalide]',
    faire: (t) => remplacer(t, 'name: iOS — IPA non signé', 'name: [non ferme'),
  },
  {
    nom: 'un déclencheur renommé',
    marqueur: '[declencheur-absent]',
    faire: (t) => remplacer(t, 'on:\n  workflow_dispatch:', 'declencheurs:\n  workflow_dispatch:'),
  },
  {
    nom: 'un bloc permissions retiré',
    marqueur: '[permissions-absentes]',
    faire: (t) => remplacer(t, 'permissions:\n  contents: write\n', ''),
  },
  {
    nom: 'un runs-on retiré',
    marqueur: '[runs-on-absent]',
    faire: (t) => remplacer(t, '    runs-on: macos-26\n', ''),
  },
  {
    nom: 'une action non épinglée',
    marqueur: '[action-non-epinglee]',
    faire: (t) => remplacer(t, 'uses: actions/checkout@v5', 'uses: actions/checkout'),
  },
  {
    nom: 'une action dont le moteur est déprécié',
    marqueur: '[action-version-inconnue]',
    faire: (t) => remplacer(t, 'uses: actions/upload-artifact@v7', 'uses: actions/upload-artifact@v4'),
  },
  {
    nom: 'une étape qui ne fait rien',
    marqueur: '[etape-vide]',
    // La mutation AJOUTE une étape vide, elle ne vide pas une étape existante.
    // Deux tentatives ont échoué avant celle-ci, et pour deux raisons
    // différentes — c'est instructif :
    //   - ajouter une clé `x` à côté du `run:` laissait le `run` en place :
    //     l'étape restait valide, rien n'était cassé ;
    //   - retirer la ligne `run: |` laissait le corps du script orphelin, donc
    //     plus indenté que sa clé : le YAML devenait INVALIDE, et le contrôle
    //     répondait `[yaml-invalide]` sans jamais atteindre `[etape-vide]`.
    // Le cas ne prouvait donc rien sur le contrôle — seulement sur ma mutation.
    faire: (t) =>
      remplacer(
        t,
        '      - name: Récupérer le dépôt\n        uses: actions/checkout@v5\n',
        '      - name: Récupérer le dépôt\n        uses: actions/checkout@v5\n' +
          '      - name: Étape qui ne fait rien\n        x: rien\n'
      ),
  },
  {
    nom: 'un « then » manquant',
    marqueur: '[script-invalide]',
    faire: (t) =>
      remplacer(
        t,
        '          if [ -z "$PROJET_APP" ]; then',
        '          if [ -z "$PROJET_APP" ]'
      ),
  },
  {
    nom: 'une sortie référencée mais jamais écrite',
    marqueur: '[sortie-non-declaree]',
    // L'ancre vise `-scheme "${{ … }}"` et non `steps.cible.outputs.scheme` :
    // cette dernière apparaît DEUX fois dans le flux — dans la compilation et
    // dans le résumé. La garde d'unicité de `remplacer` refusait donc la
    // mutation, et le cas échouait sans que le contrôle ait été exercé.
    faire: (t) =>
      remplacer(
        t,
        '-scheme "${{ steps.cible.outputs.scheme }}"',
        '-scheme "${{ steps.cible.outputs.typo }}"'
      ),
  },
  {
    nom: 'une sortie d’une étape qui n’existe pas',
    marqueur: '[sortie-inconnue]',
    faire: (t) =>
      remplacer(
        t,
        '-scheme "${{ steps.cible.outputs.scheme }}"',
        '-scheme "${{ steps.inexistante.outputs.scheme }}"'
      ),
  },
  {
    nom: 'des contrôles enchaînés sans garde',
    marqueur: '[controle-agrege]',
    faire: (t) =>
      remplacer(
        t,
        '          code=0\n          npm run check:workflows || code=1',
        '          code=0\n          npm run check:workflows'
      ),
  },
];

for (const mutation of MUTATIONS) {
  test(`le contrôle attrape ${mutation.nom}`, () => {
    const d = bac();
    try {
      ecrire(d, mutation.faire(REEL));
      attrape(d, mutation.marqueur);
    } finally {
      rmSync(d, { recursive: true, force: true });
    }
  });
}

// ---------------------------------------------------------------------------
//  Le contrôle lui-même : il doit compter ce qu'il a fait
// ---------------------------------------------------------------------------

test('le contrôle annonce un nombre de vérifications supérieur au nombre de flux', () => {
  // Un rapport qui annonce « OK » ne dit pas s'il a regardé quelque chose. On
  // exige donc qu'il compte, et que le compte soit plus grand que le nombre de
  // fichiers — sinon il n'a rien vérifié à l'intérieur.
  const sortie = [];
  const vraiLog = console.log;
  console.log = (l) => sortie.push(String(l));
  try {
    main(undefined, { silencieux: false });
  } finally {
    console.log = vraiLog;
  }
  const ligne = sortie.find((l) => l.includes('vérifications'));
  assert.ok(ligne, 'le rapport ne compte pas ses vérifications');
  const compte = Number(ligne.trim().split(/\s+/).at(-1));
  assert.ok(
    compte > FLUX_ATTENDUS.length,
    `${compte} vérifications pour ${FLUX_ATTENDUS.length} flux : le contrôle a survolé`
  );
});
