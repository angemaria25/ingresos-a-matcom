import streamlit as st
import pandas as pd

data = pd.read_json("./datos/data_grupos.json")

########################################################
st.title("Sigue el camino de Dante por el infierno...")
########################################################

############
#Repitencia
############
st.write("### Segundo círculo (LUJURIA...SE EXITA POR EL APROBADO).")
st.write("Este círculo esta reservado para las almas que son arrastradas eternamente por una tormenta violenta por pasar de año, simbolizando la pasió incontrolada por la carrera.")


#rep = data[data["Situación académica"] == "Repitente"]






############
#Reingreso
############
st.title("Dante se mantiene firme y encuentra otra puerta para regresar al infierno.")
st.write("### Tercer círculo (GLOTONES...NO APRENDIERON LO SUFICIENTE Y VIENEN A POR MÁS).")
st.write("Aquí se encuentra los que han sido azotados por una lluvia de suspensos pero siguen sonriendo pese al castigo impartido por el demonio Cerbero que no los deja superar logicamente las pruebas.")