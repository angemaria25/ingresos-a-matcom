import streamlit as st
import pandas as pd
import plotly.express as px
import re

data = pd.read_json("./datos/data_grupos.json")

########################################################
st.title("Sigue el camino de Dante por el infierno...")
########################################################

############
#Repitencia
############
st.write("## Segundo círculo (LUJURIA...SE EXITA POR EL APROBADO).")
st.write("### Este círculo esta reservado para las almas que son arrastradas eternamente por una tormenta violenta por pasar de año, simbolizando la pasión incontrolada por la carrera.")
st.write("Aclaración: La cantidad de repitentes en un curso proviene del curso anterior.")

##############################################################
repitentes = data[data['Situación académica'] == 'Repitente']
rep = repitentes.drop_duplicates(subset='Nombre y Apellidos')
##############################################################


####################################################################################################
st.write("### ¿Cómo se han comportado los repitentes desde curso 2018-2019 hasta el curso actual?")
####################################################################################################
rep_curso = rep.groupby('Curso').size().reset_index(name='Cantidad de repitentes')

fig01 = px.bar(rep_curso, 
            x='Curso', 
            y='Cantidad de repitentes', 
            title='Cantidad de Repitentes por Curso', 
            labels={'Cantidad de repitentes':'Cantidad de Repitentes', 'Curso':'Curso'})
st.plotly_chart(fig01)

#######################################################################################
st.write("### ¿Cuál es el sexo predominante entre los estudiantes que repiten curso?")
#######################################################################################
# Crear una lista de carreras para el filtro, incluyendo una opción vacía
carreras = [''] + rep['Carrera'].dropna().unique().tolist()
carrera_seleccionada = st.selectbox('Selecciona una carrera:', options=carreras)

# Filtrar los datos según la carrera seleccionada
if carrera_seleccionada:
    rep_filtrado = rep[rep['Carrera'] == carrera_seleccionada]
else:
    rep_filtrado = rep

# Agrupar por curso y sexo
rep_sexo_curso = rep_filtrado.groupby(['Curso', 'Sexo']).size().reset_index(name='Cantidad')

# Calcular el total de repitentes por curso
rep_sexo_curso['Total'] = rep_sexo_curso.groupby('Curso')['Cantidad'].transform('sum')

# Calcular la proporción de cada sexo por curso
rep_sexo_curso['Proporción'] = rep_sexo_curso['Cantidad'] / rep_sexo_curso['Total']

# Crear el título del gráfico
if carrera_seleccionada:
    titulo_grafico = f'Proporción de Hembras y Varones por Curso - Carrera: {carrera_seleccionada}'
else:
    titulo_grafico = 'Proporción de Hembras y Varones por Curso'

# Crear gráfico con Plotly
fig02 = px.bar(
    rep_sexo_curso,
    x='Curso',
    y='Proporción',
    color='Sexo',
    barmode='group',
    title=titulo_grafico,
    labels={'Proporción': 'Proporción de Repitentes', 'Curso': 'Curso'},
    text='Proporción')
fig02.update_layout(xaxis_title='Curso', yaxis_title='Proporción de Repitentes')
fig02.update_traces(texttemplate='%{text:.2%}', textposition='outside')
st.plotly_chart(fig02)

####################################################################################################
st.write(" ### ¿De qué carrera es que proceden los repitentes? ¿Qué carrera tiene más repitentes?")
####################################################################################################
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
st.plotly_chart(fig03)

######################################################################################
st.write("### ¿Qué año cursan los estudiantes repitentes?")
st.write("Aclaración: La carrera de Ciencia de Datos comenzó en el curso 2023-2024.")
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
st.plotly_chart(fig04)

################################################################################################
st.write("### ¿De los repitentes de 1er Año cuántos piden la Baja? ¿Cuántos piden Reingreso?")
st.write("Aclaraciones:")
st.write("En 2018-2019 no se tienen datos de Promoción.")
st.write("En 2021-2022 de los dos repitentes que había ninguno pidió la baja.")
################################################################################################
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
st.plotly_chart(fig05)

#########################################################################################################################
st.write("### ¿Cuántos estudiantes de Nuevo Ingreso (Primer Año) piden Repitencia? ¿Cuántos piden Año Cero?")
st.write("Aclaraciones:")
st.write("La modalidad Año Cero comenzó en el curso 2019-2020 y solo se puede pedir en el segundo semestre de primer año.")
st.write("La repitencia solo se puede pedir en el segundo semestre de un curso y solo se puede repetir un año de la carrera una sola vez.")
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
st.plotly_chart(fig06)

##########################################################################################################################
st.write("### ¿Cuáles son los motivos de los estudiantes que piden Repitencia? ¿Qué asignaturas suspenden? ¿Cuáles son estas asignaturas?")
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


############
#Reingreso
############
st.title("Dante se mantiene firme y encuentra otra puerta para regresar al infierno.")
st.write("### Tercer círculo (GLOTONES...NO APRENDIERON LO SUFICIENTE Y VIENEN A POR MÁS).")
st.write("Aquí se encuentra los que han sido azotados por una lluvia de suspensos pero siguen sonriendo pese al castigo impartido por el demonio Cerbero que no los deja superar logicamente las pruebas.")


###########################################################################################################
st.write("### ¿De los estudiantes que reingresan cuántos pasan para segundo?")
st.write("Los reingresos son los que piden Año Cero y luego entran al curso siguiente en primer año.")
###########################################################################################################

