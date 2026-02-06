import streamlit as st

from models.staging._stg_censos_censo_2 import stg_censos_censo_2
from models.staging._stg_censos_censo_1 import stg_censos_censo_1
from models.staging._stg_base_norm_censo_1 import stg_base_norm_censo_1
from models.staging._stg_base_norm_locales import stg_base_norm_locales
from models.staging._stg_base_norm_original import stg_base_norm_original

from models.staging._stg_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1

from utilities.ui_components import render_model_ui

st.header("Staging")
st.markdown("Tablas staging 1:1 con soures - bases ccu, contraros, locales, censos")



# Load the data
stg_censos_2 = stg_censos_censo_2()
stg_censos_1 = stg_censos_censo_1()
stg_base_norm_censo_1 = stg_base_norm_censo_1()
stg_base_norm_locales = stg_base_norm_locales()
stg_base_norm_original = stg_base_norm_original()

# ---

# base CCU
stg_reportes_ccu_base_2026_q1_df = stg_reportes_ccu_base_2026_q1()

st.subheader("base ccu 2026 Q1")
render_model_ui(stg_reportes_ccu_base_2026_q1_df)


# st.subheader("Base Normalizada")

# st.badge("base_norm_original")
# render_model_ui(stg_base_norm_original, source_name="base normalizada", table_name="base_normalizada_original")

# st.subheader("Locales")
# st.badge("base_norm_locales")

# render_model_ui(stg_base_norm_locales, source_name="base normalizada", table_name="locales")


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





