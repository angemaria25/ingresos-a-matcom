import streamlit as st
import os

st.set_page_config(layout="wide")
st.title("Más Allá del Aula: Análisis del Ingreso, Repitencia y Bajas en la Facultad de Matemáticas y Computación.")
st.markdown("<hr style='height:10px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)

opciones = ['🏠 Introducción', '📊 Ingresos', '📉 Bajas', '🔄 Repitencia', '📚 Fuentes de Información']
selección = st.sidebar.radio('Selecciona una opción:', opciones, key="menu_selection")

ruta = os.getcwd()

if selección == '🏠 Introducción':
    st.write("""
    La Facultad de Matemáticas y Computación (MatCom) ha sido tradicionalmente considerada una de las más rigurosas, donde solo los estudiantes más dedicados logran recorrer el largo camino hacia el título. Al igual que el peregrinaje de Dante en la Divina Comedia, los estudiantes atraviesan diversas etapas, desde el momento en que ingresan hasta la incertidumbre de la repitencia o, en los casos más desafortunados, la baja académica.""")
    st.write("""Este proyecto tiene como objetivo analizar los datos históricos de ingreso, repitencia y bajas de los estudiantes en la facultad, utilizando visualizaciones interactivas para descubrir tendencias y patrones que permitan una mejor comprensión de la situación académica. A través de un enfoque de ciencia de datos, curamos la información para ofrecer insights valiosos sobre cómo los estudiantes afrontan los retos que MatCom les presenta.
    """)
    st.write("""Las visualizaciones que encontrarás a lo largo de este análisis están diseñadas para ser interactivas y adaptarse a diferentes filtros, permitiendo observar detalles por curso, carrera, género y vía de ingreso. Esto no solo facilita la interpretación de los datos, sino que también permite realizar comparaciones a lo largo del tiempo.""")
    st.write("""Al igual que Dante en su recorrido por el Infierno, el Purgatorio y el Paraíso, el viaje académico en MatCom puede parecer una travesía por estos tres reinos: desde el entusiasmo del ingreso, pasando por el purgatorio de las asignaturas difíciles, hasta el posible descenso a los círculos de la repitencia o la baja. ¿Qué caminos recorren nuestros estudiantes? Este análisis pretende contarlo, con una dosis de humor y datos concretos que ofrecen una vista panorámica de la realidad académica.""")
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
