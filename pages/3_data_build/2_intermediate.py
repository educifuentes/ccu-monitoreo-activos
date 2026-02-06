import streamlit as st

from models.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.intermediate._int_censos_censo_1 import int_censos_censo_1
from models.intermediate._int_base_norm_censo_1 import int_base_norm_censo_1
from models.marts.fct_censos import fct_censos

# from models.marts.dim_locales import marts_dim_locales
from models.staging._stg_base_norm_locales import stg_base_norm_locales
from models.intermediate._int_dim_locales import int_reportes_ccu_locales, compare_locales_df
from utilities.ui_components import render_model_ui

# load

# locales
locales_df = stg_base_norm_locales()
int_reportes_ccu_locales_df = int_reportes_ccu_locales()
comparison_locales_df = compare_locales_df()

# censos
int_base_norm_censo_1_df = int_base_norm_censo_1()
int_censos_censo_2_df = int_censos_censo_2()


st.header("Intermediate")

st.subheader("Locales")
st.markdown("Source: Base normalizada")
st.badge("stg_base_norm_locales")
render_model_ui(locales_df)   

st.badge("int_reportes_ccu_locales")
render_model_ui(int_reportes_ccu_locales_df)



# ----

# st.subheader("Censo 1")
# st.badge("int_base_norm_censo1")
# st.write(int_base_norm_censo_1_df.shape)
# st.code(int_base_norm_censo_1_df.dtypes)

# st.markdown("Notes")
# st.markdown("- Dropped 20 rows with null id")
# st.markdown("- Dropped 687 rows with null agencia")

# st.dataframe(int_base_norm_censo_1_df) 

# st.divider()

# st.subheader("Censo 2")
# st.badge("int_censos_censo2")

# st.markdown("Notes")
# st.markdown("- asumo CANTIDAD DE SALIDAS como salidas_ccu")

# st.write(int_censos_censo_2_df.shape)
# st.dataframe(int_censos_censo_2_df)
# st.code(int_censos_censo_2_df.dtypes)


# st.subheader("Censo 2 + Locales")
# # left join int_censos_censo_2_df with locales_df
# int_censos_censo_2_df = int_censos_censo_2_df.merge(locales_df, on="local_id", how="left", indicator=True)

# missing_locales = int_censos_censo_2_df[int_censos_censo_2_df["_merge"] == "left_only"]
# st.warning(f"Hay {len(missing_locales)} filas en Censo 2 que no tienen match en Locales")

# st.dataframe(int_censos_censo_2_df)