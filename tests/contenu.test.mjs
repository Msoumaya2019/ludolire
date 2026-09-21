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
  assert.ok(detail.exercices > 0, 'aucun exercice rendu dans le contenu');
  assert.ok(detail.non_rendus > 0, 'aucune mécanique déclarée non rendue');
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

// ---------------------------------------------------------------------------
// Les exercices
//
// Le niveau qui porte des exercices rendus est le seul qui exerce ces
// contrôles : sur un niveau sans exercice, les cas ci-dessous passeraient à
// vide, et un banc vert à vide ne prouve rien. On l'exige donc explicitement.
// ---------------------------------------------------------------------------

const AVEC_EXERCICES = REEL.niveaux.find((n) => n.exercices.length > 0);

test('le témoin porte bien des exercices et des mécaniques non rendues', () => {
  assert.ok(AVEC_EXERCICES, 'aucun niveau ne porte d’exercice : les cas suivants seraient vides');
  assert.ok(AVEC_EXERCICES.exercices_exceptions.length > 0, 'aucune exception à éprouver');
});

/** Le premier exercice du niveau qui en porte. */
function premierExercice(c) {
  const n = c.niveaux.find((x) => x.exercices.length > 0);
  return n.exercices[0];
}

test('chaque phrase de preuve se retrouve dans une ligne du niveau', () => {
  // Cette propriété est vérifiée par le contrôle, mais on l'éprouve ici sur le
  // contenu réel : c'est elle qui garantit que la preuve affichée après une
  // bonne réponse est cherchable par l'enfant dans le texte qu'il vient de lire.
  let vues = 0;
  for (const n of REEL.niveaux) {
    for (const e of n.exercices) {
      for (const q of e.questions) {
        if (typeof q.phrase_preuve !== 'string' || q.phrase_preuve.length === 0) continue;
        vues += 1;
        const trouvee = n.textes.some((t) => t.lignes.some((l) => l.includes(q.phrase_preuve)));
        assert.ok(
          trouvee,
          `${e.id} : « ${q.phrase_preuve} » ne se trouve dans aucun texte du niveau`
        );
      }
    }
  }
  assert.ok(vues > 0, 'aucune phrase de preuve dans le contenu : ce cas serait vide');
});

test('un exercice sans identifiant est refusé', () => {
  const c = reempreindre(copie());
  delete premierExercice(c).id;
  attrape(c, 'un exercice sans identifiant');
});

test('un exercice sans question est refusé', () => {
  const c = reempreindre(copie());
  premierExercice(c).questions = [];
  attrape(c, 'aucune question');
});

test('un exercice sans titre est refusé', () => {
  const c = reempreindre(copie());
  premierExercice(c).titre = '';
  attrape(c, '« titre » manquant');
});

test('deux exercices du même identifiant sont refusés', () => {
  const c = reempreindre(copie());
  const n = c.niveaux.find((x) => x.exercices.length > 1);
  n.exercices[1].id = n.exercices[0].id;
  attrape(c, 'identifiant en double');
});

test('un exercice qui cite un texte absent du niveau est refusé', () => {
  const c = reempreindre(copie());
  premierExercice(c).texte = 'T99-rang99';
  attrape(c, "qui n'est pas dans le niveau");
});

test('une bonne réponse aussi comptée parmi les intruses est refusée', () => {
  const c = reempreindre(copie());
  const q = premierExercice(c).questions[0];
  q.intrus = [q.bonne, ...q.intrus];
  attrape(c, 'est aussi comptée parmi les');
});

test('deux intruses identiques sont refusées', () => {
  const c = reempreindre(copie());
  const q = premierExercice(c).questions[0];
  q.intrus = [q.intrus[0], q.intrus[0]];
  attrape(c, 'deux intruses identiques');
});

test('une intruse vide est refusée', () => {
  const c = reempreindre(copie());
  const q = premierExercice(c).questions[0];
  q.intrus = ['', q.intrus[0]];
  attrape(c, 'une intruse est vide');
});

test('une phrase de preuve introuvable dans le niveau est refusée', () => {
  const c = reempreindre(copie());
  premierExercice(c).questions[0].phrase_preuve = 'Cette phrase n’est dans aucun texte.';
  attrape(c, 'ne se trouve dans');
});

test('une phrase de preuve vide est refusée', () => {
  const c = reempreindre(copie());
  premierExercice(c).questions[0].phrase_preuve = '';
  attrape(c, 'phrase_preuve est présente mais vide');
});

test('une mécanique non rendue sans raison est refusée', () => {
  const c = reempreindre(copie());
  const n = c.niveaux.find((x) => x.exercices_non_rendus.length > 0);
  n.exercices_non_rendus[0].pourquoi = '';
  attrape(c, 'aucune raison');
});

test('une mécanique non rendue qui ne compte aucun exercice est refusée', () => {
  const c = reempreindre(copie());
  const n = c.niveaux.find((x) => x.exercices_non_rendus.length > 0);
  n.exercices_non_rendus[0].nombre = 0;
  attrape(c, 'au moins un exercice écrit');
});

test('une mécanique à la fois rendue et non rendue est refusée', () => {
  const c = reempreindre(copie());
  const n = c.niveaux.find((x) => x.exercices.length > 0 && x.exercices_non_rendus.length > 0);
  n.exercices_non_rendus[0].mecanique = n.exercices[0].mecanique;
  attrape(c, 'les deux listes se contredisent');
});

test('une exception sans raison est refusée', () => {
  const c = reempreindre(copie());
  const n = c.niveaux.find((x) => x.exercices_exceptions.length > 0);
  n.exercices_exceptions[0].raison = '';
  attrape(c, "n'a pas de raison");
});

test('un exercice déclaré rendu ET non rendu est refusé', () => {
  const c = reempreindre(copie());
  const n = c.niveaux.find((x) => x.exercices.length > 0 && x.exercices_exceptions.length > 0);
  n.exercices_exceptions[0].exercice = n.exercices[0].id;
  attrape(c, "l'écran l'afficherait en le disant injouable");
});
