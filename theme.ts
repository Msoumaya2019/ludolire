/**
 * Le thème de Ludo'Lire.
 *
 * POURQUOI LE FOND N'EST PAS BLANC
 * --------------------------------
 * L'application est une application de LECTURE, et l'écran de lecture est celui
 * qu'on regarde le plus longtemps. Un blanc pur fatigue : le contraste avec
 * l'encre est maximal, et la page « brille ». Le fond est donc un crème très
 * clair, et l'encre un bleu-noir plutôt qu'un noir — c'est le réglage d'un
 * livre, pas celui d'une interface.
 *
 * POURQUOI LES TAILLES SONT AUSSI GRANDES
 * ---------------------------------------
 * L'application s'adresse à des enfants de cinq à huit ans qui déchiffrent.
 * Un mot qu'on déchiffre se lit lettre à lettre : il demande beaucoup plus de
 * taille qu'un mot qu'on reconnaît. Les tailles de texte ci-dessous sont donc
 * nettement au-dessus de celles d'une application d'information.
 */

export const couleurs = {
  /** Le fond des pages. */
  fond: '#FBF7F0',
  /** Les cartes et les pastilles posées sur le fond. */
  surface: '#FFFFFF',
  /** Le texte principal — un bleu-noir, jamais du noir pur. */
  encre: '#1B2330',
  /** Le texte secondaire, les légendes. */
  encreDouce: '#5A6472',
  /** Le bleu de l'établissement, celui de l'icône. */
  bleu: '#2554D6',
  /** Le bleu très clair des fonds de pastille. */
  bleuPale: '#E8EEFC',
  /** Le vert des réussites. */
  vert: '#2E9E6B',
  /** Le rouge doux des erreurs — jamais un rouge vif, qui inquiète. */
  rouge: '#D2604A',
  /** Les traits de séparation. */
  trait: '#E7E0D5',
  /** Le jaune de la lumière, pour l'illustration du jeu. */
  jaune: '#F2C14E',
} as const;

export const espace = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
} as const;

export const rayon = {
  carte: 20,
  pastille: 999,
  bouton: 16,
} as const;

export const taille = {
  /** Le titre de l'application. */
  heros: 40,
  /** Le titre d'un écran. */
  titre: 28,
  /** Le titre d'une carte. */
  carte: 22,
  /** Le texte d'un bouton. */
  bouton: 20,
  /** Le texte courant. */
  courant: 18,
  /** Le texte d'un mot à lire — la taille qui compte. */
  lecture: 30,
  /** Les légendes. */
  legende: 15,
} as const;
