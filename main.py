import streamlit as st
import os

# Configuración inicial
st.set_page_config(layout="wide")
st.title("\"Análisis de Ingresos a la Facultad de Matemáticas y Computación\"")
st.markdown("<hr style='height:10px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)

# Menú de navegación
opciones = ['Introducción', 'Ingresos', 'Bajas', 'Repitencia']
selección = st.sidebar.radio('Selecciona una opción:', opciones)

# Ruta al directorio actual
ruta = os.getcwd()

# Mostrar contenido según la selección
if selección == 'Introducción':
    st.write("""
    Bienvenido al análisis de ingresos, bajas y repitencia en la Facultad de Matemáticas y Computación.
    Utiliza el menú para navegar entre las diferentes secciones del análisis.
    """)

elif selección == 'Ingresos':
    with open(f'{ruta}/ingresos.py', encoding="UTF-8") as f:
        exec(f.read())

elif selección == 'Bajas':
    with open(f'{ruta}/bajas.py', encoding="UTF-8") as f:
        exec(f.read())

elif selección == 'Repitencia':
    with open(f'{ruta}/repitencia.py', encoding="UTF-8") as f:
        exec(f.read())
