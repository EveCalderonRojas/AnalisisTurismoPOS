
# FUNCIONES DE LIMPIEZA DE TEXTOS

import re
import pandas as pd

# SE UTILIZA NLTK TAMBIÉN PARA LIMPIAR Y QUITAR STOPWORDS
import nltk
from nltk.corpus import stopwords


nltk.download('stopwords', quiet=True)


def get_stopwords(extras=None):

    base = set(stopwords.words('spanish'))
    if extras:
        base |= extras # SI SE DESEA AGREGAR STOPWORDS ADICIONALES
    return base


def filtrar_unknown(df, col_idioma='idioma_comentario'):

    filtrado = df[df[col_idioma] != 'unknown'].copy()
    filtrado.reset_index(drop=True, inplace=True)
    return filtrado


def limpiar_texto(texto, stop_words):

    if pd.isna(texto) or texto.strip() == '':
        return []
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúüñ\s]', '', texto)
    tokens = texto.split()
    return [t for t in tokens if t not in stop_words and len(t) > 2]


def aplicar_limpieza(df, col_texto='comentarios_espanol', extras_stopwords=None):

    stop_words = get_stopwords(extras_stopwords)
    todas_las_palabras = []

    for comentario in df[col_texto]:
        todas_las_palabras.extend(limpiar_texto(comentario, stop_words))

    return todas_las_palabras, stop_words




