import os

import requests
import streamlit as st

st.set_page_config(page_title="Préstamo de Libros")

st.markdown("# Gestionar Préstamo")
st.write("Formulario para realizar un préstamo.")

API_URL = os.getenv("API_URL", "http://localhost:8000")


@st.cache_data(ttl=30)
def obtener_libros():
    response = requests.get(f"{API_URL}/libros/", timeout=10)
    response.raise_for_status()
    return response.json().get("libros", [])


@st.cache_data(ttl=30)
def obtener_usuarios():
    response = requests.get(f"{API_URL}/usuarios/", timeout=10)
    response.raise_for_status()
    return response.json()


try:
    libros = obtener_libros()
    usuarios = obtener_usuarios()
except requests.exceptions.RequestException as e:
    st.error(f"Error de conexión con el servidor: {e}")
    st.stop()

with st.form("loan_form"):
    libros_disponibles = [libro for libro in libros if libro.get("disponible")]
    if not libros_disponibles:
        st.warning("No hay libros disponibles para prestar.")
    if not usuarios:
        st.warning("No hay usuarios registrados.")

    libro_opciones = {
        f'{libro["id"]} - {libro["titulo"]} ({libro["autor"]})': libro["id"]
        for libro in libros_disponibles
    }
    usuario_opciones = {
        f'{usuario["id"]} - {usuario["nombre"]} ({usuario["email"]})': usuario["id"]
        for usuario in usuarios
    }

    libro_label = None
    usuario_label = None
    if libro_opciones:
        libro_label = st.selectbox("Libro", options=list(libro_opciones.keys()))
    if usuario_opciones:
        usuario_label = st.selectbox("Usuario", options=list(usuario_opciones.keys()))
    submitted = st.form_submit_button("Realizar Préstamo")

    if submitted:
        if not libro_label or not usuario_label:
            st.error("Antes de prestar debe existir al menos un usuario y un libro disponible.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/prestamos/",
                    params={
                        "libro_id": libro_opciones[libro_label],
                        "usuario_id": usuario_opciones[usuario_label],
                    },
                    timeout=10,
                )

                if response.status_code == 200:
                    st.success("Préstamo registrado correctamente.")
                    st.json(response.json())
                    obtener_libros.clear()
                else:
                    st.error(f"No se ha podido registrar el préstamo. Código: {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"Error de conexión con el servidor: {e}")
