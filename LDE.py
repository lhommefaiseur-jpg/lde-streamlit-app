import streamlit as st
import math
from collections import Counter
import unicodedata

# ---------------- CORPUS ÉTENDU ----------------

CORPUS = {
    "français": """
Le langage humain est un système complexe permettant la communication entre individus.
Il repose sur des règles grammaticales et syntaxiques qui structurent les phrases.
L'informatique moderne utilise des algorithmes pour traiter des données textuelles.
La théorie de l'information est fondamentale pour comprendre l'entropie.
Les étudiants en ingénierie apprennent à programmer en Python et C++.
La France est connue pour sa gastronomie et son patrimoine culturel remarquable.
Les forêts françaises couvrent environ un tiers du territoire national.
Bonjour, comment allez-vous aujourd'hui ? Je suis très content de vous voir.
Le gouvernement a adopté de nouvelles mesures économiques ce mois-ci.
Les baguettes, le fromage et le vin sont emblématiques de la cuisine française.
""",
    "espagnol": """
El lenguaje humano es un sistema complejo que permite la comunicación entre personas.
Se basa en reglas gramaticales y sintácticas que organizan las frases.
La informática moderna utiliza algoritmos para procesar datos textuales.
La teoría de la información es fundamental para comprender la entropía.
Los estudiantes de ingeniería aprenden a programar en Python y C++.
España es conocida por su gastronomía y su patrimonio cultural extraordinario.
Los bosques españoles cubren aproximadamente una quinta parte del territorio.
Hola, ¿cómo está usted hoy? Estoy muy contento de verle aquí.
El gobierno ha adoptado nuevas medidas económicas este mes pasado.
Las tapas, la paella y el vino son emblemáticos de la cocina española.
""",
    "anglais": """
Human language is a complex system that enables communication between individuals.
It is based on grammatical and syntactic rules that structure sentences.
Modern computing uses algorithms to process textual data efficiently.
Information theory is essential to understand entropy and complexity.
Engineering students learn programming in Python and C++ at university.
England is known for its rich cultural heritage and history.
Hello, how are you today? I am very happy to see you here.
The government has adopted new economic measures this month.
Fish and chips, tea and scones are emblematic of British cuisine.
"""
}


def normalize_text(text):
    return ''.join(c.lower() for c in text if c.isalpha())

def get_trigram_frequencies(text):
    text = normalize_text(text)
    if len(text) < 3:
        return {}
    trigrams = [text[i:i+3] for i in range(len(text) - 2)]
    total = len(trigrams)
    counts = Counter(trigrams)
    return {k: v / total for k, v in counts.items()}

PROFILS_TRIGRAMMES = {
    langue: get_trigram_frequencies(corpus)
    for langue, corpus in CORPUS.items()
}

# ---------------- DISTANCE ----------------

def distance_langue(freq_text, freq_langue):
    all_keys = set(freq_text.keys()) | set(freq_langue.keys())
    return math.sqrt(
        sum((freq_text.get(k, 0) - freq_langue.get(k, 0)) ** 2 for k in all_keys)
    )

# ---------------- SEUIL DE REJET (langue non supportée) ----------------
# Constat empirique : quand un texte est écrit dans une langue qui
# n'appartient pas au corpus (allemand, italien, néerlandais, turc...),
# sa distance aux 3 profils français/anglais/espagnol reste très
# proche pour les trois — le texte ne "ressemble" vraiment à aucun
# d'entre eux, donc les distances sont quasiment égales.
#
# Pour un texte écrit dans une des 3 langues supportées, la meilleure
# distance se détache nettement de la deuxième (écart relatif observé
# entre 2% et 6%). Pour une langue étrangère, cet écart reste très
# faible (souvent < 1.5%), car aucune des 3 langues ne "gagne" vraiment.
#
# SEUIL_ECART_MIN fixe la limite en dessous de laquelle on considère
# que la détection n'est pas fiable, et donc que le texte n'appartient
# probablement à aucune des 3 langues supportées.
SEUIL_ECART_MIN = 0.015  # 1.5 %

# ---------------- DÉTECTION AVEC CONFIANCE ----------------

def detecter_langue(texte):
    freq_text = get_trigram_frequencies(texte)
    if not freq_text:
        return "Texte trop court", {}, None

    distances = {
        langue: distance_langue(freq_text, profil)
        for langue, profil in PROFILS_TRIGRAMMES.items()
    }

    sorted_langs = sorted(distances.items(), key=lambda x: x[1])
    meilleure_langue, meilleure_dist = sorted_langs[0]
    deuxieme_dist = sorted_langs[1][1]

    # FIX 2 : calcul d'un score de confiance
    ecart_relatif = (deuxieme_dist - meilleure_dist) / meilleure_dist

    # NOUVELLE CONDITION : si l'écart relatif est trop faible, le texte
    # ne se détache pas suffisamment d'une langue à l'autre. On
    # considère alors qu'il est écrit dans une langue non supportée
    # (ou qu'il est trop ambigu/incohérent pour être classé).
    if ecart_relatif < SEUIL_ECART_MIN:
        return "non supportée", distances, ecart_relatif

    return meilleure_langue, distances, ecart_relatif

# ---------------- INTERFACE ----------------

st.title("Détecteur de langue (Trigrammes + NLP)")

st.write(
    "Langues supportées : français, anglais, espagnol. "
    "Tout autre texte sera signalé comme non reconnu."
)

texte = st.text_area("Entrez un texte :", height=200)

if st.button("Analyser"):
    if texte.strip():
        langue, distances, confiance = detecter_langue(texte)

        if langue == "Texte trop court":
            st.error("Texte trop court pour être analysé.")

        elif langue == "non supportée":
            st.error(
                "❌ Langue non reconnue : ce texte ne correspond à aucune "
                "des 3 langues supportées (français, anglais, espagnol). "
                "Vérifiez votre saisie, ou essayez avec un texte plus long "
                "pour une détection plus fiable."
            )
            st.caption(
                f"Écart relatif obtenu : {confiance*100:.2f}% "
                f"(seuil minimum requis : {SEUIL_ECART_MIN*100:.1f}%)"
            )
            with st.expander("Détails des distances"):
                for lang, dist in sorted(distances.items(), key=lambda x: x[1]):
                    st.write(f"**{lang}** : {dist:.4f}")

        else:
            st.success(f"Langue détectée : **{langue}**")

            # FIX 3 : avertissement si la détection est peu fiable
            if confiance < 0.03:
                st.warning(
                    f"⚠️ Confiance modérée ({confiance*100:.1f}% d'écart). "
                    "Le texte est peut-être court ou un peu ambigu entre langues proches."
                )

            # Affichage des distances pour debug
            with st.expander("Détails des distances"):
                for lang, dist in sorted(distances.items(), key=lambda x: x[1]):
                    st.write(f"**{lang}** : {dist:.4f}")
    else:
        st.warning("Veuillez entrer un texte.")
