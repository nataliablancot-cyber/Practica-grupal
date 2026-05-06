import os

import pandas as pd
import requests
import streamlit as st
from streamlit_calendar import calendar


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Calendario de préstamos")


@st.cache_data(ttl=30)
def obtener_prestamos():
    response = requests.get(f"{API_URL}/prestamos/", timeout=10)
    response.raise_for_status()
    return response.json()


try:
    prestamos = obtener_prestamos()
except requests.exceptions.RequestException as e:
    st.error(f"Error de conexión con el servidor: {e}")
    st.stop()

if not prestamos:
    st.info("No hay préstamos registrados.")
else:
    eventos = []
    for prestamo in prestamos:
        eventos.append(
            {
                "title": f'{prestamo["usuario"]}: {prestamo["titulo"]}',
                "start": prestamo["fecha_prestamo"],
                "end": prestamo["fecha_devolucion"] or prestamo["fecha_prestamo"],
            }
        )

    calendar(
        events=eventos,
        options={
            "initialView": "dayGridMonth",
            "locale": "es",
            "height": 650,
        },
    )
    st.dataframe(pd.DataFrame(prestamos), use_container_width=True)
