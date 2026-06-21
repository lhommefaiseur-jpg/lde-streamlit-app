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
        "el", "los", "las", "una", "es", "para", "con", "del", "desde",
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
        "ñ", "á", "í", "ó", "ú", "ü"
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

# ---------------- SEUIL DE CONFIANCE ----------------
# Un seuil sur le score brut total est peu fiable : ce score dépend
# fortement de la longueur du texte (plus de mots = mécaniquement plus
# de mots-clés et d'accents comptés), donc aucune valeur fixe ne
# fonctionne bien à la fois sur les textes courts et longs.
#
# On utilise donc deux conditions complémentaires, plus robustes :
#
#   1) RATIO_MIN_AVANCE : la langue gagnante doit nettement se
#      détacher de la 2e meilleure langue (sinon le texte est ambigu
#      entre 2 langues, ou ressemble un peu à toutes sans appartenir
#      clairement à aucune — cas typique d'une langue étrangère
#      proche, comme l'italien ou l'allemand, qui partage quelques
#      lettres/sons avec le français/espagnol).
#
#   2) SIGNAL_LEXICAL_MIN : il faut au moins ce nombre d'indices
#      lexicaux concrets (mots-clés reconnus + caractères accentués
#      spécifiques) pour la langue gagnante. Cela évite qu'un texte
#      qui ne matche presque rien soit validé uniquement parce que
#      l'entropie d'ordre 3 penche légèrement d'un côté (l'entropie
#      seule n'est pas un signal assez fort pour décider).
RATIO_MIN_AVANCE = 1.3
SIGNAL_LEXICAL_MIN = 2

# ---------------- DETECTION ----------------

def detecter_langue(texte):

    h3 = entropie_ordre_3(texte)

    if h3 == 0:
        return None, h3, None

    scores = {}
    signal_lexical = {}

    for langue in CORPUS:

        # Score entropie : on normalise avec une pénalité plus douce
        # (corpus de référence agrandi => entropie plus stable => on
        # peut utiliser une pénalité moins agressive que *50).
        distance = abs(h3 - PROFILS_ENTROPIE[langue])
        score_entropie = max(0, 100 - distance * 20)

        # Score mots : matching par mots entiers désormais (voir
        # tokeniser/score_mots), donc plus de faux positifs sur
        # sous-chaînes.
        sm = score_mots(texte, langue)
        score_mot = sm * 10

        # Score accents : inchangé, déjà fiable car les caractères
        # accentués sont peu ambigus entre langues.
        sa = score_accents(texte, langue)
        score_accent = sa * 15

        scores[langue] = score_entropie + score_mot + score_accent

        # Nombre brut d'indices lexicaux trouvés (avant pondération),
        # utilisé uniquement pour la condition de seuil ci-dessous.
        signal_lexical[langue] = sm + sa

    meilleure_langue = max(scores, key=scores.get)

    tries = sorted(scores.values(), reverse=True)
    meilleur_score, second_score = tries[0], tries[1]

    ratio_ok = (
        second_score == 0
        or meilleur_score >= second_score * RATIO_MIN_AVANCE
    )
    signal_ok = signal_lexical[meilleure_langue] >= SIGNAL_LEXICAL_MIN

    # Si la langue gagnante ne se détache pas assez et/ou n'a pas
    # assez d'indices lexicaux concrets, on considère que le texte
    # n'appartient à aucune des 3 langues supportées.
    if not (ratio_ok and signal_ok):
        return "inconnue", h3, scores

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

        elif langue == "inconnue":
            st.error(
                "Langue non reconnue : le texte ne correspond à aucune "
                "des 3 langues supportées (français, anglais, espagnol). "
                "Vérifiez que vous avez bien saisi un texte dans l'une "
                "de ces langues, ou ajoutez un peu plus de texte pour "
                "permettre une détection plus fiable."
            )
            st.info(f"Entropie d'ordre 3 : {entropie:.4f} bits")
            with st.expander("Voir le détail des scores"):
                for l, s in sorted(scores.items(), key=lambda x: -x[1]):
                    st.write(f"{l} : {s:.2f}")

        else:
            st.success(f"Langue détectée : {langue}")
            st.info(f"Entropie d'ordre 3 : {entropie:.4f} bits")

            st.subheader("Scores")
            for l, s in sorted(scores.items(), key=lambda x: -x[1]):
                st.write(f"{l} : {s:.2f}")
