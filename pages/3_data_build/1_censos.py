import streamlit as st
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer
from models.staging._stg_censos_censo_2 import stg_censos_censo_2
from models.intermediate._int_censos_censo_2 import int_censos_censo_2


st.header("Censos")

st.subheader("Censo 2 - 2025")
# Load the data
stg_censos_2 = stg_censos_censo_2()
int_censos_2 = int_censos_censo_2()

st.dataframe(int_censos_2)

