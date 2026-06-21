import streamlit as st
import math
from collections import Counter

# ---------------- CORPUS ----------------

CORPUS = {
    "français": """
Le français est une langue largement utilisée dans le monde.
La littérature française possède une histoire riche.
Les étudiants apprennent les mathématiques, les sciences et la technologie.
L'intelligence artificielle transforme de nombreux secteurs.
La théorie de l'information utilise le concept d'entropie.
""",

    "anglais": """
English is one of the most widely spoken languages.
Students learn mathematics, science and technology.
Artificial intelligence is transforming many industries.
Information theory uses the concept of entropy.
English literature has influenced cultures worldwide.
""",

    "espagnol": """
El español es una lengua hablada por millones de personas.
Los estudiantes aprenden matemáticas, ciencias y tecnología.
La inteligencia artificial transforma numerosos sectores.
La teoría de la información utiliza el concepto de entropía.
La literatura española tiene una historia muy rica.
"""
}

# ---------------- ENTROPIE ORDRE 3 ----------------

def entropie_ordre_3(texte):

    texte = ''.join(
        c.lower()
        for c in texte
        if c.isalpha()
    )

    if len(texte) < 3:
        return 0

    trigrammes = [
        texte[i:i+3]
        for i in range(len(texte)-2)
    ]

    total = len(trigrammes)

    occurrences = Counter(trigrammes)

    entropie = 0

    for compte in occurrences.values():
        p = compte / total
        entropie -= p * math.log2(p)

    return entropie

# ---------------- PROFILS ENTROPIE ----------------

PROFILS_ENTROPIE = {
    langue: entropie_ordre_3(corpus)
    for langue, corpus in CORPUS.items()
}

# ---------------- MOTS FREQUENTS ----------------

MOTS_CLES = {

    "français": [
        "le", "la", "les", "des", "une",
        "est", "dans", "pour", "avec",
        "français", "information"
    ],

    "anglais": [
        "the", "and", "for", "with",
        "is", "are", "of", "to",
        "english", "information"
    ],

    "espagnol": [
        "el", "los", "las", "una",
        "es", "para", "con", "del",
        "español", "información"
    ]
}

# ---------------- ACCENTS ----------------

ACCENTS = {

    "français": [
        "é", "è", "ê", "à",
        "ù", "ç", "ô", "î"
    ],

    "anglais": [],

    "espagnol": [
        "ñ", "á", "í",
        "ó", "ú"
    ]
}

# ---------------- SCORE MOTS ----------------

def score_mots(texte, langue):

    texte = texte.lower()

    score = 0

    for mot in MOTS_CLES[langue]:
        score += texte.count(mot)

    return score

# ---------------- SCORE ACCENTS ----------------

def score_accents(texte, langue):

    texte = texte.lower()

    score = 0

    for caractere in ACCENTS[langue]:
        score += texte.count(caractere)

    return score

# ---------------- DETECTION ----------------

def detecter_langue(texte):

    h3 = entropie_ordre_3(texte)

    if h3 == 0:
        return None, h3

    scores = {}

    for langue in CORPUS:

        # Score entropie
        distance = abs(
            h3 - PROFILS_ENTROPIE[langue]
        )

        score_entropie = max(
            0,
            100 - distance * 50
        )

        # Score mots
        score_mot = (
            score_mots(texte, langue) * 10
        )

        # Score accents
        score_accent = (
            score_accents(texte, langue) * 15
        )

        score_total = (
            score_entropie +
            score_mot +
            score_accent
        )

        scores[langue] = score_total

    meilleure_langue = max(
        scores,
        key=scores.get
    )

    return (
        meilleure_langue,
        h3,
        scores
    )

# ---------------- STREAMLIT ----------------

st.title("Détecteur de langue")

st.write(
    "Méthode : Entropie d'ordre 3 + mots fréquents + accents"
)

texte = st.text_area(
    "Entrez un texte :",
    height=200
)

if st.button("Analyser"):

    langue, entropie, scores = detecter_langue(texte)

    if langue is None:

        st.error(
            "Texte trop court."
        )

    else:

        st.success(
            f"Langue détectée : {langue}"
        )

        st.info(
            f"Entropie d'ordre 3 : {entropie:.4f} bits"
        )

        st.subheader("Scores")

        for l, s in scores.items():
            st.write(
                f"{l} : {s:.2f}"
            )
