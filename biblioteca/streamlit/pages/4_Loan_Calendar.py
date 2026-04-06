import streamlit as st
import pandas as pd

st.title("Calendario de préstamos")

st.write("Vista de los préstamos registrados.")

# Datos de ejemplo
datos = [
    {"titulo": "1984", "fecha": "2026-04-01", "estado": "Activo"},
    {"titulo": "Don Quijote", "fecha": "2026-03-10", "estado": "Devuelto"}
]

df = pd.DataFrame(datos)

st.write("Préstamos:")
st.table(df)

st.write("Estados:")
st.write("- Activo → préstamo en curso")
st.write("- Devuelto → préstamo finalizado")