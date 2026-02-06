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
        "Nombre de Fantasía 2": "nombre_fantasia_2",
        'N° Coolers': 'coolers',
        'N° Columnas (Schoperas)': 'schoperas',
        'N° Salidas Schop CCU': 'salidas'
    }

    df.rename(columns=rename_dict, inplace=True)

    selected_columns = [
        "local_id",
        "razon_social",
        "rut",
        "direccion",
        "region",
        "ciudad",
        "nombre_fantasia",
        "nombre_fantasia_2",
        # activos ccu 2024
        "coolers",
        "schoperas",
        "salidas" ]

    # data types
    df["local_id"] = df["local_id"].astype("str")
    df["coolers"] = df["coolers"].astype("Int64")
    df["schoperas"] = df["schoperas"].astype("Int64")
    df["salidas"] = df["salidas"].astype("Int64")
 

    df = df[selected_columns]
        
    return df