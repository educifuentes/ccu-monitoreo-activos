import streamlit as st
import os
from utilities.render_docs import render_model_docs

st.title("📚 Documentación")

st.markdown("""
Esta página muestra la documentación técnica de los modelos de datos procesados. 
La información se extrae directamente de los archivos de definición del proyecto.
""")

# Ruta al archivo YAML
fct_censos_path = os.path.abspath("models/marts/_fct_censos.yml")

# Renderizar documentación
render_model_docs(fct_censos_path)