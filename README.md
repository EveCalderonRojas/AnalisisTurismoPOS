# Análisis de comentarios 

## TurisPOS

### ✏️ Descripción 

Este es un proyecto de análisis morfosintáctico en donde se pone en práctica todo el pipeline de datos requerido:
- Extracción de comentarios 
- Limpieza
- Modelado
- Visualización de resultados 

En donde los comentarios a analizar serán relacionados a lugares turísticos de Costa Rica, pasando por varias categorías para un mayor enriquecimiento de conocimiento y de resultados finales.

Cada comentario pasa por los análisis de Penn Treebank (NLTK) y Universal POS (spaCy), se comparan y se determina cuál funciona mejor para la parte morfosintáctica.

### 🛠️ Herramientas 

Aplicación no code Apify: 
- Extraer los comentarios de varios lugares turísticos de Costa Rica (solo se da el link de Google Maps de la atracción turística y la cantidad de comentarios).
- Guardado de los datos en diversos formatos (csv, excel, json...)

Python:
- Limpieza de datos.
- Manejo de emojis.
- Guardado de información en .csv de la información limpia.
- Manejo de funciones y modelos de POS Tagging.
- Visualización de información. 


Claude como asistente de IA para entendimiento y optimización de código.


Parte del código base del proyecto se extrajo del proyecto anterior de AnalisisSentimientosYT, el cual puede ser encontrado en el siguiente repositorio 👉🏻 https://github.com/EveCalderonRojas/AnalisisSentimientosYT


Plotly Dash:
- Parte visual del proyecto 
- Presentación de resultados de métricas y gráficos.
- Vista tipo página web en la que se puede navegar entre secciones.

### 📁 Organización

✅ data
- 🗁 raw: Alojamiento de los datos extraídos sin procesamiento 
- 🗁 processed: Datos a los que se les aplicó limpieza, análisis y traducción

✅ src
- 🗁 analisisPOS: funciones con los análisis de Penn Treebank y UniversalPOS
- 🗁 datosOrigen: procesamiento de los datos crudos, generando al final datos limpios para ser utilizados
- 🗁 datosProcesados: limpieza y guardado de los datos para el análisis
- 🗁 resultadosPOS: resultados al generar los análisis con ambos métodos
- 🗁 visualizaciones: resultados visuales utilizando Plotly Dash 

#### 👩🏻‍💻 Elaborado por:

Evelin Calderón Rojas 

Estudiante de Big Data 

Curso: Minería de Textos

