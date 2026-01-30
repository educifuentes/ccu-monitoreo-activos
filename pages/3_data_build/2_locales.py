import streamlit as st
from models.marts.dim_locales import marts_dim_locales


st.header("Locales")

locales = marts_dim_locales()

st.dataframe(locales)   