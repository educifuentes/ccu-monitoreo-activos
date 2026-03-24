import pandas as pd
import numpy as np

from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.utilities.load_source import load_source


def stg_censos__censo_2024_2():

    # Define file path

    file_path = get_source_metadata(
        "censo_2024_2",
        "models/sources/_src_censos__censo_2024_2.yml"
    )
    
    # Load CSV
    df = load_source(file_path)
    
    # 1. Basic Cleaning
    # Drop columns that are completely empty
    df = df.dropna(axis=1, how='all')
    
    # Filter out columns that start with 'Unnamed' (usually empty headers)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # 2. Proper Column Parsing
    
    # Convert Dates
    date_cols = ['Date', 'VStart', 'VEnd']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    # Handle specific survey columns that should be numeric
    # Based on the head output, we identify some numeric columns. 
    # This list might need refinement as we explore the data more.
    count_cols = [
        'NÚMERO TOTAL DE MÁQUINAS SCHOPERAS EN EL LOCAL',
        'NÚMERO DE MÁQUINAS SCHOPERAS DE CCU\n(ASUMIR QUE LA SCHOPERA ES CCU SI LA MAYORÍA DE LAS MARCAS SON CCU - REVISAR TARJETERO DE APOYO)',
        'NÚMERO DE MÁQUINAS SCHOPERAS DE ABINBEV\n(ASUMIR QUE LA SCHOPERA ES ABINBEV SI LA MAYORÍA DE LAS MARCAS SON ABINBEV - REVISAR TARJETERO DE APOYO)',
        'NÚMERO DE SALIDAS TOTALES DE SCHOPERAS \nMÁQUINA SCHOPERA 1:',
        'NÚMERO DE SALIDAS TOTALES DE SCHOPERAS\nMÁQUINA SCHOPERA 2:'
    ]
    for col in count_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    return df
