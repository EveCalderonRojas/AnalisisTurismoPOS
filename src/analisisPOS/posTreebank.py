import pandas as pd
import nltk
from nltk.tokenize import word_tokenize

# DESCARGA DE LOS RECURSOS NECESARIOS DE NLTK

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)


# ETIQUETA EL COMENTARIO MEDIANTE NLTK
def etiquetar_comentario(texto):

    if pd.isna(texto) or texto.strip() == '':
        return []
    tokens = word_tokenize(texto)
    return nltk.pos_tag(tokens)


# ANÁLISIS DEL CORPUS MEDIANTE PENN TREEBANK
def pos_treebank(df, col_texto='comentarios_espanol'):

    df = df.copy()
    df['PennTreebank']    = df[col_texto].apply(etiquetar_comentario) # SE CREA UNA COLUMNA NUEVA CON LOS RESULTADOS OBTENIDOS DEL ANÁLISIS
    return df


# CONTEO DE CADA ETIQUETA ENCONTRADA
def resumen_treebank(df, col_tags='PennTreebank'):

    from collections import Counter

    conteo = Counter()

    for lista_tags in df[col_tags]:
        for palabra, tag in lista_tags:
            conteo[tag] += 1

    df_resumen = pd.DataFrame(
        conteo.most_common(),
        columns=['etiqueta', 'total']
    )

    return df_resumen