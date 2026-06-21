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

# ---------------- DÉTECTION AVEC CONFIANCE ----------------

def detecter_langue(texte):
    freq_text = get_trigram_frequencies(texte)
    if not freq_text:
        return "Texte trop court", {}

    distances = {
        langue: distance_langue(freq_text, profil)
        for langue, profil in PROFILS_TRIGRAMMES.items()
    }

    sorted_langs = sorted(distances.items(), key=lambda x: x[1])
    meilleure_langue, meilleure_dist = sorted_langs[0]
    deuxieme_dist = sorted_langs[1][1]

    # FIX 2 : calcul d'un score de confiance
    ecart_relatif = (deuxieme_dist - meilleure_dist) / meilleure_dist

    return meilleure_langue, distances, ecart_relatif

# ---------------- INTERFACE ----------------

st.title("Détecteur de langue (Trigrammes + NLP)")

texte = st.text_area("Entrez un texte :", height=200)

if st.button("Analyser"):
    if texte.strip():
        langue, distances, confiance = detecter_langue(texte)

        st.success(f"Langue détectée : **{langue}**")

        # FIX 3 : avertissement si la détection est peu fiable
        if confiance < 0.05:
            st.warning(
                f"⚠️ Faible confiance ({confiance*100:.1f}% d'écart). "
                "Le texte est peut-être trop court ou ambigu entre français et espagnol."
            )

        # Affichage des distances pour debug
        with st.expander("Détails des distances"):
            for lang, dist in sorted(distances.items(), key=lambda x: x[1]):
                st.write(f"**{lang}** : {dist:.4f}")
    else:
        st.warning("Veuillez entrer un texte.")
