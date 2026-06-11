
import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import ast

dash.register_page(__name__, path='/graficos', name='Gráficos')

# PALETA DE COLORES
VERDE_OSCURO = '#1B4332'
VERDE_MEDIO  = '#2D6A4F'
VERDE_CLARO  = '#52B788'
DORADO       = '#D4A017'
GRIS_SUAVE   = '#F0EDE6'
BLANCO       = '#FFFFFF'
AZUL         = '#2C5F8A'

COLORES_POL = {'Positivo': VERDE_CLARO, 'Neutro': DORADO, 'Negativo': '#C0392B'}
COLORES_CAT = {'parque': VERDE_MEDIO, 'restaurante': DORADO, 'alojamiento': '#5B8DB8'}

# CORPUS A UTILIZAR
df = pd.read_csv('../../data/processed/dataset_Google-Maps-Reviews-Scraper-postagging.csv')

def parse_col(val):
    try:
        return ast.literal_eval(val)
    except:
        return []

df['universalpos'] = df['universalpos'].apply(parse_col)
df['penntreebank'] = df['penntreebank'].apply(parse_col)


# CLASIFICA POR LA POLARIDAD (ESTRELLAS REECIBIDAS)
def clasificar_polaridad(cal):
    if cal in [1, 2]: return 'Negativo'
    if cal == 3:      return 'Neutro'
    if cal in [4, 5]: return 'Positivo'
    return 'Sin clasificar'

df['polaridad'] = df['calificacion'].apply(clasificar_polaridad)


# MUESTRA LAS MÉTRICAS GENERALES DEL MÉTODO UNIVERSAL POS Y PENN TREEBANK RESPECTIVAMENTE
def metricas_universal(tags):
    if not tags:
        return 0, 0
    try:
        sustantivos = sum(1 for _, pos, _ in tags if pos in ('NOUN', 'PROPN'))
        verbos      = sum(1 for _, pos, _ in tags if pos in ('VERB', 'AUX'))
        adjetivos   = sum(1 for _, pos, _ in tags if pos == 'ADJ')
        total       = len(tags)
        return (round(sustantivos / verbos, 2) if verbos > 0 else 0,
                round(adjetivos / total, 4) if total > 0 else 0)
    except:
        return 0, 0

def metricas_treebank(tags):
    if not tags:
        return 0, 0
    try:
        sustantivos = sum(1 for _, tag in tags if tag.startswith('NN'))
        verbos      = sum(1 for _, tag in tags if tag.startswith('VB'))
        adjetivos   = sum(1 for _, tag in tags if tag.startswith('JJ'))
        total       = len(tags)
        return (round(sustantivos / verbos, 2) if verbos > 0 else 0,
                round(adjetivos / total, 4) if total > 0 else 0)
    except:
        return 0, 0

m_upos = df['universalpos'].apply(metricas_universal)
df['upos_ratio']    = m_upos.apply(lambda x: x[0])
df['upos_densidad'] = m_upos.apply(lambda x: x[1])

m_ptb = df['penntreebank'].apply(metricas_treebank)
df['ptb_ratio']    = m_ptb.apply(lambda x: x[0])
df['ptb_densidad'] = m_ptb.apply(lambda x: x[1])


# LAYOUT
layout = html.Div(style={'backgroundColor': GRIS_SUAVE, 'padding': '60px'}, children=[

    html.H2('Análisis por grupo', style={
        'color': VERDE_OSCURO, 'fontSize': '28px',
        'borderBottom': f'3px solid {DORADO}', 'paddingBottom': '12px',
        'maxWidth': '1100px', 'margin': '0 auto 40px'
    }),

    html.Div(style={'maxWidth': '1100px', 'margin': '0 auto 40px', 'display': 'flex', 'gap': '40px', 'flexWrap': 'wrap', 'alignItems': 'flex-end'}, children=[

        # ELEGIR EL MÉTODO A PRESENTAR
        html.Div([
            html.Label('Método de análisis', style={
                'color': VERDE_OSCURO, 'fontWeight': 'bold', 'display': 'block',
                'marginBottom': '8px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '14px'
            }),
            html.Div(style={'display': 'flex', 'gap': '0'}, children=[
                html.Button('Universal POS', id='btn-upos', n_clicks=0, style={
                    'padding': '10px 20px', 'border': f'2px solid {VERDE_MEDIO}',
                    'borderRadius': '8px 0 0 8px', 'cursor': 'pointer',
                    'backgroundColor': VERDE_MEDIO, 'color': BLANCO,
                    'fontFamily': 'Arial, sans-serif', 'fontSize': '14px', 'fontWeight': 'bold'
                }),
                html.Button('Penn Treebank', id='btn-ptb', n_clicks=0, style={
                    'padding': '10px 20px', 'border': f'2px solid {AZUL}',
                    'borderRadius': '0 8px 8px 0', 'cursor': 'pointer',
                    'backgroundColor': BLANCO, 'color': AZUL,
                    'fontFamily': 'Arial, sans-serif', 'fontSize': '14px', 'fontWeight': 'bold'
                }),
            ])
        ]),

        # FILTRAR POR POLARIDAD
        html.Div([
            html.Label('Filtrar por polaridad', style={
                'color': VERDE_OSCURO, 'fontWeight': 'bold', 'display': 'block',
                'marginBottom': '8px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '14px'
            }),
            dcc.Dropdown(
                id='graf-filtro-polaridad',
                options=[{'label': 'Todas', 'value': 'Todas'}] +
                        [{'label': p, 'value': p} for p in ['Positivo', 'Neutro', 'Negativo']],
                value='Todas', clearable=False, style={'width': '200px'}
            )
        ]),

        # FILTAR POR CATEGORÍA
        html.Div([
            html.Label('Filtrar por categoría', style={
                'color': VERDE_OSCURO, 'fontWeight': 'bold', 'display': 'block',
                'marginBottom': '8px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '14px'
            }),
            dcc.Dropdown(
                id='graf-filtro-categoria',
                options=[{'label': 'Todas', 'value': 'Todas'}] +
                        [{'label': c.capitalize(), 'value': c} for c in df['categoria'].unique()],
                value='Todas', clearable=False, style={'width': '200px'}
            )
        ]),
    ]),

    # ESTABLECE EL MÉTODO ACTIVO
    dcc.Store(id='metodo-activo', data='upos'),

    html.Div(id='graf-contenido', style={'maxWidth': '1100px', 'margin': '0 auto'}),
])


@callback(
    Output('metodo-activo', 'data'),
    Output('btn-upos', 'style'),
    Output('btn-ptb', 'style'),
    Input('btn-upos', 'n_clicks'),
    Input('btn-ptb', 'n_clicks'),
)
def seleccionar_metodo(n_upos, n_ptb):
    estilo_activo_upos = {
        'padding': '10px 20px', 'border': f'2px solid {VERDE_MEDIO}',
        'borderRadius': '8px 0 0 8px', 'cursor': 'pointer',
        'backgroundColor': VERDE_MEDIO, 'color': BLANCO,
        'fontFamily': 'Arial, sans-serif', 'fontSize': '14px', 'fontWeight': 'bold'
    }
    estilo_inactivo_upos = {**estilo_activo_upos, 'backgroundColor': BLANCO, 'color': VERDE_MEDIO}

    estilo_activo_ptb = {
        'padding': '10px 20px', 'border': f'2px solid {AZUL}',
        'borderRadius': '0 8px 8px 0', 'cursor': 'pointer',
        'backgroundColor': AZUL, 'color': BLANCO,
        'fontFamily': 'Arial, sans-serif', 'fontSize': '14px', 'fontWeight': 'bold'
    }
    estilo_inactivo_ptb = {**estilo_activo_ptb, 'backgroundColor': BLANCO, 'color': AZUL}

    from dash import ctx
    boton = ctx.triggered_id

    if boton == 'btn-ptb':
        return 'ptb', estilo_inactivo_upos, estilo_activo_ptb
    return 'upos', estilo_activo_upos, estilo_inactivo_ptb


@callback(
    Output('graf-contenido', 'children'),
    Input('metodo-activo', 'data'),
    Input('graf-filtro-polaridad', 'value'),
    Input('graf-filtro-categoria', 'value'),
)
def actualizar_graficos(metodo, polaridad, categoria):
    dff = df.copy()
    if polaridad != 'Todas':
        dff = dff[dff['polaridad'] == polaridad]
    if categoria != 'Todas':
        dff = dff[dff['categoria'] == categoria]

    col_ratio    = 'upos_ratio'    if metodo == 'upos' else 'ptb_ratio'
    col_densidad = 'upos_densidad' if metodo == 'upos' else 'ptb_densidad'
    color_metodo = VERDE_MEDIO     if metodo == 'upos' else AZUL
    nombre       = 'Universal POS (spaCy)' if metodo == 'upos' else 'Penn Treebank (NLTK)'

    estilo = dict(
        plot_bgcolor=BLANCO, paper_bgcolor=BLANCO,
        font_family='Arial', showlegend=False,
        title_font_color=VERDE_OSCURO, title_font_size=16
    )

    grp_pol = dff.groupby('polaridad')[[col_ratio, col_densidad]].mean().reset_index()
    fig_ratio_pol = px.bar(grp_pol, x='polaridad', y=col_ratio,
        color='polaridad', color_discrete_map=COLORES_POL,
        title=f'Ratio sustantivos/verbos por polaridad — {nombre}',
        labels={col_ratio: 'Ratio', 'polaridad': ''})
    fig_ratio_pol.update_layout(**estilo)

    fig_adj_pol = px.bar(grp_pol, x='polaridad', y=col_densidad,
        color='polaridad', color_discrete_map=COLORES_POL,
        title=f'Densidad de adjetivos por polaridad — {nombre}',
        labels={col_densidad: 'Densidad', 'polaridad': ''})
    fig_adj_pol.update_layout(**estilo)

    grp_cat = dff.groupby('categoria')[[col_ratio, col_densidad]].mean().reset_index()
    fig_ratio_cat = px.bar(grp_cat, x='categoria', y=col_ratio,
        color='categoria', color_discrete_map=COLORES_CAT,
        title=f'Ratio sustantivos/verbos por categoría — {nombre}',
        labels={col_ratio: 'Ratio', 'categoria': ''})
    fig_ratio_cat.update_layout(**estilo)

    fig_adj_cat = px.bar(grp_cat, x='categoria', y=col_densidad,
        color='categoria', color_discrete_map=COLORES_CAT,
        title=f'Densidad de adjetivos por categoría — {nombre}',
        labels={col_densidad: 'Densidad', 'categoria': ''})
    fig_adj_cat.update_layout(**estilo)

    fig_scatter = px.scatter(dff, x='calificacion', y=col_densidad,
        color='polaridad', color_discrete_map=COLORES_POL,
        title=f'Calificación vs densidad de adjetivos — {nombre}',
        labels={'calificacion': 'Estrellas', col_densidad: 'Densidad de adjetivos'},
        opacity=0.6)
    fig_scatter.update_layout(
        plot_bgcolor=BLANCO, paper_bgcolor=BLANCO,
        font_family='Arial', title_font_color=VERDE_OSCURO, title_font_size=16
    )

    return [
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '24px', 'marginBottom': '24px'}, children=[
            dcc.Graph(figure=fig_ratio_pol),
            dcc.Graph(figure=fig_adj_pol),
        ]),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '24px', 'marginBottom': '24px'}, children=[
            dcc.Graph(figure=fig_ratio_cat),
            dcc.Graph(figure=fig_adj_cat),
        ]),
        dcc.Graph(figure=fig_scatter),
    ]