import sqlite3
import streamlit as st

# Función para conectarse a la base de datos SQLite
def connect_db():
    return sqlite3.connect('biobank_system.db')

# Función para crear tablas si no existen
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Crear tabla de muestras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS muestras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
    ''')

    # Crear tabla de solicitantes (opcional)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Función para agregar una nueva muestra
def alta_muestra(nombre, descripcion):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO muestras (nombre, descripcion)
        VALUES (?, ?)
    ''', (nombre, descripcion))
    conn.commit()
    conn.close()

# Función para listar todas las muestras
def listar_muestras():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM muestras')
    muestras = cursor.fetchall()
    conn.close()
    return muestras

# Función principal para la aplicación en Streamlit
def main():
    st.title("Sistema de Biobanco")
    create_tables()  # Crear tablas si no existen

    # Menú de opciones
    menu = ["Administración de Muestras", "Gestión de Solicitantes", "Gestión de Asignaciones", "Gestión de Administradores", "Mantenimiento del Sistema", "Informes y Estadísticas", "Salir"]
    choice = st.sidebar.selectbox("Menú Principal", menu)

    if choice == "Administración de Muestras":
        st.subheader("Administración de Muestras")
        submenu = ["Alta Muestra", "Listar Muestras"]
        sub_choice = st.selectbox("Opciones", submenu)

        if sub_choice == "Alta Muestra":
            st.subheader("Alta de una nueva muestra")
            nombre = st.text_input("Nombre de la muestra")
            descripcion = st.text_area("Descripción de la muestra")
            if st.button("Agregar Muestra"):
                alta_muestra(nombre, descripcion)
                st.success(f"Muestra '{nombre}' agregada exitosamente.")
        
        elif sub_choice == "Listar Muestras":
            st.subheader("Lista de Muestras Registradas")
            muestras = listar_muestras()
            if muestras:
                for muestra in muestras:
                    st.write(f"ID: {muestra[0]}, Nombre: {muestra[1]}, Descripción: {muestra[2]}")
            else:
                st.write("No hay muestras registradas.")

    elif choice == "Gestión de Solicitantes":
        st.subheader("Gestión de Solicitantes")
        st.write("Opciones para solicitantes aún no implementadas.")

    elif choice == "Gestión de Asignaciones":
        st.subheader("Gestión de Asignaciones")
        st.write("Opciones para asignaciones aún no implementadas.")

    elif choice == "Gestión de Administradores":
        st.subheader("Gestión de Administradores")
        st.write("Opciones para administradores aún no implementadas.")

    elif choice == "Mantenimiento del Sistema":
        st.subheader("Mantenimiento del Sistema")
        st.write("Opciones de mantenimiento aún no implementadas.")

    elif choice == "Informes y Estadísticas":
        st.subheader("Informes y Estadísticas")
        st.write("Opciones de informes y estadísticas aún no implementadas.")

    elif choice == "Salir":
        st.write("Gracias por usar el Sistema de Biobanco.")

# Ejecutar la aplicación principal
if __name__ == "__main__":
    main()

