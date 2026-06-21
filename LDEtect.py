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
        # NB: "ü" a été retiré : ce n'est pas un caractère espagnol
        # courant, et il apparaît aussi en allemand/turc, ce qui
        # provoquait de faux positifs sur ces langues.
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

# ---------------- SEUIL DE CONFIANCE ----------------
# Constat important : sur un texte assez long, TOUTES les langues
# européennes (même sans aucun rapport, ex: néerlandais, allemand)
# obtiennent une entropie d'ordre 3 "proche" des profils de référence,
# simplement parce qu'elles partagent l'alphabet latin et une structure
# syllabique générale. Si on pondère l'entropie trop fort, ce bruit de
# fond suffit à elle seule à valider n'importe quelle langue. Le score
# d'entropie est donc maintenant pondéré beaucoup plus faiblement
# (POIDS_ENTROPIE = 0.3) : il départage les langues proches mais ne
# peut plus, seul, déclencher une détection positive.
#
# La décision finale repose sur deux conditions :
#
#   1) RATIO_MIN_AVANCE : la langue gagnante doit nettement se
#      détacher de la 2e meilleure langue.
#
#   2) SEUIL_SIGNAL : nombre minimum d'indices lexicaux concrets
#      (mots-clés + caractères accentués) requis pour la langue
#      gagnante. Ce seuil est adaptatif :
#        - texte court (< SEUIL_TEXTE_COURT mots) : on tolère un seul
#          indice solide, car un texte court contient mécaniquement
#          peu de mots-clés même s'il est dans la bonne langue.
#        - texte plus long : on exige un indice tous les 20 mots
#          environ, pour empêcher qu'un texte long dans une langue
#          étrangère passe grâce à 1-2 coïncidences lexicales isolées.
#
# Limite assumée : sur des textes très courts (quelques mots), aucune
# méthode statistique simple ne peut garantir une détection fiable à
# 100 % — il n'y a tout simplement pas assez de signal. Le seuil ici
# vise un bon compromis, pas une garantie absolue.
POIDS_ENTROPIE = 0.3
RATIO_MIN_AVANCE = 1.3
SEUIL_TEXTE_COURT = 10
SEUIL_SIGNAL_MIN_LONG = 2
DIVISEUR_SIGNAL_LONG = 20

# ---------------- DETECTION ----------------

def detecter_langue(texte):

    h3 = entropie_ordre_3(texte)

    if h3 == 0:
        return None, h3, None

    nb_mots = max(1, len(tokeniser(texte)))

    scores = {}
    signal_lexical = {}

    for langue in CORPUS:

        # Score entropie : pondéré faiblement (voir note ci-dessus),
        # car sur un texte long il peut être "élevé" pour n'importe
        # quelle langue latine, qu'elle soit supportée ou non.
        distance = abs(h3 - PROFILS_ENTROPIE[langue])
        score_entropie = max(0, 100 - distance * 20) * POIDS_ENTROPIE

        # Score mots : matching par mots entiers (voir tokeniser /
        # score_mots), donc plus de faux positifs sur sous-chaînes.
        sm = score_mots(texte, langue)
        score_mot = sm * 10

        # Score accents : caractères spécifiques à chaque langue.
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

    if nb_mots < SEUIL_TEXTE_COURT:
        seuil_signal = 1
    else:
        seuil_signal = max(
            SEUIL_SIGNAL_MIN_LONG,
            nb_mots // DIVISEUR_SIGNAL_LONG
        )

    signal_ok = signal_lexical[meilleure_langue] >= seuil_signal

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
