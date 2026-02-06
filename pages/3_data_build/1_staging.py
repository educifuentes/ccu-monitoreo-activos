import streamlit as st

from models.staging._stg_censos_censo_2 import stg_censos_censo_2
from models.staging._stg_censos_censo_1 import stg_censos_censo_1
from models.staging._stg_base_norm_censo_1 import stg_base_norm_censo_1
from models.staging._stg_base_norm_locales import stg_base_norm_locales
from models.staging._stg_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1
from models.staging._stg_reportes_ccu_base_2024_q1 import stg_reportes_ccu_base_2024_q1

from utilities.yaml_loader import get_table_config




st.header("Staging")

# Load the data
stg_censos_2 = stg_censos_censo_2()
stg_censos_1 = stg_censos_censo_1()
stg_base_norm_censo_1 = stg_base_norm_censo_1()
stg_base_norm_locales = stg_base_norm_locales()
stg_reportes_ccu_base_2026_q1_df = stg_reportes_ccu_base_2026_q1()
stg_reportes_ccu_base_2024_q1_df = stg_reportes_ccu_base_2024_q1()

# docu
reportes_ccu_base_sol_source_config = get_table_config(source_name="reportes_ccu", table_name="base_2026_q1")

st.subheader("Reportes CCU")
st.badge("reportes_ccu_base_2026_q1")

st.markdown(reportes_ccu_base_sol_source_config.get("description"))
st.write(stg_reportes_ccu_base_2026_q1_df.shape)
st.code(stg_reportes_ccu_base_2026_q1_df.columns.tolist())

st.markdown("""
Duda
- es numero de salidas lo mismo Cantidad total de salidas de schop?
""")


st.dataframe(stg_reportes_ccu_base_2026_q1_df)

st.divider()

st.subheader("Reportes CCU")
st.badge("reportes_ccu_base_2024_q1")

st.write(stg_reportes_ccu_base_2024_q1_df.shape)
st.code(stg_reportes_ccu_base_2024_q1_df.columns.tolist())

st.dataframe(stg_reportes_ccu_base_2024_q1_df)



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





