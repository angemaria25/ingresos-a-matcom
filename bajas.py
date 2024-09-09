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

fig12 = px.bar(
    bajas_por_genero,
    y='Curso',
    x='Porcentaje de Bajas',
    color='Sexo',
    barmode='group',
    orientation='h',
    title='Porcentaje de Bajas por Sexo y Curso.',
    labels={'Porcentaje de Bajas': 'Porcentaje de Bajas (%)', 'Curso': 'Curso'},
    color_discrete_map={'F': 'red', 'M': 'blue'}
)
fig12.update_traces(marker=dict(line=dict(color='#000000', width=2)))

fig12.update_layout(
    autosize=False,
    width=1200,  
    height=700,  
    margin=dict(l=100, r=40, t=50, b=40),
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
    legend=dict(
        title=dict(text='Género'),
        font=dict(size=12)  
    )
)
st.plotly_chart(fig12, use_container_width=True)


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
    
    bajas_hembras_curso['Porcentaje de Bajas Carrera'] = (bajas_hembras_curso['Número de Bajas Carrera'] / bajas_hembras_curso['Total Bajas Curso']) * 100
    
    cursos_ordenados = sorted(bajas_hembras_curso['Curso'].unique(), key=lambda x: (int(x.split('-')[0]), int(x.split('-')[1])))
    
    carreras = bajas_hembras_curso['Carrera'].unique()
    colores = px.colors.qualitative.Plotly  
    color_discrete_map = {carrera: colores[i % len(colores)] for i, carrera in enumerate(carreras)}
    
    fig13 = px.bar(
        bajas_hembras_curso, 
        y='Curso', 
        x='Porcentaje de Bajas Carrera', 
        color='Carrera',
        barmode='group',
        orientation='h',
        title='Porcentaje de Hembras que solicitan la baja en cada Curso.',
        labels={'Porcentaje de Bajas Carrera': 'Porcentaje de Bajas (%)', 'Curso': 'Curso', 'Carrera': 'Carrera'},
        color_discrete_map=color_discrete_map,
        category_orders={'Curso': cursos_ordenados}
    )
    
    fig13.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig13.update_layout(
        autosize=False,
        width=900,  
        height=600,  
        margin=dict(l=100, r=40, t=50, b=40),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color='black', size=12),
            title=dict(text='Porcentaje de Bajas', font=dict(color='black')) 
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color='black', size=12),
            title=dict(text='Curso', font=dict(color='black'))
        ),
        title=dict(
            font=dict(color='black')
        ),
        legend=dict(
            title=dict(text='Carrera'),
            font=dict(size=12)  
        )
    )
    st.plotly_chart(fig13, use_container_width=True)

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

fig15 = px.pie(
    bajas_becados_curso, 
    names='Provincia', 
    values='Porcentaje', 
    title=f'Porciento de Bajas de Estudiantes Becados por Provincia en el Curso {curso_seleccionado}',
    labels={'Provincia': 'Provincia', 'Porcentaje': 'Porcentaje de Estudiantes Becados'})
st.plotly_chart(fig15)

#########################################################################################################################
st.write("### ¿La preparación en dependencia de la Vía de Ingreso puede afectar a que el estudiante se sienta en la necesidad de pedir de la baja?")
##########################################################################################################################
bajas_por_via = bajas.groupby(['Curso', 'Vía Ingreso']).size().reset_index(name='Número de Bajas')
total_bajas_por_curso = bajas_por_via.groupby('Curso')['Número de Bajas'].sum().reset_index(name='Total Bajas')
bajas_por_via = bajas_por_via.merge(total_bajas_por_curso, on='Curso')
bajas_por_via['Porcentaje de Bajas'] = (bajas_por_via['Número de Bajas'] / bajas_por_via['Total Bajas']) * 100

bajas_por_via['Curso'] = pd.Categorical(bajas_por_via['Curso'], categories=sorted(bajas_por_via['Curso'].unique()), ordered=True)

fig16 = px.scatter(
    bajas_por_via,
    x='Curso',
    y='Vía Ingreso',
    size='Porcentaje de Bajas',
    color='Vía Ingreso',
    title='Porcentaje de Bajas por Vía de Ingreso y Curso',
    labels={'Porcentaje de Bajas': 'Porcentaje de Bajas', 'Curso': 'Curso', 'Vía Ingreso': 'Vía de Ingreso'},
    size_max=60
)
fig16.update_traces(marker=dict(line=dict(color='#000000', width=2)))

fig16.update_layout(
    autosize=True,
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black', size=12),
        title=dict(text='Curso', font=dict(color='black')),
        type='category' 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black', size=10),
        showticklabels=False,
        title=dict(text='')
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend=dict(
        title=dict(text='Leyenda'),
        font=dict(size=10)  
    )
)
st.plotly_chart(fig16, use_container_width=True)

####################################
#Distribución según el tipo de pre.
####################################
data_preuniversitario = bajas.dropna(subset=['Vía Ingreso'])
data_preuniversitario = data_preuniversitario[data_preuniversitario['Vía Ingreso'].str.contains('INSTITUTOS PREUNIVERSITARIOS', na=False)]

distribucion_pre = data_preuniversitario.groupby(['Curso', 'Tipo de Pre']).size().reset_index(name='Número de Estudiantes')

total_estudiantes_por_curso = distribucion_pre.groupby('Curso')['Número de Estudiantes'].sum().reset_index(name='Total Estudiantes')

distribucion_pre = distribucion_pre.merge(total_estudiantes_por_curso, on='Curso')
distribucion_pre['Porcentaje de Estudiantes'] = (distribucion_pre['Número de Estudiantes'] / distribucion_pre['Total Estudiantes']) * 100

fig17 = px.bar(distribucion_pre,
                y='Curso',
                x='Porcentaje de Estudiantes',
                color='Tipo de Pre',
                barmode='stack',
                orientation='h',
                title='Distribución de Estudiantes de Preuniversitario según el Tipo de Pre.',
                labels={'Porcentaje de Estudiantes': 'Porcentaje de Estudiantes', 'Curso': 'Curso'})
fig17.update_traces(marker=dict(line=dict(color='#000000', width=1)))
fig17.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Porcentaje de Estudiantes', font=dict(color='black'))
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
st.plotly_chart(fig17)

####################################################################################################################
st.write("### ¿En qué municipio se concentra la mayor cantidad de bajas de IPU según el tipo de preuniversitario?")
####################################################################################################################
pre_normal = bajas[bajas["Tipo de Pre"] == "IPU"]
a = pre_normal.groupby(["Municipio", "Curso"]).size().reset_index(name="Número de bajas")

unique_municipios = a['Municipio'].unique()

selected_municipios = st.multiselect('Seleccione una opción:', options=unique_municipios, placeholder='Seleccione los Municipios deseados')

if not selected_municipios:
    filtered_data = a
else:
    filtered_data = a[a['Municipio'].isin(selected_municipios)]
    
color_discrete_sequence = px.colors.qualitative.Dark24[:len(unique_municipios)]

fig18 = px.scatter(filtered_data, 
                    x='Curso', 
                    y='Número de bajas', 
                    color='Municipio',
                    color_discrete_sequence=color_discrete_sequence,
                    category_orders={'Curso': sorted(filtered_data['Curso'].unique())},
                    title='Distribución de Estudiantes de Baja de IPU por Municipio según los Tipos de Preuniversitarios')
fig18.update_traces(marker=dict(line=dict(color='#000000', width=1)))
fig18.update_layout(
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
st.plotly_chart(fig18)


######################################################
st.write("### Distribución de las Bajas por Carrera.")
######################################################
bajas['Curso'] = bajas['Curso'].fillna('Desconocido')
bajas['Carrera'] = bajas['Carrera'].fillna('Desconocida')

bajas = bajas[bajas['Carrera'] != 'Desconocida']

cursos_disponibles = sorted(bajas['Curso'].unique(), key=lambda x: x.split('-')[0])

cursos_select = st.select_slider(
    'Selecciona el rango de Cursos:',
    options=cursos_disponibles,
    value=(cursos_disponibles[0], cursos_disponibles[-1])
)

bajas = bajas[bajas['Curso'].between(cursos_select[0], cursos_select[1])]

carreras_disponibles = sorted(bajas['Carrera'].unique())

carreras_seleccionadas = {carrera: st.checkbox(carrera, value=True) for carrera in carreras_disponibles}

carreras_filtradas = [carrera for carrera, seleccionada in carreras_seleccionadas.items() if seleccionada]

bajas = bajas[bajas['Carrera'].isin(carreras_filtradas)]

bajas_por_carrera_curso = bajas.groupby(['Carrera', 'Curso']).size().reset_index(name='Número de Bajas')

bajas_por_carrera_curso['Curso'] = pd.Categorical(bajas_por_carrera_curso['Curso'], categories=cursos_disponibles, ordered=True)
bajas_por_carrera_curso = bajas_por_carrera_curso.sort_values('Curso')

fig19 = px.line(bajas_por_carrera_curso,
                x='Curso',
                y='Número de Bajas',
                color='Carrera',
                title='Número de Bajas por Carrera y Curso',
                labels={'Número de Bajas': 'Número de Bajas', 'Curso': 'Curso'},
                markers=True,
                color_discrete_map={carrera: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                                    for i, carrera in enumerate(bajas['Carrera'].unique())})
fig19.update_traces(
    line=dict(width=3.5),
    marker=dict(size=7, symbol='circle', line=dict(width=3, color='black'))
)
fig19.update_layout(
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
    legend_title_text='Carreras'
)
st.plotly_chart(fig19)

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

