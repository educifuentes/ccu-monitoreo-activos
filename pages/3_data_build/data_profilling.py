import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
from models.raw.staging.censos._stg_censos_censo_2025_2 import stg_censos_censo_2025_2
from models.raw.staging.censos._stg_censos_censo_2024_2 import stg_censos_censo_2024_2

from models.raw.staging.base_normalizada._stg_base_norm_censo_2024_2 import stg_base_norm_censo_2024_2

st.header("Data Profiling")


# Load the data
stg_censos_2 = stg_censos_censo_2025_2()
stg_censos_1 = stg_censos_censo_2024_2()
stg_base_norm_censo_2024_2 = stg_base_norm_censo_2024_2()


st.subheader("Base Normalizada - Censo 1")
st.write(stg_base_norm_censo_2024_2.shape)


# Use the StreamlitRenderer to embed the explorer

renderer = StreamlitRenderer(stg_base_norm_censo_2024_2)
renderer.explorer()