import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium

data_ingresos = pd.read_csv("D:\Proyecto-Pro-Ingresos\ingresos-a-matcom\datos\datos-ingresos.csv", encoding="ISO-8859-1")
data_bajas = pd.read_csv("D:\Proyecto-Pro-Ingresos\ingresos-a-matcom\datos\Listado de Bajas.csv", encoding="ISO-8859-1")

# Configurar pandas para mostrar todas las filas y columnas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

st.markdown("# Ingresos a la Facultad de Matemática y Computación.")


##############################################################################################################
st.write(" ### Tendencias de inscripción por Carrera y Año.")

data_ingresos = data_ingresos[data_ingresos['Curso'].str.contains(r'^\d{4}-\d{4}$')]

data_ingresos['Año'] = data_ingresos['Curso'].str.split('-').str[0].astype(int)

inscripciones_por_ano = data_ingresos.groupby(['Año', 'Carrera']).size().reset_index(name='Número de Inscripciones')

fig1 = px.bar(inscripciones_por_ano, 
                x='Año', 
                y='Número de Inscripciones', 
                color='Carrera', 
                barmode='group',
                title='Inscripciones por Carrera a lo Largo de los Años.',
                labels={'Número de Inscripciones':'Número de Inscripciones', 'Año':'Año'})
fig1.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig1.update_layout(
    xaxis=dict(showgrid=False),  
    yaxis=dict(showgrid=False),
    legend_title_text='Carreras:'
)
st.plotly_chart(fig1)

st.write("### Carrera con más bajas.")
#se agrupan las bajas por carrera y curso para contar cuántas bajas hay en cada combinación:




st.write("### De los ingresos en cada carrera en cada curso cuántas bajas hubo en ese curso??")


#################################################################################################################
st.write("### Análisis Geográfico por Provincia y Municipio.")

# Normalizar nombres de provincias (eliminar espacios adicionales y convertir a mayúsculas)
data_ingresos['Provincia'] = data_ingresos['Provincia'].str.strip().str.upper()

# Crear listas de opciones únicas para los filtros
cursos = data_ingresos['Curso'].unique()
carreras = data_ingresos['Carrera'].unique()

# Añadir filtros de selección en Streamlit
selected_carrera = st.selectbox('Selecciona la Carrera deseada:', carreras)
selected_curso = st.selectbox('Selecciona el Curso deseado:', cursos)

# Filtrar los datos según la selección
df_filtrado = data_ingresos[(data_ingresos['Curso'] == selected_curso) & (data_ingresos['Carrera'] == selected_carrera)]

# Filtrar datos por provincia y municipio
data_agrupada = df_filtrado.groupby('Provincia').agg({
    'CI': 'count',  # Contar inscripciones
    'Índice Académico': 'mean'  # Calcular promedio del rendimiento académico
}).reset_index()

# Renombrar columnas para mayor claridad
data_agrupada.rename(columns={'CI': 'Inscripciones', 'Índice Académico': 'Rendimiento Académico'}, inplace=True)

# # Crear un mapa base centrado en Cuba
# m = folium.Map(location=[21.5, -79.5], zoom_start=6)


# # Añadir un clúster de marcadores
# marker_cluster = MarkerCluster().add_to(m)

# # Añadir marcadores al mapa
# for idx, row in data_agrupada.iterrows():
#     folium.Marker(
#         location=[row['Latitud'], row['Longitud']],  # Asegúrate de tener las coordenadas de cada provincia
#         popup=f"Provincia: {row['Provincia']}<br>Inscripciones: {row['Inscripciones']}<br>Rendimiento Académico: {row['Rendimiento Académico']:.2f}",
#         icon=folium.Icon(color='blue', icon='info-sign')
#     ).add_to(marker_cluster)

# # Mostrar el mapa en Streamlit
# folium_static(m)


# Crear un mapa centrado en Cuba
m = folium.Map(location=[21.92791, -80.58330], zoom_start=6)

# Añadir marcadores
folium.Marker([23.10796, -82.38548], popup='La Habana').add_to(m)
folium.Marker([22.1496, -80.4434], popup='Santa Clara').add_to(m)
folium.Marker([20.9517, -76.2595], popup='Santiago de Cuba').add_to(m)

# Mostrar el mapa en Streamlit
st_folium(m, width=700, height=500)




#################################################################################################################
st.write(" ### Distribución de Estudiantes de cada carrera por Vía de Ingreso.")

# Crear listas de opciones únicas para los filtros
cursos = data_ingresos['Curso'].unique()
carreras = data_ingresos['Carrera'].unique()

# Añadir filtros de selección en Streamlit
selected_carrera = st.selectbox('Selecciona una Carrera:', carreras)
selected_curso = st.selectbox('Selecciona el Curso:', cursos)


# Filtrar los datos según la selección
df_filtrado = data_ingresos[(data_ingresos['Curso'] == selected_curso) & (data_ingresos['Carrera'] == selected_carrera)]

# Contar estudiantes por vía de ingreso para el curso y la carrera seleccionados
via_ingreso_counts = df_filtrado['Vía Ingreso'].value_counts().reset_index()
via_ingreso_counts.columns = ['Vía Ingreso', 'Número de Estudiantes']

fig3 = px.pie(via_ingreso_counts, 
                    names='Vía Ingreso', 
                    values='Número de Estudiantes', 
                    title=f'Curso: {selected_curso} - Carrera: {selected_carrera}',
                    labels={'Número de Estudiantes': 'Número de Estudiantes'},
                    color='Vía Ingreso')
fig3.update_traces(textinfo='value',
                    marker=dict(line=dict(color='#000000', width=2)))
fig3.update_layout(legend_title_text='Vías de Ingreso:')
st.plotly_chart(fig3)


#Filtrar los estudiantes con índice académico mayor que cero
df_filtrado = df_filtrado[df_filtrado['Índice Académico'] > 0]

# Calcular el número de estudiantes con índice académico disponible
df_filtrado_con_indice = df_filtrado.dropna(subset=['Índice Académico'])
num_estudiantes_con_indice = df_filtrado_con_indice.groupby('Vía Ingreso').size().reset_index(name='Número de Estudiantes con Índice')

# Mostrar el número de estudiantes con índice académico
st.write("### Número de Estudiantes con Índice Académico")
st.dataframe(num_estudiantes_con_indice)

# Calcular el índice académico promedio por vía de ingreso usando los datos originales
promedios = df_filtrado_con_indice.groupby('Vía Ingreso')['Índice Académico'].mean().reset_index()
# Crear gráfico de barras para comparar los promedios
fig_bar = px.bar(promedios, 
                    x='Vía Ingreso', 
                    y='Índice Académico', 
                    title=f'Índice Académico Promedio por Vía de Ingreso - Curso: {selected_curso} - Carrera: {selected_carrera}',
                    labels={'Índice Académico': 'Índice Académico Promedio'},
                    color='Vía Ingreso')

# Mostrar gráfico de barras
st.plotly_chart(fig_bar)

##########################################################################################################################

#st.write(" ### Relación entre Índice Académico y Resultados de Pruebas de Ingreso.")
#Objetivo: Explorar si existe una correlación entre el índice académico de los estudiantes y sus resultados en las pruebas de ingreso (Matemática, Español, Historia).
#Visualización: Gráficos de dispersión o matrices de correlación.
#Insight: Podría revelar qué tan predictivos son los resultados de las pruebas de ingreso con respecto al desempeño académico general.
#Analizar la relación entre el índice académico y los resultados en las pruebas de ingreso puede proporcionar información valiosa sobre cómo las calificaciones en pruebas específicas se correlacionan con el rendimiento académico general de los estudiantes. 
#Identificación de Patrones: Te ayuda a ver si hay patrones consistentes entre cómo los estudiantes se desempeñan en las pruebas de ingreso y su rendimiento académico general. Esto puede dar indicios de qué pruebas son mejores indicadores del éxito académico.
#Evaluación de Efectividad de las Pruebas: Permite evaluar si las pruebas de ingreso están bien alineadas con el rendimiento académico esperado. Por ejemplo, si una prueba tiene una alta correlación con el índice académico, podría ser una mejor medida de preparación para los estudios.
#Mejora en la Selección de Estudiantes: Los resultados de este análisis pueden influir en cómo se seleccionan y preparan los estudiantes para las carreras, identificando qué áreas necesitan más apoyo.


