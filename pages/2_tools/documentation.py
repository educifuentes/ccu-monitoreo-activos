import streamlit as st
import os
from utilities.render_docs import render_model_docs

st.title("📚 Documentación")


# Ruta al archivo YAML
fct_censos_path = os.path.abspath("models/marts/_fct_censos.yml")

# Renderizar documentación
render_model_docs(fct_censos_path)