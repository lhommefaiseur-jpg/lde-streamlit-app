import streamlit as st
import math
from collections import Counter

CORPUS = {
    "français": """
Le langage humain est un système complexe permettant la communication entre individus. 
Il repose sur des règles grammaticales, syntaxiques et sémantiques qui structurent les phrases.

En France, la langue française est utilisée dans l'administration, l'éducation et les médias. 
Elle a évolué au fil des siècles à partir du latin, influencée par les langues régionales et étrangères.

L'informatique moderne utilise des algorithmes pour traiter des données textuelles. 
Ces algorithmes permettent notamment la reconnaissance automatique de la langue, la traduction et l'analyse de sentiments.

Dans le domaine scientifique, les chercheurs utilisent des modèles mathématiques pour représenter des phénomènes complexes. 
La théorie de l'information, développée par Claude Shannon, est fondamentale pour comprendre la notion d'entropie.

Les étudiants en ingénierie apprennent à manipuler des outils comme Python, MATLAB ou C++ pour résoudre des problèmes concrets.
Ces compétences sont essentielles dans les domaines de l'intelligence artificielle et du traitement des données.
""",

    "anglais": """
Human language is a complex system that allows communication between individuals. 
It is based on grammatical, syntactic and semantic rules that structure sentences.

In many countries, English is used as a global language in science, technology and business. 
It has evolved over centuries and absorbed vocabulary from many other languages.

Modern computing relies on algorithms to process large amounts of textual data. 
These algorithms are used for language detection, machine translation and sentiment analysis.

In scientific fields, researchers use mathematical models to describe complex systems. 
Information theory, introduced by Claude Shannon, is essential for understanding entropy.

Engineering students learn programming languages such as Python, Java and C++ to solve real-world problems. 
These skills are widely used in artificial intelligence and data science applications.
""",

    "espagnol": """
El lenguaje humano es un sistema complejo que permite la comunicación entre personas. 
Se basa en reglas gramaticales, sintácticas y semánticas que organizan las frases.

En muchos países, el español es una lengua oficial utilizada en la educación, la administración y los medios de comunicación. 
Ha evolucionado a partir del latín y ha recibido influencias de otras lenguas.

La informática moderna utiliza algoritmos para procesar grandes cantidades de datos textuales. 
Estos algoritmos se aplican en la detección de idiomas, la traducción automática y el análisis de textos.

En el ámbito científico, los investigadores utilizan modelos matemáticos para describir fenómenos complejos. 
La teoría de la información, desarrollada por Claude Shannon, es fundamental para comprender la entropía.

Los estudiantes de ingeniería aprenden lenguajes de programación como Python, Java y C++ para resolver problemas reales. 
Estas habilidades son esenciales en inteligencia artificial y ciencia de datos.
"""
}


def entropie_ordre_2(texte):
    texte = ''.join(c.lower() for c in texte if c.isalpha())

    if len(texte) < 2:
        return 0

    bigrammes = [
        texte[i:i+2]
        for i in range(len(texte) - 1)
    ]

    total = len(bigrammes)

    occurrences = Counter(bigrammes)

    entropie = 0

    for compte in occurrences.values():
        p = compte / total
        entropie -= p * math.log2(p)

    return entropie


PROFILS_ENTROPIE = {
    langue: entropie_ordre_2(corpus)
    for langue, corpus in CORPUS.items()
}


def detecter_langue(texte):
    h2 = entropie_ordre_2(texte)

    meilleure_langue = None
    meilleure_distance = float("inf")

    for langue, entropie_ref in PROFILS_ENTROPIE.items():

        distance = abs(h2 - entropie_ref)

        if distance < meilleure_distance:
            meilleure_distance = distance
            meilleure_langue = langue

    return meilleure_langue, h2


# ---------------- Interface Streamlit ----------------

st.title("Détecteur de langue par entropie d'ordre 2")

texte = st.text_area(
    "Entrez un texte :",
    height=200
)

if st.button("Analyser"):

    langue, entropie = detecter_langue(texte)

    st.success(f"Langue détectée : {langue}")
    st.info(f"Entropie d'ordre 2 : {entropie:.4f} bits")