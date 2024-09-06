import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_json("./data/data.json")

#########################################################################################################################
st.title("Puerta de liberación inmediata.")
st.write("## Dante decide abandonar el infierno.")
st.write("Atajo de salida, los que deciden ir por  este atajo pueden ir a una 'felicidad' o EXTRAÑAR AL PROPIO INFIERNO.")
#########################################################################################################################

######################################
bajas = data[data['Estado'] == 'Baja']
######################################

###############################################################
st.write("### Bajas de los estudiantes ingresados por curso.")
###############################################################
bajas_por_curso = bajas.groupby('Curso').size().reset_index(name='Número de Bajas')

fig11 = px.bar(bajas_por_curso, 
                x='Curso', 
                y='Número de Bajas', 
                title='Total de bajas de los estudiantes ingresados.',
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

#######################################################################################################################
st.write("### ¿Cómo se comportan la cantidad de bajas respecto al sexo de los estudiantes que ingresan a la Facultad?")
########################################################################################################################
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
                title='Porcentaje de Bajas por Sexo y Curso.',
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

#####################################################################################################################
st.write("### ¿El sexo femenino es el que más tiende a pedir la baja? ¿Cómo se comporta este fenómeno por carreras? ")
#####################################################################################################################
mostrar_grafico_hembras = st.checkbox('Análisis de las Bajas del sexo Femenino por carrera.', value=False)

if mostrar_grafico_hembras:
    bajas_hembras_curso = bajas_por_genero[bajas_por_genero['Sexo'] == 'F'].copy()

    bajas_hembras = bajas[bajas['Sexo'] == 'F']
    bajas_por_carrera_curso = bajas_hembras.groupby(['Curso', 'Carrera']).size().reset_index(name='Número de Bajas Carrera')

    bajas_totales_por_curso = bajas_hembras.groupby('Curso').size().reset_index(name='Total Bajas Curso')

    bajas_hembras_curso = bajas_hembras_curso.merge(bajas_por_carrera_curso, on='Curso')

    bajas_hembras_curso = bajas_hembras_curso.merge(bajas_totales_por_curso, on='Curso')

    bajas_hembras_curso['Porcentaje de Bajas Carrera'] = (bajas_hembras_curso['Número de Bajas Carrera'] / bajas_hembras_curso['Total Bajas Curso']) * bajas_hembras_curso['Porcentaje de Bajas']

    fig13 = px.bar(bajas_hembras_curso, 
                            y='Curso', 
                            x='Porcentaje de Bajas Carrera', 
                            color='Carrera',
                            barmode='group',
                            orientation='h',
                            title='Porcentaje de Hembras que solicitan la baja en cada Curso.',
                            labels={'Porcentaje de Bajas Carrera': 'Porcentaje de Bajas (%)', 'Curso': 'Curso', 'Carrera': 'Carrera'},
                            color_discrete_map={'LIC. MATEMÁTICA': 'red',    'LIC. CIENCIAS DE LA COMPUTACIÓN': 'lightcoral'})
    fig13.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig13.update_layout(
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
    legend_title_text='Carrera')
    st.plotly_chart(fig13)
    
###########################################################################################
st.write("### ¿De que Provincias provienen los estudiantes que mayormente piden la baja?")
###########################################################################################
bajas_por_provincia = bajas.groupby(['Curso', 'Provincia']).size().reset_index(name='Número de Bajas')

heatmap_data = bajas_por_provincia.pivot(index='Provincia', columns='Curso', values='Número de Bajas')
heatmap_data = heatmap_data.fillna(0)

fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale=[[0, 'rgb(255, 230, 230)'],  
                [0.5, 'rgb(255, 140, 140)'], 
                [1, 'rgb(165, 0, 0)']],      
    colorbar=dict(title='Número de Bajas'),
    zmin=0
))
fig_heatmap.update_layout(
    xaxis=dict(
        title='Curso',
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.5)', 
        zeroline=False,
        linecolor='white',  
        titlefont=dict(color='black'), 
        tickfont=dict(color='black')  
    ),
    yaxis=dict(
        title='Provincia',
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.5)',  
        zeroline=False,
        linecolor='white',  
        titlefont=dict(color='black'),  
        tickfont=dict(color='black') 
    ),
    title='Mapa de Calor de Bajas por Provincia.'
)

for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        value = heatmap_data.iloc[i, j]
        if value > 0:  
            fig_heatmap.add_trace(go.Scatter(
                x=[heatmap_data.columns[j]],
                y=[heatmap_data.index[i]],
                text=[f'{value:.0f}'],
                mode='text',
                textfont=dict(color='black'),  
                showlegend=False
            ))
st.plotly_chart(fig_heatmap)

#####################################################################################################################
st.write("### ¿Los estudiantes becados al estar en desventaja por estar lejos de sus hogares, son los que tienden a irse de la carrera?")
#####################################################################################################################
bajas_por_curso_tipo = bajas.groupby(['Curso', 'Tipo de estudiante']).size().reset_index(name='Cantidad')

fig14 = px.bar(
    bajas_por_curso_tipo, 
    x='Curso', 
    y='Cantidad', 
    color='Tipo de estudiante',
    barmode='group',
    title='Bajas por Curso y Tipo de Estudiante',
    labels={'Cantidad': 'Número de Bajas', 'Tipo de estudiante': 'Tipo de Estudiante', 'Curso': 'Curso'})
fig14.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig14.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black')) 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Cantidad', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Tipo de Estudiante')
st.plotly_chart(fig14)


#############################################
#Bajas de estudiastes becados por provincias.
#############################################
bajas_por_curso_tipo = bajas.groupby(['Curso', 'Provincia', 'Tipo de estudiante']).size().reset_index(name='Cantidad')
total_bajas_por_curso_provincia = bajas_por_curso_tipo.groupby(['Curso', 'Provincia'])['Cantidad'].sum().reset_index(name='Total')
bajas_por_curso_tipo = bajas_por_curso_tipo.merge(total_bajas_por_curso_provincia, on=['Curso', 'Provincia'])
bajas_por_curso_tipo['Porcentaje'] = (bajas_por_curso_tipo['Cantidad'] / bajas_por_curso_tipo['Total']) * 100
bajas_becados = bajas_por_curso_tipo[bajas_por_curso_tipo['Tipo de estudiante'] == 'Becado Nacional']

cursos = bajas['Curso'].unique()
curso_seleccionado = st.selectbox('Selecciona un curso:', cursos, index=0)  

bajas_becados_curso = bajas_becados[bajas_becados['Curso'] == curso_seleccionado]

fig = px.pie(
    bajas_becados_curso, 
    names='Provincia', 
    values='Porcentaje', 
    title=f'Porciento de Bajas de Estudiantes Becados por Provincia en el Curso {curso_seleccionado}',
    labels={'Provincia': 'Provincia', 'Porcentaje': 'Porcentaje de Estudiantes Becados'})
st.plotly_chart(fig)

#########################################################################################################################
st.write("### ¿La preparación en dependencia de la Vía de Ingreso puede afectar a que el estudiante se sienta en la necesidad de pedir de la baja?")
##########################################################################################################################
bajas_por_via = bajas.groupby(['Curso', 'Vía Ingreso']).size().reset_index(name='Número de Bajas')

fig15 = px.scatter(
    bajas_por_via,
    x='Curso',
    y='Vía Ingreso',
    size='Número de Bajas',
    color='Vía Ingreso',
    title='Bajas por Vía de Ingreso y Curso',
    labels={'Número de Bajas': 'Número de Bajas', 'Curso': 'Curso', 'Vía Ingreso': 'Vía de Ingreso'},
    size_max=60)
fig15.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig15.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black')) 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Vía Ingreso', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Leyenda')
st.plotly_chart(fig15)

####################################
#Distribución según el tipo de pre
####################################
data_preuniversitario = bajas.dropna(subset=['Vía Ingreso'])
data_preuniversitario = data_preuniversitario[data_preuniversitario['Vía Ingreso'].str.contains('INSTITUTOS PREUNIVERSITARIOS', na=False)]
distribucion_pre = data_preuniversitario.groupby(['Curso', 'Tipo de Pre']).size().reset_index(name='Número de Estudiantes')
        
fig16 = px.bar(distribucion_pre, 
                            y='Curso', 
                            x='Número de Estudiantes', 
                            color='Tipo de Pre', 
                            barmode='stack',
                            orientation='h',
                            title='Distribución de Estudiantes de Preuniversitario según el Tipo de Pre.',
                            labels={'Número de Estudiantes':'Número de Estudiantes', 'Curso':'Curso'})
fig16.update_traces(marker=dict(line=dict(color='#000000', width=1)))
fig16.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Número de Estudiantes', font=dict(color='black')) 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Tipo de Pre')
st.plotly_chart(fig16)

####################################################################################################################
st.write("### ¿En qué municipio se concentra la mayor cantidad de bajas de IPU según el tipo de preuniversitario?")
####################################################################################################################
pre_normal = bajas[bajas["Tipo de Pre"] == "IPU"]
a = pre_normal.groupby(["Municipio", "Curso"]).size().reset_index(name="Número de bajas")

unique_municipios = a['Municipio'].unique()
color_discrete_sequence = px.colors.qualitative.Dark24[:len(unique_municipios)]

fig17 = px.scatter(a, 
                x='Curso', 
                y='Número de bajas', 
                color='Municipio',
                color_discrete_sequence=color_discrete_sequence,
                category_orders={'Preuniversitario': ['A', 'B', 'C']},
                title='Distribución de Estudiantes de Baja de IPU por municipio según los Tipos de Preuniversitarios')
fig17.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig17.update_layout(barmode='stack',
                    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black')) 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Número de bajas', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Municipios')
st.plotly_chart(fig17)

######################################################
st.write("### Distribución de las Bajas por Carrera.")
######################################################
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

fig18 = px.line(bajas_por_carrera_curso,
                x='Curso',
                y='Número de Bajas',
                color='Carrera',
                title='Número de Bajas por Carrera y Curso',
                labels={'Número de Bajas': 'Número de Bajas', 'Carrera': 'Carrera'},
                markers=True,
                color_discrete_map={'LIC. CIENCIAS DE LA COMPUTACION': 'blue', 'LIC. MATEMATICA': 'red'})
fig18.update_traces(
    line=dict(width=3.5),
    marker=dict(size=6, symbol='circle', line=dict(width=2, color='black'), color='black'))
fig18.update_layout(
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
    legend_title_text='Carreras')
st.plotly_chart(fig18)

##############################################################
st.write("### ¿De Matemática cuántas bajas son de varones??")
##############################################################
mat = bajas[bajas["Carrera"] == "LIC. MATEMÁTICA"]
mates = mat.groupby(["Curso", "Sexo"]).size().reset_index(name='Número de bajas')
st.write(mates)

#############################################################################################
st.write("### Comportamiento de las Bajas respecto a la cantidad de Ingresos en cada curso.")
#############################################################################################
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
    hovertemplate='%{x:.0f}<extra></extra>'))
fig.update_layout(
    title='Comparación entre Bajas y Ingresos por Cursos.',
    xaxis_title='Cantidad',
    yaxis_title='Curso',
    barmode='overlay',
    xaxis=dict(
        zeroline=False,
        showgrid=False,
        gridwidth=1,
        color='black',
        tickfont=dict(color='black'),
        titlefont=dict(color='black')
    ),
    yaxis=dict(
        title='Curso',
        showgrid=False,
        gridwidth=1,
        color='black',  
        tickfont=dict(color='black'),
        titlefont=dict(color='black')
    ),
    height=600,
    width=800
)
st.plotly_chart(fig)

