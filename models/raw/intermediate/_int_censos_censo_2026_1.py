import pandas as pd

from models.raw.staging.censos._stg_censos_censo_2026_1 import stg_censos_censo_2026_1, stg_censos_censo_2026_1_agencia_nueva, stg_censos_censo_2026_1_corregido

from utilities.transformations.yes_no_to_boolean import yes_no_to_boolean
from utilities.transformations.process_marcas import process_marcas, classify_marcas, process_marcas_questionnaire_version, correct_brand_names
from utilities.transformations.text_cleaning import clean_text
from utilities.transformations.clean_region import clean_region



def int_censos_censo_2026_1():

    df = stg_censos_censo_2026_1()

    # 1. Column Renamming
    rename_dict = {
        "ID Cliente": "local_id",
        "Dirección": "direccion",
        "Región": "region",
        "Comuna": "comuna", 
        # "RUT": "rut",
        "Nombre fantasía": "nombre_fantasia",
        "Visitador": "visitador",
        "rut Visitador": "rut_visitador",
        "Observaciones": "observaciones",
        # activos
        "EL LOCAL CUENTA CON MAQUINAS SHOPERAS?": "tiene_schoperas",
        "NÚMERO DE MÁQUINAS SCHOPERAS DE CCU(ASUMIR QUE LA SCHOPERA ES CCU SI LA MAYORÍA DE LAS MARCAS SON CCU - REVISAR TARJETERO DE APOYO)": "schoperas",
        # accion
        "CUANTAS SHOPERAS NUEVAS INSTALO CCU PARA MARCAS ARTESANALES?": "instalo",
        'CUANTAS SALIDAS DEJO LIBRE CCU PARA MARCAS ARTESANALES? s ': "disponibilizo",
        # marcas
        '¿CUALES DE ESTAS MARCAS SE VENDEN EN SCHOP?': "marcas",
        " OTRA MARCA, ESPECIFIQUE": "marcas_texto_libre"
    }

    df = df.rename(columns=rename_dict)

    # 2. Basic Data Types
    df["local_id"] = df["local_id"].astype("str")

    df["rut"] = None


        # 5. Period and Metadata
    df["periodo"] = "2026-S1"
    df["fecha"] = pd.to_datetime("2026-02-01").date()

    #. censo metadata columns
    df["permite_censo"] = None

    # 3. Brand Processing and Classification
    if "marcas" in df.columns:
        df = process_marcas(df)
        df = classify_marcas(df)

    # 4. Value Transformations
    df = yes_no_to_boolean(df, "tiene_schoperas")

    # accion columns
    df["accion_ccu"] = None
    df["marca_instalada_en_salida"] = None
    

    # dummy razon social
    df["razon_social"] = None
    
    # 6. Calculated Columns (Total outputs)
    # Total outputs (salidas) is the sum of salidas across all machine columns
    df["salidas"] = 0
    for i in range(1, 7):
        col_name = f"SCHOPERA CCU {i} - NÚMERO DE SALIDAS"
        if col_name in df.columns:
            df["salidas"] += pd.to_numeric(df[col_name], errors='coerce').fillna(0)

    # 7. Final Conversions to Int64 (nullable int)
    numeric_cols = ["salidas", "schoperas", "instalo", "disponibilizo"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

    # clean text values nombre_fantasia, direccion
    df = clean_text(df, ["nombre_fantasia", "direccion"], title=True)

    # region
    df = clean_region(df)
    
    # 8. Final Column Selection
    selected_columns = [
        "local_id",
        # locales cols
        "razon_social",
        "nombre_fantasia",
        "rut",
        "direccion",
        "region",
        "comuna",
        # censo metadata
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
        "marcas_otras_listado"
    ]
    
    return df[selected_columns]


def int_censos_censo_2026_1_agencia_nueva():

    df = stg_censos_censo_2026_1_agencia_nueva()

    # 1. Column Renamming
    rename_dict = {
        "ID cliente": "local_id",
        # info local
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
        "NÚMERO DE MÁQUINAS SCHOPERAS DE CCU": "schoperas",
        # accion
        "EN CASO DE QUE CCU TENGA MÁS DE 3 SALIDAS, ¿INSTALÓ O DISPONBILIZÓ CCU UN SCHOPERA?": "accion_ccu",
        "CUANTAS SHOPERAS NUEVAS INSTALO CCU PARA MARCAS ARTESANALES?": "instalo",
        'CUANTAS SALIDAS DEJO LIBRE CCU PARA MARCAS ARTESANALES? s ': "disponibilizo",
        # marcas
        "OTRA MARCA, ESPECIFIQUE.1": "marcas_texto_libre",
        # comptencia en salida
        "¿HAY ALGUNA MARCA DE LA COMPETENCIA DE CCU, QUE ESTÉ INSTALADA EN ESA SALIDA O SCHOPERA NUEVA?": "hay_competencia_en_salida",
        "¿CUÁL?": "marca_instalada_en_salida"
    }

    df = df.rename(columns=rename_dict)

    # 2. Basic Data Types
    df["local_id"] = df["local_id"].astype("str")


    # 3. Brand Processing and Classification

    df = process_marcas_questionnaire_version(df)
    df = classify_marcas(df)

    df["marca_instalada_en_salida"] = correct_brand_names(df["marca_instalada_en_salida"])

    # 4. Value Transformations
    # df = yes_no_to_boolean(df, "tiene_schoperas")
    
    # 5. Period and Metadata
    df["periodo"] = "2026-S1"
    df["fecha"] = pd.to_datetime("2026-02-01").date()
    
    # 6. Calculated Columns (Total outputs)
    # Total outputs (salidas) is the sum of salidas across all machine columns
    df["salidas"] = 0
    for i in range(1, 7):
        col_name = f"SCHOPERA CCU {i} - NÚMERO DE SALIDAS"
        if col_name in df.columns:
            df["salidas"] += pd.to_numeric(df[col_name], errors='coerce').fillna(0)

    # 7. Final Conversions to Int64 (nullable int)
    numeric_cols = ["salidas", "schoperas", "instalo", "disponibilizo"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

    # clean text values nombre_fantasia, direccion
    df = clean_text(df, ["nombre_fantasia", "direccion"], title=True)

    # accion columns

    df["instalo"] = None
    df["disponibilizo"] = None

    # Mapping logic for accion_ccu
    if "accion_ccu" in df.columns:
        accion = df["accion_ccu"].astype(str).str.lower()
        mask_instalo = accion.str.contains(r"instaló|instalo", regex=True, na=False)
        mask_disponibilizo = accion.str.contains(r"disponibilizó|disponibilizo", regex=True, na=False)

        df.loc[mask_instalo, "instalo"] = 1
        df.loc[mask_disponibilizo, "disponibilizo"] = 1

    # Competencia en salida

    if "hay_competencia_en_salida" in df.columns:
        df["hay_competencia_en_salida"] = df["hay_competencia_en_salida"].map(
            {"Sí, ¿cuál?": True, "No": False}
        )

    # region
    df = clean_region(df)
    
    # 8. Final Column Selection
    selected_columns = [
        "local_id",
        # locales cols
        "razon_social",
        "nombre_fantasia",
        "rut",
        "direccion",
        "region",
        "comuna",
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
        "marcas_texto_libre",
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

    df = df[selected_columns]
    
    return df