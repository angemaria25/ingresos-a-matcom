import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_json("./datos/data_grupos.json")

########################################################
st.title("Sigue el camino de Dante por el infierno...")
########################################################

############
#Repitencia
############
st.write("### Segundo círculo (LUJURIA...SE EXITA POR EL APROBADO).")
st.write("Este círculo esta reservado para las almas que son arrastradas eternamente por una tormenta violenta por pasar de año, simbolizando la pasió incontrolada por la carrera.")
st.write("La cantidad de repitentes en un curso proviene del curso anterior.")


##############################################################
repitentes = data[data['Situación académica'] == 'Repitente']
rep = repitentes.drop_duplicates(subset='Nombre y Apellidos')
##############################################################


#####################################################################################################
st.write("Cómo se han comportado los repitentes a partir del curso 2018-2019 hasta la actualidad?")
######################################################################################################
rep_curso = rep.groupby('Curso').size().reset_index(name='Cantidad de repitentes')

fig01 = px.bar(rep_curso, 
            x='Curso', 
            y='Cantidad de repitentes', 
            title='Cantidad de Repitentes por Curso', 
            labels={'Cantidad de repitentes':'Cantidad de Repitentes', 'Curso':'Curso'})
st.plotly_chart(fig01)

##############################################################################################
st.write("De qué carrera es que proceden los repitentes? Qué carrera tiene más repitentes?")
################################################################################################
rep_carrera = rep.groupby(['Curso', 'Carrera']).size().reset_index(name='Cantidad de repitentes')

fig02 = px.bar(rep_carrera, 
            x='Curso', 
            y='Cantidad de repitentes', 
            color='Carrera',
            barmode='group',
            title='Cantidad de Repitentes por Carrera', 
            labels={'Cantidad de repitentes':'Cantidad de Repitentes', 'Curso':'Curso'})
st.plotly_chart(fig02)

#################################################
st.write("De qué año proceden los repitentes?")
#################################################
rep_ano = rep.groupby(['Curso', 'Carrera', 'Año']).size().reset_index(name='Cantidad de repitentes')

curso_seleccionado = st.selectbox('Selecciona un Curso:', rep_ano['Curso'].unique())
df_filtrado = rep_ano[rep_ano['Curso'] == curso_seleccionado]

carreras_disponibles = df_filtrado['Carrera'].unique()
carreras_seleccionadas = st.multiselect('Selecciona una o más Carreras:', carreras_disponibles,default=carreras_disponibles)

df_filtrado = df_filtrado[df_filtrado['Carrera'].isin(carreras_seleccionadas)]

fig03 = px.bar(df_filtrado,
    x='Año',
    y='Cantidad de repitentes',
    color='Carrera',
    barmode='group', 
    title=f'Cantidad de Repitentes por Año y Carrera para {curso_seleccionado}',
    labels={'Cantidad de repitentes': 'Cantidad de Repitentes', 'Año': 'Año'})
st.plotly_chart(fig03)

#########################################################################################
st.write("De los repitentes de 1er Año cuántos piden la Baja? Cuántos piden Reingreso?")
st.write("En 2018-2019 no se tienen datos de Promoción.")
st.write("En 2021-2022 de los dos repitentes que había ninguno pidió la baja.")
#########################################################################################
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

fig = px.bar(
    df_analisis_melted,
    x='Curso',
    y='Cantidad',
    color='Tipo de Solicitud',
    facet_col='Carrera',
    barmode='group',
    title='Bajas y Reingresos de los Estudiantes Repitentes de Primer Año.',
    labels={'Cantidad': 'Cantidad', 'Tipo de Solicitud': 'Tipo de Solicitud'})
st.plotly_chart(fig)

#####################################################################################################################
st.write("De los estudiantes de Nuevo Ingreso(primer año) cuántos piden piden Repitencia? Cuántos piden Año Cero?")
st.write("Explicar la modalidad Año Cero")
#####################################################################################################################


############
#Reingreso
############
st.title("Dante se mantiene firme y encuentra otra puerta para regresar al infierno.")
st.write("### Tercer círculo (GLOTONES...NO APRENDIERON LO SUFICIENTE Y VIENEN A POR MÁS).")
st.write("Aquí se encuentra los que han sido azotados por una lluvia de suspensos pero siguen sonriendo pese al castigo impartido por el demonio Cerbero que no los deja superar logicamente las pruebas.")