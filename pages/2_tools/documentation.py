import streamlit as st
import os
from helpers.ui_components.render_docs import render_model_docs
from helpers.ui_components.ui_icons import ICONS

st.set_page_config(page_title="Documentación", layout="wide")

st.title(f"{ICONS['documentation']} Documentación")



st.subheader("Marcas y Grupos Corporativos")
with open("documentation/_marcas_table.md", "r", encoding="utf-8") as f:
    st.markdown(f.read())


st.divider()

st.subheader("Tablas")

# Create tabs for organization
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    f"{ICONS['clientes']} Clientes",
    f"{ICONS['censos']} Censos",
    f"{ICONS['bases_ccu']} Bases CCU",
    f"{ICONS['contratos']} Contratos",
    f"{ICONS['metrics']} Metricas"
])



with tab1:
    # dim_clientes_path = os.path.abspath("models/raw/marts/_dim_clientes.yml")
    # render_model_docs(dim_clientes_path)

with tab2:
    # fct_censos_path = os.path.abspath("models/raw/marts/_fct_censos.yml")
    # render_model_docs(fct_censos_path)

with tab3:
    fct_bases_ccu_path = os.path.abspath("models/marts/fct_bases_ccu.yml")
    render_model_docs(fct_bases_ccu_path)

with tab4:
    # fct_contratos_path = os.path.abspath("models/raw/marts/_fct_contratos.yml")
    # render_model_docs(fct_contratos_path)

with tab5:
    # st.header("Métricas")
    # fct_metricas_path = os.path.abspath("models/raw/marts/metrics/_metrics_docs.yml")
    # render_model_docs(fct_metricas_path, kind="metrics")
