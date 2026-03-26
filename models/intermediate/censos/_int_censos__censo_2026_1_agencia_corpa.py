import pandas as pd
from models.staging.censos._stg_censos__censo_2026_1_agencia_corpa import stg_censos__censo_2026_1_agencia_corpa
from models.staging.censos._stg_censos__censo_2026_1_agencia_corpa_sistematizado import stg_censos__censo_2026_1_agencia_corpa_sistematizado
from helpers.transformations.yes_no_to_boolean import yes_no_to_boolean
from helpers.transformations.process_marcas import process_marcas_questionnaire_version, classify_marcas, correct_brand_names
from helpers.transformations.text_cleaning import clean_text
from helpers.transformations.clean_region import clean_region


def int_censos__censo_2026_1_agencia_corpa():

    # 1. Load Data
    df = stg_censos__censo_2026_1_agencia_corpa()

    # 2. Column Renaming
    rename_dict = {
        "ID cliente": "cliente_id",
        # info cliente
        "DIRECCIÓN": "direccion",
        "REGIÓN": "region",
        "RUT": "rut",
        "COMUNA": "comuna",
        "LOCAL": "nombre_fantasia",
        "Razón social": "razon_social",
        "¿EL LOCAL SE ENCUENTRA...?": "estado_local",
        # censo metadata
        "NOMBRE DEL ENCUESTADO": "visitador",
        "rut Visitador": "rut_visitador",
        "Observaciones": "observaciones",
        "PERMITE AUDITORÍA": "permite_censo",
        # activos
        "NÚMERO TOTAL DE MÁQUINAS SCHOPERAS EN EL LOCAL": "schoperas_total",
        "NÚMERO DE MÁQUINAS SCHOPERAS DE CCU": "schoperas_ccu",
        "¿TIENE ALGÚN EQUIPO COOLER ENTREGADO POR CCU?": "tiene_coolers",
        # accion
        "EN CASO DE QUE CCU TENGA MÁS DE 3 SALIDAS, ¿INSTALÓ O DISPONBILIZÓ CCU UN SCHOPERA?": "accion_ccu",
        "CUANTAS SHOPERAS NUEVAS INSTALO CCU PARA MARCAS ARTESANALES?": "instalo",
        'CUANTAS SALIDAS DEJO LIBRE CCU PARA MARCAS ARTESANALES? s ': "disponibilizo",
        # marcas
        "OTRA MARCA, ESPECIFIQUE.1": "marcas_texto_libre",
        # competencia en salida
        "¿HAY ALGUNA MARCA DE LA COMPETENCIA DE CCU, QUE ESTÉ INSTALADA EN ESA SALIDA O SCHOPERA NUEVA?": "hay_competencia_en_salida",
        "¿CUÁL?": "marca_instalada_en_salida"
    }

    df = df.rename(columns=rename_dict)

    # 3. Basic Data Types
    df["cliente_id"] = df["cliente_id"].astype("str")

    # 4. Period and Metadata
    df["periodo"] = "2026-S1"
    df["fecha"] = pd.to_datetime("2026-02-01").date()
    df["agencia"] = "corpa"
    # Note: permite_censo and motivo_no_censo are added via systematized data merge later.

    # 5. Brand Processing and Classification
    df = process_marcas_questionnaire_version(df)
    df = classify_marcas(df)

    if "marca_instalada_en_salida" in df.columns:
        df["marca_instalada_en_salida"] = correct_brand_names(df["marca_instalada_en_salida"])
        df["marca_instalada_en_salida"] = df["marca_instalada_en_salida"].str.title()

    # 6. Value Transformations
    if "permite_censo" in df.columns:
        df["permite_censo"] = df["permite_censo"].map(
            {"Si acepta": True, "No acepta/ rechaza": False}
        )

    if "hay_competencia_en_salida" in df.columns:
        df["hay_competencia_en_salida"] = df["hay_competencia_en_salida"].map(
            {"Sí, ¿cuál?": True, "No": False}
        )

    # accion columns
    df["instalo"] = None
    df["disponibilizo"] = None

    if "accion_ccu" in df.columns:
        accion = df["accion_ccu"].astype(str).str.lower()
        mask_instalo = accion.str.contains(r"instaló|instalo", regex=True, na=False)
        mask_disponibilizo = accion.str.contains(r"disponibilizó|disponibilizo", regex=True, na=False)

        df.loc[mask_instalo, "instalo"] = 1
        df.loc[mask_disponibilizo, "disponibilizo"] = 1

    df["tiene_coolers"] = yes_no_to_boolean(df["tiene_coolers"])
    
    # Text and region cleaning
    df = clean_text(df, ["nombre_fantasia", "direccion"], title=True)
    df = clean_region(df)
    
    # 7. Calculated Columns
    # Total outputs (salidas) is the sum of salidas across all machine columns
    df["salidas"] = 0
    for i in range(1, 7):
        col_name = f"SCHOPERA CCU {i} - NÚMERO DE SALIDAS"
        if col_name in df.columns:
            df["salidas"] += pd.to_numeric(df[col_name], errors='coerce').fillna(0)

    numeric_cols = ["salidas", "schoperas", "instalo", "disponibilizo"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

    # Initialize missing metadata before slice
    df["permite_censo"] = None
    df["motivo_no_censo"] = None

    # 8. Final Column Selection
    selected_columns = [
        "cliente_id",
        # clientes cols
        "razon_social",
        "nombre_fantasia",
        "rut",
        "direccion",
        "region",
        "comuna",
        # censo metadata
        "periodo",
        "fecha",
        "agencia",
        "permite_censo",
        "motivo_no_censo",
        # activos
        "schoperas_total",
        "schoperas_ccu",
        "salidas",
        "tiene_coolers",
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
        # competencia en salida
        "hay_competencia_en_salida",
        "marca_instalada_en_salida"
    ]
    # Removed from corpa to match pk and later union in fct_censos: "marcas_texto_libre"
    df = df[selected_columns]

    # 9. Append final systematized data (which provides permite_censo and motivo_no_censo)
    df_sistematizado = stg_censos__censo_2026_1_agencia_corpa_sistematizado()

    rename_dict_sistematizado = {
        "ID CLIENTE": "cliente_id",
        "Permite censo (SI/NO)": "permite_censo",
        "[Si corresponde] Motivo por el que no pudo ser censado (local cerrado, no permite ingreso, etc)": "motivo_no_censo"
    }

    df_sistematizado = df_sistematizado.rename(columns=rename_dict_sistematizado)

    columns_sistematizado = ["cliente_id", "permite_censo", "motivo_no_censo"]

    df_sistematizado["cliente_id"] = df_sistematizado["cliente_id"].astype("str")

    # Drop explicitly to avoid potential merge suffixes (_x, _y)
    cols_to_drop = [col for col in ["permite_censo", "motivo_no_censo"] if col in df.columns]
    if len(cols_to_drop) > 0:
        df = df.drop(columns=cols_to_drop)

    df = df.merge(
        df_sistematizado[columns_sistematizado],
        on="cliente_id",
        how="left"
    )

    return df
