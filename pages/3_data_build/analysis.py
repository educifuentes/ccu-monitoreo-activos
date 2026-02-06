import streamlit as st

from models.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.intermediate._int_censos_censo_1 import int_censos_censo_1
from models.intermediate._int_base_norm_censo_1 import int_base_norm_censo_1
from models.marts.fct_censos import fct_censos

# from models.marts.dim_locales import marts_dim_locales
from models.staging._stg_base_norm_locales import stg_base_norm_locales
from models.intermediate._int_dim_locales import int_reportes_ccu_locales, compare_locales_df
from utilities.ui_components import render_model_ui

# load

# locales
locales_df = stg_base_norm_locales()
int_reportes_ccu_locales_df = int_reportes_ccu_locales()
comparison_locales_df = compare_locales_df()

# censos
int_base_norm_censo_1_df = int_base_norm_censo_1()
int_censos_censo_2_df = int_censos_censo_2()


st.header("Intermediate")

st.subheader("Locales Comparison")
st.markdown("Inner join between `stg_base_norm_locales` and `int_reportes_ccu_locales` on `local_id`.")
render_model_ui(comparison_locales_df)

