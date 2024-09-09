import streamlit as st
import pandas as pd
import plotly.express as px
import re

data = pd.read_json("./data/data_grupos.json")

########################################################
st.title("Sigue el camino de Dante por el infierno...")
########################################################

############
#Repitencia
############
st.write("## Segundo círculo (LUJURIA...SE EXITA POR EL APROBADO).")
st.write("### Este círculo esta reservado para las almas que son arrastradas eternamente por una tormenta violenta por pasar de año, simbolizando la pasión incontrolada por la carrera.")


##############################################################
repitentes = data[data['Situación académica'] == 'Repitente']
rep = repitentes.drop_duplicates(subset='Nombre y Apellidos')
##############################################################


##########################################################################################################################
st.write("### ¿Cuál ha sido el comportamiento de los estudiantes que han repetido curso desde el curso 2018-2019 hasta el presente?")
##########################################################################################################################
rep_curso = rep.groupby('Curso').size().reset_index(name='Cantidad de repitentes')

fig01 = px.bar(rep_curso, 
            x='Curso', 
            y='Cantidad de repitentes', 
            title='Cantidad de Repitentes por Curso', 
            labels={'Cantidad de repitentes':'Cantidad de Repitentes', 'Curso':'Curso'})
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
        title=dict(text='Cantidad de repitentes', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ))
st.plotly_chart(fig01)

###########################################################################################
st.write("### ¿Cuál es el sexo predominante entre los estudiantes que han repiten curso?")
###########################################################################################
carreras = [''] + rep['Carrera'].dropna().unique().tolist()
carrera_seleccionada = st.selectbox('Selecciona una carrera:', options=carreras)

if carrera_seleccionada:
    rep_filtrado = rep[rep['Carrera'] == carrera_seleccionada]
else:
    rep_filtrado = rep

rep_sexo_curso = rep_filtrado.groupby(['Curso', 'Sexo']).size().reset_index(name='Cantidad')

rep_sexo_curso['Total'] = rep_sexo_curso.groupby('Curso')['Cantidad'].transform('sum')

rep_sexo_curso['Proporción'] = rep_sexo_curso['Cantidad'] / rep_sexo_curso['Total']

if carrera_seleccionada:
    titulo_grafico = f'Proporción de Hembras y Varones por Curso - Carrera: {carrera_seleccionada}'
else:
    titulo_grafico = 'Proporción de Hembras y Varones por Curso'

fig02 = px.bar(
    rep_sexo_curso,
    x='Curso',
    y='Proporción',
    color='Sexo',
    barmode='group',
    title=titulo_grafico,
    labels={'Proporción': 'Proporción de Repitentes', 'Curso': 'Curso'},
    text='Proporción')
fig02.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Curso', font=dict(color='black'))
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Proporción de Repitentes', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Tipo de Pre')
fig02.update_traces(texttemplate='%{text:.2%}', textposition='outside',marker=dict(line=dict(color='#000000', width=2)))
st.plotly_chart(fig02)

##################################################################################
st.write("### ¿De qué carrera provienen los estudiantes que han repetido curso?")
##################################################################################
rep_carrera = rep.groupby(['Curso', 'Carrera']).size().reset_index(name='Cantidad de repitentes')
rep_carrera = rep_carrera.sort_values('Curso', ascending=False)

fig03 = px.bar(rep_carrera, 
            y='Curso', 
            x='Cantidad de repitentes', 
            color='Carrera',
            barmode='group',
            orientation='h',
            title='Cantidad de Repitentes por Carrera', 
            labels={'Cantidad de repitentes':'Cantidad de Repitentes', 'Curso':'Curso'})
fig03.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig03.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Cantidad de repitentes', font=dict(color='black')) 
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
st.plotly_chart(fig03)

######################################################################################
st.write("### ¿En qué año académico están los estudiantes que han repetido curso?")
st.write("Nota: La carrera de Ciencia de Datos comenzó en el curso 2023-2024.")
######################################################################################
rep_ano = rep.groupby(['Curso', 'Carrera', 'Año']).size().reset_index(name='Cantidad de repitentes')

curso_seleccionado = st.selectbox('Selecciona un Curso:', rep_ano['Curso'].unique())
df_filtrado = rep_ano[rep_ano['Curso'] == curso_seleccionado]

carreras_disponibles = df_filtrado['Carrera'].unique()
carreras_seleccionadas = st.multiselect('Selecciona una o más Carreras:', carreras_disponibles,default=carreras_disponibles)

df_filtrado = df_filtrado[df_filtrado['Carrera'].isin(carreras_seleccionadas)]

fig04 = px.bar(df_filtrado,
    x='Año',
    y='Cantidad de repitentes',
    color='Carrera',
    barmode='group', 
    title=f'Cantidad de Repitentes por Año y Carrera para {curso_seleccionado}',
    labels={'Cantidad de repitentes': 'Cantidad de Repitentes', 'Año': 'Año'})
fig04.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig04.update_layout(
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Año', font=dict(color='black')) 
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='black'),
        title=dict(text='Cantidad de repitentes', font=dict(color='black'))
    ),
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Carrera')
st.plotly_chart(fig04)

########################################################################################################################
st.write("### ¿Cuántos estudiantes que han repetido el primer año solicitan la baja? ¿Cuántos solicitan el reingreso?")
st.write("Notas aclaratorias:")
st.write("En el curso 2018-2019 no se tienen datos de promoción.")
st.write("En el curso 2021-2022, ninguno de los dos estudiantes que repitieron solicitó la baja.")
##########################################################################################################################
repitentes_1ro = rep[rep['Año'] == '1ro']
repitentes_1ro['Promoción'] = repitentes_1ro['Promoción'].fillna('')

regex_baja_voluntaria = r'(BAJA|BV\s+\d{2}[./]\d{2}[./]\d{4}|\bB\. V\.\s*\d{2}[./]\d{2}[./]\d{4})'
regex_bajas_desercion = r'(BD\s+\d{2}[./]\d{2}[./]\d{4}|\bB\. D\.\s*\d{2}[./]\d{2}[./]\d{4})'
regex_baja_insuficiencia = r'(BID\s+\d{2}[./]\d{2}[./]\d{4})'
regex_licencia_matricula = r'(LM\s+\d{2}[./]\d{2}[./]\d{4})'

baja_voluntaria = repitentes_1ro[repitentes_1ro['Promoción'].str.contains(regex_baja_voluntaria, case=False, regex=True)]
baja_voluntaria = baja_voluntaria.groupby(['Curso', 'Carrera']).size().reset_index(name='Cantidad de Baja Voluntaria')

bajas_desercion = repitentes_1ro[repitentes_1ro['Promoción'].str.contains(regex_bajas_desercion, case=False, regex=True)]
bajas_desercion = bajas_desercion.groupby(['Curso', 'Carrera']).size().reset_index(name='Cantidad de Bajas por Deserción')

baja_insuficiencia = repitentes_1ro[repitentes_1ro['Promoción'].str.contains(regex_baja_insuficiencia, case=False, regex=True)]
baja_insuficiencia = baja_insuficiencia.groupby(['Curso', 'Carrera']).size().reset_index(name='Cantidad de Bajas por Insuficiencia Docente')

licencia_matricula = repitentes_1ro[repitentes_1ro['Promoción'].str.contains(regex_licencia_matricula, case=False, regex=True)]
licencia_matricula = licencia_matricula.groupby(['Curso', 'Carrera']).size().reset_index(name='Cantidad de Licencia de Matrícula')

regex_reingresos = r'(REINGRESO|Reingreso|Reingresa)'
reingresos = repitentes_1ro[repitentes_1ro['Promoción'].str.contains(regex_reingresos, case=False, regex=True)]
reingresos = reingresos.groupby(['Curso', 'Carrera']).size().reset_index(name='Cantidad de Reingreso')

bajas_df = pd.concat([baja_voluntaria, bajas_desercion, baja_insuficiencia, licencia_matricula], ignore_index=True)
df_analisis = pd.merge(bajas_df, reingresos, on=['Curso', 'Carrera'], how='outer').fillna(0)

df_analisis_melted = df_analisis.melt(id_vars=['Curso', 'Carrera'], 
                                        value_vars=['Cantidad de Baja Voluntaria', 'Cantidad de Bajas por Deserción', 'Cantidad de Bajas por Insuficiencia Docente', 'Cantidad de Licencia de Matrícula', 'Cantidad de Reingreso'],
                                        var_name='Tipo de Solicitud',
                                        value_name='Cantidad')

df_analisis_melted['Tipo de Solicitud'] = df_analisis_melted['Tipo de Solicitud'].replace({
    'Cantidad de Baja Voluntaria': 'Baja Voluntaria',
    'Cantidad de Bajas por Deserción': 'Bajas por Deserción',
    'Cantidad de Bajas por Insuficiencia Docente': 'Bajas por Insuficiencia Docente',
    'Cantidad de Licencia de Matrícula': 'Licencia de Matrícula',
    'Cantidad de Reingreso': 'Reingreso'})

fig05 = px.bar(
    df_analisis_melted,
    x='Curso',
    y='Cantidad',
    color='Tipo de Solicitud',
    facet_col='Carrera',
    barmode='group',
    title='Bajas y Reingresos de los Estudiantes Repitentes de Primer Año.',
    labels={'Cantidad': 'Cantidad', 'Tipo de Solicitud': 'Tipo de Solicitud'})

fig05.for_each_xaxis(lambda axis: axis.update(showgrid=False, tickfont=dict(color='black'), title=dict(text='Curso', font=dict(color='black'))))
fig05.for_each_yaxis(lambda axis: axis.update(showgrid=False, tickfont=dict(color='black')))

fig05.for_each_annotation(lambda a: a.update(text=a.text.split('=')[1], font=dict(color='black', size=12), bordercolor='black', borderwidth=2))

fig05.update_yaxes(matches='y', showticklabels=True, title=dict(text='Cantidad', font=dict(color='black'), standoff=10))
fig05.update_yaxes(showticklabels=False, title=None, row=1, col=2)
fig05.update_yaxes(showticklabels=False, title=None, row=1, col=3)

fig05.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig05.update_layout(
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Tipo de solicitud'
)
st.plotly_chart(fig05)

#########################################################################################################################
st.write("### ¿Cuántos estudiantes de nuevo ingreso (primer año) solicitan repitencia? ¿Cuántos solicitan Año Cero?")
st.write("Notas aclaratorias:")
st.write("La modalidad Año Cero comenzó en el curso 2019-2020 y solo se puede pedir una vez en la carrera, en el segundo semestre del primer año en la facultad y es solo para los están por primera vez en la carrera y que tengan al menos tres asignaturas suspensas en el primer semestre.")
st.write("La repitencia solo se puede solicitar en el segundo semestre de un curso y solo se puede repetir un año de la carrera una sola vez.")
#########################################################################################################################
nuevo_ingreso = data[data["Situación académica"] == "Nuevo Ingreso"]
new = nuevo_ingreso.drop_duplicates(subset=['Nombre y Apellidos', 'Curso', 'Carrera', 'Grupo', 'Semestre'])
new['Promoción'] = new['Promoción'].apply(lambda x: 'Repitencia' if pd.notna(x) and re.search(r'(?i)^repite', x) else x)
filtrado = new[new['Promoción'].isin(['Repitencia', 'Año Cero'])]
conteo = filtrado.groupby(['Carrera', 'Curso', 'Promoción']).size().reset_index(name='Cantidad')

fig06 = px.bar(conteo, 
                x='Curso', 
                y='Cantidad', 
                color='Promoción', 
                barmode='group',
                facet_col='Carrera',
                title='Estudiantes de Nuevo Ingreso que Solicitaron Repitencia o Año Cero')
fig06.for_each_xaxis(lambda axis: axis.update(showgrid=False, tickfont=dict(color='black'), title=dict(text='Curso', font=dict(color='black'))))
fig06.for_each_yaxis(lambda axis: axis.update(showgrid=False, tickfont=dict(color='black')))

fig06.for_each_annotation(lambda a: a.update(text=a.text.split('=')[1], font=dict(color='black', size=12), bordercolor='black', borderwidth=2))

fig06.update_yaxes(matches='y', showticklabels=True, title=dict(text='Cantidad', font=dict(color='black'), standoff=10))
fig06.update_yaxes(showticklabels=False, title=None, row=1, col=2)
fig06.update_yaxes(showticklabels=False, title=None, row=1, col=3)

fig06.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig06.update_layout(
    title=dict(
        font=dict(color='black')
    ),
    legend_title_text='Promoción'
)
st.plotly_chart(fig06)

##########################################################################################################################
st.write("### ¿Cuáles son los motivos de los estudiantes que solicitan repitencia? ¿Qué asignaturas suspenden? ¿Cuáles son estas asignaturas?")
##########################################################################################################################
filtrado = new[new['Promoción'] == 'Repitencia']

asignaturas_desaprobadas = filtrado.melt(
    id_vars=['Carrera', 'Curso'],
    value_vars=['Desaprobadas Sem.1', 'Desaprobadas Sem.2'],
    var_name='Semestre',
    value_name='Asignaturas Desaprobadas')

asignaturas_desaprobadas = asignaturas_desaprobadas.dropna(subset=['Asignaturas Desaprobadas'])
asignaturas_desaprobadas['Asignaturas Desaprobadas'] = asignaturas_desaprobadas['Asignaturas Desaprobadas'].str.split(',')
asignaturas_desaprobadas = asignaturas_desaprobadas.explode('Asignaturas Desaprobadas')

asignaturas_desaprobadas['Asignaturas Desaprobadas'] = asignaturas_desaprobadas['Asignaturas Desaprobadas'].str.strip()

conteo_asignaturas = asignaturas_desaprobadas.groupby(['Carrera', 'Curso', 'Semestre', 'Asignaturas Desaprobadas']).size().reset_index(name='Cantidad')

fig_treemap = px.treemap(conteo_asignaturas, 
                            path=['Carrera', 'Curso', 'Semestre', 'Asignaturas Desaprobadas'], 
                            values='Cantidad', 
                            color='Cantidad',
                            color_continuous_scale='RdBu',
                            title='Asignaturas Desaprobadas por Estudiantes que Solicitaron Repitencia según el Semestre')
st.plotly_chart(fig_treemap)

