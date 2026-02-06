import streamlit as st
from streamlit_gsheets import GSheetsConnection

from utilities.config import TTL_VALUE

@st.cache_data
def load_data_gsheets():
    """Return DataFrames for given worksheet names."""
    
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=TTL_VALUE)
    worksheets = ["locales", "censos", "bases_ccu", "contratos"]

    return tuple(conn.read(worksheet=w) for w in worksheets)

def locales():
    """Return the 'locales' worksheet."""
    return load_data_gsheets()[0]

def censos():
    """Return the 'censos' worksheet."""
    return load_data_gsheets()[1]

def bases_ccu():
    """Return the 'bases_ccu' worksheet."""
    return load_data_gsheets()[2]

def contratos():
    """Return the 'contratos' worksheet."""
    return load_data_gsheets()[3]