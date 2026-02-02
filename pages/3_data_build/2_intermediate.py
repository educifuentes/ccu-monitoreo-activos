import streamlit as st

from models.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.intermediate._int_censos_censo_1 import int_censos_censo_1
from models.intermediate._int_base_norm_censo_1 import int_base_norm_censo_1
from models.marts.fct_censos import fct_censos

# from models.marts.dim_locales import marts_dim_locales
from models.staging._stg_base_norm_locales import stg_base_norm_locales

# load
locales_df = stg_base_norm_locales()
int_base_norm_censo_1_df = int_base_norm_censo_1()


st.header("Intermediate")

st.subheader("Locales")
st.write(locales_df.shape)
st.markdown("Source: Base normalizada")

st.dataframe(locales_df)   

# ----

st.subheader("Censo 1")
st.badge("int_base_norm_censo1")
st.write(int_base_norm_censo_1_df.shape)

st.markdown("Notes")
st.markdown("- Dropped 20 rows with null id")
st.markdown("- Dropped 687 rows with null agencia")

st.dataframe(int_base_norm_censo_1_df) 