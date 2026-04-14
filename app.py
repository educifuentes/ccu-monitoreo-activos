import streamlit as st
import os

from helpers.utilities.app_version import get_app_version
from helpers.utilities.auth import check_password
from helpers.utilities.check_environment import get_environment

if not check_password():
    st.stop()
# Page configuration

# Section - Reports
general_page = st.Page("pages/1_reports/1_general.py", title="General", icon=":material/dashboard:")
clientes_page = st.Page("pages/1_reports/1_clientes.py", title="Clientes", icon=":material/sports_bar:")
reportes_page = st.Page("pages/1_reports/3_reportes.py", title="Reportes", icon=":material/article:")

# Section - Tools
explore_page = st.Page("pages/2_tools/data_explorer.py", title="Explorar Tablas", icon=":material/search:")
validations_page = st.Page("pages/2_tools/validations.py", title="Validaciones", icon=":material/check_circle:")
documentation_page = st.Page("pages/2_tools/documentation.py", title="Documentación", icon=":material/book:")

# Navigation Logic
nav_dict = {
    "Vistas": [
        general_page, 
        clientes_page,
        reportes_page
    ],
    "Herramientas": [explore_page, validations_page, documentation_page],
}


# Only expose the development environment tabs locally
env = get_environment()
is_local = env == "local"
if is_local:
    nav_dict["Desarrollo"] = [
        st.Page("pages/3_dev/1_staging.py", title="Staging", icon=":material/dashboard:"),
        st.Page("pages/3_dev/2_intermediate.py", title="Intermediate", icon=":material/inventory_2:"),
        st.Page("pages/3_dev/3_marts.py", title="Marts", icon=":material/account_tree:"),
        st.Page("pages/3_dev/4_exposures.py", title="Exposures", icon=":material/visibility:"),
        st.Page("pages/3_dev/5_catalog.py", title="Catalog", icon=":material/book:"),
        st.Page("pages/3_dev/model_details.py", icon=":material/info:")
    ]

# current page
pg = st.navigation(nav_dict)

with st.sidebar:
    if st.button("Actualizar Datos 🔄", width='stretch', help="Forzar la recarga de datos desde Google Sheets"):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    # Logo and version
    app_version = get_app_version()
    # st.image("utilities/assets/logo_gotomarket_solid.png", width='stretch')
    st.caption(f"Version: {app_version}")

pg.run()


