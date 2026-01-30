import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
from models.staging._stg_censos_censo_2 import stg_censos_censo_2


st.header("Data Profiling")

st.subheader("Censo 2 - 2025")

# Load the data
stg_censos_2 = stg_censos_censo_2()

# Use the StreamlitRenderer to embed the explorer
renderer = StreamlitRenderer(stg_censos_2)
renderer.explorer()