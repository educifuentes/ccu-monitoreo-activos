import pandas as pd

from models.marts._fct_bases_ccu import fct_bases_ccu


def exp_contratos():

    df = fct_bases_ccu()

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