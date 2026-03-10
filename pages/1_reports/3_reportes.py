import streamlit as st


from models.raw.marts.reports._report_censo_2026 import report_censo_2026


st.set_page_config(page_title="Reportes", layout="wide")


st.header("Reporte Censo 2026")

st.dataframe(report_censo_2026())