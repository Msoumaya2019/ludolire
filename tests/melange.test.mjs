/**
 * Banc du mélange des cartes.
 *
 * POURQUOI CE BANC EXISTE
 * -----------------------
 * Le corpus déclare les cartes d'un item dans l'ordre « la bonne, puis les
 * intruses ». C'est le bon ordre pour un fichier, et le pire pour un jeu :
 * l'enfant qui touche toujours la première carte gagne sans lire, et il apprend
 * cela en trois items. Le mélange est donc la seule chose qui empêche le jeu de
 * s'annuler lui-même — et rien ne le vérifiait.
 *
 * Mesuré une fois à la main avant d'écrire ce fichier : sur les 42 items, la
 * bonne carte tombait 15 fois en première position, 14 fois en deuxième, 13 fois
 * en troisième. Une mesure faite à la main ne survit pas à la première retouche
 * de la fonction ni au premier réordonnancement du corpus.
 *
 * LE CONTRÔLE PREND LE MÉLANGE EN PARAMÈTRE, ET C'EST LE POINT
 * -----------------------------------------------------------
 * `defautsDuMelange(melanger)` ne teste pas le mélange réel : il teste **un**
 * mélange qu'on lui passe. C'est ce qui permet de lui présenter des
 * implémentations fausses — un mélange identité, un mélange qui perd une carte,
 * un mélange qui la duplique — et d'exiger qu'il les refuse. Sans cela, ce banc
 * ne serait qu'une fonction qui renvoie une liste vide.
 *
 * Un banc qu'on ne peut pas falsifier ne prouve rien : il dit « vert » aussi
 * bien quand le contrôle regarde que quand il ne regarde pas.
 *
 * CE QU'IL VÉRIFIE, ET CE QU'IL NE VÉRIFIE PAS
 * -------------------------------------------
 * Il vérifie que le mélange est une **permutation** — aucune carte perdue,
 * aucune carte en double —, que la bonne carte **atteint toutes les positions**
 * sur plusieurs parties, et que la prémisse tient : le corpus met bien la bonne
 * carte en tête.
 *
 * Il ne juge pas si l'ordre est *agréable* ni s'il est *difficile* : ce sont des
 * jugements pédagogiques, et ils appartiennent au porteur du projet.
 */

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';

import { graine, melanger } from '../melange.ts';

const CHEMIN = new URL('../assets/contenu-app.json', import.meta.url);
const CONTENU = JSON.parse(readFileSync(CHEMIN, 'utf8'));

/** Les items du jeu, dans le contenu réellement embarqué dans l'application. */
const ITEMS = CONTENU.niveaux.find((n) => n.id === 'gs').jeu_syllabes;

/**
 * Le nombre de parties sur lesquelles on exige que l'ordre varie.
 *
 * Trois parties ne suffiraient pas : avec trois cartes, un item sur neuf garde
 * la même position par hasard, donc sur 42 items quatre ou cinq échoueraient
 * sans qu'aucun défaut existe. Quinze parties ramènent cette probabilité à
 * l'ordre de 1 sur 100 000 par item — mesuré sur le contenu réel : **aucun**
 * item ne conserve la même position, et **tous** atteignent les trois.
 */
const PARTIES = 15;

/**
 * Le contrôle du mélange, écrit comme une fonction de son sujet.
 *
 * @param {import('../melange.ts').melanger} melange le mélange à éprouver
 * @returns {string[]} les défauts trouvés, vide si le mélange fait son travail
 */
function defautsDuMelange(melange) {
  const defauts = [];

  for (const item of ITEMS) {
    const bonne = item.syllabes[item.trou];

    // La prémisse, sans laquelle le mélange n'a plus la même raison d'être :
    // si le corpus cessait de mettre la bonne carte en tête, un mélange
    // identité ne ferait plus de tort — et ce banc ne prouverait plus rien.
    if (item.cartes[0] !== bonne) {
      defauts.push(
        `${item.id} : la bonne carte « ${bonne} » n'est pas en tête du corpus ` +
          `(« ${item.cartes[0]} » y est) — la prémisse du mélange a changé`
      );
      continue;
    }

    const positions = new Set();
    for (let partie = 0; partie < PARTIES; partie += 1) {
      const ordre = melange(item.cartes, graine(item.id, partie));

      if (ordre.length !== item.cartes.length) {
        defauts.push(
          `${item.id} : ${ordre.length} carte(s) rendue(s) pour ${item.cartes.length} — ` +
            'le mélange perd ou ajoute des cartes'
        );
        break;
      }

      const attendu = [...item.cartes].sort().join('|');
      const obtenu = [...ordre].sort().join('|');
      if (obtenu !== attendu) {
        defauts.push(
          `${item.id} : le mélange n'est pas une permutation — ` +
            `attendu {${attendu}}, obtenu {${obtenu}}`
        );
        break;
      }

      positions.add(ordre.indexOf(bonne));
    }

    if (positions.size < item.cartes.length) {
      defauts.push(
        `${item.id} : en ${PARTIES} parties, la bonne carte n'atteint que ` +
          `${positions.size} position(s) sur ${item.cartes.length} — ` +
          "l'enfant peut la mémoriser au lieu de lire"
      );
    }
  }

  return defauts;
}

// ---------------------------------------------------------------------------
//  Le témoin
// ---------------------------------------------------------------------------

test('témoin : le mélange réel fait son travail sur les 42 items', () => {
  const defauts = defautsDuMelange(melanger);
  assert.deepEqual(defauts, [], `défauts rendus :\n  ${defauts.join('\n  ')}`);
});

test('témoin : le jeu compte bien 42 items à trois cartes', () => {
  assert.equal(ITEMS.length, 42);
  for (const item of ITEMS) {
    assert.equal(
      item.cartes.length,
      3,
      `${item.id} : ${item.cartes.length} cartes — ce banc suppose trois`
    );
  }
});

// ---------------------------------------------------------------------------
//  Les falsifications : le contrôle doit refuser une implémentation fausse
// ---------------------------------------------------------------------------

test('le contrôle attrape un mélange qui ne mélange rien', () => {
  const defauts = defautsDuMelange((cartes) => [...cartes]);
  assert.ok(
    defauts.length > 0,
    'un mélange identité laisse la bonne carte en tête : le contrôle aurait dû le refuser'
  );
});

test('le contrôle attrape un mélange qui perd une carte', () => {
  const defauts = defautsDuMelange((cartes) => cartes.slice(0, -1));
  assert.ok(defauts.length > 0, 'un mélange qui perd une carte est passé');
});

test('le contrôle attrape un mélange qui duplique une carte', () => {
  const defauts = defautsDuMelange((cartes) => [cartes[0], cartes[0], cartes[2]]);
  assert.ok(defauts.length > 0, 'un mélange qui duplique une carte est passé');
});

test('le contrôle attrape un mélange qui ignore la partie', () => {
  // Le défaut que ce banc existe pour empêcher : un ordre figé pour toujours.
  // C'est exactement ce que faisait l'application avant que la graine ne
  // dépende de la partie — l'enfant gagnait sans lire au troisième passage.
  const defauts = defautsDuMelange((cartes, graineItem) => {
    // Un mélange qui déplace bien la bonne carte, mais toujours pareil.
    const figee = [...cartes].reverse();
    return figee;
  });
  assert.ok(
    defauts.length > 0,
    "un mélange qui donne toujours le même ordre est passé — c'est le défaut d'origine"
  );
});

// ---------------------------------------------------------------------------
//  La graine
// ---------------------------------------------------------------------------

test('la première partie se rejoue à l’identique', () => {
  // La graine de la partie 0 est l'identifiant NU, sans suffixe : c'est ce qui
  // rend une première partie reproductible d'une version de l'application à
  // l'autre, même si le format de la graine évoluait.
  assert.equal(graine('J03', 0), 'J03');
});

test('les parties suivantes ont une graine distincte', () => {
  const vues = new Set();
  for (let partie = 0; partie < PARTIES; partie += 1) {
    vues.add(graine('J03', partie));
  }
  assert.equal(vues.size, PARTIES, 'deux parties partagent la même graine');
});
