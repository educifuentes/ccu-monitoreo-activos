import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

from utilities.config import TTL_VALUE
from utilities.transformations.date_parsing import parse_spanish_month_year
from utilities.transformations.yes_no_to_boolean import yes_no_to_boolean
from utilities.transformations.add_row_number import add_row_number


@st.cache_data
def load_data_gsheets():
    """Return DataFrames for given worksheet names."""
    
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=TTL_VALUE)
    worksheets = ["locales", "censos", "bases_ccu", "contratos"]

    # add row number
    dataframes = []
    for w in worksheets:
        df = conn.read(worksheet=w)
        df = add_row_number(df)
        dataframes.append(df)

    return tuple(dataframes)

def locales():
    """Return the 'locales' worksheet."""

    df = load_data_gsheets()[0]

    # cast to proper data types
    df["local_id"] = df["local_id"].astype("str")

    
    return df

def censos():
    """Return the 'censos' worksheet."""

    df = load_data_gsheets()[1]

    # cast to proper data types
    df["local_id"] = df["local_id"].astype("str")
    df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True, errors="coerce").dt.date

    df["schoperas"] = df["schoperas"].astype("Int64")
    df["salidas"] = df["salidas"].astype("Int64")
    
    return df

def bases_ccu():
    """Return the 'bases_ccu' worksheet."""

    df = load_data_gsheets()[2]

    # cast to proper data types
    df["local_id"] = df["local_id"].astype("str")
    df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True, errors="coerce").dt.date
    
    df["coolers"] = df["coolers"].astype("Int64")
    df["schoperas"] = df["schoperas"].astype("Int64")
    df["salidas"] = df["salidas"].astype("Int64")
    
    return df

def contratos():
    """Return the 'contratos' worksheet."""

    df = load_data_gsheets()[3]

    # cast to proper data types
    df["local_id"] = df["local_id"].astype("str")

    if "es_local_imagen?" in df.columns:
        df = yes_no_to_boolean(df, "es_local_imagen?")
    
    if "fecha_inicio" in df.columns:
        df = parse_spanish_month_year(df, "fecha_inicio")
    
    if "fecha_termino" in df.columns:
        df = parse_spanish_month_year(df, "fecha_termino")
    
    if "activos_entregados" in df.columns:
        df["activos_entregados"] = df["activos_entregados"].astype("Int64")
    
    return df