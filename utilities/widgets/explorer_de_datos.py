import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def explorer_de_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Versión en español de dataframe_explorer.
    Permite filtrar un dataframe con una interfaz en español.
    """
    df = df.copy()
    
    # Intentar convertir objetos a fechas si es posible
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass
        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    contenedor = st.container()
    with contenedor:
        columnas_a_filtrar = st.multiselect(
            "Filtrar dataframe por:", 
            df.columns,
            placeholder="Selecciona columnas..."
        )
        
        for col in columnas_a_filtrar:
            # Columnas categóricas o con pocos valores únicos
            if is_categorical_dtype(df[col]) or df[col].nunique() < 10:
                seleccion = st.multiselect(
                    f"Valores para {col}",
                    df[col].unique(),
                    default=list(df[col].unique()),
                )
                df = df[df[col].isin(seleccion)]
                
            # Columnas numéricas
            elif is_numeric_dtype(df[col]):
                _min, _max = float(df[col].min()), float(df[col].max())
                paso = (_max - _min) / 100
                if paso == 0:
                    paso = 1.0
                valores = st.slider(
                    f"Rango de {col}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=paso,
                )
                df = df[df[col].between(*valores)]
                
            # Columnas de fecha
            elif is_datetime64_any_dtype(df[col]):
                rango_fechas = st.date_input(
                    f"Rango de fechas para {col}",
                    value=(df[col].min().to_pydatetime(), df[col].max().to_pydatetime()),
                )
                if len(rango_fechas) == 2:
                    start, end = pd.to_datetime(rango_fechas[0]), pd.to_datetime(rango_fechas[1])
                    df = df[(df[col] >= start) & (df[col] <= end)]
            
            # Texto / Otros
            else:
                busqueda = st.text_input(f"Buscar patrón en {col}")
                if busqueda:
                    df = df[df[col].astype(str).str.contains(busqueda, case=False)]

    return df
