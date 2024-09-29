import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# Función para guardar los datos en un archivo Excel
def guardar_en_excel(data):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Consulta')
    output.seek(0)
    return output

# Mostrar el logo y títulos
st.image("nuevo-escudo-INC.jpg", width=200)  # Ajusta el tamaño del logo con el parámetro 'width'
st.title("Consulta de Primera Vez")
st.subheader("Instituto Nacional de Cardiología Ignacio Chávez")

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
    if not nombre_completo or not whatsapp or not correo or not correo_confirmacion or not fecha_nacimiento:
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

        # Guardar el archivo en el estado de sesión para descargarlo más tarde
        st.session_state['excel_data'] = excel_data
        
        st.success("¡Registro completado! Los datos han sido guardados.")

# Botón para descargar el archivo guardado
if 'excel_data' in st.session_state:
    st.download_button(
        label="Descargar Excel",
        data=st.session_state['excel_data'],
        file_name=f"consulta_primera_vez_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx",
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

