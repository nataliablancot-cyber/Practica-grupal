import streamlit as st
import time

st.set_page_config(page_title='Gestor de Bibliotecas', layout='wide')

# Placeholder for logo or header
st.write("# Gestor de Bibliotecas ")

st.markdown(
    """Qué puedes hacer
- Ver el catálogo de libros
- Buscar libros por título o autor
- Registrar préstamos
- Consultar el historial
- Ver una vista de calendario de préstamos

Usa el menú de la izquierda para entrar en cada apartado.
"""
)

st.sidebar.success("Selecciona una opción arriba.")
