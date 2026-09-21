/**
 * Le mélange des cartes du mot à trous.
 *
 * POURQUOI CE FICHIER EXISTE, ALORS QUE LE MÉLANGE TIENT EN QUINZE LIGNES
 * ----------------------------------------------------------------------
 * Parce qu'il est éprouvable ici et qu'il ne l'était pas dans l'écran.
 * `app/jeu.tsx` importe React Native : un banc ne peut pas le charger, donc la
 * seule façon de vérifier que le mélange fait son travail était de le relire.
 * Mesuré une fois à la main — sur les 42 items, la bonne carte tombe 14 fois en
 * première position, 14 fois en deuxième, 14 fois en troisième —, ce n'est plus
 * mesuré du tout dès que quelqu'un retouche la fonction ou réordonne le corpus.
 *
 * Ce module n'importe RIEN. C'est ce qui le rend éprouvable, et c'est une
 * décision de conception, pas de rangement.
 *
 * CE QUE LE MÉLANGE DOIT GARANTIR
 * -------------------------------
 * Le corpus déclare les cartes dans l'ordre « la bonne, puis les intruses ».
 * C'est le bon ordre pour un fichier et le pire pour un jeu : l'enfant qui
 * touche toujours la première carte gagne sans lire, et il apprend cela en trois
 * items. Le mélange doit donc déplacer la bonne carte, pour chaque item.
 *
 * POURQUOI LA GRAINE DÉPEND AUSSI DE LA PARTIE
 * --------------------------------------------
 * La graine contient l'identifiant de l'item, donc l'ordre est reproductible :
 * la **première** partie se rejoue à l'identique, ce qui permet de retrouver un
 * défaut d'affichage signalé par un parent, ou de comparer deux versions de
 * l'application sur la même disposition.
 *
 * Mais si la graine ne dépendait QUE de l'item, l'ordre serait figé pour
 * toujours. Au troisième passage, l'enfant aurait mémorisé que `pa` est la
 * première carte de `papa`, et il gagnerait sans lire — exactement ce que le
 * mélange existe pour empêcher. Un jeu qui se joue une fois n'a pas ce défaut ;
 * un jeu qui a un bouton « Recommencer » l'a.
 *
 * Le numéro de partie entre donc dans la graine. La première reste
 * reproductible ; les suivantes ne se ressemblent pas.
 */

/**
 * Mélange les cartes, de façon reproductible.
 *
 * @param cartes les cartes, dans l'ordre du corpus — la bonne en tête
 * @param graine  ce qui détermine l'ordre, voir `graine()`
 * @returns une **permutation** des cartes : jamais une carte perdue, jamais une
 *          carte en double
 */
export function melanger(cartes: string[], graine: string): string[] {
  // FNV-1a pour réduire la graine à un entier, puis un générateur congruentiel
  // pour tirer les échanges. Deux primitives courtes et déterministes, sans
  // dépendance.
  //
  // `Math.imul` n'est pas un détail : une multiplication ordinaire au-delà de
  // 2^53 perd des bits, et le mélange dépendrait alors du moteur JavaScript —
  // l'ordre serait reproductible sur une machine et pas sur une autre.
  let h = 2166136261;
  for (let i = 0; i < graine.length; i += 1) {
    h ^= graine.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }

  // Un échange de Fisher-Yates, du dernier vers le premier.
  const melange = [...cartes];
  for (let i = melange.length - 1; i > 0; i -= 1) {
    h = Math.imul(h ^ (h >>> 15), 2246822507);
    const j = Math.abs(h) % (i + 1);
    const a = melange[i] as string;
    const b = melange[j] as string;
    melange[i] = b;
    melange[j] = a;
  }
  return melange;
}

/**
 * La graine d'un item : son identifiant, et le numéro de partie.
 *
 * La convention vit ici, et non dans l'écran, pour la même raison que le
 * mélange : c'est une règle qu'un banc peut tenir, donc elle doit être du côté
 * que le banc atteint. La partie 0 rend l'identifiant **nu** — la première
 * partie est ainsi reproductible d'une version à l'autre, même si le format de
 * la graine changeait un jour.
 */
export function graine(itemId: string, partie: number): string {
  return partie === 0 ? itemId : `${itemId}#${partie}`;
}
