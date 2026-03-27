import streamlit as st
from streamlit_gsheets import GSheetsConnection
from helpers.utilities.data_connection_config import TTL_VALUE

@st.cache_data
def load_gsheets_worksheet(worksheet_name: str):
    """Load a specific worksheet from Google Sheets."""
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=TTL_VALUE)
    df = conn.read(worksheet=worksheet_name)
    return df
