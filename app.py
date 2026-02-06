import streamlit as st

# Page configuration

# Section - Reports
general_page = st.Page("pages/1_reports/1_general.py", title="General", icon=":material/dashboard:")
detalles_page = st.Page("pages/1_reports/2_detalles.py", title="Detalles", icon=":material/inventory_2:")

# Section - Tools
explore_page = st.Page("pages/2_tools/data_explorer.py", title="Explorador de Datos", icon=":material/search:")
validations_page = st.Page("pages/2_tools/validations.py", title="Validaciones", icon=":material/check_circle:")
documentation_page = st.Page("pages/2_tools/documentation.py", title="Documentación", icon=":material/book:")

# dbt Models
staging_page = st.Page("pages/3_data_build/1_staging.py", title="Staging", icon=":material/dashboard:")
intermediate_page = st.Page("pages/3_data_build/2_intermediate.py", title="Intermediate", icon=":material/inventory_2:")
finals_page = st.Page("pages/3_data_build/3_finals.py", title="Finals", icon=":material/dashboard:")
data_profilling_page = st.Page("pages/3_data_build/data_profilling.py", title="Data Profiling", icon=":material/dashboard:")
requerimientos_page = st.Page("pages/3_data_build/requerimientos.py", title="Requerimientos", icon=":material/dashboard:")
analysis_page = st.Page("pages/3_data_build/analysis.py", title="Analysis", icon=":material/experiment:")
bi_tables_page = st.Page("pages/3_data_build/4_bi_tables.py", title="BI Tables", icon=":material/dashboard:")

# current page
pg = st.navigation({
    "Vistas": [general_page, detalles_page],
    "Herramientas": [explore_page, validations_page, documentation_page],
    "Dev - Modelos": [staging_page, intermediate_page, finals_page, data_profilling_page, requerimientos_page, analysis_page, bi_tables_page]
})

with st.sidebar:
    if st.button("Actualizar Datos 🔄", width='stretch', help="Forzar la recarga de datos desde Google Sheets"):
        st.cache_data.clear()
        st.rerun()

pg.run()

