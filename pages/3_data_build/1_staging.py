import streamlit as st

from models.staging._stg_censos_censo_2 import stg_censos_censo_2
from models.staging._stg_censos_censo_1 import stg_censos_censo_1
from models.staging._stg_base_norm_censo_1 import stg_base_norm_censo_1
from models.staging._stg_base_norm_locales import stg_base_norm_locales
from models.staging._stg_base_norm_original import stg_base_norm_original

from utilities.ui_components import render_model_ui

st.header("Staging")

# Load the data
stg_censos_2 = stg_censos_censo_2()
stg_censos_1 = stg_censos_censo_1()
stg_base_norm_censo_1 = stg_base_norm_censo_1()
stg_base_norm_locales = stg_base_norm_locales()
stg_base_norm_original = stg_base_norm_original()

# ---

st.subheader("Base Normalizada")

st.badge("base_norm_original")
render_model_ui(stg_base_norm_original, source_name="base normalizada", table_name="base_normalizada_original")

# st.subheader("Locales")
# st.badge("base_norm_locales")
# st.write(stg_base_norm_locales.shape)
# st.dataframe(stg_base_norm_locales)

# st.divider()

# st.subheader("Censo 1")
# st.badge("base_norm_censo1")

# st.write(stg_base_norm_censo_1.shape)
# st.dataframe(stg_base_norm_censo_1)

# st.divider()


# st.subheader("Censo 2 - 2025")
# st.write(stg_censos_2.shape)
# st.badge("censos_censo2")

# st.dataframe(stg_censos_2)



# # ---


# st.subheader("Descartadas")

# # CENSO 1 
# st.subheader("Censo 1 - 2024")
# st.badge("censos_censo1")
# st.warning ("No usar")


# st.write(stg_censos_1.shape)
# st.dataframe(stg_censos_1)





