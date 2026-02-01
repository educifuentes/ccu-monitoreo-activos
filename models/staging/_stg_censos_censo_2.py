import pandas as pd
import numpy as np

def stg_censos_censo_2():
    # Define file path
    file_path = "seeds/censos/CENSO CCU PK 27JULIO ID 260725-2 - Hoja1.csv"
    
    # Load CSV, skipping the first row of commas
    df = pd.read_csv(file_path, skiprows=1)
    
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
        'CUANTAS SALIDAS DEJO LIBRE CCU EN TOTAL? s '
    ]
    for col in count_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # 3. Output Information
    # print("--- DataFrame Head ---")
    # print(df.iloc[:, :5].head())

    # print("\n--- List of Column Names ---")
    # for i, col in enumerate(df.columns):
    #     print(f"{i}: {col}")
        
    return df

if __name__ == "__main__":
    # To run this script directly for verification:
    # python models/staging/_stg_censos_censo_2.py
    print("Executing model locally for verification...")
    stg_censos_censo_2()