
import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import ast
import random

dash.register_page(__name__, path='/metricas', name='Métricas')

# PALETA DE COLORES
VERDE_OSCURO = '#1B4332'
VERDE_MEDIO  = '#2D6A4F'
VERDE_CLARO  = '#52B788'
DORADO       = '#D4A017'
AZUL         = '#2C5F8A'
BLANCO       = '#FFFFFF'
GRIS_SUAVE   = '#F0EDE6'
CREMA        = '#F9F5EC'

COLORES_POL = {'Positivo': VERDE_CLARO, 'Neutro': DORADO, 'Negativo': '#C0392B'}

# CORPUS A UTILIZAR
df = pd.read_csv('../../data/processed/dataset_Google-Maps-Reviews-Scraper-postagging.csv')

def parse_col(val):
    try: return ast.literal_eval(val)
    except: return []

df['universalpos'] = df['universalpos'].apply(parse_col)
df['penntreebank'] = df['penntreebank'].apply(parse_col)


# CLASIFICACIÓN DE POLARIDAD Y MÉTRICAS A UTILIZAR EN PENN TREEBANK Y UNIVERSAL POS
def clasificar_polaridad(cal):
    if cal in [1, 2]: return 'Negativo'
    if cal == 3:      return 'Neutro'
    if cal in [4, 5]: return 'Positivo'
    return 'Sin clasificar'

df['polaridad'] = df['calificacion'].apply(clasificar_polaridad)

def metricas_universal(tags):
    if not tags: return 0, 0
    try:
        s = sum(1 for _, pos, _ in tags if pos in ('NOUN', 'PROPN'))
        v = sum(1 for _, pos, _ in tags if pos in ('VERB', 'AUX'))
        a = sum(1 for _, pos, _ in tags if pos == 'ADJ')
        t = len(tags)
        return (round(s/v, 2) if v > 0 else 0, round(a/t, 4) if t > 0 else 0)
    except: return 0, 0

def metricas_treebank(tags):
    if not tags: return 0, 0
    try:
        s = sum(1 for _, tag in tags if tag.startswith('NN'))
        v = sum(1 for _, tag in tags if tag.startswith('VB'))
        a = sum(1 for _, tag in tags if tag.startswith('JJ'))
        t = len(tags)
        return (round(s/v, 2) if v > 0 else 0, round(a/t, 4) if t > 0 else 0)
    except: return 0, 0

m_upos = df['universalpos'].apply(metricas_universal)
df['upos_ratio']    = m_upos.apply(lambda x: x[0])
df['upos_densidad'] = m_upos.apply(lambda x: x[1])

m_ptb = df['penntreebank'].apply(metricas_treebank)
df['ptb_ratio']    = m_ptb.apply(lambda x: x[0])
df['ptb_densidad'] = m_ptb.apply(lambda x: x[1])


# HELPERS
def tarjeta(valor, etiqueta, color):
    return html.Div(style={
        'backgroundColor': BLANCO, 'borderRadius': '10px',
        'padding': '16px 24px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
        'borderLeft': f'5px solid {color}', 'marginBottom': '12px'
    }, children=[
        html.Span(str(valor), style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color, 'display': 'block'}),
        html.Span(etiqueta, style={'fontSize': '13px', 'color': '#666', 'fontFamily': 'Arial, sans-serif'})
    ])

def bloque_metodo(titulo, color_titulo, ratio, densidad, total, cal):
    return html.Div(style={
        'backgroundColor': BLANCO, 'borderRadius': '12px', 'padding': '28px',
        'boxShadow': '0 2px 12px rgba(0,0,0,0.08)', 'flex': '1', 'minWidth': '280px'
    }, children=[
        html.Div(titulo, style={
            'backgroundColor': color_titulo, 'color': BLANCO,
            'padding': '10px 16px', 'borderRadius': '8px', 'fontWeight': 'bold',
            'fontSize': '15px', 'fontFamily': 'Arial, sans-serif',
            'marginBottom': '20px', 'textAlign': 'center', 'letterSpacing': '0.5px'
        }),
        tarjeta(f'{total:,}', 'reseñas analizadas',   VERDE_MEDIO),
        tarjeta(cal,          'calificación promedio', DORADO),
        tarjeta(ratio,        'ratio sust./verbos',    VERDE_CLARO),
        tarjeta(densidad,     'densidad de adjetivos', '#5B8DB8'),
    ])

def chip(palabra, tag, color_borde, color_tag):
    return html.Span(style={
        'display': 'inline-flex', 'flexDirection': 'column', 'alignItems': 'center',
        'border': f'1px solid {color_borde}', 'borderRadius': '6px',
        'padding': '4px 8px', 'margin': '3px', 'backgroundColor': BLANCO,
        'fontSize': '12px', 'fontFamily': 'Arial, sans-serif'
    }, children=[
        html.Span(palabra, style={'color': '#333', 'fontWeight': 'bold'}),
        html.Span(tag,     style={'color': color_tag, 'fontSize': '10px', 'marginTop': '2px'})
    ])


# LAYOUT
layout = html.Div(style={'padding': '60px', 'maxWidth': '1100px', 'margin': '0 auto'}, children=[

    html.H2('Métricas del corpus', style={
        'color': VERDE_OSCURO, 'fontSize': '28px',
        'borderBottom': f'3px solid {DORADO}', 'paddingBottom': '12px', 'marginBottom': '40px'
    }),

    # FILTRADO SEGÚN LO DESEADO
    html.Div(style={'display': 'flex', 'gap': '40px', 'marginBottom': '40px', 'flexWrap': 'wrap'}, children=[
        html.Div([
            html.Label('Filtrar por polaridad', style={
                'color': VERDE_OSCURO, 'fontWeight': 'bold', 'display': 'block',
                'marginBottom': '8px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '14px'
            }),
            dcc.Dropdown(
                id='met-filtro-polaridad',
                options=[{'label': 'Todas', 'value': 'Todas'}] +
                        [{'label': p, 'value': p} for p in ['Positivo', 'Neutro', 'Negativo']],
                value='Todas', clearable=False, style={'width': '220px'}
            )
        ]),
        html.Div([
            html.Label('Filtrar por categoría', style={
                'color': VERDE_OSCURO, 'fontWeight': 'bold', 'display': 'block',
                'marginBottom': '8px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '14px'
            }),
            dcc.Dropdown(
                id='met-filtro-categoria',
                options=[{'label': 'Todas', 'value': 'Todas'}] +
                        [{'label': c.capitalize(), 'value': c} for c in df['categoria'].unique()],
                value='Todas', clearable=False, style={'width': '220px'}
            )
        ]),
    ]),

    # MÉTRICAS
    html.Div(id='met-bloques', style={'display': 'flex', 'gap': '24px', 'flexWrap': 'wrap', 'marginBottom': '60px'}),

    # ESCOGE UN COMENTARIO AL AZAR DEL CORPUS Y LO MUESTRA JUNTO CON SUS RESPECTIVOS ANÁLISIS EN AMBOS MÉTODOS
    html.Div(style={'borderTop': f'3px solid {DORADO}', 'paddingTop': '40px'}, children=[
        html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '24px', 'flexWrap': 'wrap', 'gap': '16px'}, children=[
            html.H3('Análisis morfosintáctico por comentario', style={
                'color': VERDE_OSCURO, 'fontSize': '22px', 'margin': '0'
            }),
            html.Button('Ver otro comentario', id='btn-random', n_clicks=0, style={
                'padding': '10px 24px', 'backgroundColor': VERDE_MEDIO, 'color': BLANCO,
                'border': 'none', 'borderRadius': '25px', 'cursor': 'pointer',
                'fontFamily': 'Arial, sans-serif', 'fontSize': '14px', 'fontWeight': 'bold',
            })
        ]),
        dcc.Store(id='indice-comentario', data=0),
        html.Div(id='comentario-detalle'),
    ]),
])



@callback(
    Output('met-bloques', 'children'),
    Input('met-filtro-polaridad', 'value'),
    Input('met-filtro-categoria', 'value')
)
def actualizar_metricas(polaridad, categoria):
    dff = df.copy()
    if polaridad != 'Todas': dff = dff[dff['polaridad'] == polaridad]
    if categoria != 'Todas': dff = dff[dff['categoria'] == categoria]

    total   = len(dff)
    avg_cal = round(dff['calificacion'].mean(), 2) if total > 0 else 0

    return [
        bloque_metodo('Universal POS — spaCy', VERDE_MEDIO,
            ratio   = round(dff['upos_ratio'].mean(), 2)    if total > 0 else 0,
            densidad= round(dff['upos_densidad'].mean(), 4) if total > 0 else 0,
            total=total, cal=avg_cal),
        bloque_metodo('Penn Treebank — NLTK', AZUL,
            ratio   = round(dff['ptb_ratio'].mean(), 2)    if total > 0 else 0,
            densidad= round(dff['ptb_densidad'].mean(), 4) if total > 0 else 0,
            total=total, cal=avg_cal),
    ]


@callback(
    Output('indice-comentario', 'data'),
    Input('btn-random', 'n_clicks'),
)
def nuevo_indice(n):
    return random.randint(0, len(df) - 1)


@callback(
    Output('comentario-detalle', 'children'),
    Input('indice-comentario', 'data'),
)
def mostrar_comentario(idx):
    fila = df.iloc[idx]
    texto     = fila['comentarios_espanol']
    lugar     = fila['lugar']
    cal       = fila['calificacion']
    polaridad = fila['polaridad']
    tags_upos = fila['universalpos']
    tags_ptb  = fila['penntreebank']

    color_pol = {'Positivo': VERDE_CLARO, 'Neutro': DORADO, 'Negativo': '#C0392B'}.get(polaridad, '#aaa')


    chips_upos = [chip(p, pos, VERDE_MEDIO, VERDE_MEDIO) for p, pos, _ in tags_upos] if tags_upos else []


    chips_ptb = [chip(p, tag, AZUL, AZUL) for p, tag in tags_ptb] if tags_ptb else []

    return html.Div(style={
        'backgroundColor': BLANCO, 'borderRadius': '12px',
        'padding': '28px', 'boxShadow': '0 2px 12px rgba(0,0,0,0.08)'
    }, children=[

        # TÍTULO DEL COMENTARIO
        html.Div(style={'display': 'flex', 'gap': '16px', 'alignItems': 'center', 'marginBottom': '16px', 'flexWrap': 'wrap'}, children=[
            html.Span(f'📍 {lugar}', style={'color': VERDE_MEDIO, 'fontWeight': 'bold', 'fontFamily': 'Arial, sans-serif', 'fontSize': '14px'}),
            html.Span('⭐' * int(cal), style={'fontSize': '14px'}),
            html.Span(polaridad, style={
                'backgroundColor': color_pol, 'color': BLANCO,
                'padding': '3px 12px', 'borderRadius': '12px',
                'fontSize': '12px', 'fontFamily': 'Arial, sans-serif', 'fontWeight': 'bold'
            }),
        ]),

        html.P(f'"{texto}"', style={
            'color': '#444', 'fontSize': '15px', 'lineHeight': '1.7',
            'fontStyle': 'italic', 'marginBottom': '28px',
            'borderLeft': f'4px solid {DORADO}', 'paddingLeft': '16px'
        }),

        # MUESTRA LOS ANÁLISIS UNO EN CADA COLUMNA SEPARADA
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '24px'}, children=[

            #NLTK
            html.Div(style={'backgroundColor': GRIS_SUAVE, 'borderRadius': '10px', 'padding': '20px'}, children=[
                html.Div('Universal POS — spaCy', style={
                    'backgroundColor': VERDE_MEDIO, 'color': BLANCO,
                    'padding': '8px 14px', 'borderRadius': '6px',
                    'fontWeight': 'bold', 'fontSize': '13px',
                    'fontFamily': 'Arial, sans-serif', 'marginBottom': '16px'
                }),
                html.Div(style={'display': 'flex', 'flexWrap': 'wrap'}, children=chips_upos)
            ]),

            #SPACY
            html.Div(style={'backgroundColor': GRIS_SUAVE, 'borderRadius': '10px', 'padding': '20px'}, children=[
                html.Div('Penn Treebank — NLTK', style={
                    'backgroundColor': AZUL, 'color': BLANCO,
                    'padding': '8px 14px', 'borderRadius': '6px',
                    'fontWeight': 'bold', 'fontSize': '13px',
                    'fontFamily': 'Arial, sans-serif', 'marginBottom': '16px'
                }),
                html.Div(style={'display': 'flex', 'flexWrap': 'wrap'}, children=chips_ptb)
            ]),
        ])
    ])