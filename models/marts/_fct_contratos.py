import pandas as pd

from models.staging._stg_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1


def fct_contratos_ccu():
    stg_reportes_ccu_base_2026_q1_df = stg_reportes_ccu_base_2026_q1()

    columns_contratos = ['local_id',  
                         'es_local_imagen?', 
                         'Folio', 
                         'fecha_suscripcion_comodato', 
                         'fecha_termino_contrato', 
                         'activos_entregados']

    df = stg_reportes_ccu_base_2026_q1_df[columns_contratos]

    return df