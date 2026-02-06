import streamlit as st

from models.staging._stg_censos_censo_2 import stg_censos_censo_2
from models.staging._stg_censos_censo_1 import stg_censos_censo_1
from models.staging._stg_base_norm_censo_1 import stg_base_norm_censo_1
from models.staging._stg_base_norm_locales import stg_base_norm_locales
from models.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1
from models.intermediate._int_reportes_ccu_base_2024_q1 import int_reportes_ccu_base_2024_q1
from utilities.ui_components import render_model_ui

st.header("Staging")

# Load the data
stg_censos_2 = stg_censos_censo_2()
stg_censos_1 = stg_censos_censo_1()
stg_base_norm_censo_1 = stg_base_norm_censo_1()
stg_base_norm_locales = stg_base_norm_locales()
int_reportes_ccu_base_2026_q1_df = int_reportes_ccu_base_2026_q1()
int_reportes_ccu_base_2024_q1_df = int_reportes_ccu_base_2024_q1()

# ---

st.subheader("Reportes CCU")

st.badge("reportes_ccu_base_2026_q1")
render_model_ui(int_reportes_ccu_base_2026_q1_df, source_name="reportes_ccu", table_name="base_2026_q1")

st.divider()

st.subheader("Reportes CCU")
st.badge("reportes_ccu_base_2024_q1")
render_model_ui(int_reportes_ccu_base_2024_q1_df, source_name="reportes_ccu", table_name="base_2024_q1")




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





