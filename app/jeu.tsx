/**
 * Le mot à trous — le jeu des syllabes manquantes.
 *
 * LA SEULE ACTIVITÉ ENTIÈREMENT JOUABLE AUJOURD'HUI
 * -------------------------------------------------
 * Toutes les autres activités du projet reposent sur la voix, et aucun son
 * n'est enregistré. Celle-ci se joue avec les yeux et le doigt : un mot, une
 * syllabe manquante, des cartes à poser. C'est donc la première à livrer.
 *
 * POURQUOI L'APPLICATION MÉLANGE LES CARTES
 * -----------------------------------------
 * Le corpus déclare les cartes dans l'ordre « la bonne, puis les intruses ».
 * C'est le bon ordre pour un fichier, et le pire pour un jeu : l'enfant qui
 * touche toujours la première carte gagne sans lire, et il apprend cela en
 * trois items.
 *
 * Le mélange lui-même vit dans `melange.ts`, et non ici, pour une raison
 * mesurable : cet écran importe React Native, donc un banc ne peut pas le
 * charger, donc **rien** ne pouvait vérifier que le mélange déplace réellement
 * la bonne carte. La règle est dans le module, le banc la tient.
 *
 * L'écran, lui, tient le numéro de PARTIE. La graine dépend de l'item et de la
 * partie : la première partie se rejoue à l'identique — utile pour retrouver un
 * défaut signalé par un parent —, mais les suivantes changent d'ordre. Sans
 * cela l'ordre serait figé pour toujours, et l'enfant qui touche « Recommencer »
 * retrouverait la disposition qu'il vient de mémoriser : il gagnerait sans lire
 * au troisième passage, ce que le mélange existe précisément pour empêcher.
 *
 * POURQUOI LA BONNE RÉPONSE N'EST PAS DANS LE CONTENU
 * ---------------------------------------------------
 * Elle se déduit : c'est la syllabe du mot à la place du trou. Le contenu
 * embarqué ne la recopie nulle part, donc rien ne peut diverger entre la
 * question et sa réponse.
 */

import { Stack, useLocalSearchParams } from 'expo-router';
import type { JSX } from 'react';
import { useMemo, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { niveau as chercherNiveau, type ItemJeu } from '../contenu-app';
import { graine, melanger } from '../melange';
import { couleurs, espace, rayon, taille } from '../theme';

export default function EcranJeu(): JSX.Element {
  const { niveau: idNiveau } = useLocalSearchParams<{ niveau?: string }>();
  const n = idNiveau ? chercherNiveau(idNiveau) : undefined;
  const items: ItemJeu[] = n?.jeu_syllabes ?? [];

  const [index, setIndex] = useState(0);
  const [partie, setPartie] = useState(0);
  const [posee, setPosee] = useState<string | null>(null);
  const [fini, setFini] = useState(false);

  const item = items[index];
  const cartes = useMemo(
    () => (item ? melanger(item.cartes, graine(item.id, partie)) : []),
    [item, partie]
  );

  if (!n || items.length === 0) {
    return (
      <View style={styles.vide}>
        <Text style={styles.videTexte}>
          {n ? 'Ce niveau n\u2019a pas encore de jeu.' : 'Ce niveau n\u2019existe pas.'}
        </Text>
      </View>
    );
  }

  if (fini || !item) {
    return (
      <View style={styles.vide}>
        <Text style={styles.finTitre}>Terminé !</Text>
        <Text style={styles.finTexte}>
          {items.length} mot{items.length > 1 ? 's' : ''} complété
          {items.length > 1 ? 's' : ''}.
        </Text>
        <Pressable
          accessibilityRole="button"
          onPress={() => {
            setIndex(0);
            // Une nouvelle partie change l'ordre des cartes. Sans cela, l'enfant
            // qui recommence retrouve la disposition qu'il vient de mémoriser,
            // et il gagne sans lire — le jeu s'annulerait lui-même.
            setPartie((p) => p + 1);
            setPosee(null);
            setFini(false);
          }}
          style={styles.bouton}
        >
          <Text style={styles.boutonTexte}>Recommencer</Text>
        </Pressable>
      </View>
    );
  }

  const bonne = item.syllabes[item.trou] as string;
  const reussi = posee === bonne;

  function poser(carte: string): void {
    if (reussi) return;
    setPosee(carte);
  }

  function suivante(): void {
    setPosee(null);
    if (index + 1 >= items.length) {
      setFini(true);
    } else {
      setIndex(index + 1);
    }
  }

  return (
    <>
      <Stack.Screen options={{ title: `${n.court} · le mot à trous` }} />
      <ScrollView contentContainerStyle={styles.contenu}>
        <Text style={styles.compteur}>
          mot {index + 1} sur {items.length}
        </Text>

        {/* Le mot, découpé en cases. La case du trou reste vide tant que rien
            n'est posé, et c'est la seule qui puisse l'être. */}
        <View style={styles.mot}>
          {item.syllabes.map((syllabe, i) => {
            const estLeTrou = i === item.trou;
            const contenu = estLeTrou ? (posee ?? '') : syllabe;
            return (
              <View
                key={`${item.id}-${i}`}
                style={[
                  styles.case,
                  estLeTrou && styles.caseTrou,
                  estLeTrou && reussi && styles.caseReussie,
                  estLeTrou && posee !== null && !reussi && styles.caseRatee,
                ]}
              >
                <Text style={styles.caseTexte}>{contenu}</Text>
              </View>
            );
          })}
        </View>

        <Text style={styles.consigne}>
          {posee === null
            ? 'Quelle syllabe manque ?'
            : reussi
              ? 'Bravo, c\u2019est le bon mot.'
              : 'Non, ce n\u2019est pas ce mot. Essaie encore.'}
        </Text>

        <View style={styles.cartes}>
          {cartes.map((carte) => (
            <Pressable
              key={`${item.id}-carte-${carte}`}
              accessibilityRole="button"
              accessibilityLabel={`Carte ${carte}`}
              onPress={() => poser(carte)}
              style={({ pressed }) => [styles.carte, pressed && styles.cartePressee]}
            >
              <Text style={styles.carteTexte}>{carte}</Text>
            </Pressable>
          ))}
        </View>

        {reussi ? (
          <Pressable accessibilityRole="button" onPress={suivante} style={styles.bouton}>
            <Text style={styles.boutonTexte}>
              {index + 1 >= items.length ? 'Voir la fin' : 'Mot suivant'}
            </Text>
          </Pressable>
        ) : null}

        <Text style={styles.note}>
          Le son n&apos;est pas encore enregistré : le mot ne se dit pas. Pour l&apos;instant, le
          jeu se joue en regardant le mot écrit.
        </Text>
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  contenu: { padding: espace.lg, paddingBottom: espace.xxl },
  compteur: {
    fontSize: taille.legende,
    color: couleurs.encreDouce,
    textAlign: 'center',
  },
  mot: {
    flexDirection: 'row',
    justifyContent: 'center',
    flexWrap: 'wrap',
    gap: espace.sm,
    marginTop: espace.lg,
  },
  case: {
    minWidth: 96,
    paddingHorizontal: espace.md,
    paddingVertical: espace.md,
    borderRadius: rayon.bouton,
    backgroundColor: couleurs.surface,
    alignItems: 'center',
  },
  caseTrou: {
    borderWidth: 2,
    borderStyle: 'dashed',
    borderColor: couleurs.bleu,
    backgroundColor: couleurs.bleuPale,
  },
  caseReussie: { borderStyle: 'solid', borderColor: couleurs.vert, backgroundColor: '#E4F5EC' },
  caseRatee: { borderStyle: 'solid', borderColor: couleurs.rouge, backgroundColor: '#FBEAE6' },
  caseTexte: {
    fontSize: taille.lecture,
    fontWeight: '700',
    color: couleurs.encre,
  },
  consigne: {
    fontSize: taille.courant,
    color: couleurs.encre,
    textAlign: 'center',
    marginTop: espace.lg,
  },
  cartes: {
    flexDirection: 'row',
    justifyContent: 'center',
    flexWrap: 'wrap',
    gap: espace.md,
    marginTop: espace.lg,
  },
  carte: {
    minWidth: 96,
    paddingHorizontal: espace.lg,
    paddingVertical: espace.md,
    borderRadius: rayon.bouton,
    backgroundColor: couleurs.surface,
    borderWidth: 2,
    borderColor: couleurs.trait,
    alignItems: 'center',
  },
  cartePressee: { opacity: 0.7 },
  carteTexte: {
    fontSize: taille.lecture,
    fontWeight: '700',
    color: couleurs.bleu,
  },
  bouton: {
    alignSelf: 'center',
    marginTop: espace.xl,
    backgroundColor: couleurs.bleu,
    paddingHorizontal: espace.xl,
    paddingVertical: espace.md,
    borderRadius: rayon.bouton,
  },
  boutonTexte: {
    color: couleurs.surface,
    fontSize: taille.bouton,
    fontWeight: '700',
  },
  note: {
    marginTop: espace.xl,
    fontSize: taille.legende,
    color: couleurs.encreDouce,
    textAlign: 'center',
    lineHeight: 22,
  },
  vide: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: espace.sm },
  videTexte: { fontSize: taille.courant, color: couleurs.encreDouce },
  finTitre: { fontSize: taille.titre, fontWeight: '800', color: couleurs.vert },
  finTexte: { fontSize: taille.courant, color: couleurs.encreDouce },
});
