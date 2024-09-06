import streamlit as st
import os

st.set_page_config(layout="wide")
st.title("Más Allá del Aula: Un Viaje a través de Ingresos, Desafíos y Repitencias en la Facultad de Matemática y Computación.")
st.markdown("<hr style='height:10px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)

opciones = ['🏠 Introducción', '📊 Ingresos', '📉 Bajas', '🔄 Repitencia', '📚 Fuentes de Información']
selección = st.sidebar.radio('Selecciona una opción:', opciones, key="menu_selection")

ruta = os.getcwd()

if selección == '🏠 Introducción':
    st.write("""
    Bienvenido al análisis de ingresos, bajas y repitencia en la Facultad de Matemáticas y Computación.
    Utiliza el menú para navegar entre las diferentes secciones del análisis.
    """)
elif selección == '📊 Ingresos':
    with open(f'{ruta}/ingresos.py', encoding="UTF-8") as f:
        exec(f.read())
    
elif selección == '📉 Bajas':
    with open(f'{ruta}/bajas.py', encoding="UTF-8") as f:
        exec(f.read())
    
elif selección == '🔄 Repitencia':
    with open(f'{ruta}/repitencia.py', encoding="UTF-8") as f:
        exec(f.read())

elif selección == '📚 Fuentes de Información':
    st.write("""
    ## Fuentes de Información

    La información utilizada en este proyecto proviene de los siguientes datos y fuentes:

    ### Datos de Ingresos
    - **Fuente:** Secretaría de la Facultad de Matemáticas y Computación.
    - **Descripción:** Datos sobre los ingresos de estudiantes a la facultad, incluyendo información sobre fechas y cifras de admisión.

    ### Datos de Bajas
    - **Fuente:** Secretaría de la Facultad de Matemáticas y Computación.
    - **Descripción:** Información sobre las bajas de estudiantes.

    ### Datos de Grupos
    - **Fuente:** Secretaría de la Facultad de Matemáticas y Computación.
    - **Descripción:** Datos sobre los grupos y divisiones de estudiantes dentro de la facultad.

    ### Agradecimientos
    Agradecemos a la Secretaría de la Facultad de Matemáticas y Computación por proporcionar los datos necesarios para este análisis. Sin su colaboración, este proyecto no habría sido posible.

    """)
