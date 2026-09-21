/**
 * Ce qu'un niveau propose.
 *
 * L'écran montre ce qui EXISTE, et seulement ce qui existe. Un niveau sans
 * texte n'affiche pas une section « Lire » vide avec un message d'excuse : il
 * n'affiche pas la section. C'est la même règle que partout ailleurs dans le
 * projet — une promesse qui ne se remplit pas se voit, et se voit comme un
 * manque plutôt que comme un défaut.
 */

import { Stack, useLocalSearchParams, useRouter } from 'expo-router';
import type { JSX } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { niveau as chercherNiveau, type Niveau } from '../contenu-app';
import { couleurs, espace, rayon, taille } from '../theme';

function Ligne({
  titre,
  detail,
  onPress,
}: {
  titre: string;
  detail?: string;
  onPress: () => void;
}): JSX.Element {
  return (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      style={({ pressed }) => [styles.ligne, pressed && styles.lignePressee]}
    >
      <Text style={styles.ligneTitre}>{titre}</Text>
      {detail ? <Text style={styles.ligneDetail}>{detail}</Text> : null}
      <Text style={styles.chevron}>›</Text>
    </Pressable>
  );
}

function Section({ titre, children }: { titre: string; children: React.ReactNode }): JSX.Element {
  return (
    <View style={styles.section}>
      <Text style={styles.sectionTitre}>{titre}</Text>
      <View style={styles.bloc}>{children}</View>
    </View>
  );
}

export default function EcranNiveau(): JSX.Element {
  const { niveau: id } = useLocalSearchParams<{ niveau?: string }>();
  const router = useRouter();
  const n: Niveau | undefined = id ? chercherNiveau(id) : undefined;

  if (!n) {
    return (
      <View style={styles.vide}>
        <Text style={styles.videTexte}>Ce niveau n&apos;existe pas.</Text>
      </View>
    );
  }

  return (
    <>
      <Stack.Screen options={{ title: n.court }} />
      <ScrollView contentContainerStyle={styles.contenu}>
        <View style={[styles.enTete, { backgroundColor: n.couleur }]}>
          <Text style={styles.enTeteNom}>{n.nom}</Text>
          <Text style={styles.enTeteSousTitre}>{n.sous_titre}</Text>
        </View>

        {n.textes.length > 0 ? (
          <Section titre="Lire">
            {n.textes.map((t) => (
              <Ligne
                key={t.id}
                titre={t.titre}
                detail={t.rang === null ? undefined : `rang ${t.rang}`}
                onPress={() =>
                  router.push({ pathname: '/lecture', params: { niveau: n.id, texte: t.id } })
                }
              />
            ))}
          </Section>
        ) : null}

        {n.jeu_syllabes.length > 0 ? (
          <Section titre="Jouer">
            <Ligne
              titre="Le mot à trous"
              detail={`${n.jeu_syllabes.length} mots — une syllabe manque`}
              onPress={() => router.push({ pathname: '/jeu', params: { niveau: n.id } })}
            />
          </Section>
        ) : null}

        {n.correspondances.length > 0 ? (
          <Section titre="Les sons et leurs lettres">
            {n.correspondances.map((c) => (
              <View key={c.rang} style={styles.son}>
                <Text style={styles.sonPhoneme}>{c.phoneme}</Text>
                <Text style={styles.sonGraphies}>{c.graphies.join('  ·  ')}</Text>
                <Text style={styles.sonSemaine}>
                  {c.semaine === null ? '' : `semaine ${c.semaine}`}
                </Text>
              </View>
            ))}
          </Section>
        ) : null}

        {n.unites.length > 0 ? (
          <Section titre="Ce qu'on apprend">
            <Ligne
              titre={`Les ${n.unites.length} étapes du niveau`}
              detail="les objectifs, dans l'ordre"
              onPress={() => router.push({ pathname: '/unites', params: { niveau: n.id } })}
            />
          </Section>
        ) : null}
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  contenu: { paddingBottom: espace.xxl },
  enTete: {
    paddingHorizontal: espace.lg,
    paddingVertical: espace.lg,
  },
  enTeteNom: {
    fontSize: taille.titre,
    fontWeight: '800',
    color: couleurs.surface,
  },
  enTeteSousTitre: {
    fontSize: taille.legende,
    color: couleurs.surface,
    opacity: 0.9,
    marginTop: espace.xs,
  },
  section: { marginTop: espace.lg, paddingHorizontal: espace.lg },
  sectionTitre: {
    fontSize: taille.legende,
    fontWeight: '700',
    color: couleurs.encreDouce,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: espace.sm,
  },
  bloc: {
    backgroundColor: couleurs.surface,
    borderRadius: rayon.carte,
    overflow: 'hidden',
  },
  ligne: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: espace.md,
    paddingHorizontal: espace.md,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: couleurs.trait,
  },
  lignePressee: { backgroundColor: couleurs.bleuPale },
  ligneTitre: {
    flex: 1,
    fontSize: taille.courant,
    color: couleurs.encre,
    fontWeight: '600',
  },
  ligneDetail: {
    fontSize: taille.legende,
    color: couleurs.encreDouce,
    marginRight: espace.sm,
  },
  chevron: {
    fontSize: taille.carte,
    color: couleurs.bleu,
    fontWeight: '700',
  },
  son: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: espace.sm,
    paddingHorizontal: espace.md,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: couleurs.trait,
  },
  sonPhoneme: {
    width: 72,
    fontSize: taille.courant,
    color: couleurs.bleu,
    fontWeight: '700',
  },
  sonGraphies: {
    flex: 1,
    fontSize: taille.courant,
    color: couleurs.encre,
  },
  sonSemaine: {
    fontSize: taille.legende,
    color: couleurs.encreDouce,
  },
  vide: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  videTexte: { fontSize: taille.courant, color: couleurs.encreDouce },
});
