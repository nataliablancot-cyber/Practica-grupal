import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Catálogo de Libros", page_icon="📖")

st.markdown("# Catálogo de Libros")
st.write("Listado de libros disponibles en la biblioteca.")

API_URL = "http://localhost:8000"

try:
    response = requests.get(f"{API_URL}/libros/", timeout=10)
    response.raise_for_status()

    data = response.json()
    libros = data.get("libros", [])

    if libros:
        df = pd.DataFrame(libros)

        busqueda = st.text_input("Buscar por título o autor")
        solo_disponibles = st.checkbox("Mostrar solo disponibles")

        if busqueda:
            df = df[
                df["titulo"].astype(str).str.contains(busqueda, case=False, na=False) |
                df["autor"].astype(str).str.contains(busqueda, case=False, na=False)
            ]

        if solo_disponibles:
            df = df[df["disponible"] == True]

        st.write(f"Total de libros mostrados: {len(df)}")

        if df.empty:
            st.info("No se han encontrado libros con ese criterio.")
        else:
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay libros disponibles.")

except requests.exceptions.RequestException as e:
    st.error(f"Error de conexión con el servidor: {e}")
    st.info("Asegúrate de que FastAPI está funcionando en http://localhost:8001")
except Exception as e:
    st.error(f"Se ha producido un error: {e}")