import streamlit as st

from models.staging._stg_base_norm_locales import stg_base_norm_locales
from models.intermediate._int_dim_locales import int_reportes_ccu_locales, compare_locales_df
from models.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1
from models.intermediate._int_reportes_ccu_base_2024_q1 import int_reportes_ccu_base_2024_q1

from models.staging._stg_base_norm_original import stg_base_norm_original

from utilities.ui_components import render_model_ui

# load df
stg_base_norm_original_df = stg_base_norm_original()

# locales
locales_df = stg_base_norm_locales()
int_reportes_ccu_locales_df = int_reportes_ccu_locales()
comparison_locales_df = compare_locales_df()

st.subheader("Locales Comparison")
st.markdown("Inner join between `stg_base_norm_locales` and `int_reportes_ccu_locales` on `local_id`.")
render_model_ui(comparison_locales_df)


st.subheader("Base Normalizada")

st.badge("base_norm_original")

# Number of rows with None in Censo 1 column
null_count = stg_base_norm_original_df['Censo 1'].isnull().sum()
st.write(f"Filas con Censo 1 nulo: {null_count}")

# print df with censo 1 column null
st.dataframe(stg_base_norm_original_df[stg_base_norm_original_df['Censo 1'].isnull()])
