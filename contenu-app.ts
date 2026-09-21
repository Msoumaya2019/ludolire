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
 * Il porte les textes, les découpes syllabiques, les objectifs. Il ne porte
 * AUCUN SON : rien n'est enregistré à ce jour. Les activités qui reposent sur la
 * voix ne sont donc pas jouables, et l'application le dit à l'écran plutôt que
 * de proposer un bouton qui ne fait rien.
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
  if (n.unites.length > 0) {
    capacites.push(`${n.unites.length} étapes`);
  }
  return capacites;
}
