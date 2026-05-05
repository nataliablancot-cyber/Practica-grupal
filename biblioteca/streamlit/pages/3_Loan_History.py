<<<<<<< HEAD
import streamlit as st
import pandas as pd

st.title("Historial de préstamos")

usuario = st.text_input("Introduce el usuario")

# Datos provisionales hasta conectar con el backend
datos = [
    {
        "Usuario": "ana",
        "Libro": "1984",
        "Fecha préstamo": "2024-04-01",
        "Fecha devolución": "2024-04-10",
        "Estado": "Devuelto"
    },
    {
        "Usuario": "ana",
        "Libro": "El Principito",
        "Fecha préstamo": "2024-04-15",
        "Fecha devolución": "",
        "Estado": "Activo"
    },
    {
        "Usuario": "juan",
        "Libro": "Don Quijote",
        "Fecha préstamo": "2024-03-20",
        "Fecha devolución": "2024-04-01",
        "Estado": "Devuelto"
    }
]

if usuario:
    st.warning("El historial de préstamos todavía no está conectado al backend.")
    st.write("Para que esta pantalla funcione definitivamente, el backend debe guardar préstamos por usuario.")
    st.write("Usuario buscado:", usuario)

    df = pd.DataFrame(datos)

    # Filtramos por usuario, sin distinguir mayúsculas/minúsculas
    df_filtrado = df[df["Usuario"].str.lower() == usuario.lower()]

    if df_filtrado.empty:
        st.info("Este usuario no tiene historial de préstamos.")
    else:
        st.table(df_filtrado)

else:
    st.info("Introduce un usuario para consultar su historial.")
=======
import os

import pandas as pd
import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Historial de préstamos")

usuario_id = st.text_input("ID de usuario")

if usuario_id:
    try:
        response = requests.get(
            f"{API_URL}/prestamos/historial",
            params={"usuario_id": int(usuario_id)},
            timeout=10,
        )

        if response.status_code == 200:
            prestamos = response.json().get("prestamos", [])
            if prestamos:
                st.table(pd.DataFrame(prestamos))
            else:
                st.info("Este usuario no tiene préstamos registrados.")
        else:
            st.error(f"No se ha podido consultar el historial. Código: {response.status_code}")
            st.text(response.text)

    except ValueError:
        st.error("Introduce un ID de usuario numérico.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión con el servidor: {e}")
else:
    st.info("Introduce un usuario para consultar su historial.")
>>>>>>> 2f8987a (cambi en el error de presatmos)
