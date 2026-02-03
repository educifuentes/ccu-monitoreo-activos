import streamlit as st
import os
from utilities.render_docs import render_model_docs

st.title("📚 Documentación")


# Ruta al archivo YAML
fct_censos_path = os.path.abspath("models/marts/_fct_censos.yml")
dim_locales_path = os.path.abspath("models/marts/_dim_locales.yml")
fct_comodatos_path = os.path.abspath("models/marts/_fct_comodatos.yml")
fct_contratos_path = os.path.abspath("models/marts/_fct_contratos.yml")

# Renderizar documentación
render_model_docs(fct_censos_path)

render_model_docs(dim_locales_path)

render_model_docs(fct_comodatos_path)

render_model_docs(fct_contratos_path)
