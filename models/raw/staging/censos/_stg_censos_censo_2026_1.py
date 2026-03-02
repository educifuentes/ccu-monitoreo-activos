import pandas as pd
import numpy as np

from utilities.yaml_loader import load_yaml_config

def stg_censos_censo_2026_1():
    # Define file path
    source_config_path = "models/raw/sources/raw_data_censos/_src_censos__censo_3_2026.yml"
    
    # Extract path from config
    config = load_yaml_config(source_config_path)
    file_path = next((s.get("path") for s in config.get("sources", []) if s.get("name") == "censo_2026"), None)
    
    if not file_path:
        raise ValueError("Could not find path for table 'censo_2026' in yaml source.")
    
    # Load CSV using the second row as header
    df = pd.read_csv(file_path, header=1)

    # 1. Basic Cleaning
    # Drop columns that are completely empty
    df = df.dropna(axis=1, how='all')
    
    # Filter out columns that start with 'Unnamed' (usually empty headers)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # 2. Proper Column Parsing
    
    # Convert Dates
    date_cols = ['Inicio', 'Fin']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    # Handle specific survey columns that should be numeric
    count_cols = [
        'NÚMERO TOTAL DE MÁQUINAS SCHOPERAS EN EL LOCAL',
        'NÚMERO DE MÁQUINAS SCHOPERAS DE CCU(ASUMIR QUE LA SCHOPERA ES CCU SI LA MAYORÍA DE LAS MARCAS SON CCU - REVISAR TARJETERO DE APOYO)',
        'SCHOPERA CCU 1 - NÚMERO DE SALIDAS',
        'SCHOPERA CCU 2 - NÚMERO DE SALIDAS',
        'SCHOPERA CCU 3 - NÚMERO DE SALIDAS',
        'SCHOPERA CCU 4 - NÚMERO DE SALIDAS',
        'SCHOPERA CCU 5 - NÚMERO DE SALIDAS',
        'SCHOPERA CCU 6 - NÚMERO DE SALIDAS',
        'CUANTAS SHOPERAS PARA DISPONIBILIZAR NUEVAS INSTALO CCU ?',
        'CUANTAS SALIDAS DEJO LIBRE CCU EN TOTAL? s ',
        'NÚMERO DE MÁQUINAS SCHOPERAS QUE NO SEAN DE CCU'
    ]
    for col in count_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    return df
