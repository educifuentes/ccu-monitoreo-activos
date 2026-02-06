import streamlit as st

from models.analysis.compare_bases_ccu import compare_locales_df, compare_activos_df

from models.intermediate._int_base_norm_locales import int_base_norm_locales
from models.staging._stg_base_norm_original import stg_base_norm_original

from utilities.ui_components import render_model_ui


# base 2024 vs 2026

# dfs
comparison_locales_df = compare_locales_df()
comparison_activos_df = compare_activos_df()

st.subheader("Base ccu 2024 vs 2026")
st.markdown("Inner join between `stg_base_norm_locales` and `int_reportes_ccu_locales` on `local_id`.")
render_model_ui(comparison_locales_df)

st.subheader("Base ccu 2024 vs 2026")
st.markdown("Inner join between `stg_base_norm_locales` and `int_reportes_ccu_locales` on `local_id`.")
render_model_ui(comparison_activos_df)


# ---

# Aanalsiis base normalizasda
stg_base_norm_original_df = stg_base_norm_original()

st.subheader("Base Normalizada")

st.badge("base_norm_original")

# Number of rows with None in Censo 1 column
null_count = stg_base_norm_original_df['Censo 1'].isnull().sum()
st.write(f"Filas con Censo 1 nulo: {null_count}")

# print df with censo 1 column null
st.dataframe(stg_base_norm_original_df[stg_base_norm_original_df['Censo 1'].isnull()])
