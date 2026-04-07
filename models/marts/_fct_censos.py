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
    

    final_columns = [
        # keys
        "cliente_id",
        "periodo",
        "fecha",
        "agencia",
        # clientes info
        "razon_social",
        "direccion",
        "rut",
        "region",
        "comuna",
        "nombre_fantasia",
        # censo metadata
        "permite_censo",
        "motivo_no_censo",
        # activos
        "schoperas_total",
        "schoperas_ccu",
        "schoperas_competencia",
        "salidas",
        "tiene_coolers",
        # accion
        "instalo",
        "disponibilizo",
        "hay_competencia_en_salida",
        "marca_competidor_en_salida",
        #presencia  marcas
        "marcas_abinbev",
        "marcas_kross",
        "marcas_otras",
        "marcas",
        "marcas_otras_listado",
    ]

    # 5. Union and Final Processing
    df = safe_concat_with_columns(
        [df_censo_2024_2, 
        df_censo_2025_2, 
        df_censo_2026_1,
        ], 
        final_columns
    )

    # rename columns
    rename_dict = {
        "marcas": "marcas_listado",
    }
    df = df.rename(columns=rename_dict)

    # types
    df["periodo"] = df["periodo"].astype(str)
    df.sort_values(by=["periodo"], ascending=False, inplace=True)

    # clean invalid IDs
    df = df[df["cliente_id"].notna()]
    df = df[df["cliente_id"].astype(str).str.lower() != "nan"]

    final_columns_ordered = [
        # keys
        "cliente_id",
        "periodo",
        "fecha",
        "agencia",
        # clientes info
        "razon_social",
        "direccion",
        "rut",
        "region",
        "comuna",
        "nombre_fantasia",
        # censo metadata
        "permite_censo",
        "motivo_no_censo",
        # activos
        "schoperas_total",
        "schoperas_ccu",
        "schoperas_competencia",
        "salidas",
        "tiene_coolers",
        # accion
        "instalo",
        "disponibilizo",
        "hay_competencia_en_salida",
        "marca_competidor_en_salida",
        #presencia  marcas
        "marcas_abinbev",
        "marcas_kross",
        "marcas_otras",
        "marcas_listado",
        "marcas_otras_listado",
    ]

    df = df[final_columns_ordered]

    return df

