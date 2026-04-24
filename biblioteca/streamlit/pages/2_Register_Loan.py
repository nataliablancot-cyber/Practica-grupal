import streamlit as st
import requests

st.set_page_config(page_title="Préstamo de Libros")

st.markdown("# Gestionar Préstamo")
st.write("Formulario para realizar un préstamo.")

API_URL = "http://localhost:8001"

with st.form("loan_form"):
    libro_id = st.number_input("ID del Libro", min_value=1, step=1)
    usuario_id = st.text_input("ID de Usuario")
    submitted = st.form_submit_button("Realizar Préstamo")

    if submitted:
        if not usuario_id.strip():
            st.error("Introduce el ID de usuario.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/prestamos/",
                    params={"libro_id": int(libro_id)},
                    timeout=10
                )

                if response.status_code == 200:
                    st.success("Préstamo registrado correctamente.")
                    st.json(response.json())
                else:
                    st.error(f"No se ha podido registrar el préstamo. Código: {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"Error de conexión con el servidor: {e}")

    st.markdown("---")
    st.caption("Esta pantalla está conectada con la API disponible actualmente.")