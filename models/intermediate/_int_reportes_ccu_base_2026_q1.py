import pandas as pd
import numpy as np



from models.staging.bases_ccu._stg_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1

def int_reportes_ccu_base_2026_q1():
    # Use staging model instead of loading CSV directly
    df = stg_reportes_ccu_base_2026_q1()

    # new columns (Intermediate specific logic)
    df["periodo"] = "2026-Q1"
    df["fecha"] = pd.to_datetime("2026-01-01").date() 

    return df

def int_reportes_ccu_base_2026_q1_locales():
    locales_columns = ['local_id', 'razon_social', 'rut', 'direccion', 'region', 'ciudad', 'comuna', 'nombre_fantasia']

    base_2026_q1_df = int_reportes_ccu_base_2026_q1()

    df = base_2026_q1_df[locales_columns]

    return df

def int_reportes_ccu_base_2026_q1_activos():
    activos_columns = ['local_id', 'schoperas', 'salidas', 'coolers']

    base_2026_q1_df = int_reportes_ccu_base_2026_q1()



    df = base_2026_q1_df[activos_columns]
    return df
