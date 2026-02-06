import pandas as pd
import numpy as np

def stg_base_norm_locales():
    # Define file path
    file_path = "seeds/base_normalizada/base_normalizada - locales.csv"
    
    # Load CSV
    df = pd.read_csv(file_path)

    # rename
    rename_dict = {
        "id": "local_id",
        "RAZON SOCIAL": "razon_social",
        "RUT": "rut",
        "DIRECCIÓN": "direccion",
        "REGIÓN": "region",
        "CIUDAD":  "ciudad", 
        "Nombre de Fantasía ": "nombre_fantasia",
        "Nombre de Fantasía 2": "nombre_fantasia_2"
    }

    df.rename(columns=rename_dict, inplace=True)

    selected_columns = [
        "local_id",
        "razon_social",
        "rut",
        "direccion",
        "region",
        "ciudad",
        "nombre_fantasia" ]

    # data types
    df["local_id"] = df["local_id"].astype("str")

    # print data types
    print("\n--- Data Types ---")
    print(df.dtypes)

    print("\n--- List of Column Names ---")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")

    df = df[selected_columns]
        
    return df