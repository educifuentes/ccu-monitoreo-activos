import pandas as pd
import numpy as np

from models.raw.staging.censos._stg_censos_fne_listado_2026_1 import stg_censos_fne_listado_2026_1


def int_censos_fne_listado_2026_1():
    # Define file path
    df = stg_censos_fne_listado_2026_1()

    rename_dict = {
        "ID CLIENTE": "local_id",
        "NOMBRE FANTASÍA": "nombre_fantasia",
        "RAZÓN SOCIAL": "razon_social",
        "RUT": "rut",
        "REGIÓN": "region",
        "COMUNA": "comuna",
        "DIRECCIÓN": "direccion"
    }

    df = df.rename(columns=rename_dict)

    select_cols = [
        "local_id",
        "nombre_fantasia",
        "razon_social",
        "rut",
        "region",
        "comuna",
        "direccion"
    ]

    # Data Types
    df["local_id"] = df["local_id"].astype("str")

    df = df[select_cols]

    
    return df
