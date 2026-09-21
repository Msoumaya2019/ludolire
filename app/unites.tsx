/**
 * Ce qu'on apprend, dans l'ordre.
 *
 * CET ÉCRAN EST POUR L'ADULTE, PAS POUR L'ENFANT
 * ----------------------------------------------
 * Il ne se joue pas : il se lit. C'est la progression du programme, rang par
 * rang, telle qu'elle est écrite dans les corpus. Il sert au parent qui veut
 * savoir ce que son enfant travaille, et à l'enseignant qui veut vérifier que
 * l'application suit bien le programme.
 *
 * C'est la raison pour laquelle il est sobre : pas de couleur de niveau, pas
 * d'illustration, pas de bouton. Le seul ornement est le rang.
 */

import { Stack, useLocalSearchParams } from 'expo-router';
import type { JSX } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

import { niveau as chercherNiveau } from '../contenu-app';
import { couleurs, espace, rayon, taille } from '../theme';

export default function EcranUnites(): JSX.Element {
  const { niveau: id } = useLocalSearchParams<{ niveau?: string }>();
  const n = id ? chercherNiveau(id) : undefined;

  if (!n) {
    return (
      <View style={styles.vide}>
        <Text style={styles.videTexte}>Ce niveau n&apos;existe pas.</Text>
      </View>
    );
  }

  return (
    <>
      <Stack.Screen options={{ title: `${n.court} — les étapes` }} />
      <ScrollView contentContainerStyle={styles.contenu}>
        {n.unites.map((u) => (
          <View key={u.rang} style={styles.unite}>
            <View style={[styles.rang, { backgroundColor: n.couleur }]}>
              <Text style={styles.rangTexte}>{u.rang}</Text>
            </View>
            <View style={styles.corps}>
              <Text style={styles.objectif}>{u.objectif}</Text>
              {u.action === null ? null : <Text style={styles.action}>{u.action}</Text>}
              {u.domaine === null ? null : <Text style={styles.domaine}>{u.domaine}</Text>}
            </View>
          </View>
        ))}
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  contenu: { padding: espace.lg, paddingBottom: espace.xxl, gap: espace.sm },
  unite: {
    flexDirection: 'row',
    gap: espace.md,
    backgroundColor: couleurs.surface,
    borderRadius: rayon.carte,
    padding: espace.md,
  },
  rang: {
    width: 40,
    height: 40,
    borderRadius: rayon.pastille,
    alignItems: 'center',
    justifyContent: 'center',
  },
  rangTexte: { color: couleurs.surface, fontSize: taille.legende, fontWeight: '800' },
  corps: { flex: 1 },
  objectif: { fontSize: taille.courant, color: couleurs.encre, fontWeight: '600' },
  action: {
    fontSize: taille.legende,
    color: couleurs.encreDouce,
    marginTop: espace.xs,
    lineHeight: 22,
  },
  domaine: {
    fontSize: taille.legende,
    color: couleurs.bleu,
    marginTop: espace.xs,
    letterSpacing: 0.5,
  },
  vide: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  videTexte: { fontSize: taille.courant, color: couleurs.encreDouce },
});
