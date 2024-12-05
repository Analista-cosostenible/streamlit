import streamlit as st
import pandas as pd

# Función para cargar datos iniciales
@st.cache_data
def cargar_datos_iniciales():
    try:
        return pd.read_csv('Repositorio Cosostenible.csv')
    except FileNotFoundError:
        st.error("El archivo 'Repositorio Cosostenible.csv' no se encontró.")
        return pd.DataFrame()

# Función para cargar datos del uploader
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        st.error("Formato de archivo no soportado.")
        return pd.DataFrame()

# Cargar datos iniciales
datos = cargar_datos_iniciales()

# Mostrar datos iniciales
st.title("Visualización de Datos Pre-Cargados")
if not datos.empty:
    st.dataframe(datos)

# Subida de archivos
st.title("Visualizador de Documentos desde un Archivo CSV o Excel")
uploaded_file = st.file_uploader("Sube un archivo CSV o Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    df = load_data(uploaded_file)

    if not df.empty:
        required_columns = ["Distribuidor", "Ceco", "Referencia", "Marca", "URL"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"La hoja no contiene las siguientes columnas requeridas: {', '.join(missing_columns)}")
            st.stop()

        # Aplicar filtros y visualizar datos
        st.dataframe(df)
