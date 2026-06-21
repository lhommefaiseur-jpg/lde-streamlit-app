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

# ---------------- ENTROPIE ORDRE 3 ----------------

def entropie_ordre_3(texte):
    texte = ''.join(c.lower() for c in texte if c.isalpha())

    if len(texte) < 3:
        return 0

    # trigrammes
    trigrammes = [
        texte[i:i+3]
        for i in range(len(texte) - 2)
    ]

    total = len(trigrammes)
    occurrences = Counter(trigrammes)

    entropie = 0

    for compte in occurrences.values():
        p = compte / total
        entropie -= p * math.log2(p)

    return entropie


# ---------------- PROFILS ----------------

PROFILS_ENTROPIE = {
    langue: entropie_ordre_3(corpus)
    for langue, corpus in CORPUS.items()
}


# ---------------- DETECTION ----------------

def detecter_langue(texte):
    h3 = entropie_ordre_3(texte)

    meilleure_langue = None
    meilleure_distance = float("inf")

    for langue, entropie_ref in PROFILS_ENTROPIE.items():

        distance = abs(h3 - entropie_ref)

        if distance < meilleure_distance:
            meilleure_distance = distance
            meilleure_langue = langue

    return meilleure_langue, h3


# ---------------- INTERFACE STREAMLIT ----------------

st.title("Détecteur de langue par entropie d'ordre 3")

texte = st.text_area("Entrez un texte :", height=200)

if st.button("Analyser"):

    langue, entropie = detecter_langue(texte)

    st.success(f"Langue détectée : {langue}")
    st.info(f"Entropie d'ordre 3 : {entropie:.4f} bits")
