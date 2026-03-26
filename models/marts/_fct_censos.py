import pandas as pd
from helpers.transformations.dataframe_alignment import safe_concat_with_columns

from models.intermediate.censos._int_censos__censo_2025_2 import int_censos__censo_2025_2
from models.intermediate.censos._int_censos__censo_2026_1_agencia_pk import int_censos__censo_2026_1_agencia_pk
from models.intermediate.censos._int_censos__censo_2026_1_agencia_corpa import int_censos__censo_2026_1_agencia_corpa
from models.intermediate.censos._int_censos__censo_2026_1_corregido_manual import int_censos__censo_2026_1_corregido_manual

from models.intermediate.censos._int_censos__censo_2024_2 import int_censos__censo_2024_2


def fct_censos():

    # 1. Load intermediate models
    df_censo_2024_2 = int_censos__censo_2024_2()
    df_censo_2025_2 = int_censos__censo_2025_2()
    df_censo_2026_1_agencia_pk = int_censos__censo_2026_1_agencia_pk()
    df_censo_2026_1_agencia_corpa = int_censos__censo_2026_1_agencia_corpa()
    df_censo_2026_1_corregido_manual = int_censos__censo_2026_1_corregido_manual()

    selected_columns = [
        # keys
        "cliente_id",
        "periodo",
        "fecha",
        # clientes info
        "razon_social",
        "direccion",
        "rut",
        "region",
        "comuna",
        "nombre_fantasia",
        # censo metadata
        "agencia",
        "permite_censo",
        "motivo_no_censo",
        # activos
        "schoperas_total",
        "schoperas_ccu",
        "salidas",
        # accion
        "instalo",
        "disponibilizo",
        # marcas
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras",
        # listados
        "marcas",
        "marcas_otras_listado",
        # competencia
        "hay_competencia_en_salida",
        "marca_instalada_en_salida",
    ]

    # 5. Union and Final Processing
    df = safe_concat_with_columns(
        [df_censo_2024_2, 
        df_censo_2025_2, 
        df_censo_2026_1_agencia_pk, 
        df_censo_2026_1_agencia_corpa,
        df_censo_2026_1_corregido_manual
        ], 
        selected_columns
    )

 
    df.sort_values(by=["periodo"], ascending=False, inplace=True)

    return df

