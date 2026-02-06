import streamlit as st

from models.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.intermediate._int_censos_censo_1 import int_censos_censo_1
from models.intermediate._int_base_norm_censo_1 import int_base_norm_censo_1

from models.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1
from models.intermediate._int_reportes_ccu_base_2024_q1 import int_reportes_ccu_base_2024_q1


from models.marts.fct_censos import fct_censos

# from models.marts.dim_locales import marts_dim_locales
from models.staging._stg_base_norm_locales import stg_base_norm_locales
from models.intermediate._int_dim_locales import int_reportes_ccu_locales
from models.analysis.compare_bases_ccu import compare_locales_df
from utilities.ui_components import render_model_ui

# load

# locales
locales_df = stg_base_norm_locales()

int_reportes_ccu_base_2024_q1_df = int_reportes_ccu_base_2024_q1()
int_reportes_ccu_base_2026_q1_df = int_reportes_ccu_base_2026_q1()

int_reportes_ccu_locales_df = int_reportes_ccu_locales()
comparison_locales_df = compare_locales_df()

# censos
int_base_norm_censo_1_df = int_base_norm_censo_1()
int_censos_censo_2_df = int_censos_censo_2()


st.header("Intermediate")

st.subheader("Reportes CCU")

st.badge("reportes_ccu_base_2026_q1")
render_model_ui(int_reportes_ccu_base_2026_q1_df, source_name="reportes_ccu", table_name="base_2026_q1")

st.divider()

st.subheader("Reportes CCU")
st.badge("reportes_ccu_base_2024_q1")

render_model_ui(int_reportes_ccu_base_2024_q1_df, source_name="reportes_ccu", table_name="base_2024_q1")



st.subheader("Locales")
st.markdown("Source: Base normalizada")
st.badge("stg_base_norm_locales")
render_model_ui(locales_df)   

st.badge("int_reportes_ccu_locales")
render_model_ui(int_reportes_ccu_locales_df)



# ----

st.subheader("Censo 1")
st.badge("int_base_norm_censo1")

st.markdown("Notes")
st.markdown("- Dropped 20 rows with null id")
st.markdown("- Dropped 687 rows with null agencia")

render_model_ui(int_base_norm_censo_1_df) 

st.divider()

st.subheader("Censo 2")
st.badge("int_censos_censo2")

st.markdown("Notes")
st.markdown("- asumo CANTIDAD DE SALIDAS como salidas_ccu")

render_model_ui(int_censos_censo_2_df)


st.subheader("Censo 2 + Locales")
# left join int_censos_censo_2_df with locales_df
int_censos_censo_2_df = int_censos_censo_2_df.merge(locales_df, on="local_id", how="left", indicator=True)

missing_locales = int_censos_censo_2_df[int_censos_censo_2_df["_merge"] == "left_only"]
if not missing_locales.empty:
    st.warning(f"Hay {len(missing_locales)} filas en Censo 2 que no tienen match en Locales")

render_model_ui(int_censos_censo_2_df)