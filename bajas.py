import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


data = pd.read_json("./datos/datos_clasificados.json")

#Eliminar espacios en blanco al principio y al final de los nombres de las columnas
data.columns = data.columns.str.strip()
# Eliminar espacios en blanco al principio y al final de todas las celdas
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
# Configurar pandas para mostrar todas las filas y columnas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)  
pd.set_option('display.expand_frame_repr', False)

#####################################
st.markdown("# Bajas de la MATCOM.")
#####################################

#df filtrado de las bajas.
bajas = data[data['Estado'] == 'Baja']

#################################
st.write("### Bajas  por Curso.")
#################################
bajas_por_curso = bajas.groupby('Curso').size().reset_index(name='Número de Bajas')

cursos_disponibles = bajas_por_curso['Curso'].unique()

# Slider para seleccionar cursos, con todos los cursos seleccionados por defecto
cursos_seleccionados = st.select_slider(
    'Seleccione el rango de cursos que desee visualizar:', 
    options=sorted(cursos_disponibles),  # Opciones ordenadas
    value=(min(cursos_disponibles), max(cursos_disponibles))  # Mostrar todos los cursos por defecto
)

# Filtrar los datos según los cursos seleccionados
cursos_filtrados = bajas_por_curso[(bajas_por_curso['Curso'] >= cursos_seleccionados[0]) & (bajas_por_curso['Curso'] <= cursos_seleccionados[1])]

fig11 = px.bar(cursos_filtrados, 
                x='Curso', 
                y='Número de Bajas', 
                title='Total de Bajas por Curso.',
                labels={'Número de Bajas':'Número de Bajas', 'Curso':'Curso'})

fig11.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig11.update_layout(
    xaxis=dict(showgrid=False),  
    yaxis=dict(showgrid=False),
    legend_title_text='Cursos')
st.plotly_chart(fig11)

##################################
st.write("### Bajas por Género.")
##################################
ingresos_por_genero = data.groupby(['Curso', 'Sexo']).size().reset_index(name='Total Ingresos')
bajas_por_genero = bajas.groupby(['Curso', 'Sexo']).size().reset_index(name='Número de Bajas')
bajas_por_genero = bajas_por_genero.merge(ingresos_por_genero, on=['Curso', 'Sexo'])
    
bajas_por_genero['Porcentaje de Bajas'] = (bajas_por_genero['Número de Bajas'] / bajas_por_genero['Total Ingresos']) * 100

fig12 = px.bar(bajas_por_genero, 
                x='Curso', 
                y='Porcentaje de Bajas', 
                color='Sexo', 
                barmode='group',
                title='Porcentaje de Bajas por Género y Curso.',
                labels={'Porcentaje de Bajas':'Porcentaje de Bajas (%)', 'Curso':'Curso'},
                color_discrete_map={'F': 'pink', 'M': 'blue'})
fig12.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig12.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), legend_title_text='Género')
st.plotly_chart(fig12)

#####################################
st.write("### Bajas por Provincia.")
#####################################
bajas_por_provincia = bajas.groupby(['Curso', 'Provincia']).size().reset_index(name='Número de Bajas')
    
fig13 = px.bar(bajas_por_provincia, 
                    x='Curso', 
                    y='Número de Bajas', 
                    color='Provincia', 
                    barmode='group',
                    title='Bajas por Provincia y Curso.',
                    labels={'Número de Bajas':'Número de Bajas', 'Curso':'Curso'})
fig13.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig13.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), legend_title_text='Provincia')
st.plotly_chart(fig13)

st.write("### De los estudiantes de baja de la habana(que no son becados) de que municipio son.")

##########################################
st.write("### Bajas por Vía de Ingreso.")
##########################################
bajas_por_via = bajas.groupby(['Curso', 'Vía Ingreso']).size().reset_index(name='Número de Bajas')

# Crear gráfico de burbujas
fig_bubble = px.scatter(
    bajas_por_via,
    x='Curso',
    y='Vía Ingreso',
    size='Número de Bajas',
    color='Vía Ingreso',
    title='Bajas por Vía de Ingreso y Curso',
    labels={'Número de Bajas': 'Número de Bajas', 'Curso': 'Curso', 'Vía Ingreso': 'Vía de Ingreso'},
    size_max=60
)

# Actualizar diseño del gráfico
fig_bubble.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    legend_title_text='Leyenda:'
)
st.plotly_chart(fig_bubble)

#clasificacion de tipo de pre
data_preuniversitario = bajas.dropna(subset=['Vía Ingreso'])

data_preuniversitario = data_preuniversitario[data_preuniversitario['Vía Ingreso'].str.contains('INSTITUTOS PREUNIVERSITARIOS', na=False)]

distribucion_pre = data_preuniversitario.groupby(['Curso', 'Tipo de Pre']).size().reset_index(name='Número de Estudiantes')
        
fig06 = px.bar(distribucion_pre, 
                            y='Curso', 
                            x='Número de Estudiantes', 
                            color='Tipo de Pre', 
                            barmode='stack',
                            orientation='h',
                            title='Distribución de Estudiantes de Preuniversitario según el Tipo de Pre.',
                            labels={'Número de Estudiantes':'Número de Estudiantes', 'Curso':'Curso'})
fig06.update_traces(marker=dict(line=dict(color='#000000', width=1)))
fig06.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), legend_title_text='Tipo de Pre')
st.plotly_chart(fig06)


###############################################################################################
st.write("### De las bajas de Pre normal, de qué preuniversitario es que vienen más bajas??")
###############################################################################################
pre_normal = bajas[bajas["Tipo de Pre"] == "Pre normal"]

a = pre_normal.groupby(["Municipio", "Curso"]).size().reset_index(name="Número de bajas")

# Definir una lista de colores oscuros únicos
unique_municipios = a['Municipio'].unique()
color_discrete_sequence = px.colors.qualitative.Dark24[:len(unique_municipios)]

# Crear el gráfico de dispersión
fig = px.scatter(a, 
                x='Curso', 
                y='Número de bajas', 
                color='Municipio',
                color_discrete_sequence=color_discrete_sequence,
                category_orders={'Preuniversitario': ['A', 'B', 'C']},
                title='Distribución de Estudiantes de Pre de la calle por Municipio y Tipo de Preuniversitario')

fig.update_layout(barmode='stack')

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

st.write("### Cojer los municipios que mas se repiten y hacer mapa para visualizar a que distancia estan de la universidad??")



################################################################################################
st.write("### De las bajas cuántos estudiantes son becados??")
st.write("### De que provincia o municipio son???")
st.write("### existe alguna correlación entre los estudiantes de baja con que sean becados???")
#################################################################################################


###################################
st.write("### Bajas por Carrera.")
###################################
cursos_disponibles = bajas['Curso'].unique()

cursos_select = st.select_slider(
    'Selecciona el rango de Cursos:',
    options=sorted(cursos_disponibles),  # Opciones ordenadas
    value=(min(cursos_disponibles), max(cursos_disponibles))  # Mostrar todos los cursos por defecto
)

# Filtrar los datos de bajas por el rango de cursos seleccionados
bajas = bajas[(bajas['Curso'] >= cursos_select[0]) & (bajas['Curso'] <= cursos_select[1])]

carreras_disponibles = bajas['Carrera'].unique()

# Crear un diccionario para almacenar el estado de cada casilla de verificación
carreras_seleccionadas = {}

# Crear casillas de verificación para cada carrera
st.write('Carreras:')
for carrera in sorted(carreras_disponibles):
    carreras_seleccionadas[carrera] = st.checkbox(carrera, value=True)

# Filtrar las bajas por las carreras seleccionadas
carreras_filtradas = []

# Iterar sobre los elementos del diccionario carreras_seleccionadas
for carrera, seleccionada in carreras_seleccionadas.items():
    # Si la carrera está seleccionada, añadirla a la lista carreras_filtradas
    if seleccionada:
        carreras_filtradas.append(carrera)

bajas = bajas[bajas['Carrera'].isin(carreras_filtradas)]

bajas_por_carrera_curso = bajas.groupby(['Carrera', 'Curso']).size().reset_index(name='Número de Bajas')

fig16 = px.line(bajas_por_carrera_curso,
                x='Curso',
                y='Número de Bajas',
                color='Carrera',
                title='Número de Bajas por Carrera y Curso',
                labels={'Número de Bajas': 'Número de Bajas', 'Carrera': 'Carrera'},
                markers=True,
                color_discrete_map={'LIC. CIENCIAS DE LA COMPUTACION': 'blue', 'LIC. MATEMATICA': 'red'})

fig16.update_traces(
    line=dict(width=3.5),
    marker=dict(size=6, symbol='circle', line=dict(width=2, color='black'), color='black')
)

fig16.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    legend_title_text='Carreras:')  
st.plotly_chart(fig16)

#####################################################
st.write("### Comparación entre los ingresos y las bajas en cada curso.")
#####################################################
# Agrupa y cuenta los datos
bajas = data[data["Estado"]=="Baja"].groupby('Curso').size().reset_index(name='Número de Bajas')
ingresos = data.groupby('Curso').size().reset_index(name='Número de Ingresos')

# Crea un DataFrame con los resultados
df = pd.merge(bajas, ingresos, on='Curso', how='outer').fillna(0)

# Renombra las columnas
df.columns = ['Curso', 'Bajas', 'Ingresos']

# Crear la figura
fig = go.Figure()

# Agregar las barras horizontales para Bajas
fig.add_trace(go.Bar(
    y=df['Curso'],
    x=-df['Bajas'],
    orientation='h',
    name='Total Bajas por Curso',
    marker_color='red',
    marker_line=dict(color='black', width=1),
    hovertemplate='%{x:.0f}<extra></extra>'
))

# Agregar las barras horizontales para Ingresos
fig.add_trace(go.Bar(
    y=df['Curso'],
    x=df['Ingresos'],
    orientation='h',
    name='Total Ingresos por Curso',
    marker_color='green',
    marker_line=dict(color='black', width=1),
    hovertemplate='%{x:.0f}<extra></extra>'
))

# Configurar el diseño del gráfico
fig.update_layout(
    title='Comparación entre Bajas y Ingresos por Cursos',
    xaxis_title='Cantidad',
    yaxis_title='Curso',
    barmode='overlay',
    xaxis=dict(zeroline=False, showgrid=False, gridwidth=1),
    yaxis=dict(title='Curso', showgrid=False, gridwidth=1)
)

# Ajustar el tamaño del gráfico
fig.update_layout(height=600, width=800)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)





######################################################

# # Agrupar las bajas por curso y vía de ingreso
# bajas_por_via = bajas.groupby(['Curso', 'Vía Ingreso']).size().reset_index(name='Número de Bajas')


# #TREEMAP

# # Agrupar las bajas por curso, vía de ingreso y preuniversitario
# bajas_por_via = bajas.groupby(['Curso', 'Vía Ingreso']).size().reset_index(name='Número de Bajas')

# # Crear gráfico de treemap
# fig_treemap = px.treemap(
#     bajas_por_via,
#     path=['Curso', 'Vía Ingreso',],  # Jerarquía del gráfico
#     values='Número de Bajas',
#     title='Bajas por Curso, Vía de Ingreso',
#     color='Vía Ingreso',
#     color_discrete_sequence=px.colors.qualitative.Plotly,
#     labels={'Número de Bajas': 'Número de Bajas', 'Curso': 'Curso', 'Vía Ingreso': 'Vía de Ingreso'}
# )

# # Actualizar diseño del gráfico
# fig_treemap.update_layout(
#     legend_title_text='Vía de Ingreso'
# )

# # Mostrar gráfico de treemap en Streamlit
# st.plotly_chart(fig_treemap)


# #MAPA DE CALOR

# # Agrupar las bajas por curso y vía de ingreso
# bajas_por_via = bajas.groupby(['Curso', 'Vía Ingreso']).size().reset_index(name='Número de Bajas')

# # Crear la matriz de valores para el mapa de calor
# heatmap_data = bajas_por_via.pivot(index='Vía Ingreso', columns='Curso', values='Número de Bajas')

# # Reemplazar NaN con 0 en la matriz de datos
# heatmap_data = heatmap_data.fillna(0)

# # Crear el mapa de calor
# fig_heatmap = go.Figure(data=go.Heatmap(
#     z=heatmap_data.values,
#     x=heatmap_data.columns,
#     y=heatmap_data.index,
#     colorscale='Viridis',  # Escala de colores para representar la intensidad
#     colorbar=dict(title='Número de Bajas'),
#     zmin=0
# ))

# # Agregar cuadrículas
# fig_heatmap.update_layout(
#     xaxis=dict(
#         title='Curso',
#         showgrid=True,
#         gridcolor='rgba(255, 255, 255, 0.5)',  # Color de la línea de cuadrícula
#         zeroline=False
#     ),
#     yaxis=dict(
#         title='Vía de Ingreso',
#         showgrid=True,
#         gridcolor='rgba(255, 255, 255, 0.5)',  # Color de la línea de cuadrícula
#         zeroline=False
#     ),
#     title='Mapa de Calor de Bajas por Curso y Vía de Ingreso'
# )

# # Agregar anotaciones solo para valores no nulos
# for i in range(len(heatmap_data.index)):
#     for j in range(len(heatmap_data.columns)):
#         value = heatmap_data.iloc[i, j]
#         if value > 0:  # Solo agregar anotaciones para valores mayores a 0
#             fig_heatmap.add_trace(go.Scatter(
#                 x=[heatmap_data.columns[j]],
#                 y=[heatmap_data.index[i]],
#                 text=[f'{value:.0f}'],
#                 mode='text',
#                 showlegend=False
#             ))

# # Mostrar mapa de calor en Streamlit
# st.plotly_chart(fig_heatmap)


# # Crear gráfico de rosca multinivel
# fig_sunburst = px.sunburst(
#     bajas_por_via,
#     path=['Curso', 'Vía Ingreso'],  # Jerarquía del gráfico
#     values='Número de Bajas',
#     title='Bajas por Curso y Vía de Ingreso',
#     color='Vía Ingreso',
#     color_discrete_sequence=px.colors.qualitative.Plotly,
# )

# # Actualizar diseño del gráfico
# fig_sunburst.update_layout(
#     legend_title_text='Vía de Ingreso',
#     width=600,  # Ajustar el ancho del gráfico
#     height=600,  # Ajustar la altura del gráfico
#     margin=dict(t=100, b=100, l=100, r=100)  # Ajustar márgenes
# )

# # Actualizar trazas para bordes más gruesos
# fig_sunburst.update_traces(
#     marker=dict(
#         line=dict(
#             width=2,  # Grosor del borde
#             color='black'  # Color del borde
#         )
#     )
# )

# # Mostrar gráfico de rosca en Streamlit
# st.plotly_chart(fig_sunburst)



# import altair as alt

# # Datos de ejemplo
# d = {
#     'Curso': ['Curso A', 'Curso B', 'Curso C', 'Curso D'],
#     'Valores 1': [20, 35, 30, 35],
#     'Valores 2': [25, 32, 34, 20]
# }

# # Convertir los datos a un DataFrame de pandas
# df = pd.DataFrame(d)

# # Transformar los datos para Altair
# df_melted = df.melt(id_vars='Curso', value_vars=['Valores 1', 'Valores 2'], var_name='Tipo', value_name='Valor')

# # Crear el gráfico
# chart = alt.Chart(df_melted).mark_bar().encode(
#     y=alt.Y('Curso:N', sort='-x'),
#     x=alt.X('Valor:Q', axis=alt.Axis(title='Valores')),
#     color='Tipo:N',
#     tooltip=['Curso', 'Tipo', 'Valor']
# ).properties(
#     title='Comparación de dos valores por curso'
# ).configure_axis(
#     labelFontSize=12,
#     titleFontSize=14
# ).configure_title(
#     fontSize=16
# )

# # Mostrar el gráfico en Streamlit
# st.altair_chart(chart, use_container_width=True)


