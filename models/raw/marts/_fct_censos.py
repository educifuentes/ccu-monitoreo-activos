import pandas as pd
from utilities.transformations.dataframe_alignment import safe_concat_with_columns

from models.raw.intermediate._int_censos_censo_2025_2 import int_censos_censo_2025_2
from models.raw.intermediate._int_censos_censo_2026_1 import int_censos_censo_2026_1_agencia_pk, int_censos_censo_2026_1_agencia_corpa

from models.raw.intermediate._int_base_norm_censo_2024_2 import int_base_norm_original_censo_2024


def fct_censos_2026():
    # blends corpa and pk agencias

    df_censo_2026_1 = int_censos_censo_2026_1_agencia_pk()
    df_censo_2026_1_agencia_corpa = int_censos_censo_2026_1_agencia_corpa()

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
        "agencia",
        "permite_censo",
        "motivo_no_censo",
        # activos
        "schoperas_total",
        "schoperas_ccu",
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
    df = safe_concat_with_columns([df_censo_2026_1, df_censo_2026_1_agencia_corpa], selected_columns)

    return df

def fct_censos():

    # 1. Load intermediate models
    df_censo_2024_2 = int_base_norm_original_censo_2024()
    df_censo_2025_2 = int_censos_censo_2025_2()

    df_censo_2026_1 = fct_censos_2026()

    selected_columns = [
        "local_id",
        # metadata censo
        "periodo",
        "fecha",
        "agencia",
        "permite_censo",
        "motivo_no_censo",
        # activos
        "schoperas_total",
        "schoperas_ccu",
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
        "marcas_otras_listado"
    
    ]


    # 5. Union and Final Processing
    df = safe_concat_with_columns([df_censo_2024_2, df_censo_2025_2, df_censo_2026_1], selected_columns)

    return df

