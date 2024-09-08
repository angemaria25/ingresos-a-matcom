import json

with open('data.json', 'r') as file:
    data = json.load(file)

nombres_hombres = [
    "Alejandro", "Carlos", "Diego", "Eduardo", "Fernando", "Gabriel", "Héctor", "Iván", 
    "Javier", "Luis", "Manuel", "Nicolás", "Oscar", "Pablo", "Raúl", "Sergio", "Tomás", 
    "Vicente", "Andrés", "Rubén", "Alberto", "Benjamín", "Cristóbal", "David", "Emilio", 
    "Felipe", "Gonzalo", "Hugo", "Ignacio", "José", "Kevin", "Leandro", "Marcos", "Néstor", 
    "Omar", "Pedro", "Ricardo", "Samuel", "Teodoro", "Ulises", "Víctor", "Walter", "Xavier", 
    "Yago", "Zacarías", "Adrián", "Bernardo", "Camilo", "Daniel", "Esteban", "Federico", 
    "Gerardo", "Hernán", "Ismael", "Joaquín", "Kirian", "Lorenzo", "Matías", "Nahuel", 
    "Orlando", "Patricio", "Ramiro", "Sebastián", "Thiago", "Uriel", "Valentín", "William", 
    "Yeray", "Zenón", "Arturo", "Bruno", "César", "Damián", "Efrén", "Fabián", "Germán", 
    "Horacio", "Iñigo", "Jonás", "Kilian", "Leonardo", "Mario", "Nicolás", "Osvaldo", 
    "Pascual", "Rodrigo", "Simón", "Tadeo", "Vladimir", "Wenceslao", "Ximeno", "Yamil", 
    "Zoltán", "Arnoldo", "Braulio", "Claudio", "Domingo", "Elías", "Félix", "Guillermo", 
    "Hilario", "Iker", "Julio", "Kiko", "Luciano", "Mauricio", "Nelson", "Otto", 
    "Pancho", "Rafael", "Saúl", "Tristán", "Valerio", "Wilfredo", "Yerson", "Zeus", "Jorge", "Cristian", "Roberto", "Enrique", "Gustavo", "Roberto", "Richard", "Miguel", "Lazaro", "Sebastian", "Jose", "Bryan", "Jesus", "Adrian", "CRISTHIAN", "REne", "Ernesto", "Francisco", "Raul", "Henry",
    "Antonio", "Evelio","Maikol", "Andy","Damian", "Reiniel", "Darian", "JESÚS", "Adriel",
]

nombres_mujeres = [
    "Adriana", "Beatriz", "Carla", "Daniela", "Elena", "Fernanda", "Gabriela", "Helena", 
    "Isabel", "Julia", "Karina", "Lucía", "María", "Natalia", "Olga", "Patricia", "Rocío", 
    "Sara", "Tatiana", "Valeria", "Ximena", "Zulema", "Alejandra", "Belén", "Claudia", 
    "Diana", "Estela", "Florencia", "Graciela", "Hilda", "Irene", "Jazmín", "Karla", 
    "Laura", "Marta", "Nerea", "Ofelia", "Paola", "Rebeca", "Sofía", "Teresa", 
    "Vanesa", "Wendy", "Yolanda", "Zaira", "Alicia", "Brenda", "Cecilia", "Dolores", 
    "Elisa", "Francisca", "Guadalupe", "Hanna", "Inés", "Juana", "Katherine", 
    "Lourdes", "Mónica", "Norma", "Oriana", "Paloma", "Raquel", "Selena", "Tamara", 
    "Verónica", "Waleska", "Xiomara", "Yadira", "Zenaida", "Ángela", "Bárbara", 
    "Carolina", "Debora", "Emilia", "Fátima", "Gloria", "Herminia", "Ivana", 
    "Jennifer", "Kiara", "Lidia", "Magdalena", "Nicol", "Otilia", "Pilar", "Romina", 
    "Silvia", "Tania", "Valentina", "Xenia", "Yessica", "Zoé", "Amalia", "Bianca", 
    "Carmen", "Delia", "Eva", "Fabiana", "Gema", "Hermelinda", "Iris", "Jessica", 
    "Keila", "Lilian", "Marina", "Nadia", "Olivia", "Petra", "Rosa", "Sandra", 
    "Susana", "Ursula", "Victoria", "Xochitl", "Yesenia", "Zara", "Amanda", "Sheyla", "Loraine", "Marian", "Lauren", "Penelope", "DALIANYS", "SHEILA","AIRELYS","MARTHA","Osmany",
]

nombres_mujeres = [nombre.upper() for nombre in nombres_mujeres]
nombres_hombres = [nombre.upper() for nombre in nombres_hombres]



for item in data:
    if item["Sexo"] == "":
        for nombre in nombres_hombres:
            if nombre in item["Apellidos y Nombres"]:
                item["Sexo"] = "M"
                continue
        for nombre in nombres_mujeres:
            if nombre in item["Apellidos y Nombres"]:
                item["Sexo"] = "F"
                continue

with open('data1.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)




#########################################
# Crear DataFrame
df = pd.DataFrame(data)

# Contar la cantidad de inscripciones por vía de ingreso y curso
df_grouped = df.groupby(["Curso", "Vía Ingreso"]).size().reset_index(name="Inscripciones")

# Crear gráfica de áreas apiladas con Plotly
fig = px.area(df_grouped, x="Curso", y="Inscripciones", color="Vía Ingreso", line_group="Vía Ingreso", markers=True)

# Configurar diseño de la gráfica
fig.update_layout(
    title="Inscripciones por Vía de Ingreso y Curso",
    xaxis_title="Curso",
    yaxis_title="Número de Inscripciones",
    legend_title="Vía de Ingreso",
    width=1000,  # Cambiar el ancho
    height=400   # Cambiar la altura (opcional)
)

# Mostrar gráfica en Streamlit
st.title("Visualización de Ingresos por Vía de Ingreso")
st.plotly_chart(fig, use_container_width=False)  # Elimina use_container_width para usar el ancho personalizado

