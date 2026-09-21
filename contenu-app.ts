/**
 * L'accès au contenu embarqué.
 *
 * D'OÙ VIENT CE FICHIER
 * ---------------------
 * `assets/contenu-app.json` n'est pas écrit à la main : il est fabriqué par
 * `outils/generer-contenu-app.py`, à partir des corpus du projet — les
 * progressions, les textes, la banque du jeu de syllabes, la table des
 * correspondances du CP. Les corpus restent la source unique ; ce fichier-ci
 * n'est qu'une mise en forme pour l'écran.
 *
 * C'est pourquoi on ne corrige JAMAIS une faute dans `contenu-app.json` : on la
 * corrige dans le corpus, et on relance le générateur. Une correction faite ici
 * disparaîtrait à la fabrication suivante.
 *
 * CE QUE LE CONTENU PORTE, ET CE QU'IL NE PORTE PAS
 * -------------------------------------------------
 * Il porte les textes, les découpes syllabiques, les objectifs, et les exercices
 * dont la mécanique reçoit une forme dans `outils/formes-exercices.json`. Il ne
 * porte AUCUN SON : rien n'est enregistré à ce jour. Les activités qui reposent
 * sur la voix ne sont donc pas jouables, et l'application le dit à l'écran plutôt
 * que de proposer un bouton qui ne fait rien.
 *
 * Et ce qu'il ne porte pas est COMPTÉ : `exercices_non_rendus` dit, par
 * mécanique, combien d'exercices sont écrits et pourquoi l'application ne les
 * rend pas. L'écran du niveau les affiche. Un exercice écrit qu'on cache est un
 * mensonge ; un exercice écrit qu'on montre comme injouable est un état.
 */

import brut from './assets/contenu-app.json';

export type Texte = {
  id: string;
  titre: string;
  rang: number | null;
  genre: string | null;
  lignes: string[];
};

export type ItemJeu = {
  id: string;
  mot: string;
  syllabes: string[];
  trou: number;
  cartes: string[];
  rendu: string | null;
  sert: number | null;
};

export type Unite = {
  rang: number;
  periode: number | null;
  domaine: string | null;
  objectif: string | null;
  action: string | null;
};

export type Correspondance = {
  rang: number;
  semaine: number | null;
  phoneme: string | null;
  graphies: string[];
};

/**
 * Une question d'exercice : la question, la bonne réponse, ses intruses, et la
 * phrase du texte qui prouve la réponse.
 *
 * La bonne réponse EST ici, contrairement à celle du jeu des syllabes qui se
 * déduit. Ce n'est pas une incohérence : la banque d'exercices porte
 * elle-même ses `questions` avec leur bonne réponse, et la recopier ailleurs
 * serait créer une seconde source. Ici la source unique, c'est la banque.
 */
export type QuestionExercice = {
  question: string;
  bonne: string;
  intrus: string[];
  phrase_preuve: string | null;
};

/**
 * Un exercice que l'application sait rendre.
 *
 * `consigne` est le TEXTE de la consigne, celui qui sert aussi de script à
 * l'enregistrement à faire. Tant qu'aucun son n'existe, c'est lui qui s'affiche :
 * l'enfant du CE1 lit, donc sa consigne peut être écrite là où celle de la GS
 * doit être dite.
 *
 * `texte` cite un texte du niveau quand l'exercice s'appuie sur une lecture.
 */
export type Exercice = {
  id: string;
  unite: number;
  mecanique: string;
  titre: string;
  consigne: string | null;
  geste: string;
  duree_s: number | null;
  entraine: string;
  texte: string | null;
  questions: QuestionExercice[];
};

/**
 * Une mécanique écrite mais non rendue, avec sa raison et son nombre
 * d'exercices. L'écran les montre : un exercice écrit et injouable est un
 * manque, et un manque se voit plutôt que de disparaître.
 */
export type MecaniqueNonRendue = {
  mecanique: string;
  nombre: number;
  pourquoi: string;
};

/** Un exercice jouable que l'application ne rend pas, avec la raison. */
export type ExceptionExercice = {
  exercice: string;
  raison: string;
};

export type Niveau = {
  id: string;
  nom: string;
  court: string;
  sous_titre: string;
  couleur: string;
  textes: Texte[];
  jeu_syllabes: ItemJeu[];
  unites: Unite[];
  correspondances: Correspondance[];
  exercices: Exercice[];
  exercices_non_rendus: MecaniqueNonRendue[];
  exercices_exceptions: ExceptionExercice[];
};

export type Meta = {
  titre: string;
  sous_titre: string;
  etablissement: string;
  version: string;
  role: string;
  source: string;
  audio: string;
  empreinte: string;
};

export type Contenu = {
  meta: Meta;
  niveaux: Niveau[];
};

export const contenu = brut as unknown as Contenu;

export const meta = contenu.meta;
export const niveaux = contenu.niveaux;

export function niveau(id: string): Niveau | undefined {
  return niveaux.find((n) => n.id === id);
}

export function texte(niveauId: string, texteId: string): Texte | undefined {
  return niveau(niveauId)?.textes.find((t) => t.id === texteId);
}

/**
 * Ce qu'un niveau permet de faire aujourd'hui.
 *
 * Sert à l'accueil : une carte de niveau qui annonce « 23 textes » alors que le
 * niveau n'en a aucun serait un mensonge d'interface. On compte donc ce qui
 * existe réellement, et on le dit.
 */
export function ceQuOnPeutFaire(n: Niveau): string[] {
  const capacites: string[] = [];
  if (n.textes.length > 0) {
    capacites.push(n.textes.length === 1 ? '1 texte à lire' : `${n.textes.length} textes à lire`);
  }
  if (n.jeu_syllabes.length > 0) {
    capacites.push(
      n.jeu_syllabes.length === 1 ? '1 mot à compléter' : `${n.jeu_syllabes.length} mots à compléter`
    );
  }
  if (n.correspondances.length > 0) {
    capacites.push(`${n.correspondances.length} sons à découvrir`);
  }
  if (n.exercices.length > 0) {
    capacites.push(
      n.exercices.length === 1 ? '1 exercice' : `${n.exercices.length} exercices`
    );
  }
  if (n.unites.length > 0) {
    capacites.push(`${n.unites.length} étapes`);
  }
  return capacites;
}
