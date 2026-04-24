import streamlit as st
import pandas as pd

st.title("Historial de préstamos")

usuario = st.text_input("Introduce el usuario")

if usuario != "":
    st.write("Historial del usuario:", usuario)

    # Datos de prueba
    datos = [
        {
            "titulo": "1984",
            "fecha_prestamo": "2026-04-01",
            "fecha_devolucion": "",
            "estado": "Activo"
        },
        {
            "titulo": "Don Quijote de la Mancha",
            "fecha_prestamo": "2026-03-10",
            "fecha_devolucion": "2026-03-25",
            "estado": "Devuelto"
        }
    ]

    df = pd.DataFrame(datos)

    st.table(df)