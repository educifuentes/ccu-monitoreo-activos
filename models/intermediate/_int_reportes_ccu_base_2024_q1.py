import pandas as pd
import numpy as np

def int_reportes_ccu_base_2024_q1():
    # Define file path
    file_path = "seeds/base_normalizada/base_normalizada - locales.csv"

    # Load CSV
    df = pd.read_csv(file_path)

    # rename columns

    rename_dict = {
        "id": "local_id",
        'N° Coolers': 'coolers',
        'N° Columnas (Schoperas)': 'schoperas',
        'N° Salidas Schop CCU': 'salidas',
    }
    
   
    df.rename(columns=rename_dict, inplace=True)

    select_cols = [
        # row identifiers
        "local_id",
        "periodo",
        "fecha",
        # activos
        "schoperas",
        "salidas",
        "coolers"
    ]

    # data types
    df["local_id"] = df["local_id"].astype(str)
    df["coolers"] = df["coolers"].astype('Int64')
    df["schoperas"] = df["schoperas"].astype('Int64')
    df["salidas"] = df["salidas"].astype('Int64')

    # new columns
    # note: should be done in stg model, but int model. exepction. refactir later
    df["periodo"] = "2024-Q1"
    df["fecha"] = pd.to_datetime("2024-01-01").date() # todo: get real date

    
    return df[select_cols]