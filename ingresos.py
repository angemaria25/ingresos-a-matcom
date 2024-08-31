import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

data = pd.read_json("./datos/datos_clasificados.json")

# Eliminar espacios en blanco al principio y al final de los nombres de las columnas
data.columns = data.columns.str.strip()
# Eliminar espacios en blanco al principio y al final de todas las celdas
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
# Configurar pandas para mostrar todas las filas y columnas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)  
pd.set_option('display.expand_frame_repr', False)

st.markdown("# Ingresos a la MATCOM.")
###################################################################
st.write("### Inscripciones a la facultad a lo largo del tiempo.")
###################################################################
# Calcular el número de inscripciones por curso contando las repeticiones
inscripciones_por_curso = data['Curso'].value_counts().reset_index()
inscripciones_por_curso.columns = ['Curso', 'Inscripciones']

# Ordenar los cursos
inscripciones_por_curso = inscripciones_por_curso.sort_values('Curso')

# Crear filtros para seleccionar el curso de inicio y el curso final
curso_inicio = st.selectbox(
    'Selecciona el curso de inicio',
    options=inscripciones_por_curso['Curso'].unique(),
    index=0  # Por defecto, selecciona el primer curso en la lista
)

curso_final = st.selectbox(
    'Selecciona el curso final',
    options=inscripciones_por_curso['Curso'].unique(),
    index=len(inscripciones_por_curso['Curso'].unique()) - 1  # Por defecto, selecciona el último curso en la lista
)

# Filtrar los datos según el intervalo de cursos seleccionado
datos_filtrados = inscripciones_por_curso[
    (inscripciones_por_curso['Curso'] >= curso_inicio) & 
    (inscripciones_por_curso['Curso'] <= curso_final)
]

# Crear la gráfica de barras para el intervalo seleccionado
fig01 = px.bar(datos_filtrados, 
                x='Curso', 
                y='Inscripciones', 
                title=f'Número de Inscripciones para Cursos entre {curso_inicio} y {curso_final}',
                labels={'Inscripciones':'Número de Inscripciones', 'Curso':'Curso'})
fig01.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig01.update_layout(
    xaxis=dict(showgrid=False),  
    yaxis=dict(showgrid=False),
    legend_title_text='Cursos')
st.plotly_chart(fig01)

##########################################
st.write("### Inscripciones por genero.")
##########################################
st.write("### Falta hacer la grafica para CD.")
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
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Género')
st.plotly_chart(fig02)

inscripciones_por_genero_carrera = data.groupby(['Curso', 'Carrera', 'Sexo']).size().reset_index(name='Número de Inscripciones')

fig03 = px.bar(inscripciones_por_genero_carrera, 
                x='Curso', 
                y='Número de Inscripciones', 
                color='Sexo', 
                barmode='stack',
                facet_col='Carrera',
                title='Inscripciones por Género, Curso y Carrera (Apilado)',
                labels={'Número de Inscripciones':'Número de Inscripciones', 'Curso':'Curso'},
                color_discrete_map={'F': 'pink', 'M': 'blue'})

fig03.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig03.update_layout(
    xaxis=dict(showgrid=False),  
    yaxis=dict(showgrid=False),
    legend_title_text='Género')
st.plotly_chart(fig03)
#########################################################################
st.write("### Inscripciones por Carrera y Curso a lo Largo de los Años.")
#########################################################################
carreras_unicas = data['Carrera'].unique()
carreras_seleccionadas = st.multiselect('Seleccione las carreras que desea visualizar:', options=carreras_unicas, placeholder='Carreras')

cursos_unicos = data['Curso'].unique()
cursos_seleccionados = st.multiselect('Seleccione los cursos que desea visualizar:', options=cursos_unicos, placeholder='Cursos')

if cursos_seleccionados and carreras_seleccionadas:
    data_filtrada = data[data['Curso'].isin(cursos_seleccionados) & data['Carrera'].isin(carreras_seleccionadas)]
elif cursos_seleccionados:
    data_filtrada = data[data['Curso'].isin(cursos_seleccionados)]
elif carreras_seleccionadas:
    data_filtrada = data[data['Carrera'].isin(carreras_seleccionadas)]
else:
    data_filtrada = data

inscripciones_por_curso = data_filtrada.groupby(['Curso', 'Carrera']).size().reset_index(name='Número de Inscripciones')
fig04 = px.bar(inscripciones_por_curso, 
                y='Curso', 
                x='Número de Inscripciones', 
                color='Carrera', barmode='group',
                orientation='h',
                labels={'Número de Inscripciones':'Número de Inscripciones', 'Año':'Año'})
fig04.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig04.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), legend_title_text='Carreras:')
st.plotly_chart(fig04)

################################################
st.write("### Distribución por Vía de Ingreso")
################################################
inscripciones_por_via = data.groupby(['Curso', 'Vía Ingreso']).size().reset_index(name='Número de Inscripciones')
fig05 = px.bar(inscripciones_por_via, 
                    x='Curso', 
                    y='Número de Inscripciones', 
                    color='Vía Ingreso', 
                    barmode='group',
                    title='Inscripciones por Vía de Ingreso y Curso.',
                    labels={'Número de Inscripciones':'Número de Inscripciones', 'Curso':'Curso'})
fig05.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig05.update_layout(
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Vía de Ingreso')
st.plotly_chart(fig05)
    
data_preuniversitario = data.dropna(subset=['Vía Ingreso'])

data_preuniversitario = data_preuniversitario[data_preuniversitario['Vía Ingreso'].str.contains('INSTITUTOS PREUNIVERSITARIOS', na=False)]

distribucion_pre = data_preuniversitario.groupby(['Curso', 'Tipo de Pre']).size().reset_index(name='Número de Estudiantes')
        
fig06 = px.line(distribucion_pre, 
                            x='Curso', 
                            y='Número de Estudiantes', 
                            color='Tipo de Pre', 
                            title='Distribución de Estudiantes de Preuniversitario según el Tipo de Pre.',
                            labels={'Número de Estudiantes':'Número de Estudiantes', 'Curso':'Curso'})
fig06.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig06.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), legend_title_text='Tipo de Pre')
st.plotly_chart(fig06)
###########################################
st.write("### Vía de Ingreso por Carrera.")
###########################################
fil = data.groupby(["Curso", "Carrera", "Vía Ingreso"]).size().reset_index(name="Cantidad")
st.write(fil)

cursos = data['Curso'].unique()
carreras = data['Carrera'].unique()

selected_carrera = st.selectbox('Selecciona la Carrera deseada:', carreras)
selected_curso = st.selectbox('Selecciona el Curso:', cursos)

df_filtrado = data[(data['Curso'] == selected_curso) & (data['Carrera'] == selected_carrera)]

via_ingreso_counts = df_filtrado['Vía Ingreso'].value_counts().reset_index()
via_ingreso_counts.columns = ['Vía Ingreso', 'Número de Estudiantes']

# Calcular porcentajes
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

# Gráfico de Línea para 'Número de Estudiantes' por Tipo de Instituto
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
    st.plotly_chart(fig07, use_container_width=True)  # Gráfico de Pie en la primera columna

with col2:
    st.plotly_chart(fig08, use_container_width=True)  # Gráfico de Línea en la segunda columna

########################################################
st.write("### Inscripciones por Provincia.")
########################################################
inscripciones_por_provincia = data.groupby(['Curso', 'Provincia']).size().reset_index(name='Número de Inscripciones')

fig09 = px.bar(inscripciones_por_provincia, 
                    x='Curso', 
                    y='Número de Inscripciones', 
                    color='Provincia', 
                    barmode='group',
                    title='Inscripciones por Provincia.',
                    labels={'Número de Inscripciones':'Número de Inscripciones', 'Curso':'Curso'})
fig09.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig09.update_layout(
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Provincia')
st.plotly_chart(fig09)

