import streamlit as st
import math
from collections import Counter

# ---------------- CORPUS ----------------

CORPUS = CORPUS = {
    "français": """
La langue française est l’une des principales langues de communication internationale. Elle est utilisée dans de nombreux pays et joue un rôle important dans les domaines de l’éducation, de la culture, de la diplomatie et des échanges économiques. Grâce à son histoire et à son rayonnement, elle demeure une langue étudiée dans le monde entier.

L’histoire du français trouve ses origines dans le latin parlé par les populations de la Gaule à l’époque romaine. Au fil des siècles, cette langue a évolué sous l’influence de différents peuples et a développé une richesse lexicale remarquable. Aujourd’hui, elle continue de s’enrichir grâce aux évolutions culturelles et technologiques.

La littérature française possède un patrimoine exceptionnel. Des auteurs tels que Victor Hugo, Molière, Voltaire, Gustave Flaubert ou Albert Camus ont marqué l’histoire de la pensée et de la création littéraire. Leurs œuvres sont étudiées dans de nombreux établissements scolaires et universitaires à travers le monde.

L’éducation constitue un élément fondamental du développement des individus et des sociétés. Les élèves y acquièrent des connaissances dans des domaines variés tels que les mathématiques, les sciences, l’histoire, la géographie et les langues. L’apprentissage favorise l’esprit critique et prépare les citoyens aux défis du futur.

Les progrès technologiques ont profondément transformé les modes de vie contemporains. Les ordinateurs, les téléphones intelligents et les réseaux numériques permettent d’accéder rapidement à l’information et facilitent la communication entre les personnes situées dans différentes régions du monde.

L’informatique moderne repose sur des algorithmes capables de traiter efficacement de grandes quantités de données. Ces algorithmes sont utilisés dans des applications variées telles que la recherche d’informations, la traduction automatique, la reconnaissance vocale et l’analyse de documents textuels.

L’intelligence artificielle représente aujourd’hui un domaine majeur de recherche et d’innovation. Les systèmes intelligents peuvent apprendre à partir de données, identifier des régularités et prendre certaines décisions de manière automatisée. Ces technologies sont utilisées dans la médecine, l’industrie, les transports et de nombreux autres secteurs.

La théorie de l’information, développée au milieu du vingtième siècle, fournit des outils essentiels pour étudier les systèmes de communication. Le concept d’entropie permet notamment de mesurer l’incertitude associée à une source d’information et joue un rôle central dans le traitement des données numériques.

Les chercheurs en sciences utilisent des modèles mathématiques afin de représenter et de comprendre des phénomènes complexes. Ces modèles permettent d’analyser des systèmes physiques, biologiques ou économiques et d’effectuer des prévisions fondées sur des observations expérimentales.

L’ingénierie combine des connaissances scientifiques et techniques pour concevoir des solutions adaptées à des besoins concrets. Les ingénieurs participent à la création d’infrastructures, au développement de logiciels, à la production d’énergie et à l’amélioration des technologies utilisées dans la vie quotidienne.

L’économie étudie la production, la distribution et la consommation des biens et des services. Les économistes cherchent à comprendre les mécanismes qui influencent les marchés, les entreprises et les comportements des consommateurs afin de proposer des politiques adaptées aux enjeux contemporains.

La protection de l’environnement est devenue une priorité mondiale. Les gouvernements, les entreprises et les citoyens sont encouragés à réduire leur impact écologique, à préserver les ressources naturelles et à favoriser le développement de solutions énergétiques durables.

Le système de santé joue un rôle essentiel dans le bien-être des populations. Les professionnels de la santé travaillent à prévenir les maladies, à améliorer les traitements médicaux et à promouvoir des habitudes de vie favorables à une meilleure qualité de vie.

La mondialisation a renforcé les échanges entre les différentes régions du monde. Les progrès des transports et des technologies de communication facilitent les collaborations internationales dans les domaines scientifiques, économiques et culturels.

L’apprentissage des langues étrangères constitue un atout précieux dans un contexte international. Il permet de découvrir d’autres cultures, de développer de nouvelles compétences et d’accéder à davantage d’opportunités professionnelles et académiques.

Les avancées dans le domaine de la science des données ont permis le développement de méthodes performantes pour analyser les textes. Les techniques statistiques et les algorithmes d’apprentissage automatique sont aujourd’hui utilisés pour classifier des documents, extraire des informations pertinentes et détecter automatiquement la langue d’un texte.

""",

    "anglais": """
English is one of the most widely spoken languages in the world and serves as a major means of international communication. It is used in education, science, business, technology, and diplomacy, making it an important language for global interactions and knowledge exchange.

The history of the English language is rich and diverse. Originating from Germanic languages brought to Britain by early settlers, English gradually evolved through contact with Latin, French, and many other languages. This historical development contributed to its extensive vocabulary and flexibility.

English literature has produced some of the most influential writers in history. Authors such as William Shakespeare, Charles Dickens, Jane Austen, George Orwell, and many others have left a lasting impact on culture and literature. Their works continue to be studied and appreciated around the world.

Education plays a crucial role in the development of individuals and societies. Students acquire knowledge in subjects such as mathematics, science, history, geography, and language studies. Continuous learning helps people adapt to technological and social changes throughout their lives.

Technological innovation has transformed modern society. Computers, smartphones, and digital networks enable rapid communication and provide access to vast amounts of information. These tools support collaboration between individuals and organizations across different countries.

Modern computing relies on algorithms designed to process data efficiently. These algorithms are used in applications such as search engines, machine translation, speech recognition, recommendation systems, and many other technologies that people use every day.

Artificial intelligence has become one of the most active areas of scientific research. Intelligent systems are capable of identifying patterns in data, learning from experience, and performing tasks that traditionally required human expertise. These technologies are increasingly applied in healthcare, transportation, finance, and manufacturing.

Information theory provides mathematical tools for studying communication systems and data transmission. The concept of entropy is particularly important because it measures the uncertainty associated with information sources and helps optimize coding and compression methods.

Scientists use mathematical models to describe and analyze complex phenomena. These models support research in physics, biology, economics, and engineering by allowing researchers to test hypotheses and predict the behavior of various systems.

Engineering combines scientific knowledge with practical problem-solving techniques. Engineers design structures, machines, software systems, and technological solutions that contribute to economic development and improve living conditions around the world.

Economics examines how resources are produced, distributed, and consumed. Economists study markets, financial systems, and human behavior to better understand economic growth, employment, and the impact of public policies on society.

Environmental protection has become a major global concern. Governments and organizations invest in renewable energy, sustainable development, and conservation initiatives aimed at reducing pollution and preserving natural resources for future generations.

Healthcare systems are essential for maintaining public well-being. Medical professionals work to prevent diseases, improve treatments, and promote healthy lifestyles. Advances in medical research continue to improve life expectancy and quality of life in many countries.

Globalization has increased interactions among nations in economic, cultural, and scientific fields. Improved transportation and communication technologies allow people to exchange ideas, conduct business, and collaborate on research projects more effectively than ever before.

Learning foreign languages provides numerous personal and professional advantages. It enables individuals to communicate with people from different backgrounds, understand diverse cultures, and access broader educational and career opportunities.

Recent developments in data science have led to powerful methods for analyzing textual information. Statistical techniques and machine learning algorithms are used to classify documents, identify patterns, extract relevant information, and automatically determine the language of written content.

""",

    "espagnol": """
El idioma español es una de las lenguas más habladas del mundo y constituye un importante medio de comunicación entre millones de personas. Se utiliza en numerosos países de Europa, América y otras regiones, donde desempeña un papel fundamental en la educación, la cultura, la administración y los medios de comunicación.

La historia del español se remonta al latín vulgar introducido en la península ibérica durante la expansión del Imperio romano. Con el paso de los siglos, esta lengua evolucionó y recibió influencias de diversos pueblos y culturas, lo que contribuyó a la riqueza de su vocabulario y de sus expresiones.

La literatura en lengua española posee una tradición excepcional. Autores como Miguel de Cervantes, Federico García Lorca, Gabriel García Márquez y muchos otros han contribuido al desarrollo de una producción literaria reconocida internacionalmente. Sus obras son estudiadas en escuelas y universidades de numerosos países.

La educación constituye uno de los pilares fundamentales de las sociedades modernas. En las escuelas, los estudiantes aprenden conocimientos relacionados con las matemáticas, las ciencias, la historia, la geografía y la lengua. El aprendizaje continuo permite desarrollar habilidades críticas y preparar a los ciudadanos para los desafíos del futuro.

La tecnología ha transformado profundamente la manera en que las personas trabajan, estudian y se comunican. El uso de computadoras, teléfonos inteligentes y redes de comunicación facilita el acceso a grandes cantidades de información y favorece la colaboración entre individuos de diferentes partes del mundo.

La informática moderna se basa en algoritmos capaces de procesar datos de manera eficiente. Estos algoritmos permiten realizar tareas como la búsqueda de información, la traducción automática, el reconocimiento de voz, el análisis de imágenes y la detección automática de idiomas.

La inteligencia artificial es una de las áreas más dinámicas de la investigación científica actual. Los sistemas inteligentes son capaces de aprender patrones a partir de grandes volúmenes de datos y de tomar decisiones basadas en modelos matemáticos complejos. Estas tecnologías encuentran aplicaciones en la medicina, la industria, el transporte y numerosos otros sectores.

La teoría de la información, desarrollada por Claude Shannon, proporciona herramientas esenciales para analizar la transmisión y el almacenamiento de datos. Conceptos como la entropía permiten medir la incertidumbre de una fuente de información y desempeñan un papel importante en el estudio de los sistemas de comunicación.
Las ciencias físicas buscan comprender los fenómenos que gobiernan el universo. Los investigadores utilizan modelos matemáticos para describir el movimiento de los cuerpos, la propagación de las ondas, las interacciones entre partículas y muchos otros procesos observados en la naturaleza.
La ingeniería combina conocimientos científicos y técnicos con el fin de diseñar soluciones a problemas concretos. Los ingenieros participan en la construcción de infraestructuras, el desarrollo de sistemas informáticos, la producción de energía y la creación de tecnologías innovadoras que mejoran la calidad de vida.
La economía estudia la producción, distribución y consumo de bienes y servicios. Los economistas analizan mercados, comportamientos de los consumidores y políticas públicas para comprender mejor el funcionamiento de las sociedades modernas y proponer estrategias de desarrollo sostenible.
La protección del medio ambiente representa uno de los grandes desafíos del siglo veintiuno. La reducción de las emisiones contaminantes, la preservación de los recursos naturales y el desarrollo de energías renovables son objetivos prioritarios para numerosos países y organizaciones internacionales.
La salud pública desempeña un papel esencial en el bienestar de las poblaciones. Los sistemas sanitarios trabajan para prevenir enfermedades, promover hábitos saludables y garantizar el acceso a tratamientos médicos adecuados. La investigación médica contribuye continuamente al descubrimiento de nuevas terapias y tecnologías.
La globalización ha incrementado los intercambios culturales, económicos y científicos entre las naciones. Gracias a los avances en transporte y telecomunicaciones, las personas pueden colaborar a distancia y compartir conocimientos de manera más rápida que en cualquier otro momento de la historia.
El aprendizaje de idiomas extranjeros ofrece numerosas ventajas personales y profesionales. Permite acceder a diferentes culturas, ampliar oportunidades laborales y facilitar la comunicación internacional. Por esta razón, muchas instituciones educativas fomentan el estudio de varias lenguas desde edades tempranas.
Los avances en ciencia de datos han permitido desarrollar métodos sofisticados para analizar información textual. Técnicas estadísticas y algoritmos de aprendizaje automático son utilizados para clasificar documentos, identificar temas y detectar automáticamente el idioma de un texto desconocido.

"""
}

def entropie_ordre_3(texte):
    texte = ''.join(c.lower() for c in texte if c.isalpha())

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


# ---------------- PROFILS ----------------

PROFILS_ENTROPIE = {
    langue: entropie_ordre_3(corpus)
    for langue, corpus in CORPUS.items()
}


# ---------------- DETECTION ----------------

def detecter_langue(texte):
    h3 = entropie_ordre_3(texte)

    if h3 == 0:
        return None, h3  # texte trop court

    meilleure_langue = None
    meilleure_distance = float("inf")

    for langue, entropie_ref in PROFILS_ENTROPIE.items():
        distance = abs(h3 - entropie_ref)
        if distance < meilleure_distance:
            meilleure_distance = distance
            meilleure_langue = langue

    # Seuil de rejet : si trop éloigné de tous les profils → langue inconnue
    SEUIL = 0.5
    if meilleure_distance > SEUIL:
        return None, h3

    return meilleure_langue, h3

# ---------------- INTERFACE STREAMLIT ----------------

st.title("Détecteur de langue par entropie d'ordre 3")

texte = st.text_area("Entrez un texte :", height=200)

if st.button("Analyser"):

    langue, entropie = detecter_langue(texte)

    st.success(f"Langue détectée : {langue}")
    st.info(f"Entropie d'ordre 3 : {entropie:.4f} bits")
