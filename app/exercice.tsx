/**
 * Un exercice du CE1 — « toucher la bonne carte ».
 *
 * POURQUOI CET ÉCRAN EXISTE, ET POURQUOI IL EST LE PREMIER
 * --------------------------------------------------------
 * La banque d'exercices du CE1 porte 57 exercices, dont 52 déclarés jouables à
 * l'écran. Aucun n'était rendu. Ceux d'ici sont les treize dont la mécanique
 * reçoit la forme `carte_a_choisir` dans `outils/formes-exercices.json` : lire
 * la question, puis toucher la carte qui y répond. C'est la forme que la donnée
 * porte le plus souvent — `questions` avec une bonne réponse et ses intruses —
 * et c'est aussi celle qui existait déjà, éprouvée, dans le jeu des syllabes.
 *
 * LES AUTRES NE SONT PAS CACHÉS
 * -----------------------------
 * L'écran du niveau affiche, à côté de ces treize, les vingt mécaniques écrites
 * et non rendues, avec leur raison et leur nombre d'exercices. Un exercice écrit
 * qu'on cache est un mensonge ; un exercice écrit qu'on montre comme injouable
 * est un état.
 *
 * POURQUOI LES EXERCICES DE LA GS NE SONT PAS ICI
 * -----------------------------------------------
 * Parce que leur consigne se donne PAR LA VOIX — c'est la règle du projet — et
 * qu'aucun son n'est enregistré. Un enfant de grande section ne lit pas encore
 * la consigne écrite : lui présenter l'exercice sans elle serait lui demander de
 * deviner. C'est mesuré, pas supposé : la table des formes déclare les vingt
 * mécaniques de la GS non rendues, dont dix-sept pour cette seule raison.
 *
 * POURQUOI LE TITRE DU TEXTE N'EST JAMAIS AFFICHÉ
 * -----------------------------------------------
 * La mécanique `choisir_titre` demande de choisir, parmi trois, le titre qui
 * convient au texte lu. Le titre du texte est justement la bonne réponse : le
 * montrer donnerait la réponse. On affiche donc le corps du texte, et jamais son
 * titre — pour toutes les mécaniques, parce qu'une règle qui ne s'applique qu'à
 * un cas est une règle qu'on oubliera d'appliquer au suivant.
 *
 * POURQUOI LES CARTES SONT MÉLANGÉES
 * ----------------------------------
 * Même raison que dans le jeu des syllabes, et le même module : la banque range
 * la bonne réponse en tête, et l'enfant qui touche toujours la première carte
 * gagnerait sans lire. Le mélange vit dans `melange.ts`, où un banc le tient.
 * La graine dépend de la question ET de la partie : la première partie se rejoue
 * à l'identique — utile pour retrouver un défaut signalé —, les suivantes
 * changent d'ordre.
 */

import { Stack, useLocalSearchParams } from 'expo-router';
import type { JSX } from 'react';
import { useMemo, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { niveau as chercherNiveau, texte as chercherTexte, type Exercice } from '../contenu-app';
import { graine, melanger } from '../melange';
import { couleurs, espace, rayon, taille } from '../theme';

export default function EcranExercice(): JSX.Element {
  const { niveau: idNiveau, exercice: idExercice } = useLocalSearchParams<{
    niveau?: string;
    exercice?: string;
  }>();
  const n = idNiveau ? chercherNiveau(idNiveau) : undefined;
  const liste: Exercice[] = n?.exercices ?? [];

  const depart = Math.max(
    0,
    liste.findIndex((e) => e.id === idExercice)
  );

  const [index, setIndex] = useState(depart);
  const [question, setQuestion] = useState(0);
  const [partie, setPartie] = useState(0);
  const [choix, setChoix] = useState<string | null>(null);
  const [fini, setFini] = useState(false);

  const ex = liste[index];
  const q = ex?.questions[question];

  const cartes = useMemo(() => {
    if (!ex || !q) return [];
    // La graine mêle l'exercice, la question et la partie : deux questions d'un
    // même exercice ne se mélangent pas de la même façon, et « Recommencer »
    // change l'ordre.
    return melanger([q.bonne, ...q.intrus], graine(`${ex.id}#q${question}`, partie));
  }, [ex, q, question, partie]);

  if (!n || liste.length === 0) {
    return (
      <View style={styles.vide}>
        <Text style={styles.videTexte}>
          {n ? 'Ce niveau n’a pas encore d’exercice jouable.' : 'Ce niveau n’existe pas.'}
        </Text>
      </View>
    );
  }

  if (fini || !ex || !q) {
    return (
      <View style={styles.vide}>
        <Text style={styles.finTitre}>Terminé !</Text>
        <Text style={styles.finTexte}>
          {liste.length} exercice{liste.length > 1 ? 's' : ''} fait
          {liste.length > 1 ? 's' : ''}.
        </Text>
        <Pressable
          accessibilityRole="button"
          onPress={() => {
            setIndex(0);
            setQuestion(0);
            // Une nouvelle partie change l'ordre des cartes. Sans cela, l'enfant
            // qui recommence retrouve la disposition qu'il vient de mémoriser,
            // et il gagne sans lire — l'exercice s'annulerait lui-même.
            setPartie((p) => p + 1);
            setChoix(null);
            setFini(false);
          }}
          style={styles.bouton}
        >
          <Text style={styles.boutonTexte}>Recommencer</Text>
        </Pressable>
      </View>
    );
  }

  const leTexte = ex.texte ? chercherTexte(n.id, ex.texte) : undefined;
  const reussi = choix === q.bonne;
  const plusieurs = ex.questions.length > 1;

  function suivant(): void {
    setChoix(null);
    if (question + 1 < ex!.questions.length) {
      setQuestion(question + 1);
    } else if (index + 1 < liste.length) {
      setIndex(index + 1);
      setQuestion(0);
    } else {
      setFini(true);
    }
  }

  return (
    <>
      <Stack.Screen options={{ title: `${n.court} · s’entraîner` }} />
      <ScrollView contentContainerStyle={styles.contenu}>
        <Text style={styles.compteur}>
          exercice {index + 1} sur {liste.length}
          {plusieurs ? ` · question ${question + 1} sur ${ex.questions.length}` : ''}
        </Text>

        {ex.consigne ? <Text style={styles.consigne}>{ex.consigne}</Text> : null}

        {/* Le corps du texte, jamais son titre : le titre est la réponse de la
            mécanique « choisir le titre ». */}
        {leTexte ? (
          <View style={styles.texte}>
            {leTexte.lignes.map((ligne, i) => (
              <Text key={`${leTexte.id}-${i}`} style={styles.texteLigne}>
                {ligne}
              </Text>
            ))}
          </View>
        ) : null}

        <Text style={styles.question}>{q.question}</Text>

        <View style={styles.cartes}>
          {cartes.map((carte) => (
            <Pressable
              key={`${ex.id}-${question}-${carte}`}
              accessibilityRole="button"
              accessibilityLabel={`Carte ${carte}`}
              onPress={() => {
                if (!reussi) setChoix(carte);
              }}
              style={({ pressed }) => [
                styles.carte,
                pressed && styles.cartePressee,
                choix === carte && reussi && styles.carteReussie,
                choix === carte && !reussi && styles.carteRatee,
              ]}
            >
              <Text style={styles.carteTexte}>{carte}</Text>
            </Pressable>
          ))}
        </View>

        {choix === null ? null : reussi ? (
          <>
            <Text style={styles.bravo}>Bravo, c’est la bonne réponse.</Text>
            {q.phrase_preuve ? (
              <Text style={styles.preuve}>« {q.phrase_preuve} »</Text>
            ) : null}
            <Pressable accessibilityRole="button" onPress={suivant} style={styles.bouton}>
              <Text style={styles.boutonTexte}>
                {question + 1 < ex.questions.length
                  ? 'Question suivante'
                  : index + 1 < liste.length
                    ? 'Exercice suivant'
                    : 'Voir la fin'}
              </Text>
            </Pressable>
          </>
        ) : (
          <Text style={styles.encore}>Non, ce n’est pas celle-là. Essaie encore.</Text>
        )}

        <Text style={styles.note}>
          Le son n’est pas encore enregistré : la consigne se lit. L’exercice se joue en
          lisant.
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
  consigne: {
    fontSize: taille.bouton,
    color: couleurs.bleu,
    fontWeight: '700',
    textAlign: 'center',
    marginTop: espace.md,
  },
  texte: {
    backgroundColor: couleurs.surface,
    borderRadius: rayon.carte,
    padding: espace.md,
    marginTop: espace.lg,
  },
  texteLigne: {
    fontSize: taille.courant,
    lineHeight: 32,
    color: couleurs.encre,
  },
  question: {
    fontSize: taille.carte,
    fontWeight: '700',
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
    minWidth: 140,
    maxWidth: 320,
    paddingHorizontal: espace.lg,
    paddingVertical: espace.md,
    borderRadius: rayon.bouton,
    backgroundColor: couleurs.surface,
    borderWidth: 2,
    borderColor: couleurs.trait,
    alignItems: 'center',
  },
  cartePressee: { opacity: 0.7 },
  carteReussie: { borderColor: couleurs.vert, backgroundColor: '#E4F5EC' },
  carteRatee: { borderColor: couleurs.rouge, backgroundColor: '#FBEAE6' },
  carteTexte: {
    fontSize: taille.courant,
    fontWeight: '700',
    color: couleurs.encre,
    textAlign: 'center',
  },
  bravo: {
    fontSize: taille.courant,
    color: couleurs.vert,
    fontWeight: '700',
    textAlign: 'center',
    marginTop: espace.lg,
  },
  preuve: {
    fontSize: taille.legende,
    color: couleurs.encreDouce,
    textAlign: 'center',
    marginTop: espace.sm,
    fontStyle: 'italic',
  },
  encore: {
    fontSize: taille.courant,
    color: couleurs.rouge,
    textAlign: 'center',
    marginTop: espace.lg,
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
