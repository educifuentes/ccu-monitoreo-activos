import pandas as pd

from models.intermediate.censos._int_censos__censo_2026_1_agencia_pk import int_censos__censo_2026_1_agencia_pk
from models.intermediate.censos._int_censos__censo_2026_1_agencia_corpa import int_censos__censo_2026_1_agencia_corpa
from models.intermediate.censos._int_censos__censo_2026_1_corregido_manual import int_censos__censo_2026_1_corregido_manual

from helpers.transformations.dataframe_alignment import safe_concat_with_columns


def int_censos__censo_2026_1():
    # se usa la fuente manual como fuente de verdad, y se complementa con algunas columnas de las orginales corpa y pk

    # 1. Load intermediate models
    # agencias
    df_censo_2026_1_agencia_pk = int_censos__censo_2026_1_agencia_pk()
    df_censo_2026_1_agencia_corpa = int_censos__censo_2026_1_agencia_corpa()

    # manual
    df_censo_2026_1_corregido_manual = int_censos__censo_2026_1_corregido_manual()

    columns_manuales = [
        "cliente_id",
        # info cliente
        "nombre_fantasia",
        "razon_social",
        "rut",
        "region",
        "comuna",
        "direccion",
        # metadata censo
        "permite_censo",
        "motivo_no_censo",
        # activos
        "schoperas_ccu",
        "schoperas_total",
        "schoperas_competencia",
        "salidas",
        # marcas
        "marcas_abinbev",
        "marcas_kross",
        "marcas_otras",
        "marcas_otras_listado",
        "marca_competidor_en_salida",
        # acciones
        "instalo",
        "disponibilizo",
        "hay_competencia_en_salida"
    ]

    # Filter to expected columns to ensure marcas_otras existence from this source
    df_censo_2026_1_corregido_manual = df_censo_2026_1_corregido_manual[
        [col for col in columns_manuales if col in df_censo_2026_1_corregido_manual.columns]
    ]

    # Column lists for union and selection
    columns_agencias = [
        "cliente_id",
        # metadata
        "periodo",
        "fecha",
        "agencia",
        # activos
        "tiene_coolers",
        # marcas
        "marcas",
        "marcas_otras",
    ]

    # all agencias
    df_agencias = pd.concat(
        [df_censo_2026_1_agencia_pk, df_censo_2026_1_agencia_corpa],
        ignore_index=True
    )


    df = df_censo_2026_1_corregido_manual.merge(df_agencias[columns_agencias], on="cliente_id", how="left", suffixes=("", "_agencia"))
    # Data cleaning: drop rows with invalid cliente_id
    df = df[df["cliente_id"].notna()]
    df = df[df["cliente_id"].astype(str).str.lower() != "nan"]

    # 3. Fill missing metadata for 2026-1
    df["periodo"] = df["periodo"].fillna("2026-S1")
    df["fecha"] = df["fecha"].fillna(pd.to_datetime("2026-03-11").date())

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
        # marcas
        "marcas_abinbev",
        "marcas_kross",
        "marcas_otras",
        # listados
        "marcas",
        "marcas_otras_listado",
    ]

    df = df[final_columns]

    return df
