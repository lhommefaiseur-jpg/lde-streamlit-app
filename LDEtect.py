import streamlit as st
import math
from collections import Counter

# ---------------- CORPUS ----------------

CORPUS = {
    "français": """
Le langage humain est un système complexe permettant la communication entre individus.
Il repose sur des règles grammaticales et syntaxiques qui structurent les phrases.
L'informatique moderne utilise des algorithmes pour traiter des données textuelles.
La théorie de l'information est fondamentale pour comprendre l'entropie.
Les étudiants en ingénierie apprennent à programmer en Python et C++.
""",

    "anglais": """
Human language is a complex system that enables communication between individuals.
It is based on grammatical and syntactic rules that structure sentences.
Modern computing uses algorithms to process textual data.
Information theory is essential to understand entropy.
Engineering students learn programming in Python and C++.
""",

    "espagnol": """
El lenguaje humano es un sistema complejo que permite la comunicación entre personas.
Se basa en reglas gramaticales y sintácticas que organizan las frases.
La informática moderna utiliza algoritmos para procesar datos textuales.
La teoría de la información es fundamental para comprender la entropía.
Los estudiantes de ingeniería aprenden a programar en Python y C++.
"""
}

# ---------------- TRIGRAMMES ----------------

def get_trigram_frequencies(text):
    text = ''.join(c.lower() for c in text if c.isalpha())

    if len(text) < 3:
        return {}

    trigrammes = [text[i:i+3] for i in range(len(text)-2)]
    total = len(trigrammes)

    counts = Counter(trigrammes)

    return {k: v / total for k, v in counts.items()}


# ---------------- PROFILS LANGUES ----------------

PROFILS_TRIGRAMMES = {
    langue: get_trigram_frequencies(corpus)
    for langue, corpus in CORPUS.items()
}


# ---------------- DISTANCE ----------------

def distance_langue(freq_text, freq_langue):
    all_keys = set(freq_text.keys()) | set(freq_langue.keys())

    return math.sqrt(
        sum(
            (freq_text.get(k, 0) - freq_langue.get(k, 0)) ** 2
            for k in all_keys
        )
    )


# ---------------- DETECTION ----------------

def detecter_langue(texte):
    freq_text = get_trigram_frequencies(texte)

    if not freq_text:
        return "Texte trop court"

    meilleure_langue = None
    meilleure_distance = float("inf")

    for langue, profil in PROFILS_TRIGRAMMES.items():

        dist = distance_langue(freq_text, profil)

        if dist < meilleure_distance:
            meilleure_distance = dist
            meilleure_langue = langue

    return meilleure_langue


# ---------------- INTERFACE STREAMLIT ----------------

st.title("Détecteur de langue (Trigrammes + NLP)")

texte = st.text_area("Entrez un texte :", height=200)

if st.button("Analyser"):

    resultat = detecter_langue(texte)

    st.success(f"Langue détectée : {resultat}")
