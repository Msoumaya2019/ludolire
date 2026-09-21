/**
 * L'accueil : le nom de l'application, et le choix du niveau.
 *
 * POURQUOI LE CHOIX DU NIVEAU EST SUR L'ACCUEIL
 * ---------------------------------------------
 * L'application est destinée à trois tranches d'âge qui ne font pas la même
 * chose. Mettre ce choix derrière un menu obligerait à lire une interface avant
 * de lire quoi que ce soit, ce qui est exactement ce qu'un enfant qui apprend à
 * lire ne peut pas faire. Les trois niveaux sont donc posés côte à côte, avec
 * leur couleur, et rien d'autre à comprendre.
 */

import { useRouter } from 'expo-router';
import type { JSX } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ceQuOnPeutFaire, meta, niveaux } from '../contenu-app';
import { couleurs, espace, rayon, taille } from '../theme';

function CarteNiveau({
  id,
  court,
  nom,
  sousTitre,
  couleur,
  capacites,
}: {
  id: string;
  court: string;
  nom: string;
  sousTitre: string;
  couleur: string;
  capacites: string[];
}): JSX.Element {
  const router = useRouter();
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={`Niveau ${nom}`}
      onPress={() => router.push({ pathname: '/niveau', params: { niveau: id } })}
      style={({ pressed }) => [
        styles.carte,
        { borderLeftColor: couleur },
        pressed && styles.cartePressee,
      ]}
    >
      <View style={[styles.pastille, { backgroundColor: couleur }]}>
        <Text style={styles.pastilleTexte}>{court}</Text>
      </View>
      <View style={styles.carteCorps}>
        <Text style={styles.carteNom}>{nom}</Text>
        <Text style={styles.carteSousTitre}>{sousTitre}</Text>
        <Text style={styles.carteCapacites}>{capacites.join(' · ')}</Text>
      </View>
    </Pressable>
  );
}

export default function Accueil(): JSX.Element {
  return (
    <SafeAreaView style={styles.ecran} edges={['top', 'left', 'right']}>
      <ScrollView contentContainerStyle={styles.contenu}>
        <Text style={styles.etablissement}>{meta.etablissement}</Text>
        <Text style={styles.titre}>{meta.titre}</Text>
        <Text style={styles.sousTitre}>{meta.sous_titre}</Text>

        <View style={styles.cartes}>
          {niveaux.map((n) => (
            <CarteNiveau
              key={n.id}
              id={n.id}
              court={n.court}
              nom={n.nom}
              sousTitre={n.sous_titre}
              couleur={n.couleur}
              capacites={ceQuOnPeutFaire(n)}
            />
          ))}
        </View>

        {/* Ce que l'application ne fait pas encore, dit à l'écran plutôt que
            caché : rien n'est enregistré à ce jour, et une activité qui
            demanderait la voix ne peut pas fonctionner. */}
        <View style={styles.note}>
          <Text style={styles.noteTitre}>À savoir</Text>
          <Text style={styles.noteTexte}>{meta.audio}</Text>
        </View>

        <Text style={styles.pied}>
          Version {meta.version} · contenu {meta.empreinte}
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  ecran: { flex: 1, backgroundColor: couleurs.fond },
  contenu: {
    paddingHorizontal: espace.lg,
    paddingBottom: espace.xxl,
    paddingTop: espace.lg,
  },
  etablissement: {
    fontSize: taille.legende,
    color: couleurs.encreDouce,
    letterSpacing: 0.5,
    textTransform: 'uppercase',
  },
  titre: {
    fontSize: taille.heros,
    fontWeight: '800',
    color: couleurs.bleu,
    marginTop: espace.xs,
  },
  sousTitre: {
    fontSize: taille.courant,
    color: couleurs.encreDouce,
    marginTop: espace.xs,
    marginBottom: espace.xl,
  },
  cartes: { gap: espace.md },
  carte: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: couleurs.surface,
    borderRadius: rayon.carte,
    borderLeftWidth: 6,
    padding: espace.md,
    gap: espace.md,
  },
  cartePressee: { opacity: 0.7 },
  pastille: {
    width: 64,
    height: 64,
    borderRadius: rayon.pastille,
    alignItems: 'center',
    justifyContent: 'center',
  },
  pastilleTexte: {
    color: couleurs.surface,
    fontSize: taille.carte,
    fontWeight: '800',
  },
  carteCorps: { flex: 1 },
  carteNom: {
    fontSize: taille.carte,
    fontWeight: '700',
    color: couleurs.encre,
  },
  carteSousTitre: {
    fontSize: taille.legende,
    color: couleurs.encreDouce,
    marginTop: 2,
  },
  carteCapacites: {
    fontSize: taille.legende,
    color: couleurs.bleu,
    marginTop: espace.xs,
  },
  note: {
    marginTop: espace.xl,
    backgroundColor: couleurs.bleuPale,
    borderRadius: rayon.carte,
    padding: espace.md,
  },
  noteTitre: {
    fontSize: taille.legende,
    fontWeight: '700',
    color: couleurs.bleu,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  noteTexte: {
    fontSize: taille.legende,
    color: couleurs.encre,
    marginTop: espace.xs,
    lineHeight: 22,
  },
  pied: {
    marginTop: espace.xl,
    fontSize: taille.legende,
    color: couleurs.encreDouce,
    textAlign: 'center',
  },
});
