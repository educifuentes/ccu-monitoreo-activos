import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
from models.staging.censos._stg_censos_censo_2 import stg_censos_censo_2
from models.staging.censos._stg_censos_censo_1 import stg_censos_censo_1

from models.staging.base_normalizada._stg_base_norm_censo_1 import stg_base_norm_censo_1

st.header("Data Profiling")


# Load the data
stg_censos_2 = stg_censos_censo_2()
stg_censos_1 = stg_censos_censo_1()
stg_base_norm_censo_1 = stg_base_norm_censo_1()


st.subheader("Base Normalizada - Censo 1")
st.write(stg_base_norm_censo_1.shape)


# Use the StreamlitRenderer to embed the explorer

renderer = StreamlitRenderer(stg_base_norm_censo_1)
renderer.explorer()