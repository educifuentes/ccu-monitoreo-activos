import pandas as pd

from models.intermediate.censos._int_censos__censo_2026_1_agencia_pk import int_censos__censo_2026_1_agencia_pk
from models.intermediate.censos._int_censos__censo_2026_1_agencia_corpa import int_censos__censo_2026_1_agencia_corpa
from models.intermediate.censos._int_censos__censo_2026_1_corregido_manual import int_censos__censo_2026_1_corregido_manual

from helpers.transformations.dataframe_alignment import safe_concat_with_columns


def int_censos__censo_2026_1():

    # 1. Load intermediate models
    df_censo_2026_1_agencia_pk = int_censos__censo_2026_1_agencia_pk()
    df_censo_2026_1_agencia_corpa = int_censos__censo_2026_1_agencia_corpa()
    df_censo_2026_1_corregido_manual = int_censos__censo_2026_1_corregido_manual()

    # Column lists for union and selection
    columns_agencias = [
        "cliente_id", "periodo", "fecha", "razon_social", "direccion", "rut", "region", "comuna",
        "nombre_fantasia", "agencia", "schoperas_total", "schoperas_ccu", "salidas", "tiene_coolers",
        "instalo", "disponibilizo", "marcas_abinbev", "marcas_kross", "marcas_ccu", "marcas_otras",
        "marcas", "marcas_otras_listado", "hay_competencia_en_salida", "marca_instalada_en_salida"
    ]

    selected_columns = [
        "cliente_id", "periodo", "fecha", "razon_social", "direccion", "rut", "region", "comuna",
        "nombre_fantasia", "agencia", "permite_censo", "motivo_no_censo", "schoperas_total",
        "schoperas_ccu", "salidas", "tiene_coolers", "instalo", "disponibilizo", "marcas_abinbev",
        "marcas_kross", "marcas_ccu", "marcas_otras", "marcas", "marcas_otras_listado",
        "hay_competencia_en_salida", "marca_instalada_en_salida"
    ]

    # 1. Union agencias
    df_agencias = safe_concat_with_columns(
        [df_censo_2026_1_agencia_pk, df_censo_2026_1_agencia_corpa],
        columns_agencias
    )

    # 2. Add manual corrections (provides permite_censo, motivo_no_censo)
    columns_manuales = ["cliente_id", "permite_censo", "motivo_no_censo"]
    df_manuales = df_censo_2026_1_corregido_manual[columns_manuales].copy()

    df_agencias = df_agencias.merge(df_manuales, on="cliente_id", how="left")

    # 3. Data type conversions
    # permite_censo comes as 'True'/'False' text from merge or source
    df_agencias["permite_censo"] = df_agencias["permite_censo"].astype(str).str.strip().str.lower().map({
        'true': True, 'false': False, 'si': True, 'sí': True, 'no': False
    }).astype("boolean")

    df_agencias = df_agencias[selected_columns]

    return df_agencias
