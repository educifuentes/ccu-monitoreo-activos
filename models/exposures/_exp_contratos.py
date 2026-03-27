import pandas as pd

from models.marts.gsheets._fct_bases_ccu_gsheets import fct_bases_ccu_gsheets


def exp_contratos():

    df = fct_bases_ccu_gsheets()

    selected_columns = [
        "cliente_id",
        "folio",
        "fecha_suscripcion_comodato",
        "fecha_termino_contrato",
        "es_local_imagen",
    ]

    df = df[selected_columns].sort_values(
        "fecha_suscripcion_comodato", ascending=False
    )

    df = df.drop_duplicates(subset=["cliente_id"], keep="first")

    return df