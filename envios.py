import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Procesador de Archivo .xlsx - Costo de Envío por Fecha")

# Subida del archivo .xlsx
uploaded_file = st.file_uploader("Sube un archivo .xlsx", type="xlsx")

if uploaded_file is not None:
    try:
        # Leer el archivo Excel
        df = pd.read_excel(uploaded_file)
        st.write("Archivo cargado correctamente.")
    except Exception as e:
        st.error(f"No se pudo leer el archivo: {e}")
        st.stop()

    # Mostrar las columnas detectadas
    st.write("Columnas detectadas:", list(df.columns))

    # Validar columnas necesarias
    required_columns = ["fecha_venta", "id_venta", "costo_envio"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Faltan las siguientes columnas requeridas: {missing_columns}")
        st.stop()

    try:
        # Eliminar filas duplicadas basadas en 'id_venta'
        unique_sales = df.drop_duplicates(subset="id_venta")

        # Convertir 'costo_envio' a numérico
        unique_sales["costo_envio"] = pd.to_numeric(unique_sales["costo_envio"], errors="coerce")

        # Convertir 'fecha_venta' a formato datetime
        unique_sales["fecha_venta"] = pd.to_datetime(unique_sales["fecha_venta"], errors="coerce", format='%Y-%m-%d')

        # Agrupar por fecha_venta y sumar costos de envío
        grouped_data = unique_sales.groupby(unique_sales["fecha_venta"].dt.date)["costo_envio"].sum().reset_index()
        grouped_data.columns = ["Fecha de Venta", "Costo Total de Envío"]

        # Mostrar los datos procesados
        st.subheader("Datos Filtrados y Agrupados por Fecha:")
        st.dataframe(grouped_data)

        # Descargar los datos agrupados
        csv = grouped_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV Agrupado",
            data=csv,
            file_name='costo_envio_por_fecha.csv',
            mime='text/csv'
        )
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("Por favor, sube un archivo .xlsx para comenzar.")
