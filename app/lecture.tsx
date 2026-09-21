/**
 * L'écran de lecture.
 *
 * C'EST L'ÉCRAN QUI COMPTE
 * ------------------------
 * Tout le reste de l'application y mène. Trois décisions y sont prises, et
 * chacune vient d'une contrainte de lecture plutôt que d'un goût :
 *
 *   - LE TEXTE EST EN GROS ET AÉRÉ. Un enfant qui déchiffre lit lettre à
 *     lettre ; il a besoin de plus de taille et de plus d'interligne qu'un
 *     lecteur adulte, et d'un fond crème plutôt que blanc.
 *   - LES MOTS SONT SÉPARÉS ET TOUCHABLES. Toucher un mot le met en évidence.
 *     Aujourd'hui c'est tout ce que cela fait — aucun son n'est enregistré.
 *     L'écran le dit, plutôt que de laisser croire à un bouton muet.
 *   - LA PONCTUATION RESTE COLLÉE AU MOT. Un point séparé par une espace se
 *     lit comme un mot de plus, et l'enfant compte une syllabe qui n'existe pas.
 */

import { Stack, useLocalSearchParams } from 'expo-router';
import type { JSX } from 'react';
import { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { niveau as chercherNiveau, texte as chercherTexte } from '../contenu-app';
import { couleurs, espace, rayon, taille } from '../theme';

/** Un mot, et la ponctuation qui le suit, inséparables à l'écran. */
function motsDe(ligne: string): string[] {
  return ligne.split(/\s+/).filter(Boolean);
}

export default function EcranLecture(): JSX.Element {
  const { niveau: idNiveau, texte: idTexte } = useLocalSearchParams<{
    niveau?: string;
    texte?: string;
  }>();
  const [motTouche, setMotTouche] = useState<string | null>(null);

  const n = idNiveau ? chercherNiveau(idNiveau) : undefined;
  const t = idNiveau && idTexte ? chercherTexte(idNiveau, idTexte) : undefined;

  if (!n || !t) {
    return (
      <View style={styles.vide}>
        <Text style={styles.videTexte}>Ce texte n&apos;existe pas.</Text>
      </View>
    );
  }

  return (
    <>
      <Stack.Screen options={{ title: t.titre }} />
      <ScrollView contentContainerStyle={styles.contenu}>
        <Text style={styles.titre}>{t.titre}</Text>
        <Text style={styles.legende}>
          {n.court}
          {t.rang === null ? '' : ` · rang ${t.rang}`}
          {t.genre === null ? '' : ` · ${t.genre}`}
        </Text>

        <View style={styles.page}>
          {t.lignes.map((ligne, i) => (
            <View key={`${t.id}-${i}`} style={styles.ligne}>
              {motsDe(ligne).map((mot, j) => (
                <Pressable
                  key={`${t.id}-${i}-${j}`}
                  accessibilityRole="button"
                  accessibilityLabel={mot}
                  onPress={() => setMotTouche(mot)}
                >
                  <Text style={[styles.mot, motTouche === mot && styles.motTouche]}>{mot}</Text>
                </Pressable>
              ))}
            </View>
          ))}
        </View>

        <Text style={styles.note}>
          Touche un mot pour le mettre en évidence. Le son n&apos;est pas encore enregistré : rien
          ne se dit pour l&apos;instant.
        </Text>
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  contenu: { paddingBottom: espace.xxl },
  titre: {
    fontSize: taille.titre,
    fontWeight: '800',
    color: couleurs.encre,
    paddingHorizontal: espace.lg,
    paddingTop: espace.lg,
  },
  legende: {
    fontSize: taille.legende,
    color: couleurs.encreDouce,
    paddingHorizontal: espace.lg,
    marginTop: espace.xs,
  },
  page: {
    margin: espace.lg,
    padding: espace.lg,
    backgroundColor: couleurs.surface,
    borderRadius: rayon.carte,
    gap: espace.md,
  },
  ligne: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: espace.sm,
  },
  mot: {
    fontSize: taille.lecture,
    lineHeight: 46,
    color: couleurs.encre,
  },
  motTouche: {
    backgroundColor: couleurs.jaune,
    color: couleurs.encre,
    borderRadius: rayon.bouton,
    paddingHorizontal: espace.xs,
  },
  note: {
    fontSize: taille.legende,
    color: couleurs.encreDouce,
    paddingHorizontal: espace.lg,
    lineHeight: 22,
  },
  vide: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  videTexte: { fontSize: taille.courant, color: couleurs.encreDouce },
});
