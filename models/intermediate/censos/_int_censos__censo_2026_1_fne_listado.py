import pandas as pd
import numpy as np

from models.staging.censos._stg_censos__censo_2026_1_fne_listado import stg_censos__censo_2026_1_fne_listado


def int_censos__censo_2026_1_fne_listado():
    # Define file path
    df = stg_censos__censo_2026_1_fne_listado()

    rename_dict = {
        "ID CLIENTE": "cliente_id",
        "NOMBRE FANTASÍA": "nombre_fantasia",
        "RAZÓN SOCIAL": "razon_social",
        "RUT": "rut",
        "REGIÓN": "region",
        "COMUNA": "comuna",
        "DIRECCIÓN": "direccion"
    }

    df = df.rename(columns=rename_dict)

    select_cols = [
        "cliente_id",
        "nombre_fantasia",
        "razon_social",
        "rut",
        "region",
        "comuna",
        "direccion"
    ]

    # Data Types
    df["cliente_id"] = df["cliente_id"].astype("str")

    df = df[select_cols]

    
    return df
