import pandas as pd
import streamlit as st
import plotly.express as px

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

st.markdown("# Ingresos a la Facultad de Matemática y Computación.")

#################################################################################
st.write("### Comparación entre el total de inscripciones y bajas.")

inscripciones = data.groupby('Curso').size().reset_index(name='Número de Inscripciones')
bajas = data[data['Estado'] == 'Baja'].groupby('Curso').size().reset_index(name='Número de Bajas')

datos_combinados = pd.merge(inscripciones, bajas, on=['Curso'], how='outer').fillna(0)

datos_melted = datos_combinados.melt(id_vars='Curso', value_vars=['Número de Inscripciones', 'Número de Bajas'], var_name='Métrica', value_name='Número')

fig = px.line(datos_melted, 
                x='Curso', 
                y='Número', 
                color='Métrica', 
                title='Comparación de Inscripciones y Bajas por Curso',
                labels={'Número': 'Número', 'Métrica': 'Métrica', 'Curso': 'Curso'}, markers=True)
fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig.update_layout(
    xaxis=dict(showgrid=False),  
    yaxis=dict(showgrid=False),
    legend_title_text='Métricas'
)
st.plotly_chart(fig)
#########################################################
st.write("### Ingresos a MATCOM a lo largo del tiempo.")
#########################################################
opcion_visualizacion = st.selectbox('Seleccione el tipo de visualización:', ['Total de Inscripciones', 'Inscripciones por Género', 'Inscripciones por Provincia', 'Inscripciones por Vía de Ingreso'])

inscripciones_por_curso = data.groupby('Curso').size().reset_index(name='Número de Inscripciones')

fig01 = px.bar(inscripciones_por_curso, 
                x='Curso', 
                y='Número de Inscripciones', 
                title='Total de Inscripciones por Curso.',
                labels={'Número de Inscripciones':'Número de Inscripciones', 'Curso':'Curso'})

fig01.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig01.update_layout(
    xaxis=dict(showgrid=False),  
    yaxis=dict(showgrid=False),
    legend_title_text='Cursos')

if opcion_visualizacion == 'Inscripciones por Género':
    
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
elif opcion_visualizacion == 'Inscripciones por Provincia':
    inscripciones_por_provincia = data.groupby(['Curso', 'Provincia']).size().reset_index(name='Número de Inscripciones')
    fig03 = px.bar(inscripciones_por_provincia, 
                    x='Curso', 
                    y='Número de Inscripciones', 
                    color='Provincia', 
                    barmode='group',
                    title='Inscripciones por Provincia y Curso.',
                    labels={'Número de Inscripciones':'Número de Inscripciones', 'Curso':'Curso'})
    fig03.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig03.update_layout(
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Provincia')
    st.plotly_chart(fig03)
elif opcion_visualizacion == 'Inscripciones por Vía de Ingreso':
    inscripciones_por_via = data.groupby(['Curso', 'Vía Ingreso']).size().reset_index(name='Número de Inscripciones')
    fig04 = px.bar(inscripciones_por_via, 
                    x='Curso', 
                    y='Número de Inscripciones', 
                    color='Vía Ingreso', 
                    barmode='group',
                    title='Inscripciones por Vía de Ingreso y Curso.',
                    labels={'Número de Inscripciones':'Número de Inscripciones', 'Curso':'Curso'})
    fig04.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig04.update_layout(
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Vía de Ingreso')
    st.plotly_chart(fig04)
    
    data_preuniversitario = data.dropna(subset=['Vía Ingreso'])

    data_preuniversitario = data_preuniversitario[data_preuniversitario['Vía Ingreso'].str.contains('INSTITUTOS PREUNIVERSITARIOS', na=False)]

    distribucion_pre = data_preuniversitario.groupby(['Curso', 'Tipo de Pre']).size().reset_index(name='Número de Estudiantes')
        
    fig05 = px.bar(distribucion_pre, 
                            x='Curso', 
                            y='Número de Estudiantes', 
                            color='Tipo de Pre', 
                            barmode='group',
                            title='Distribución de Estudiantes de Preuniversitario según el Tipo de Pre.',
                            labels={'Número de Estudiantes':'Número de Estudiantes', 'Curso':'Curso'})
    fig05.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig05.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), legend_title_text='Tipo de Pre')
    st.plotly_chart(fig05)
else:
    st.plotly_chart(fig01)


##############################################
st.write("### Ingresos por Carrera y Curso.")
##############################################
opcion_seleccionada = st.radio("Seleccione la opción deseada:",("Ingresos por Carrera y Curso.", "Distribución por Vía de Ingreso."))

if opcion_seleccionada == "Ingresos por Carrera y Curso.":
    st.write("### Inscripciones por Carrera y Curso a lo Largo de los Años.")
    
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
    fig1 = px.bar(inscripciones_por_curso, x='Curso', y='Número de Inscripciones', color='Carrera', barmode='group',
                    labels={'Número de Inscripciones':'Número de Inscripciones', 'Año':'Año'})
    fig1.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig1.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), legend_title_text='Carreras:')
    st.plotly_chart(fig1)

elif opcion_seleccionada == "Distribución por Vía de Ingreso.":
    st.write("### Distribución por Vía de Ingreso")
    
    cursos = data['Curso'].unique()
    carreras = data['Carrera'].unique()

    selected_carrera = st.selectbox('Selecciona la Carrera deseada:', carreras)
    selected_curso = st.selectbox('Selecciona el Curso:', cursos)

    df_filtrado = data[(data['Curso'] == selected_curso) & (data['Carrera'] == selected_carrera)]

    via_ingreso_counts = df_filtrado['Vía Ingreso'].value_counts().reset_index()
    via_ingreso_counts.columns = ['Vía Ingreso', 'Número de Estudiantes']

    fig2 = px.pie(via_ingreso_counts, 
                        names='Vía Ingreso', 
                        values='Número de Estudiantes', 
                        title=f'Curso: {selected_curso} - Carrera: {selected_carrera}',
                        labels={'Número de Estudiantes': 'Número de Estudiantes'},
                        color='Vía Ingreso')
    fig2.update_traces(textinfo='value',
                        hole=0.6,  # Ajusta el tamaño del agujero en el centro
                        marker=dict(line=dict(color='#000000', width=2)))
    fig2.update_layout(legend_title_text='Vías de Ingreso:')
    st.plotly_chart(fig2)
#################################
st.write("### Bajas generales.")
#################################
bajas = data[data['Estado'] == 'Baja']

opcion_visualizacion = st.selectbox('Seleccione la opción deseada:',['Bajas Totales', 'Bajas por Género', 'Bajas por Provincia', 'Bajas por Vía de Ingreso'])

bajas_por_curso = bajas.groupby('Curso').size().reset_index(name='Número de Bajas')

fig11 = px.bar(bajas_por_curso, 
                x='Curso', 
                y='Número de Bajas', 
                title='Total de Bajas por Curso.',
                labels={'Número de Bajas':'Número de Bajas', 'Curso':'Curso'})

fig11.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig11.update_layout(
    xaxis=dict(showgrid=False),  
    yaxis=dict(showgrid=False),
    legend_title_text='Cursos')

if opcion_visualizacion == 'Bajas por Género':
    
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
    fig12.update_layout(
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Género')
    st.plotly_chart(fig12)
elif opcion_visualizacion == 'Bajas por Provincia':
    bajas_por_provincia = bajas.groupby(['Curso', 'Provincia']).size().reset_index(name='Número de Bajas')
    fig13 = px.bar(bajas_por_provincia, 
                    x='Curso', 
                    y='Número de Bajas', 
                    color='Provincia', 
                    barmode='group',
                    title='Bajas por Provincia y Curso.',
                    labels={'Número de Bajas':'Número de Bajas', 'Curso':'Curso'})
    fig13.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig13.update_layout(
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Provincia')
    st.plotly_chart(fig13)
elif opcion_visualizacion == 'Bajas por Vía de Ingreso':
    bajas_por_via = bajas.groupby(['Curso', 'Vía Ingreso']).size().reset_index(name='Número de Bajas')
    fig14 = px.bar(bajas_por_via, 
                    x='Curso', 
                    y='Número de Bajas', 
                    color='Vía Ingreso', 
                    barmode='group',
                    title='Bajas por Vía de Ingreso y Curso.',
                    labels={'Número de Bajas':'Número de Bajas', 'Curso':'Curso'})
    fig14.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig14.update_layout(
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Vía de Ingreso')
    st.plotly_chart(fig14)
    
    bajas_preuniversitarios = bajas[bajas['Vía Ingreso'].str.contains('INSTITUTOS PREUNIVERSITARIOS', na=False)]
    bajas_por_tipo_pre = bajas_preuniversitarios.groupby(['Curso', 'Tipo de Pre']).size().reset_index(name='Número de Bajas')
    
    fig15 = px.bar(bajas_por_tipo_pre, 
                    x='Curso', 
                    y='Número de Bajas', 
                    color='Tipo de Pre', 
                    barmode='group',
                    title='Bajas por Tipo de Preuniversitario y Curso.',
                    labels={'Número de Bajas':'Número de Bajas', 'Curso':'Curso', 'Tipo de Pre':'Tipo de Pre'})
    
    fig15.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig15.update_layout(
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Tipo de Pre')
    st.plotly_chart(fig15)
else:
    st.plotly_chart(fig11)
###########################################
st.write("### Bajas por Curso y Carrera.")
###########################################
opciones = st.radio("Seleccione una opción:",("Bajas por Carrera y Curso.", "Bajas por Vía de Ingreso."))

bajas = data[data['Estado'] == 'Baja']

if opciones == "Bajas por Carrera y Curso.":
    cursos = data['Curso'].unique()
    cursos_select = st.multiselect('Selecciona los Cursos:', cursos, default=[], placeholder='Cursos')
    bajas = bajas[bajas['Curso'].isin(cursos_select) | (cursos_select == [])]

    bajas_por_carrera_curso = bajas.groupby(['Carrera', 'Curso']).size().reset_index(name='Número de Bajas')
    bajas_totales_por_carrera = bajas.groupby('Carrera').size().reset_index(name='Número de Bajas')
    fig3 = px.bar(bajas_por_carrera_curso, 
                    y='Número de Bajas', 
                    x='Curso', 
                    color='Carrera', 
                    barmode='group', 
                    title='Número de Bajas por Carrera y Curso.',
                    labels={'Número de Bajas': 'Número de Bajas', 'Carrera': 'Carrera'},
                    color_discrete_sequence=px.colors.qualitative.Plotly)
    fig3.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig3.update_layout(
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Carreras:'
    )
    st.plotly_chart(fig3)
elif opciones == "Bajas por Vía de Ingreso.":
    st.write("### Vía de ingreso de las bajas.")
    st.write("### La mayor cantidad de bjas son de Pre , en el caso de matematica los que se quedan sin carrera se les otorga matematica")
    
    cursos = data['Curso'].unique()

    carreras = data['Carrera'].unique()

    selected_carrera = st.radio('Selecciona una Carrera:', carreras)

    selected_curso = st.selectbox('Selecciona un Curso:', cursos)

    df_filtrado = bajas[(bajas['Curso'] == selected_curso) & (bajas['Carrera'] == selected_carrera)]

    via_ingreso_counts = df_filtrado.groupby(['Vía Ingreso', 'Carrera', 'Curso']).size().reset_index(name='Número de Bajas')

    fig4 = px.bar(via_ingreso_counts, 
                    x='Vía Ingreso', 
                    y='Número de Bajas', 
                    color='Carrera', 
                    barmode='group', 
                    title=f'Número de Bajas por Vía de Ingreso - Curso: {selected_curso} - Carrera: {selected_carrera}',
                    labels={'Número de Bajas': 'Número de Bajas', 'Vía Ingreso': 'Vía de Ingreso'},
                    color_discrete_sequence=px.colors.qualitative.Plotly)
    fig4.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig4.update_layout(
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False),
        legend_title_text='Carreras:'
    )
    st.plotly_chart(fig4)
    

st.write("### MOTIVOS DE LAS BAJAS???")
st.write("### Xq piden la baja??En que opcion la cojieron??q promedio tenian??.")
st.write("### De los de Pre piden mas la baja los de ipcv o los del pre de la calle??")
st.write("### Motivo de las bajas de Pre?? En que opción cojieron la carrera???de donde vienen??TIENEN ALGO EN COMÚN LAS BAJAS???")
st.write("### Los que mas piden la baja son de Provincia??")
st.write("### Cuantos piden la baja de provincia??")
st.write("### de que via de ingreso vienen los estudiantes de provincia")
st.write("### Existe alguna correlación entre los estudiantes que piden la baja con la opcion??")
st.write("### Cantidad de repitentes?de reingresos?")
st.write("### Como ha variado el promedio del escalafón para el ingreso a las diferentes carreras a lo largo de los años??")
st.write("### Que genero coje mas una carrera especifica y que genero la deja mas")