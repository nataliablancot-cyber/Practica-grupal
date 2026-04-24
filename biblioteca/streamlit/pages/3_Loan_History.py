import streamlit as st
import pandas as pd

st.title("Historial de préstamos")

usuario = st.text_input("Introduce el usuario")


    if usuario:
        st.warning("El historial de préstamos todavía no está conectado al backend.")
        st.write("Para que esta pantalla funcione, el backend debe guardar préstamos por usuario.")
        st.write("Usuario buscado:", usuario)
    else:
        st.info("Introduce un usuario para consultar su historial.")
    df = pd.DataFrame(datos)

    st.table(df)