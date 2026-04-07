import pandas as pd

from models.marts.gsheets._fct_censos_gsheets import fct_censos_gsheets
from models.exposures._exp_clientes import exp_clientes

from models.metrics.clasification_censo import clasify_censo

def exp_censos():
    """
    censo con dim clientes
    """
    # 1. Data Loading and Integration
    df = fct_censos_gsheets()

    # calculate new metrics
    df["schoperas_competencia"] = df["schoperas_total"] - df["schoperas_ccu"]

    # 2. Classification Logic (Moved to metrics layer)
    df = clasify_censo(df)

    censo_columns = [
        "cliente_id",
        "periodo",
        "fecha",
        "agencia",
        "permite_censo",
        "motivo_no_censo",
        "schoperas_total",
        "schoperas_ccu",
        "schoperas_competencia",
        "salidas",
        "instalo",
        "disponibilizo",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_otras",
        "marcas_listado",
        "marcas_otras_listado",
        "hay_competencia_en_salida",
        "marca_competidor_en_salida",
        "aplica_regla",
        "salidas_objetivo",
        "salidas_competencia",
        "clasificacion"
    ]

    df = df[censo_columns]

    # Merge; clientes_df is the authoritative source for shared columns
    clientes_df = exp_clientes()
    df = df.merge(clientes_df, on='cliente_id', how='left')

    return df
