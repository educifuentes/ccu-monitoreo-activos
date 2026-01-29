import streamlit as st
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer
from models.staging._stg_censos_censo_2 import stg_censos_censo_2

st.title("Validations")
st.write("Work in progress...")

st.markdown("""
todo:
- Regiones con valores de ciudad
- texto donde deben ir numeros
- validar que los censos tengan la misma cantidad de locales que los locales
- validar que los contratos tengan la misma cantidad de locales que los locales
- validar que las nominas tengan la misma cantidad de locales que los locales
- validar que los activos tengan la misma cantidad de locales que los locales
""")


censos_2 = stg_censos_censo_2

# Use the StreamlitRenderer to embed the explorer
renderer = StreamlitRenderer(censos_2)
renderer.explorer()