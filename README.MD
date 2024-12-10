# Planificador de Rutas de Trenes de Galicia

Bienvenido al **Planificador de Rutas de Trenes de Galicia**, una aplicación web interactiva diseñada para ayudarte a encontrar las rutas más eficientes entre diferentes estaciones de tren en Galicia. Utilizando tecnologías avanzadas como Neo4j para la gestión de grafos y Streamlit para la interfaz de usuario, esta herramienta ofrece una experiencia intuitiva tanto para los usuarios como para los administradores.

## ¿Qué es el Planificador de Rutas de Trenes de Galicia?

El Planificador de Rutas de Trenes de Galicia es una aplicación que permite a los usuarios seleccionar estaciones de inicio y destino para obtener la ruta más corta en términos de tiempo de viaje. Además, incorpora una funcionalidad avanzada que permite simular retrasos en ciertas estaciones, ajustando dinámicamente las rutas para evitar demoras adicionales.

## Características Principales

- **Búsqueda de Rutas Óptimas**: Calcula la ruta más rápida entre dos estaciones utilizando el algoritmo de Dijkstra.
- **Simulación de Retrasos**: Permite a los administradores simular retrasos en estaciones específicas, afectando automáticamente las rutas calculadas para los usuarios.
- **Interfaz Intuitiva**: Una interfaz amigable creada con Streamlit que facilita la interacción tanto para usuarios como para administradores.
- **Visualización de Rutas**: Representa gráficamente las rutas seleccionadas, destacando estaciones con retrasos y rutas alternativas.
- **Notificaciones Informativas**: Informa a los usuarios cuando se ajusta su ruta para evitar estaciones con retrasos, mejorando la transparencia y la experiencia de usuario.

## Cómo Funciona

### Arquitectura del Proyecto

La aplicación está compuesta por tres componentes principales:

1. **Neo4j**: Una base de datos de grafos que almacena la información de las estaciones y las conexiones entre ellas. Cada estación es un nodo y las conexiones (`CONNECTED_TO`) representan las vías entre estaciones con un atributo de tiempo de viaje.

2. **Python y NetworkX**: Utiliza la biblioteca NetworkX para construir y manipular grafos en Python, permitiendo el cálculo eficiente de rutas utilizando el algoritmo de Dijkstra.

3. **Streamlit**: Proporciona la interfaz de usuario interactiva donde los usuarios pueden seleccionar estaciones y ver las rutas calculadas, y donde los administradores pueden simular retrasos en las estaciones.

### Flujo de Trabajo

1. **Datos de las Estaciones**: Las estaciones de tren y sus conexiones están modeladas en Neo4j. Cada estación tiene propiedades como `name` y `id`, y las conexiones entre estaciones tienen un atributo `time` que representa el tiempo de viaje en minutos.

2. **Interfaz de Usuario**: Los usuarios seleccionan una estación de inicio y una estación de destino desde un menú desplegable. Al presionar el botón "Calcular Ruta Más Corta", la aplicación consulta Neo4j para obtener la ruta óptima.

3. **Cálculo de Rutas**:
    - **Ruta Original**: Se calcula la ruta más rápida sin considerar retrasos.
    - **Ruta Ajustada**: Si se han simulado retrasos en alguna estación, se ajustan los tiempos de viaje en el grafo para reflejar estos retrasos y se recalcula la ruta óptima.
    - **Comparación de Rutas**: Se compara la ruta original con la ruta ajustada para determinar si se ha evitado alguna estación con retraso. Si es así, se notifica al usuario sobre el cambio de ruta para evitar demoras adicionales.

4. **Visualización**: La ruta seleccionada se visualiza gráficamente utilizando PyVis, destacando las estaciones con retraso y las rutas preferidas.

### Simulación de Retrasos

En el panel lateral de la aplicación, los administradores pueden seleccionar estaciones específicas y asignarles un tiempo de retraso en minutos. Estos retrasos afectan directamente el cálculo de las rutas:

- **Ajuste de Pesos**: Los tiempos de viaje entre estaciones se ajustan sumando los retrasos correspondientes, haciendo que las rutas que pasan por estaciones con retrasos sean menos atractivas.
- **Preferencia de Rutas Alternativas**: El algoritmo de Dijkstra prefiere automáticamente rutas que evitan estaciones con retrasos si estas rutas resultan más rápidas en total.
- **Notificaciones al Usuario**: Cuando se ajusta una ruta para evitar una estación con retraso, se muestra un mensaje informativo al usuario indicando el cambio y las razones detrás de él.

## Interfaz de Usuario

### Panel Principal

- **Selección de Estaciones**: Menús desplegables para elegir la estación de inicio y la estación de destino.
- **Cálculo de Ruta**: Botón para iniciar el cálculo de la ruta más corta.
- **Resultados de la Ruta**:
  - **Tiempo Total de Viaje**: Muestra el tiempo total estimado para el viaje.
  - **Detalle de la Ruta**: Lista secuencial de estaciones que componen la ruta, indicando retrasos si los hay.
- **Visualización Gráfica**: Un grafo interactivo que muestra la ruta seleccionada, destacando estaciones con retrasos y las conexiones utilizadas.

### Panel de Administración (Panel Lateral)

- **Simulación de Retrasos**:
  - **Selección de Estaciones**: Lista de estaciones donde se pueden seleccionar aquellas que tendrán retrasos.
  - **Asignación de Retrasos**: Campos numéricos para especificar la duración del retraso en minutos para cada estación seleccionada.

## Ejemplo de Uso

1. **Usuario Normal**:
   - Selecciona "A Coruña" como estación de inicio y "Vigo" como destino.
   - Presiona "Calcular Ruta Más Corta".
   - La aplicación muestra la ruta más rápida disponible con el tiempo total de viaje y una visualización gráfica.

2. **Administrador Simulando Retraso**:
   - En el panel lateral, selecciona la estación "Santiago" y asigna un retraso de 10 minutos.
   - El usuario realiza nuevamente la búsqueda de ruta.
   - La aplicación recalcula la ruta, evita "Santiago" si es posible, y muestra un mensaje informativo:  
     _"Tu ruta de viaje más corta de **A Coruña** hacia **Vigo** se encontraba interrumpida por la estación **Santiago**. Hemos cambiado tu ruta para evitar demoras adicionales en tu viaje."_
   - Se actualiza la visualización gráfica para reflejar la nueva ruta seleccionada.

## Tecnologías Utilizadas

- **Neo4j**: Base de datos de grafos para almacenar y gestionar las estaciones y sus conexiones.
- **Python**: Lenguaje de programación principal para la lógica de negocio y el manejo de datos.
- **NetworkX**: Biblioteca de Python para la creación, manipulación y estudio de la estructura, dinámica y funciones de grafos complejos.
- **Streamlit**: Framework de Python para construir aplicaciones web interactivas de manera rápida y sencilla.
- **PyVis**: Biblioteca para la visualización de grafos interactivos en la web.

## Arquitectura Detallada

### Componentes

1. **Neo4j Database**:
   - **Nodos**: Representan las estaciones de tren con propiedades como `name` e `id`.
   - **Relaciones**: Conexiones `CONNECTED_TO` entre estaciones con un atributo `time` que indica el tiempo de viaje en minutos.

2. **Backend (`journey.py`)**:
   - **Clase `Journey`**: Gestiona la conexión con Neo4j, obtiene la lista de estaciones y las conexiones entre ellas.
   - **Métodos**:
     - `get_all_stations()`: Recupera todas las estaciones de la base de datos.
     - `get_graph()`: Obtiene todas las conexiones entre estaciones con sus respectivos tiempos de viaje.

3. **Frontend (`app.py`)**:
   - **Interfaz de Usuario**: Construida con Streamlit, permite a los usuarios seleccionar estaciones y calcular rutas.
   - **Panel de Administración**: Permite simular retrasos en estaciones específicas.
   - **Cálculo de Rutas**:
     - Construye dos grafos: uno original sin retrasos y otro ajustado con retrasos.
     - Calcula rutas óptimas en ambos grafos y compara para detectar ajustes necesarios.
   - **Visualización**: Muestra la ruta seleccionada y un grafo interactivo con PyVis.

### Flujo de Datos

1. **Selección de Estaciones**: El usuario selecciona las estaciones de inicio y destino en la interfaz de Streamlit.
2. **Simulación de Retrasos**: El administrador selecciona estaciones y asigna retrasos en el panel lateral.
3. **Construcción de Grafos**:
   - **Grafo Original**: Basado en tiempos de viaje sin considerar retrasos.
   - **Grafo Ajustado**: Basado en tiempos de viaje ajustados con los retrasos asignados.
4. **Cálculo de Rutas**:
   - **Ruta Original**: Calculada usando el grafo original.
   - **Ruta Ajustada**: Calculada usando el grafo ajustado.
5. **Comparación y Notificación**:
   - Si la ruta ajustada evita estaciones con retraso presentes en la ruta original, se notifica al usuario.
6. **Visualización**: Se muestra la ruta óptima actualizada y un grafo interactivo que resalta las estaciones con retrasos y las rutas seleccionadas.

## Beneficios del Proyecto

- **Flexibilidad**: Permite a los administradores simular diferentes escenarios de retraso, lo que ayuda a planificar y gestionar mejor las operaciones.
- **Mejora de la Experiencia del Usuario**: Al evitar rutas con retrasos, se garantiza que los usuarios reciban recomendaciones de rutas más eficientes y confiables.
- **Visualización Clara**: La representación gráfica de las rutas y estaciones facilita la comprensión de las conexiones y las alternativas disponibles.
- **Escalabilidad**: La arquitectura basada en grafos de Neo4j permite manejar eficientemente grandes cantidades de estaciones y conexiones, facilitando futuras expansiones.

## Conclusión

El **Planificador de Rutas de Trenes de Galicia** es una herramienta poderosa que combina la gestión eficiente de datos con una interfaz de usuario intuitiva. Al integrar Neo4j para la gestión de grafos y Streamlit para la visualización interactiva, ofrece una solución robusta para la planificación de rutas ferroviarias, mejorando tanto la operación administrativa como la experiencia del usuario final.

¡Esperamos que esta herramienta te sea de gran utilidad para gestionar y optimizar tus viajes en tren por Galicia!

