/**
 * Banc du contrôle des routes.
 *
 * POURQUOI CE BANC EXISTE
 * -----------------------
 * Le contrôle des routes a été écrit parce que `typedRoutes` ne rendait pas le
 * service attendu dans la chaîne de vérification. Mais un contrôle qu'on vient
 * d'écrire est exactement celui dont on ne sait rien : il rend « conforme » sur
 * le dépôt, et rien ne dit qu'il refuserait quoi que ce soit.
 *
 * On lui présente donc chaque défaut qu'il prétend attraper, et on exige qu'il
 * l'attrape — en le NOMMANT, par son marqueur ASCII, parce qu'un fragment de
 * prose française se reformule.
 *
 * ET UN CAS DE FAUX POSITIF
 * -------------------------
 * Un contrôle qui crie au loup ne sert à rien : on apprend à l'ignorer. Le
 * dernier cas vérifie donc qu'une route **imbriquée** valide est acceptée —
 * `app/niveau/index.tsx` répond à `/niveau`, et refuser cette cible serait un
 * défaut du contrôle, pas du code.
 */

import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';

import { APP, defautsDe, main } from '../scripts/verifier-routes.mjs';

function bac() {
  return mkdtempSync(join(tmpdir(), 'ludolire-routes-'));
}

/**
 * Écrit une application minimale mais VALIDE, puis laisse le cas la muter.
 *
 * @param {string} dossier   la racine de l'application
 * @param {object} [options] de quoi casser une chose précise à la fois
 */
function ecrireApp(dossier, options = {}) {
  const {
    routes = { 'index.tsx': '', 'niveau.tsx': '' },
    miseEnPage = [
      'export default function Pile() {',
      '  return (',
      '    <Stack>',
      "      <Stack.Screen name=\"index\" />",
      "      <Stack.Screen name=\"niveau\" />",
      '    </Stack>',
      '  );',
      '}',
      '',
    ].join('\n'),
    navigation = "router.push({ pathname: '/niveau' });",
  } = options;

  mkdirSync(dossier, { recursive: true });
  for (const [nom, contenu] of Object.entries(routes)) {
    const chemin = join(dossier, nom);
    mkdirSync(join(chemin, '..'), { recursive: true });
    writeFileSync(chemin, contenu, 'utf8');
  }
  if (miseEnPage !== null) {
    writeFileSync(join(dossier, '_layout.tsx'), miseEnPage, 'utf8');
  }
  if (navigation !== null) {
    writeFileSync(join(dossier, 'index.tsx'), navigation, 'utf8');
  }
}

function attrape(dossier, marqueur) {
  const defauts = defautsDe(dossier);
  assert.ok(
    defauts.some((d) => d.includes(marqueur)),
    `le contrôle n'a pas vu ${marqueur}.\nDéfauts rendus :\n  ${defauts.join('\n  ') || '(aucun)'}`
  );
}

// ---------------------------------------------------------------------------
//  Les témoins
// ---------------------------------------------------------------------------

test('témoin : les routes du dépôt sont conformes', () => {
  assert.equal(main(undefined, { silencieux: true }), 0);
});

test('témoin : une application minimale et valide passe', () => {
  const d = bac();
  try {
    ecrireApp(d);
    assert.deepEqual(defautsDe(d), []);
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

// ---------------------------------------------------------------------------
//  Les falsifications
// ---------------------------------------------------------------------------

test('une cible de navigation sans route est signalée', () => {
  const d = bac();
  try {
    ecrireApp(d, { navigation: "router.push({ pathname: '/lectur' });" });
    attrape(d, '[cible-inconnue]');
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

test('un écran déclaré qui n’existe pas est signalé', () => {
  const d = bac();
  try {
    ecrireApp(d, {
      miseEnPage: [
        'export default function Pile() {',
        '  return (',
        '    <Stack>',
        "      <Stack.Screen name=\"index\" />",
        "      <Stack.Screen name=\"niveau\" />",
        "      <Stack.Screen name=\"fantome\" />",
        '    </Stack>',
        '  );',
        '}',
        '',
      ].join('\n'),
    });
    attrape(d, '[ecran-inconnu]');
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

test('une route non déclarée dans la mise en page est signalée', () => {
  const d = bac();
  try {
    // `unites.tsx` existe et n'est déclarée nulle part : l'écran s'afficherait
    // avec « unites » pour titre, un nom de fichier sous les yeux d'un enfant.
    ecrireApp(d, { routes: { 'index.tsx': '', 'niveau.tsx': '', 'unites.tsx': '' } });
    attrape(d, '[route-non-declaree]');
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

test('un écran déclaré deux fois est signalé', () => {
  const d = bac();
  try {
    ecrireApp(d, {
      miseEnPage: [
        'export default function Pile() {',
        '  return (',
        '    <Stack>',
        "      <Stack.Screen name=\"index\" />",
        "      <Stack.Screen name=\"niveau\" />",
        "      <Stack.Screen name=\"niveau\" />",
        '    </Stack>',
        '  );',
        '}',
        '',
      ].join('\n'),
    });
    attrape(d, '[ecran-en-double]');
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

test('une mise en page absente est signalée', () => {
  const d = bac();
  try {
    ecrireApp(d, { miseEnPage: null });
    attrape(d, '[mise-en-page-absente]');
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

test('un dossier d’application absent est signalé', () => {
  const defauts = defautsDe(join(tmpdir(), 'ludolire-app-qui-nexiste-pas'));
  assert.ok(defauts.some((x) => x.includes('[dossier-app-absent]')));
});

test('un dossier sans aucune route est signalé', () => {
  const d = bac();
  try {
    ecrireApp(d, { routes: {}, navigation: null });
    attrape(d, '[aucune-route]');
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

// ---------------------------------------------------------------------------
//  Le faux positif : un contrôle qui crie au loup ne sert à rien
// ---------------------------------------------------------------------------

test('une route imbriquée valide n’est PAS refusée', () => {
  const d = bac();
  try {
    // `app/niveau/index.tsx` répond à `/niveau`. La cible `/niveau` doit donc
    // être acceptée : le segment correspond à un DOSSIER, pas à un fichier.
    ecrireApp(d, {
      routes: { 'index.tsx': '', 'niveau/index.tsx': '' },
      miseEnPage: [
        'export default function Pile() {',
        '  return (',
        '    <Stack>',
        "      <Stack.Screen name=\"index\" />",
        '    </Stack>',
        '  );',
        '}',
        '',
      ].join('\n'),
    });
    assert.deepEqual(defautsDe(d), [], 'le contrôle refuse une route imbriquée valide');
  } finally {
    rmSync(d, { recursive: true, force: true });
  }
});

// ---------------------------------------------------------------------------
//  Le contrôle lui-même : il doit compter ce qu'il a fait
// ---------------------------------------------------------------------------

test('le contrôle annonce un nombre de vérifications supérieur au nombre de routes', () => {
  const sortie = [];
  const vraiLog = console.log;
  console.log = (l) => sortie.push(String(l));
  try {
    main(APP, { silencieux: false });
  } finally {
    console.log = vraiLog;
  }
  const ligne = sortie.find((l) => l.includes('vérifications'));
  assert.ok(ligne, 'le rapport ne compte pas ses vérifications');
  const compte = Number(ligne.trim().split(/\s+/).at(-1));
  assert.ok(compte > 5, `${compte} vérifications : le contrôle a survolé`);
});
