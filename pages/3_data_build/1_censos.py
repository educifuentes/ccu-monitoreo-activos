import streamlit as st
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer
from models.staging._stg_censos_censo_2 import stg_censos_censo_2
from models.staging._stg_censos_censo_1 import stg_censos_censo_1
from models.staging._stg_base_norm_censo_1 import stg_base_norm_censo_1
from models.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.intermediate._int_censos_censo_1 import int_censos_censo_1
from models.intermediate._int_base_norm_censo_1 import int_base_norm_censo_1
from models.marts.fct_censos import fct_censos


st.header("Censos")

# Load the data
stg_censos_2 = stg_censos_censo_2()
int_censos_2 = int_censos_censo_2()
stg_censos_1 = stg_censos_censo_1()
int_censos_1 = int_censos_censo_1()
stg_base_norm_censo_1 = stg_base_norm_censo_1()
int_base_norm_censo_1 = int_base_norm_censo_1()

# fct_censos = fct_censos()


# st.markdown("### Final")
# st.write(fct_censos.shape)
# st.dataframe(fct_censos)


# CENSO 2
st.subheader("Censo 2 - 2025")

# ---

st.markdown("### Intermediate")
st.write(int_censos_2.shape)
st.dataframe(int_censos_2)

st.markdown("### Staging")

st.write(stg_censos_2.shape)
st.dataframe(stg_censos_2)


# CENSO 1 
st.subheader("Censo 1 - 2024")

st.markdown("### Staging")
st.badge("censos_censo_1")

st.write(stg_censos_1.shape)
st.dataframe(stg_censos_1)


# ---

st.markdown("### Intermediate")
st.write(int_censos_1.shape)
st.dataframe(int_censos_1)

# --------------------
st.divider()


st.header("Base Normalizada - Censo 1")

st.markdown("### Intermediate")
st.badge("int_base_norm_censo1")
st.write(int_base_norm_censo_1.shape)
st.dataframe(int_base_norm_censo_1) 



st.badge("base_norm_censo1")

st.write(stg_base_norm_censo_1.shape)
st.dataframe(stg_base_norm_censo_1)


