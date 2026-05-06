import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Registrar usuario")

with st.form("user_form"):
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")
    activo = st.checkbox("Usuario activo", value=True)
    submitted = st.form_submit_button("Crear usuario")

    if submitted:
        if not nombre.strip() or not email.strip():
            st.error("Nombre y email son obligatorios.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/usuarios/",
                    json={"nombre": nombre.strip(), "email": email.strip(), "activo": activo},
                    timeout=10,
                )
                if response.status_code == 200:
                    st.success("Usuario creado correctamente.")
                    st.json(response.json())
                else:
                    st.error(f"No se ha podido crear el usuario. Código: {response.status_code}")
                    st.text(response.text)
            except requests.exceptions.RequestException as e:
                st.error(f"Error de conexión con el servidor: {e}")
