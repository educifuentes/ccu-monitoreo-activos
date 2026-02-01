import pandas as pd
import numpy as np

def stg_censos_censo_1():
    # Define file path
    file_path = "seeds/censos/corpa- Go to market - Censo Restaurantes PDV BBDD FINAL - BBDD.csv"
    
    # Load CSV
    df = pd.read_csv(file_path)
    
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

    # 3. Output Information
    # print("--- DataFrame Head ---")
    # print(df.iloc[:, :5].head())

    # print("\n--- List of Column Names ---")
    # for i, col in enumerate(df.columns):
    #     print(f"{i}: {col}")
        
    return df

if __name__ == "__main__":
    # To run this script directly for verification:
    # python models/staging/_stg_censos_censo_1.py
    print("Executing model locally for verification...")
    stg_censos_censo_1()