import pandas as pd
import numpy as np

from models.raw.staging.bases_ccu._stg_reportes_ccu_base_2024_q1 import stg_reportes_ccu_base_2024_q1

def int_reportes_ccu_base_2024_q1():
    # Load CSV
    df = stg_reportes_ccu_base_2024_q1()

    # rename columns

    rename_dict = {
        "id": "local_id",
        'N° Coolers': 'coolers',
        'N° Columnas (Schoperas)': 'schoperas',
        'N° Salidas Schop CCU': 'salidas',
    }
   
    df.rename(columns=rename_dict, inplace=True)

    # data types
    df["local_id"] = df["local_id"].astype(str)
    df["coolers"] = df["coolers"].astype('Int64')
    df["schoperas"] = df["schoperas"].astype('Int64')
    df["salidas"] = df["salidas"].astype('Int64')

    # clean
    df["local_id"] = df["local_id"].replace("nan", None)

    # new columns
    # note: should be done in stg model, but int model. exepction. refactir later
    df["periodo"] = "2024-Q1"
    df["fecha"] = pd.to_datetime("2024-01-01").date() 

    # nuevas columns de fecha - pedido el feb 19, 2026
    df["fecha_suscripcion_comodato"] = pd.to_datetime("2024-01-01").date() 
    df["fecha_termino_contrato"] = pd.NA
    df["activos_entregados"] = pd.NA

    selected_columns = [
        # row identifiers
        "local_id",
        "periodo",
        "fecha",
        # activos
        "schoperas",
        "salidas",
        "coolers",
        # fechas
        "fecha_suscripcion_comodato",
        "fecha_termino_contrato",
        "activos_entregados"
    ]

    
    return df[selected_columns]