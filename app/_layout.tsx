/**
 * Racine de l'application.
 *
 * Elle fournit les marges de sécurité et décrit la pile de navigation.
 *
 * POURQUOI LES TITRES SONT DÉCLARÉS ICI
 * -------------------------------------
 * expo-router découvre les écrans à partir des fichiers, mais sans déclaration
 * le titre de l'en-tête est le nom de la route — « lecture », « niveau » — et
 * l'enfant ou le parent y lit un nom de fichier. On déclare donc les titres, et
 * on déclare aussi les écrans qui ne doivent PAS d'en-tête : sans cela ils en
 * reçoivent un, et leur marge haute se cumule avec celle de l'en-tête.
 */

import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import type { JSX } from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { couleurs, taille } from '../theme';

function Pile(): JSX.Element {
  return (
    <>
      <StatusBar style="dark" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: couleurs.fond },
          headerTintColor: couleurs.bleu,
          headerTitleStyle: {
            color: couleurs.encre,
            fontSize: taille.bouton,
            fontWeight: '600',
          },
          headerShadowVisible: false,
          headerBackTitle: 'Retour',
          contentStyle: { backgroundColor: couleurs.fond },
        }}
      >
        {/* L'accueil porte son propre titre en corps de page : un en-tête y
            afficherait « index », et son écran cumulerait deux marges hautes. */}
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="niveau" options={{ title: 'Choisir' }} />
        <Stack.Screen name="lecture" options={{ title: 'Lire' }} />
        <Stack.Screen name="jeu" options={{ title: 'Le mot à trous' }} />
        <Stack.Screen name="unites" options={{ title: "Ce qu'on apprend" }} />
      </Stack>
    </>
  );
}

export default function RootLayout(): JSX.Element {
  return (
    <SafeAreaProvider>
      <Pile />
    </SafeAreaProvider>
  );
}
