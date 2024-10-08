import pandas as pd
import streamlit as st
import plotly.express as px

data = pd.read_json("./data/data.json")

#########################################################################################################################
st.title("Primera Puerta al infierno de Dante.")
st.write("## Primer círculo (ESTAS EN EL LIMBO).")
st.write("Aquí se encuentran las almas de aquellos que no cometieron pecado alguno, pero que no fueron bautizados con la sabiduría de escoger otra carrera, mas bien viven en la felicidad de su ignorancia(SE MATRÍCULAN).")
#########################################################################################################################

###################################################################
st.write("### Inscripciones a la facultad a lo largo del tiempo.")
################################################################## 
inscripciones_por_curso = data['Curso'].value_counts().reset_index()
inscripciones_por_curso.columns = ['Curso', 'Inscripciones']
inscripciones_por_curso = inscripciones_por_curso.sort_values('Curso')

fig01 = px.bar(inscripciones_por_curso, 
                x='Curso', 
                y='Inscripciones', 
                title=f'Número de Inscripciones por Cursos.',
                labels={'Inscripciones':'Número de Inscripciones', 'Curso':'Curso'})
fig01.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig01.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black')) 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Inscripciones', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ))
st.plotly_chart(fig01)

##########################################
st.write("### Inscripciones por género.")
##########################################
inscripciones_por_genero = data.groupby(['Curso', 'Sexo']).size().reset_index(name='Número de Inscripciones')

fig02 = px.bar(inscripciones_por_genero, 
                    x='Curso', 
                    y='Número de Inscripciones', 
                    color='Sexo', 
                    barmode='group',
                    title='Inscripciones por Género y Curso.',
                    labels={'Número de Inscripciones':'Número de Inscripciones', 'Curso':'Curso'},
                    color_discrete_map={'F': 'pink', 'M': 'blue'})
fig02.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig02.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black')) 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Número de Inscripciones', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Género')
st.plotly_chart(fig02)

##############################inscripciones por carreras#####################################
inscripciones_por_genero_carrera = data.groupby(['Curso', 'Carrera', 'Sexo']).size().reset_index(name='Número de Inscripciones')

inscripciones_por_genero_carrera['Curso'] = pd.Categorical(inscripciones_por_genero_carrera['Curso'],
categories = sorted(inscripciones_por_genero_carrera['Curso'].unique()),ordered = True)

fig03 = px.bar(inscripciones_por_genero_carrera, 
                x='Curso', 
                y='Número de Inscripciones', 
                color='Sexo', 
                barmode='stack',
                facet_col='Carrera',
                title='Inscripciones por Género, Curso y Carrera',
                labels={'Número de Inscripciones':'Número de Inscripciones', 'Curso':'Curso'},
                color_discrete_map={'F': 'pink', 'M': 'blue'})
fig03.update_traces(marker=dict(line=dict(color='#000000', width=1)))

fig03.for_each_xaxis(lambda axis: axis.update(showgrid=False, tickfont=dict(color='black'), title=dict(text='Curso', font=dict(color='black'))))
fig03.for_each_yaxis(lambda axis: axis.update(showgrid=False, tickfont=dict(color='black')))

fig03.for_each_annotation(lambda a: a.update(text=a.text.split('=')[1], font=dict(color='black', size=12), bordercolor='black', borderwidth=2))

fig03.update_layout(
    title=dict(
        text='Inscripciones por Género, Curso y Carrera',
        font=dict(color='black')
    ),
    legend_title_text='Género',
    width=1000,  
    height=600,
    xaxis_title=dict(text='Curso', font=dict(color='black')),
    yaxis_title=dict(text='Número de Inscripciones', font=dict(color='black')))
st.plotly_chart(fig03)

#########################################################################
st.write("### Inscripciones por Carrera y Curso a lo Largo de los Años.")
#########################################################################
inscripciones_por_curso = data.groupby(['Curso', 'Carrera']).size().reset_index(name='Número de Inscripciones')
inscripciones_por_curso = inscripciones_por_curso.sort_values('Curso', ascending=False)

fig04 = px.bar(inscripciones_por_curso, 
                y='Curso', 
                x='Número de Inscripciones', 
                color='Carrera',
                barmode='group',
                orientation='h',
                labels={'Número de Inscripciones':'Número de Inscripciones', 'Año':'Año'})
fig04.update_traces(marker=dict(line=dict(width=0)))  
fig04.update_layout(
    title=dict(
        text="Inscripciones por Curso y Carrera", 
        font=dict(color='black')
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Cursos', font=dict(color='black')) 
    ),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Número de Inscripciones', font=dict(color='black'))
    ),
    legend_title_text='Carreras',
    width=900,  
    height=600  
)
st.plotly_chart(fig04)

################################################
st.write("###  Ingresos segun la Vía de Ingreso")
################################################
df_grouped = data.groupby(["Curso", "Vía Ingreso"]).size().reset_index(name="Inscripciones")

fig = px.bar(df_grouped, 
                x="Curso", 
                y="Inscripciones", 
                color="Vía Ingreso", 
                title="Inscripciones por Vía de Ingreso y Curso",
                labels={'Inscripciones': 'Número de Inscripciones', 'Curso': 'Curso'},
                barmode='stack',  
                text_auto=True)
fig.update_layout(
    yaxis=dict(
        title="Número de Inscripciones",
        range=[0, 250],  
        dtick=20,       
        showgrid=False,
        tickfont=dict(color='black')
    ),
    xaxis=dict(
        title="Curso",
        showgrid=False,
        tickfont=dict(color='black')
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title="Vía de Ingreso",
    width=1000,  
    height=600   
)
st.plotly_chart(fig, use_container_width=False)  

###########################################
st.write("### Vía de Ingreso por Carrera.")
###########################################
fil = data.groupby(["Curso", "Carrera", "Vía Ingreso"]).size().reset_index(name="Cantidad")

cursos = data['Curso'].unique()
carreras = data['Carrera'].unique()

selected_carrera = st.selectbox('Selecciona la Carrera deseada:', carreras)
selected_curso = st.selectbox('Selecciona el Curso:', cursos)

df_filtrado = data[(data['Curso'] == selected_curso) & (data['Carrera'] == selected_carrera)]

via_ingreso_counts = df_filtrado['Vía Ingreso'].value_counts().reset_index()
via_ingreso_counts.columns = ['Vía Ingreso', 'Número de Estudiantes']

via_ingreso_counts['Porcentaje'] = (via_ingreso_counts['Número de Estudiantes'] / via_ingreso_counts['Número de Estudiantes'].sum()) * 100

fig07 = px.pie(via_ingreso_counts, 
                        names='Vía Ingreso', 
                        values='Número de Estudiantes', 
                        title=f'Curso: {selected_curso} - Carrera: {selected_carrera}',
                        labels={'Número de Estudiantes': 'Número de Estudiantes'},
                        color='Vía Ingreso')
fig07.update_traces(textinfo='percent',
                        marker=dict(line=dict(color='#000000', width=2)))
fig07.update_layout(legend_title_text='Vías de Ingreso:',
                    width=400,
                    height=400,
                    margin=dict(l=0, r=0, t=30, b=2))

df_preuniversitario = df_filtrado[df_filtrado['Vía Ingreso'].str.contains('INSTITUTOS PREUNIVERSITARIOS', na=False)]

distribucion_pre = df_preuniversitario.groupby(['Curso', 'Tipo de Pre']).size().reset_index(name='Número de Estudiantes')

fig08 = px.pie(distribucion_pre, 
                names='Tipo de Pre', 
                values='Número de Estudiantes', 
                labels={'Número de Estudiantes': 'Número de Estudiantes'},
                color='Tipo de Pre')
fig08.update_traces(textinfo='percent',
                        marker=dict(line=dict(color='#000000', width=2)))
fig08.update_layout(legend_title_text='Tipo de INSTITUTO PREUNIVERSITARIO',
                    width=600,
                    height=400,
                    margin=dict(l=20, r=20, t=50, b=20))

col1, col2 = st.columns([2, 1.6])
with col1:
    st.plotly_chart(fig07, use_container_width=True)  

with col2:
    st.plotly_chart(fig08, use_container_width=True)  

##############################################
st.write("### Inscripciones por Provincia.")
##############################################
inscripciones_por_provincia = data.groupby(['Curso', 'Provincia']).size().reset_index(name='Número de Inscripciones')
inscripciones_por_provincia['Curso'] = pd.Categorical(inscripciones_por_provincia['Curso'], categories=sorted(inscripciones_por_provincia['Curso'].unique()), ordered=True)
inscripciones_por_provincia = inscripciones_por_provincia.sort_values('Curso')
unique_provincias = inscripciones_por_provincia['Provincia'].unique()

selected_provincias = st.multiselect('Selecciona la opción deseada:', options=unique_provincias, default=[], placeholder="Seleccione las Provincias deseadas")
if selected_provincias:
    filtered_data = inscripciones_por_provincia[inscripciones_por_provincia['Provincia'].isin(selected_provincias)]
else:
    filtered_data = inscripciones_por_provincia

color_map = {provincia: color for provincia, color in zip(unique_provincias, px.colors.qualitative.Plotly)}

fig09 = px.line(filtered_data, 
                x='Curso', 
                y='Número de Inscripciones', 
                color='Provincia', 
                markers=True, 
                title='Inscripciones por Provincia',
                labels={'Número de Inscripciones': 'Número de Inscripciones', 'Curso': 'Curso'},
                color_discrete_map=color_map)  
fig09.update_traces(line=dict(width=4), marker=dict(size=7, line=dict(color='#000000', width=2)))
fig09.update_layout(
    width=800,  
    height=600,  
    xaxis=dict(
        showgrid=False, 
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black')),
        categoryorder='category ascending'  
    ),  
    yaxis=dict(
        showgrid=False, 
        tickfont=dict(color='black'),
        title=dict(text='Número de Inscripciones', font=dict(color='black')),
        range=[0, 250], 
        dtick=25  
    ),
    title=dict(font=dict(color='black')),
    legend_title_text='Provincia'
)
st.plotly_chart(fig09)
