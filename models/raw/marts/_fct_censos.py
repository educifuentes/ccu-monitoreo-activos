import pandas as pd

from models.raw.intermediate._int_censos_censo_2025_2 import int_censos_censo_2025_2
from models.raw.intermediate._int_censos_censo_2026_1 import int_censos_censo_2026_1, int_censos_censo_2026_1_agencia_nueva

from models.raw.intermediate._int_base_norm_censo_2024_2 import int_base_norm_original_censo_2024


def fct_censos():
    """
    Combines Censo 1 and Censo 2 data into a single fact table.
    Standardizes columns across both datasets to ensure a consistent schema.
    """
    # 1. Load intermediate models
    df_censo_2024_2 = int_base_norm_original_censo_2024()
    df_censo_2025_2 = int_censos_censo_2025_2()
    df_censo_2026_1 = int_censos_censo_2026_1()
    df_censo_2026_1_agencia_nueva = stg_censos_censo_2026_1_agencia_nueva()

    selected_columns = [
        "local_id",
        # metadata
        "periodo",
        "fecha",
        # activos
        "schoperas",
        "salidas",
        # accion
        "accion_ccu",
        "instalo",
        "disponibilizo",
        # marcas
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras",
        # marcas - listados
        "marcas_abinbev_listado",
        "marcas_kross_listado",
        "marcas_ccu_listado",
        "marcas_otras_listado"
     

    ]

    # 5. Union and Final Processing
    df = pd.concat([df_censo_2024_2, df_censo_2025_2, df_censo_2026_1], ignore_index=True)

    df = df[selected_columns]

    return df

def fct_censos_2026():

    df_censo_2026_1 = int_censos_censo_2026_1()
    df_censo_2026_1_agencia_nueva = int_censos_censo_2026_1_agencia_nueva()

    selected_columns = [
        "local_id",
        # locales info
        "razon_social",
        "direccion",
        "rut",
        "region",
        "comuna",
        "nombre_fantasia",
        # metadata
        "periodo",
        "fecha",
        "permite_censo",
        # activos
        "schoperas",
        "salidas",
        # accion
        "accion_ccu",
        "instalo",
        "disponibilizo",
        # marcas
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras",
        # listados
        "marcas_abinbev_listado",
        "marcas_kross_listado",
        "marcas_ccu_listado",
        "marcas_otras_listado",
        # competencia
        "marca_instalada_en_salida",
        "hay_competencia_en_salida"

    ]

    # 5. Union and Final Processing
    df = pd.concat([df_censo_2026_1, df_censo_2026_1_agencia_nueva], ignore_index=True)

    df = df[selected_columns]

    return df