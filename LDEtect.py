import streamlit as st
import math
import re
from collections import Counter

# ---------------- CORPUS (élargi pour stabiliser l'entropie) ----------------

CORPUS = {
    "français": """
Le français est une langue largement utilisée dans le monde entier.
La littérature française possède une histoire riche et variée, depuis
le Moyen Âge jusqu'à nos jours. Les étudiants apprennent les
mathématiques, les sciences et la technologie dans de nombreuses écoles.
L'intelligence artificielle transforme de nombreux secteurs de
l'économie, de la santé à l'industrie. La théorie de l'information
utilise le concept d'entropie pour mesurer l'incertitude d'une source.
Paris est la capitale de la France et abrite de nombreux monuments
historiques comme la tour Eiffel et le Louvre. Les chercheurs publient
régulièrement de nouveaux articles scientifiques dans ce domaine.
La cuisine française est réputée dans le monde entier pour sa qualité
et sa diversité régionale. Beaucoup de gens étudient le français comme
seconde langue à l'école ou à l'université.
""",

    "anglais": """
English is one of the most widely spoken languages in the world today.
Students learn mathematics, science and technology in schools across
many countries. Artificial intelligence is transforming many industries,
from healthcare to finance and transportation. Information theory uses
the concept of entropy to measure the uncertainty of a source of data.
English literature has influenced cultures worldwide for centuries,
from Shakespeare to modern novelists. London is the capital of England
and is home to many famous landmarks and museums. Researchers regularly
publish new scientific articles in this growing field of study. Many
people around the world learn English as a second language at school
or through online courses. The history of the English language is long
and complex, shaped by many other languages over time.
""",

    "espagnol": """
El español es una lengua hablada por millones de personas en todo el
mundo. Los estudiantes aprenden matemáticas, ciencias y tecnología en
muchas escuelas de distintos países. La inteligencia artificial
transforma numerosos sectores, desde la salud hasta la industria y el
transporte. La teoría de la información utiliza el concepto de entropía
para medir la incertidumbre de una fuente de datos. La literatura
española tiene una historia muy rica, desde el Siglo de Oro hasta la
actualidad. Madrid es la capital de España y alberga muchos monumentos
históricos y museos importantes. Los investigadores publican
regularmente nuevos artículos científicos en este campo. Muchas
personas en el mundo aprenden español como segunda lengua en la escuela
o la universidad.
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
        for i in range(len(texte) - 2)
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

# ---------------- MOTS FREQUENTS (mots entiers uniquement) ----------------
# Mots courants ET suffisamment discriminants (on évite les mots ultra
# courts comme "es", "el", "la" qui se retrouvent partout par hasard).

MOTS_CLES = {

    "français": [
        "le", "la", "les", "des", "une", "est", "dans", "pour", "avec",
        "français", "langue", "histoire", "monde", "depuis", "comme",
        "informatique", "information", "étudiants", "apprennent",
        "littérature", "entropie", "université", "école"
    ],

    "anglais": [
        "the", "and", "for", "with", "is", "are", "of", "to", "from",
        "english", "language", "history", "world", "since", "like",
        "computer", "information", "students", "learn",
        "literature", "entropy", "university", "school"
    ],

    "espagnol": [
        "el", "los", "las", "una", "para", "con", "del", "desde",
        "como", "español", "lengua", "historia", "mundo", "informática",
        "información", "estudiantes", "aprenden",
        "literatura", "entropía", "universidad", "escuela"
    ]
}

# ---------------- ACCENTS ----------------

ACCENTS = {

    "français": [
        "é", "è", "ê", "à", "ù", "ç", "ô", "î", "â", "ë", "ï", "û"
    ],

    "anglais": [],

    "espagnol": [
        "ñ", "á", "í", "ó", "ú"
    ]
}

# ---------------- TOKENISATION ----------------

def tokeniser(texte):
    """
    Découpe le texte en mots entiers (lettres latines + accents),
    en minuscules. Évite les faux positifs de type 'count' sur
    sous-chaînes (ex: 'es' matchant dans 'est' ou 'intéressant').
    """
    return re.findall(
        r"[a-zàâäéèêëïîôöùûüçñáíóúü]+",
        texte.lower()
    )

# ---------------- SCORE MOTS ----------------

def score_mots(texte, langue):
    mots_texte = tokeniser(texte)
    compteur_mots = Counter(mots_texte)

    score = 0
    for mot in MOTS_CLES[langue]:
        score += compteur_mots.get(mot, 0)

    return score

# ---------------- SCORE ACCENTS ----------------

def score_accents(texte, langue):
    texte = texte.lower()

    score = 0
    for caractere in ACCENTS[langue]:
        score += texte.count(caractere)

    return score

# ---------------- PONDÉRATION ENTROPIE ----------------
# Le score d'entropie est pondéré faiblement : sur un texte long, il
# peut être "élevé" pour n'importe quelle langue latine (même non
# supportée), car toutes partagent l'alphabet et une structure
# syllabique générale. On le garde comme simple facteur de
# départage entre les 3 langues, pas comme signal dominant.
POIDS_ENTROPIE = 0.3

# ---------------- DETECTION ----------------

def detecter_langue(texte):

    h3 = entropie_ordre_3(texte)

    if h3 == 0:
        return None, h3, None

    scores = {}

    for langue in CORPUS:

        distance = abs(h3 - PROFILS_ENTROPIE[langue])
        score_entropie = max(0, 100 - distance * 20) * POIDS_ENTROPIE

        score_mot = score_mots(texte, langue) * 10

        score_accent = score_accents(texte, langue) * 15

        scores[langue] = score_entropie + score_mot + score_accent

    meilleure_langue = max(scores, key=scores.get)

    return meilleure_langue, h3, scores

# ---------------- STREAMLIT ----------------

st.title("Détecteur de langue")

st.write(
    "Méthode : Entropie d'ordre 3 + mots fréquents (mots entiers) + accents"
)

texte = st.text_area(
    "Entrez un texte :",
    height=200
)

if st.button("Analyser"):

    if not texte.strip():
        st.warning("Veuillez entrer un texte.")
    else:
        langue, entropie, scores = detecter_langue(texte)

        if langue is None:
            st.error("Texte trop court.")

        else:
            st.success(f"Langue détectée : {langue}")
            st.info(f"Entropie d'ordre 3 : {entropie:.4f} bits")

            st.subheader("Scores")
            for l, s in sorted(scores.items(), key=lambda x: -x[1]):
                st.write(f"{l} : {s:.2f}")
