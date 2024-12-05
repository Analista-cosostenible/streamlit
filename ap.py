import streamlit as st
import pandas as pd
import requests
from io import StringIO

# URL del archivo CSV en tu repositorio de GitHub (asegúrate de que sea un enlace RAW)
DEFAULT_CSV_URL = "https://raw.githubusercontent.com/Analista-cosostenible/streamlit/refs/heads/main/RepositorioCosostenible.csv"

# Función para cargar datos desde una URL
@st.cache_data
def load_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica que no haya errores en la solicitud
        return pd.read_csv(StringIO(response.text))
    except Exception as e:
        st.error(f"Error al cargar los datos desde la URL: {e}")
        return pd.DataFrame()

# Función para cargar datos desde un archivo subido por el usuario
@st.cache_data
def load_data_from_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    else:
        st.error("El archivo debe ser CSV o Excel")
        return pd.DataFrame()

# Título de la aplicación
st.title("Visualizador de Documentos desde una Base de Datos")

# Cargar datos automáticamente desde la URL del repositorio si no se sube un archivo
uploaded_file = st.file_uploader("Sube un archivo CSV o Excel", type=["csv", "xlsx"])
if uploaded_file is not None:
    df = load_data_from_file(uploaded_file)
else:
    st.info("Cargando datos predeterminados desde el repositorio de GitHub...")
    df = load_data_from_url(DEFAULT_CSV_URL)

# Procesar los datos cargados
if not df.empty:
    # Validar que las columnas requeridas existen
    required_columns = ["Distribuidor", "Ceco", "Referencia", "Marca", "URL"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"La hoja no contiene las siguientes columnas requeridas: {', '.join(missing_columns)}")
    else:
        # Filtros dinámicos
        st.write("### Filtros:")
        selected_filters = {}
        for column in required_columns:
            if column != "URL":  # No filtrar por URL
                unique_values = df[column].dropna().unique()
                selected_values = st.multiselect(f"Selecciona valores para '{column}'", unique_values)

                if selected_values:
                    selected_filters[column] = selected_values
                    df = df[df[column].isin(selected_values)]

        # Filtro para seleccionar tipo de documento
        st.write("### Filtrar por Tipo de Documento:")
        document_types = ['Todos', 'Videos', 'PDFs', 'Textos/CSV', 'Excel', 'Imágenes']
        selected_doc_type = st.selectbox("Selecciona el tipo de documento que deseas visualizar", document_types)

        # Resultados filtrados
        st.write("### Resultados Filtrados:")
        st.dataframe(df)

        # Mostrar detalles de los documentos (URLs)
        if "URL" in df.columns:
            st.write("### Visualización de Documentos")
            for index, row in df.iterrows():
                url = row["URL"]
                referencia = row.get("Referencia", "Sin referencia")
                descripcion = row.get("Descripción", "Sin descripción")
                precio_tipo = row.get("Tipo de Precio", "Sin tipo de precio")
                precio = row.get("Precio", "Sin precio")

                st.write(f"**Documento para la fila {index + 1}:**")
                st.write(f"Referencia: {referencia}")
                st.write(f"Descripción: {descripcion}")
                st.write(f"Tipo de Precio: {precio_tipo}")
                st.write(f"Precio: {precio}")

                # Condicionar la visualización de documentos según el tipo seleccionado
                try:
                    if selected_doc_type == 'Imágenes' and url.endswith(('.jpg', '.jpeg', '.png')):
                        st.image(url, caption=f"Vista de la imagen {index + 1}", use_column_width=True)

                    elif selected_doc_type == 'Videos' and url.endswith(('.mp4', '.webm', '.ogg')):
                        st.video(url)

                    elif selected_doc_type == 'PDFs' and "drive.google.com" in url:
                        # Enlace de Google Drive para PDFs públicos
                        file_id = url.split('/d/')[1].split('/')[0]
                        google_drive_url = f"https://drive.google.com/file/d/{file_id}/preview"
                        st.markdown(f'<iframe src="{google_drive_url}" width="700" height="500"></iframe>', unsafe_allow_html=True)

                    elif selected_doc_type == 'Todos':
                        if url.endswith(('.jpg', '.jpeg', '.png')):
                            st.image(url, caption=f"Vista de la imagen {index + 1}", use_column_width=True)
                        elif url.endswith(('.mp4', '.webm', '.ogg')):
                            st.video(url)
                        elif "drive.google.com" in url:
                            file_id = url.split('/d/')[1].split('/')[0]
                            google_drive_url = f"https://drive.google.com/file/d/{file_id}/preview"
                            st.markdown(f'<iframe src="{google_drive_url}" width="700" height="500"></iframe>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error al intentar visualizar el archivo desde la URL {url}: {str(e)}")