/**
 * Banc du contrôle du contenu embarqué.
 *
 * POURQUOI CE BANC EXISTE
 * -----------------------
 * Un contrôle qui n'a jamais échoué n'est pas un contrôle : c'est une fonction
 * qui renvoie `[]`. On fabrique donc ici des contenus FAUX, un par défaut que
 * le contrôle prétend attraper, et on exige qu'il les attrape — en nommant le
 * défaut, et pas seulement en échouant.
 *
 * Le dernier cas est un TÉMOIN : le contenu réel, non modifié, doit passer.
 * Sans lui, un contrôle qui refuserait tout serait vert sur tous les autres cas.
 */

import assert from 'node:assert/strict';
import { test } from 'node:test';

import { controler, empreinteDe, lire } from '../scripts/verifier-contenu.mjs';

const REEL = lire();

/** Une copie profonde, pour ne jamais abîmer le contenu réel d'un cas à l'autre. */
function copie() {
  return JSON.parse(JSON.stringify(REEL));
}

/** Recalcule l'empreinte : les cas qui visent un autre défaut ne doivent pas
 *  échouer sur l'empreinte, sinon ils ne prouvent rien du défaut visé. */
function reempreindre(c) {
  c.meta.empreinte = empreinteDe(c);
  return c;
}

function attrape(contenu, extrait) {
  const { erreurs } = controler(contenu);
  assert.ok(
    erreurs.some((e) => e.includes(extrait)),
    `le contrôle n'a pas vu « ${extrait} ».\nErreurs rendues :\n  ${erreurs.join('\n  ')}`
  );
}

test('témoin : le contenu réel est conforme', () => {
  const { erreurs, detail } = controler(REEL);
  assert.deepEqual(erreurs, []);
  assert.ok(detail.items > 0, 'aucun item de jeu dans le contenu');
  assert.ok(detail.textes > 0, 'aucun texte dans le contenu');
});

test("l'empreinte déclarée est celle du contenu", () => {
  assert.equal(empreinteDe(REEL), REEL.meta.empreinte);
});

test("l'empreinte attrape une retouche d'une seule lettre", () => {
  const c = copie();
  const niveau = c.niveaux.find((n) => n.textes.length > 0);
  const avant = niveau.textes[0].titre;
  // La retouche est VÉRIFIÉE, et non supposée : la première version de ce cas
  // retirait un accent à un titre qui n'en portait pas, `replace` ne changeait
  // rien, et le cas échouait en accusant le contrôle. Un cas qui ne modifie pas
  // ce qu'il croit modifier ne prouve rien.
  const apres = avant + ' ';
  assert.notEqual(apres, avant, 'la retouche doit changer le contenu');
  niveau.textes[0].titre = apres;
  attrape(c, 'empreinte');
});

test("l'empreinte attrape une réponse du jeu modifiée", () => {
  const c = copie();
  const niveau = c.niveaux.find((n) => n.jeu_syllabes.length > 0);
  niveau.jeu_syllabes[0].cartes[0] = 'zzz';
  attrape(c, 'empreinte');
});

test('une empreinte absente est refusée', () => {
  const c = copie();
  delete c.meta.empreinte;
  attrape(c, 'empreinte est absente');
});

test('un niveau sans identifiant est refusé', () => {
  const c = reempreindre(copie());
  delete c.niveaux[0].id;
  attrape(c, 'identifiant manquant');
});

test('deux niveaux du même identifiant sont refusés', () => {
  const c = reempreindre(copie());
  c.niveaux[1].id = c.niveaux[0].id;
  attrape(c, 'identifiant en double');
});

test('un niveau sans couleur est refusé', () => {
  const c = reempreindre(copie());
  c.niveaux[0].couleur = '';
  attrape(c, '« couleur » manquant');
});

test('un texte sans titre est refusé', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.textes.length > 0);
  niveau.textes[0].titre = '';
  attrape(c, 'un texte sans titre');
});

test('un texte sans ligne est refusé', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.textes.length > 0);
  niveau.textes[0].lignes = [];
  attrape(c, "n'a aucune ligne");
});

test('une ligne vide dans un texte est refusée', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.textes.length > 0);
  niveau.textes[0].lignes = ['   '];
  attrape(c, 'porte une ligne vide');
});

test('un item du jeu en double est refusé', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.jeu_syllabes.length > 0);
  niveau.jeu_syllabes[1].id = niveau.jeu_syllabes[0].id;
  attrape(c, 'en double');
});

test('un item sans trou est refusé', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.jeu_syllabes.length > 0);
  niveau.jeu_syllabes[0].trou = 99;
  attrape(c, 'hors de la découpe');
});

test('une découpe qui ne recompose pas le mot est refusée', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.jeu_syllabes.length > 0);
  niveau.jeu_syllabes[0].syllabes = ['xx', 'yy'];
  attrape(c, 'ne recompose pas');
});

test('un item dont la bonne syllabe manque parmi les cartes est refusé', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.jeu_syllabes.length > 0);
  const item = niveau.jeu_syllabes[0];
  const bonne = item.syllabes[item.trou];
  item.cartes = item.cartes.filter((x) => x !== bonne);
  attrape(c, "n'est pas parmi les cartes");
});

test('deux cartes identiques sont refusées', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.jeu_syllabes.length > 0);
  const item = niveau.jeu_syllabes[0];
  item.cartes = [item.cartes[0], item.cartes[0]];
  attrape(c, 'deux cartes identiques');
});

test('une seule carte recompose le mot, pour chaque item', () => {
  // Cette propriété n'a PAS de contrôle dédié dans le vérificateur, et c'est
  // délibéré : elle est impossible à violer une fois la découpe et l'unicité
  // des cartes vérifiées. On l'éprouve donc ici, sur le contenu réel, plutôt
  // que d'écrire un contrôle inatteignable qui ferait semblant de la garder.
  for (const niveau of REEL.niveaux) {
    for (const item of niveau.jeu_syllabes) {
      const gagnantes = item.cartes.filter((carte) => {
        const essai = [...item.syllabes];
        essai[item.trou] = carte;
        return essai.join('') === item.mot;
      });
      assert.equal(
        gagnantes.length,
        1,
        `${niveau.id}/${item.id} : ${gagnantes.length} carte(s) recomposent « ${item.mot} » ` +
          `(${gagnantes.join(', ')})`
      );
      assert.equal(gagnantes[0], item.syllabes[item.trou]);
    }
  }
});

test('deux unités du même rang sont refusées', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.unites.length > 1);
  niveau.unites[1].rang = niveau.unites[0].rang;
  attrape(c, 'deux unités portent le rang');
});

test("une unité sans objectif est refusée", () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.unites.length > 0);
  niveau.unites[0].objectif = '';
  attrape(c, "n'a pas d'objectif");
});

test('une correspondance sans graphie est refusée', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.correspondances.length > 0);
  niveau.correspondances[0].graphies = [];
  attrape(c, "n'a aucune graphie");
});

test('une correspondance sans phonème est refusée', () => {
  const c = reempreindre(copie());
  const niveau = c.niveaux.find((n) => n.correspondances.length > 0);
  niveau.correspondances[0].phoneme = '';
  attrape(c, "n'a pas de phonème");
});

test('un contenu sans niveau est refusé', () => {
  attrape({ meta: { empreinte: 'x' }, niveaux: [] }, 'aucun niveau');
});

test('un contenu sans meta est refusé', () => {
  attrape({ niveaux: [] }, 'meta manquant');
});
