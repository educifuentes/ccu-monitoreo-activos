import pandas as pd
import numpy as np
from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.utilities.load_source import load_source

def stg_bases_manuales__clientes():
    # Define file path
    file_path = get_source_metadata("base_normalizada_clientes", "models/sources/_src_bases_manuales.yml")
    
    # Load CSV
    df = load_source(file_path)

    # rename
    rename_dict = {
        "id": "cliente_id",
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
        "cliente_id",
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
    df["cliente_id"] = df["cliente_id"].astype("str")
    df["coolers"] = df["coolers"].astype("Int64")
    df["schoperas"] = df["schoperas"].astype("Int64")
    df["salidas"] = df["salidas"].astype("Int64")
 

    df = df[selected_columns]
        
    return df