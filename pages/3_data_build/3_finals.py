import streamlit as st

from models.marts.fct_censos import fct_censos

fct_censos_df = fct_censos()

st.header("Finales")

st.markdown("### FCT Censos")
st.write(fct_censos_df.shape)
st.dataframe(fct_censos_df)
