import pandas as pd
from helpers.transformations.dataframe_alignment import safe_concat_with_columns

from models.intermediate.censos._int_censos__censo_2025_2 import int_censos__censo_2025_2
from models.intermediate.censos._int_censos__censo_2024_2 import int_censos__censo_2024_2
from models.intermediate.censos._int_censos__censo_2026_1 import int_censos__censo_2026_1

def fct_censos():

    # 1. Load intermediate models
    df_censo_2024_2 = int_censos__censo_2024_2()
    df_censo_2025_2 = int_censos__censo_2025_2()
    df_censo_2026_1 = int_censos__censo_2026_1()

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
        "tiene_coolers",
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
        df_censo_2026_1,
        ], 
        selected_columns
    )

 
    df.sort_values(by=["periodo"], ascending=False, inplace=True)

    return df

