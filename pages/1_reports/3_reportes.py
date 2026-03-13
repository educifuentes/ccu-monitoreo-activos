import streamlit as st


from models.raw.marts.reports._report_censo_2026 import report_censo_2026


st.set_page_config(page_title="Reportes", layout="wide")


st.header("Reporte Censo 2026")
st.markdown("Última actualización: 2026-03-13")

col1, col2 = st.columns(2)

df = report_censo_2026()

with col1:
    st.code(df.shape)

with col2:
    st.dataframe(df["AGENCIA"].value_counts().reset_index(), hide_index=True)

st.dataframe(df, hide_index=True, height=700)