import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_json("./datos/data.json")

# Configurar pandas para mostrar todas las filas y columnas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)  
pd.set_option('display.expand_frame_repr', False)

#####################################
st.markdown("# Bajas de la MATCOM.")
#####################################

bajas = data[data['Estado'] == 'Baja']

#################################
st.write("### Bajas  por Curso.")
#################################
bajas_por_curso = bajas.groupby('Curso').size().reset_index(name='Número de Bajas')

cursos_disponibles = bajas_por_curso['Curso'].unique()

cursos_seleccionados = st.select_slider(
    'Seleccione el rango de cursos que desee visualizar:', 
    options=sorted(cursos_disponibles), 
    value=(min(cursos_disponibles), max(cursos_disponibles)))

cursos_filtrados = bajas_por_curso[(bajas_por_curso['Curso'] >= cursos_seleccionados[0]) & (bajas_por_curso['Curso'] <= cursos_seleccionados[1])]

fig11 = px.bar(cursos_filtrados, 
                x='Curso', 
                y='Número de Bajas', 
                title='Total de Bajas por Curso.',
                labels={'Número de Bajas':'Número de Bajas', 'Curso':'Curso'})

fig11.update_traces(marker=dict(color='red', line=dict(color='#000000', width=2)))

fig11.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black')) 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Número de Bajas', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Cursos')
st.plotly_chart(fig11)



##################################
st.write("### Bajas por Género.")
##################################
ingresos_por_genero = data.groupby(['Curso', 'Sexo']).size().reset_index(name='Total Ingresos')
bajas_por_genero = bajas.groupby(['Curso', 'Sexo']).size().reset_index(name='Número de Bajas')
bajas_por_genero = bajas_por_genero.merge(ingresos_por_genero, on=['Curso', 'Sexo'])
    
bajas_por_genero['Porcentaje de Bajas'] = (bajas_por_genero['Número de Bajas'] / bajas_por_genero['Total Ingresos']) * 100

bajas_por_genero = bajas_por_genero.sort_values('Curso', ascending=False)

fig12 = px.bar(bajas_por_genero, 
                y='Curso', 
                x='Porcentaje de Bajas', 
                color='Sexo', 
                barmode='group',
                orientation='h',
                title='Porcentaje de Bajas por Género y Curso.',
                labels={'Porcentaje de Bajas':'Porcentaje de Bajas (%)', 'Curso':'Curso'},
                color_discrete_map={'F': 'red', 'M': 'blue'})
fig12.update_traces(marker=dict(line=dict(color='#000000', width=2)))

fig12.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Porcentaje de Bajas', font=dict(color='black')) 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Género')
st.plotly_chart(fig12)

#####################################################
st.write("### De qué carrera vienen las hembras??")
#####################################################
mostrar_grafico_hembras = st.checkbox('Análisis de las Bajas del sexo Femenino por carrera.', value=False)

if mostrar_grafico_hembras:
    bajas_hembras_curso = bajas_por_genero[bajas_por_genero['Sexo'] == 'F'].copy()

    bajas_hembras = bajas[bajas['Sexo'] == 'F']
    bajas_por_carrera_curso = bajas_hembras.groupby(['Curso', 'Carrera']).size().reset_index(name='Número de Bajas Carrera')

    bajas_totales_por_curso = bajas_hembras.groupby('Curso').size().reset_index(name='Total Bajas Curso')

    bajas_hembras_curso = bajas_hembras_curso.merge(bajas_por_carrera_curso, on='Curso')

    bajas_hembras_curso = bajas_hembras_curso.merge(bajas_totales_por_curso, on='Curso')

    bajas_hembras_curso['Porcentaje de Bajas Carrera'] = (bajas_hembras_curso['Número de Bajas Carrera'] / bajas_hembras_curso['Total Bajas Curso']) * bajas_hembras_curso['Porcentaje de Bajas']

    fig_hembras = px.bar(bajas_hembras_curso, 
                            y='Curso', 
                            x='Porcentaje de Bajas Carrera', 
                            color='Carrera',
                            barmode='group',
                            orientation='h',
                            title='Porcentaje de Bajas de Hembras por Carrera dentro de cada Curso.',
                            labels={'Porcentaje de Bajas Carrera': 'Porcentaje de Bajas (%)', 'Curso': 'Curso', 'Carrera': 'Carrera'},
                            color_discrete_map={'LIC. MATEMÁTICA': 'red',    'LIC. CIENCIAS DE LA COMPUTACIÓN': 'lightcoral'})

    fig_hembras.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    
    fig_hembras.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Porcentaje de Bajas', font=dict(color='black')) 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Género')
    st.plotly_chart(fig_hembras)
    
#####################################
st.write("### Bajas por Provincia.")
#####################################
bajas_por_provincia = bajas.groupby(['Curso', 'Provincia']).size().reset_index(name='Número de Bajas')
    
# fig13 = px.bar(bajas_por_provincia, 
#                     x='Curso', 
#                     y='Número de Bajas', 
#                     color='Provincia', 
#                     barmode='group',
#                     title='Bajas por Provincia y Curso.',
#                     labels={'Número de Bajas':'Número de Bajas', 'Curso':'Curso'})
# fig13.update_traces(marker=dict(line=dict(color='#000000', width=2)))
# fig13.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), legend_title_text='Provincia')
# st.plotly_chart(fig13)


# Crear la matriz de valores para el mapa de calor
heatmap_data = bajas_por_provincia.pivot(index='Provincia', columns='Curso', values='Número de Bajas')

# Reemplazar NaN con 0 en la matriz de datos
heatmap_data = heatmap_data.fillna(0)

# Crear el mapa de calor con escala de colores personalizada
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale=[[0, 'rgb(255, 230, 230)'],   # Color claro para valores bajos
                [0.5, 'rgb(255, 140, 140)'], # Color intermedio
                [1, 'rgb(165, 0, 0)']],      # Color oscuro para valores altos
    colorbar=dict(title='Número de Bajas'),
    zmin=0
))

# Agregar cuadrículas
fig_heatmap.update_layout(
    xaxis=dict(
        title='Curso',
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.5)',  # Color de la línea de cuadrícula
        zeroline=False
    ),
    yaxis=dict(
        title='Provincia',
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.5)',  # Color de la línea de cuadrícula
        zeroline=False
    ),
    title='Mapa de Calor de Bajas por Provincia.'
)

# Agregar anotaciones solo para valores no nulos
for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        value = heatmap_data.iloc[i, j]
        if value > 0:  # Solo agregar anotaciones para valores mayores a 0
            fig_heatmap.add_trace(go.Scatter(
                x=[heatmap_data.columns[j]],
                y=[heatmap_data.index[i]],
                text=[f'{value:.0f}'],
                mode='text',
                showlegend=False
            ))
st.plotly_chart(fig_heatmap)

##############################################################################
st.write("### Los estudiantes becados son los que mas piden la baja?")
##############################################################################
a = bajas.groupby(['Curso','Provincia','Situación académica', 'Tipo de estudiante' ]).size().reset_index(name='Cantidad')
st.write(a)
st.write("### La mayor cantidad de bajas de La Habana es Voluntaria, en cambio en el resto de las provincias vienen de estudiantes becados.")
# hab = bajas[(bajas['Provincia'] == 'LA HABANA') & (bajas['Situación académica'] == 'Voluntaria')]
# # Agrupar por curso, situación académica y tipo de estudiante
# habana = hab.groupby(['Curso', 'Situación académica', 'Tipo de estudiante', 'Carrera']).size().reset_index(name='Cantidad')
# st.write(habana)

##########################################
st.write("### Bajas por Vía de Ingreso.")
##########################################
bajas_por_via = bajas.groupby(['Curso', 'Vía Ingreso']).size().reset_index(name='Número de Bajas')

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

fig_bubble.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    legend_title_text='Leyenda:'
)
st.plotly_chart(fig_bubble)

#####################################
#Distribución según el tipo de pre
####################################
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

#########################################################################################
st.write("### De las bajas de IPU, de qué preuniversitario es que vienen más bajas??")
#########################################################################################
pre_normal = bajas[bajas["Tipo de Pre"] == "IPU"]
a = pre_normal.groupby(["Municipio", "Curso"]).size().reset_index(name="Número de bajas")

unique_municipios = a['Municipio'].unique()
color_discrete_sequence = px.colors.qualitative.Dark24[:len(unique_municipios)]

fig = px.scatter(a, 
                x='Curso', 
                y='Número de bajas', 
                color='Municipio',
                color_discrete_sequence=color_discrete_sequence,
                category_orders={'Preuniversitario': ['A', 'B', 'C']},
                title='Distribución de Estudiantes de Pre de la calle por Municipio y Tipo de Preuniversitario')

fig.update_layout(barmode='stack')
st.plotly_chart(fig)

st.write("### Cojer los municipios que mas se repiten y hacer mapa para visualizar a que distancia estan de la universidad??")

###################################
st.write("### Bajas por Carrera.")
###################################
cursos_disponibles = bajas['Curso'].unique()
cursos_select = st.select_slider(
    'Selecciona el rango de Cursos:',
    options=sorted(cursos_disponibles),  
    value=(min(cursos_disponibles), max(cursos_disponibles)))

bajas = bajas[(bajas['Curso'] >= cursos_select[0]) & (bajas['Curso'] <= cursos_select[1])]
carreras_disponibles = bajas['Carrera'].unique()

carreras_seleccionadas = {}

st.write('Carreras:')
for carrera in sorted(carreras_disponibles):
    carreras_seleccionadas[carrera] = st.checkbox(carrera, value=True)

carreras_filtradas = []

for carrera, seleccionada in carreras_seleccionadas.items():
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

##############################################################
st.write("### De matematica cuantas bajas son de varones??")
##############################################################
mat = bajas[bajas["Carrera"] == "LIC. MATEMÁTICA"]
mates = mat.groupby(["Curso", "Sexo"]).size().reset_index(name='Número de bajas')
st.write(mates)

com = bajas[bajas["Carrera"] == "LIC. CIENCIAS DE LA COMPUTACIÓN"]
comput = com.groupby(["Curso", "Sexo"]).size().reset_index(name='Número de bajas')
st.write(comput)

##########################################################################
st.write("### Comparación entre los ingresos y las bajas en cada curso.")
##########################################################################
bajas = data[data["Estado"]=="Baja"].groupby('Curso').size().reset_index(name='Número de Bajas')
ingresos = data.groupby('Curso').size().reset_index(name='Número de Ingresos')

df = pd.merge(bajas, ingresos, on='Curso', how='outer').fillna(0)

df.columns = ['Curso', 'Bajas', 'Ingresos']

fig = go.Figure()

fig.add_trace(go.Bar(
    y=df['Curso'],
    x=-df['Bajas'],
    orientation='h',
    name='Total Bajas por Curso',
    marker_color='red',
    marker_line=dict(color='black', width=1),
    hovertemplate='%{x:.0f}<extra></extra>'
))

fig.add_trace(go.Bar(
    y=df['Curso'],
    x=df['Ingresos'],
    orientation='h',
    name='Total Ingresos por Curso',
    marker_color='green',
    marker_line=dict(color='black', width=1),
    hovertemplate='%{x:.0f}<extra></extra>'
))

fig.update_layout(
    title='Comparación entre Bajas y Ingresos por Cursos',
    xaxis_title='Cantidad',
    yaxis_title='Curso',
    barmode='overlay',
    xaxis=dict(zeroline=False, showgrid=False, gridwidth=1),
    yaxis=dict(title='Curso', showgrid=False, gridwidth=1)
)

fig.update_layout(height=600, width=800)
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


