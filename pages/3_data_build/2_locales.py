import streamlit as st
# from models.marts.dim_locales import marts_dim_locales
from models.staging._stg_base_norm_locales import stg_base_norm_locales

# load
locales_df = stg_base_norm_locales()


st.header("Locales")
st.write(locales_df.shape)
st.dataframe(locales_df)   