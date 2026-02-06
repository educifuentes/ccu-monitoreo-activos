import pandas as pd

from models.staging._stg_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1
from utilities.transformations.yes_no_to_boolean import yes_no_to_boolean
from utilities.transformations.date_parsing import parse_spanish_month_year


def fct_contratos_ccu():
    stg_reportes_ccu_base_2026_q1_df = stg_reportes_ccu_base_2026_q1()

    columns_contratos = ['local_id',  
                         'es_local_imagen?', 
                         'Folio', 
                         'fecha_suscripcion_comodato', 
                         'fecha_termino_contrato', 
                         'activos_entregados']

    df = stg_reportes_ccu_base_2026_q1_df[columns_contratos]

    # data types
    df = yes_no_to_boolean(df, 'es_local_imagen?')

    df['fecha_suscripcion_comodato_original'] = df['fecha_suscripcion_comodato']
    df['fecha_termino_contrato_original'] = df['fecha_termino_contrato']

    # clean dates
    df = parse_spanish_month_year(df, 'fecha_suscripcion_comodato')
    df = parse_spanish_month_year(df, 'fecha_termino_contrato')

    return df