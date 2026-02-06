import streamlit as st

from models.marts.fct_censos import fct_censos
from models.marts.dim_locales import dim_locales
from models.marts.dashboard.bi_censo_locales import bi_censo_locales
from models.marts._fct_bases_ccu import fct_bases_ccu

from utilities.ui_components import render_model_ui

fct_censos_df = fct_censos()
dim_locales_df = dim_locales()
bi_censo_locales_df = bi_censo_locales()
fct_bases_ccu_df = fct_bases_ccu()

st.header("Finales")

# st.markdown("### BI Censo Locales")
# st.markdown(" calcula columna clasificacion")
# render_model_ui(bi_censo_locales_df)

# st.divider()

# st.markdown("### FCT Censos")
# render_model_ui(fct_censos_df)

st.markdown("### FCT Bases CCU")
render_model_ui(fct_bases_ccu_df)

# Locales en ambos periodos
count_ambos = fct_bases_ccu_df[fct_bases_ccu_df["en_ambos_periodos"] == True]["local_id"].nunique()
st.markdown(f"Locales en ambos periodos: **{count_ambos}**")


st.markdown("### DIM Locales")
render_model_ui(dim_locales_df)




