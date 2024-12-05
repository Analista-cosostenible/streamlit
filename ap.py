import streamlit as st
import pandas as pd

# Ruta del archivo CSV
DATA_PATH = "RepositorioCosostenible.csv"  # Cambia el nombre por el de tu archivo CSV

@st.cache
def cargar_datos():
    # Cargar datos al iniciar
    return pd.read_csv(DATA_PATH)

# Cargar datos
datos = cargar_datos()

# Mostrar datos en la app
st.title("Visualización de Datos")
st.write("Datos cargados automáticamente:")
st.dataframe(datos)

# Título de la aplicación
st.title("Visualizador de Documentos desde un Archivo CSV o Excel")

# Subir archivo CSV o Excel
uploaded_file = st.file_uploader("Sube un archivo CSV o Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Cargar los datos del archivo
    df = load_data(uploaded_file)

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
            document_types = ['Imágenes', 'Videos', 'PDFs', 'Textos/CSV', 'Excel', 'Todos']
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
                                # Enlace de Google Drive para PDFs públicos
                                file_id = url.split('/d/')[1].split('/')[0]
                                google_drive_url = f"https://drive.google.com/file/d/{file_id}/preview"
                                st.markdown(f'<iframe src="{google_drive_url}" width="700" height="500"></iframe>', unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Error al intentar visualizar el archivo desde la URL {url}: {str(e)}")
