import pandas as pd
import spacy
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "spacy", "download", "es_core_news_sm", "-q"])

# MODELO A UTILIZAR
nlp = spacy.load('es_core_news_sm')

# ETIQUETA EL COMENTARIO MEDIANTE SPACY
def etiquetar_comentario_spacy(texto):

    if pd.isna(texto) or texto.strip() == '':
        return []
    doc = nlp(texto)
    return [(token.text, token.pos_, token.lemma_) for token in doc]


# ANÁLISIS DEL CORPUS MEDIANTE SPACY
def pos_universal(df, col_texto='comentarios_espanol'):

    df = df.copy()
    df['UniversalPOS']   = df[col_texto].apply(etiquetar_comentario_spacy) # SE CREA UNA COLUMNA NUEVA CON LOS RESULTADOS OBTENIDOS DEL ANÁLISIS
    return df


# CONTEO DE CADA ETIQUETA ENCONTRADA
def resumen_universal(df, col_tags='UniversalPOS'):

    from collections import Counter

    conteo = Counter()

    for lista_tags in df[col_tags]:
        for palabra, pos, lema in lista_tags:
            conteo[pos] += 1

    df_resumen = pd.DataFrame(
        conteo.most_common(),
        columns=['etiqueta', 'total']
    )

    return df_resumen