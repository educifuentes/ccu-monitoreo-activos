import streamlit as st
import os

from helpers.ui_components.render_docs import render_model_docs, render_metrics_docs
from helpers.ui_components.ui_icons import ICONS

st.set_page_config(page_title="Documentación", layout="wide")

st.title(f"{ICONS['documentation']} Documentación")

st.subheader("Tablas")

# Create tabs for organization
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    f"{ICONS['metrics']} Metricas",
    f"{ICONS['metrics']} Marcas",
    f"{ICONS['clientes']} Clientes",
    f"{ICONS['censos']} Censos",
    f"{ICONS['bases_ccu']} Bases CCU",

])

with tab1:
    st.header("Métricas")
    fct_metricas_path = os.path.abspath("models/metrics/_metrics.yml")
    render_metrics_docs(fct_metricas_path)

with tab2:
    st.header("Marcas y sus Grupos")
    with open("documentation/_marcas_table.md", "r", encoding="utf-8") as f:
        st.markdown(f.read())

with tab3:
    st.header("Clientes")

    dim_clientes_path = os.path.abspath("models/marts/dim_clientes.yml")
    render_model_docs(dim_clientes_path)

with tab4:  
    st.header("Censos")
    fct_censos_path = os.path.abspath("models/marts/fct_censos.yml")
    render_model_docs(fct_censos_path)

with tab5:
    st.header("Bases CCU")
    fct_bases_ccu_path = os.path.abspath("models/marts/fct_bases_ccu.yml")
    render_model_docs(fct_bases_ccu_path)



