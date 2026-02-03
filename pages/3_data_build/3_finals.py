import streamlit as st

from models.marts.fct_censos import fct_censos
from models.marts.dim_locales import dim_locales

fct_censos_df = fct_censos()
dim_locales_df = dim_locales()

st.header("Finales")

st.markdown("### FCT Censos")
st.write(fct_censos_df.shape)
st.code(fct_censos_df.columns.tolist())

st.dataframe(fct_censos_df)


st.markdown("### DIM Locales")
st.write(dim_locales_df.shape)
st.code(dim_locales_df.columns.tolist())

st.dataframe(dim_locales_df)

