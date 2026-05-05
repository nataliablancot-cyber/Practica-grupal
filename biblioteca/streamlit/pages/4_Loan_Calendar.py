import streamlit as st
import pandas as pd

st.warning("El calendario todavía no está conectado al historial real de préstamos.")

st.write("Para que esta pantalla se actualice, el backend debe devolver los préstamos con:")
st.write("- usuario")
st.write("- libro")
st.write("- fecha de préstamo")
st.write("- fecha de devolución")
st.write("- estado")

st.info("Esta pantalla queda preparada para integrarse cuando exista el endpoint de historial.")