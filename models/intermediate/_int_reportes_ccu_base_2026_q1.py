import pandas as pd
import numpy as np

from utilities.yaml_loader import get_table_config

def int_reportes_ccu_base_2026_q1():
    # Fetch configuration from YAML
    config = get_table_config(source_name="reportes_ccu", table_name="base_2026_q1")
    file_path = config.get('filename')
    
    # Load CSV
    df = pd.read_csv(file_path)

    # rename
    rename_dict = {
        "id": "local_id",
        "numero de schoperas": "schoperas",
        "numero de salidas": "salidas",
        "numero de coolers": "coolers",
        "¿es local imagen?": "es_local_imagen?",
        "Fecha de suscripción del comodato": "fecha_suscripcion_comodato",
        "Fecha de término del contrato (de aplicar)": "fecha_termino_contrato",
        "Activos entregados": "activos_entregados",
        "Cantidad total de salidas de schop": "cantidad_total_salidas_schop",
    }

    df.rename(columns=rename_dict, inplace=True)

    # data type
    df["local_id"] = df["local_id"].astype(str)

    # new columns
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
