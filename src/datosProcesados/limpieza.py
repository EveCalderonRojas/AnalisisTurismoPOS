
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Descarga silenciosa de recursos NLTK
nltk.download('stopwords', quiet=True)


def get_stopwords(extras=None):

    base = set(stopwords.words('spanish'))
    if extras:
        base |= extras
    return base


def filtrar_unknown(df, col_idioma='idioma_comentario'):

    filtrado = df[df[col_idioma] != 'unknown'].copy()
    filtrado.reset_index(drop=True, inplace=True)
    return filtrado


def limpiar_texto(texto, stop_words):
    """
    Limpia un comentario individual:
    - Convierte a minúsculas
    - Elimina puntuación y números
    - Separa en palabras (tokens)
    - Quita stopwords y palabras de menos de 3 caracteres

    Retorna una lista de palabras limpias.
    """
    if pd.isna(texto) or texto.strip() == '':
        return []
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúüñ\s]', '', texto)
    tokens = texto.split()
    return [t for t in tokens if t not in stop_words and len(t) > 2]


def aplicar_limpieza(df, col_texto='comentarios_espanol', extras_stopwords=None):
    """
    Aplica limpiar_texto() a todos los comentarios del corpus.

    Retorna:
        - todas_las_palabras : lista con todas las palabras del corpus
        - stop_words         : conjunto de stopwords que se usó
    """
    stop_words = get_stopwords(extras_stopwords)
    todas_las_palabras = []

    for comentario in df[col_texto]:
        todas_las_palabras.extend(limpiar_texto(comentario, stop_words))

    return todas_las_palabras, stop_words


def get_frecuencias(palabras, top_n=30):
    """
    Cuenta cuántas veces aparece cada palabra y retorna
    un DataFrame con las top_n más frecuentes.
    """
    frecuencias = Counter(palabras)
    df_freq = pd.DataFrame(
        frecuencias.most_common(top_n),
        columns=['palabra', 'frecuencia']
    )
    return df_freq

