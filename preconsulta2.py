import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from github import Github

# Configura el token personal y el repositorio
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"  # Reemplaza con tu token personal de GitHub
REPO_NAME = "usuario/repositorio"  # Reemplaza con tu usuario y nombre del repositorio
BRANCH = "main"  # Nombre de la rama donde se subirá el archivo

# Función para subir el archivo a GitHub
def subir_a_github(file_content, file_name):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    try:
        # Subir el archivo al repositorio
        repo.create_file(
            path=f"data/{file_name}",
            message=f"Subiendo archivo de datos: {file_name}",
            content=file_content.getvalue(),
            branch=BRANCH
        )
        st.success(f"Archivo subido correctamente a GitHub como 'data/{file_name}'")
    except Exception as e:
        st.error(f"Error al subir el archivo a GitHub: {e}")

# Función para guardar los datos en un archivo Excel
def guardar_en_excel(data):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Consulta')
    output.seek(0)
    return output

# Configuración del formulario en Streamlit
st.title("Consulta de Primera Vez - Instituto Nacional de Cardiología Ignacio Chávez")

# Campos del formulario
nombre_completo = st.text_input("Nombre Completo")
genero = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])
fecha_nacimiento = st.date_input("Fecha de Nacimiento", value=None, min_value=pd.Timestamp('1900-01-01'))

# Lista de países con "Mexico" sin acento y como opción predeterminada
paises_america = ["Argentina", "Bolivia", "Brasil", "Canada", "Chile", "Colombia", "Costa Rica", "Cuba", "Ecuador", "El Salvador", "Estados Unidos", "Guatemala", "Honduras", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Republica Dominicana", "Uruguay", "Venezuela"]
paises_europa = ["Alemania", "España", "Francia", "Italia", "Portugal", "Reino Unido"]

pais_nacimiento = st.selectbox("País de Nacimiento", paises_america + paises_europa, index=paises_america.index("Mexico"))
whatsapp = st.text_input("Número de WhatsApp", placeholder="+521234567890")
correo = st.text_input("Correo Electrónico")
correo_confirmacion = st.text_input("Confirma tu Correo Electrónico")

# Validación y guardado de información
if st.button("Enviar"):
    if not nombre_completo or not whatsapp or not correo or not correo_confirmacion:
        st.error("Por favor, completa todos los campos antes de enviar.")
    elif correo != correo_confirmacion:
        st.error("Los correos electrónicos no coinciden.")
    else:
        resultados = {
            "Nombre Completo": nombre_completo,
            "Género": genero,
            "Fecha de Nacimiento": fecha_nacimiento.strftime('%d/%m/%Y'),
            "País de Nacimiento": pais_nacimiento,
            "WhatsApp": whatsapp,
            "Correo Electrónico": correo
        }

        # Convertir a un DataFrame
        df = pd.DataFrame([resultados])
        
        # Guardar los datos en un archivo Excel en memoria
        excel_data = guardar_en_excel(df)
        
        # Crear un nombre único para el archivo basado en la fecha y hora
        file_name = f"consulta_primera_vez_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
        
        # Subir el archivo a GitHub
        subir_a_github(excel_data, file_name)

