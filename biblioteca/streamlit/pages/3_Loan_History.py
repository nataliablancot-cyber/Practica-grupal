import os

import pandas as pd
import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Historial de préstamos")


@st.cache_data(ttl=30)
def obtener_usuarios():
    response = requests.get(f"{API_URL}/usuarios/", timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=30)
def obtener_historial(usuario_id):
    response = requests.get(
        f"{API_URL}/prestamos/historial",
        params={"usuario_id": usuario_id},
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("prestamos", [])


try:
    usuarios = obtener_usuarios()
except requests.exceptions.RequestException as e:
    st.error(f"Error de conexión con el servidor: {e}")
    st.stop()

if not usuarios:
    st.info("No hay usuarios registrados.")
else:
    usuario_opciones = {
        f'{usuario["id"]} - {usuario["nombre"]} ({usuario["email"]})': usuario["id"]
        for usuario in usuarios
    }
    usuario_label = st.selectbox("Usuario", options=list(usuario_opciones.keys()))

    try:
        prestamos = obtener_historial(usuario_opciones[usuario_label])
        if prestamos:
            st.dataframe(pd.DataFrame(prestamos), use_container_width=True)
        else:
            st.info("Este usuario no tiene préstamos registrados.")
    except requests.exceptions.HTTPError as e:
        st.error(f"No se ha podido consultar el historial: {e.response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión con el servidor: {e}")
