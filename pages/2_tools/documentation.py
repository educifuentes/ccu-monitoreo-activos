import streamlit as st
import os
from utilities.render_docs import render_model_docs

st.title("📚 Documentación")


# Create tabs for organization
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Locales",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU",
    ":material/contract: Contratos"
])

with tab1:
    st.header("Dim Locales")
    dim_locales_path = os.path.abspath("models/marts/_dim_locales.yml")
    render_model_docs(dim_locales_path)

with tab2:
    st.header("Fact Censos")
    fct_censos_path = os.path.abspath("models/marts/_fct_censos.yml")
    render_model_docs(fct_censos_path)

with tab3:
    st.header("Bases CCU / Comodatos")
    fct_comodatos_path = os.path.abspath("models/marts/_fct_comodatos.yml")
    render_model_docs(fct_comodatos_path)

with tab4:
    st.header("Fact Contratos")
    fct_contratos_path = os.path.abspath("models/marts/_fct_contratos.yml")
    render_model_docs(fct_contratos_path)
