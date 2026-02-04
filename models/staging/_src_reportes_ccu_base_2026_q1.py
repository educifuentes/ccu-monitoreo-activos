import pandas as pd
import numpy as np

from utilities.yaml_loader import get_table_config

def stg_reportes_ccu_base_2026_q1():
    # Fetch configuration from YAML
    config = get_table_config(source_name="reportes_ccu", table_name="base_solicitada")
    file_path = config.get('filename')
    
    # Load CSV
    df = pd.read_csv(file_path)

    # rename
    rename_dict = {
        "id": "local_id",
        "numero de schoperas": "schoperas",
        "numero de salidas": "num_salidas",
        "numero de coolers": "num_coolers",
        "¿es local imagen?": "es_local_imagen",
        "Fecha de suscripción del comodato": "marcas",
        "Fecha de término del contrato (de aplicar)": "fecha_termino_contrato",
        "Activos entregados": "activos_entregados",
        "Cantidad total de salidas de schop": "salidas_totales",
    }

    df.rename(columns=rename_dict, inplace=True)

    return df