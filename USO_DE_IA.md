
# Uso responsable de IA en proyectos

## TurisPOS

### 🛠️ Herramientas

Para este proyecto en particular se utilizó a Claude como la IA para entender y generar ideas sobre estructura, dudas y código nuevo, ya que parte del código es una reutilización de código de otro proyecto, solo se adaptó para este.
Además de funciones de optimización ee código y explicaciones varias.


### 🧾 Ejemplos de prompts 

Dentro de los prompts que le di para trabajar a Claude, la mayoría se trató de preguntas que tenía con respecto a organización, que me revisara los errores que me daba al momento de ejecución, y que me ayudara con la parte visual, como se muestra en estos dos siguientes:

<img width="778" height="283" alt="Captura de pantalla 2026-06-11 140648" src="https://github.com/user-attachments/assets/03120044-f198-4c83-a2ef-e76ff9215058" />
<img width="791" height="381" alt="Captura de pantalla 2026-06-11 140716" src="https://github.com/user-attachments/assets/66780a2c-e70c-44f3-a950-067bca75c658" />

Ahí incluso le hice un pequeño 'boceto' de cómo quería que quedara la página, y le pregunté de si era posible hacerlo tipo página web con navegación; ya ahí me preguntó incluso la paleta de colores que quería y generó toda la estructura visual.

Otro caso fue el de una pregunta que tenía para generar el csv con el corpus ya analizado con ambos métodos, como lo muestro a continuación: 

<img width="804" height="629" alt="Captura de pantalla 2026-06-11 141333" src="https://github.com/user-attachments/assets/e0ef0a8a-ec6d-46c9-80d9-2006a385a1de" />

Aquí más bien me simplificó bastante el código y me refrescó la memoria acerca de la función .copy() que no recordaba.

Además de decirle que me ayudara con ciertos manejos de texto que no sabía cómo hacer o verificar, como en el caso de la separación de emojis y al final saber que con NLTK también se puede hacer el proceso de quitar stopwords.

### 👩🏻‍💻 La IA en el aprendizaje 

Personalmente me ayudó bastante en la parte de comprensión de algunas funciones, en manejar lo de las visualizaciones con Plotly, ya que era algo nuevo, y saber que sí se podía hacer tipo página web fue algo que me ayudó bastante.

Además de que me optimizó varias partes del código y me corrigió varias ideas que tenía equivocadas y poco funcionales y agotadoras.
Aparte de explicarme casi que línea por línea lo que hacían las funciones correspondientes del análisis con los dos métodos.

Y obviamente el recurso del tiempo, ya que gracias al manejo de generación de código por su parte, es menos tiempo el que se pasa programando, pero más tiempo en otras funciones como entendimiento, corrección y demás tareas importantes.

### ⌨️ Modificaciones al código 
Las modificaciones fueron casi que mínimas, ya que el código generado fue para mi sorpresa bastante completo, y al pedirle que me lo explicara detalladamente se entendió bastante bien.
Lo único fue con un par de funciones que generó que al final no aportaban ni gracia entonces mejor las dejé por aparte; y también una lista manual con las etiquetas que debían generarse con los análisis POS, entonces lo dejé por fuera. Obviamente fijándome que no se viera afectado el código al momento de la ejecución, cosa que no pasó.
Y el acomodo de cómo leía los csv, ya que asumía que todo estaba en el mismo 'lugar', y yo lo tenía agrupado en carpetas.





