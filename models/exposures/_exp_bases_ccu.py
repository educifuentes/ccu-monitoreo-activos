import pandas as pd

from models.marts._fct_bases_ccu import fct_bases_ccu
from models.exposures._exp_clientes import exp_clientes

from models.metrics.clasification_censo import clasify_censo

def exp_bases_ccu():
    """
    Consolida la información de bases CCU con la dimensión de clientes.
    """
    # 1. Data Loading from Marts
    df = fct_bases_ccu()

    # Define standard columns to keep from CCU
    ccu_columns = [
        "cliente_id",
        "periodo",
        "fecha",
        "schoperas_ccu",
        "salidas",
        "coolers",
        "folio",
        "es_local_imagen",
        "fecha_suscripcion_comodato",
        "fecha_termino_contrato",
        "activos_entregados",
        "cantidad_total_salidas_schop",
        "modificacion",
        "mes_cambio",
    ]

    df = df[ccu_columns]

    # Merge; clientes_df is the authoritative source for shared columns
    clientes_df = exp_clientes()
    df = df.merge(clientes_df, on='cliente_id', how='left')

    return df
