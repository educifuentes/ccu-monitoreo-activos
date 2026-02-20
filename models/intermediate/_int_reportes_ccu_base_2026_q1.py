import pandas as pd
import numpy as np

from utilities.transformations.yes_no_to_boolean import yes_no_to_boolean
from utilities.transformations.date_parsing import parse_spanish_month_year



from models.raw.bases_ccu._stg_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1

def int_reportes_ccu_base_2026_q1():
    # Use staging model instead of loading CSV directly
    df = stg_reportes_ccu_base_2026_q1()

    # rename
    rename_dict = {
        "Folio": "folio",
    }
    df.rename(columns=rename_dict, inplace=True)

    # new columns (Intermediate specific logic)
    df["periodo"] = "2026-Q1"
    df["fecha"] = pd.to_datetime("2026-01-01").date() 

    # dtypes 
    df = yes_no_to_boolean(df, "es_local_imagen?")

    return df

def int_reportes_ccu_base_2026_q1_locales():
    locales_columns = ['local_id', 'razon_social', 'rut', 'direccion', 'region', 'ciudad', 'comuna', 'nombre_fantasia']

    base_2026_q1_df = int_reportes_ccu_base_2026_q1()

    df = base_2026_q1_df[locales_columns]

    return df

def int_reportes_ccu_base_2026_q1_activos():
    df = int_reportes_ccu_base_2026_q1()

    selected_columns = ['local_id', 'periodo', 'fecha', 'schoperas', 'salidas', 'coolers', 'fecha_suscripcion_comodato', 'fecha_termino_contrato', 'activos_entregados']

     # dtypes tp dates
    df = parse_spanish_month_year(df, "fecha_suscripcion_comodato")
    df = parse_spanish_month_year(df, "fecha_termino_contrato")

    df = df[selected_columns]
    return df

def int_reportes_ccu_base_2026_q1_contratos_imagen():

    df = int_reportes_ccu_base_2026_q1()

    # drop rows where es_local_imagen is False
    df = df[df["es_local_imagen?"] == True]

    selected_columns = ['local_id', 'folio']

    df = df[selected_columns]

    return df