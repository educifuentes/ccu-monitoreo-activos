import pandas as pd
import numpy as np
from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.utilities.load_source import load_source

def stg_bases_ccu__base_2026_q1():
    # Fetch configuration from YAML
    file_path = get_source_metadata("base_solicitada_2026", "models/sources/_src_bases_ccu.yml")
    
    # Load CSV
    df = load_source(file_path)

    # rename
    rename_dict = {
        "local_id": "cliente_id",
        "numero de schoperas": "schoperas",
        "numero de salidas": "salidas",
        "numero de coolers": "coolers",
        "¿es local imagen?": "es_local_imagen",
        "Fecha de suscripción del comodato": "fecha_suscripcion_comodato",
        "Fecha de término del contrato (de aplicar)": "fecha_termino_contrato",
        "Activos entregados": "activos_entregados",
        "Cantidad total de salidas de schop": "cantidad_total_salidas_schop",
    }

    df.rename(columns=rename_dict, inplace=True)

    # data types
    df["cliente_id"] = df["cliente_id"].astype(str)

    return df
