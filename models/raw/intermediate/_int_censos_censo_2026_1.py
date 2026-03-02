import pandas as pd

from models.raw.staging.censos._stg_censos_censo_2026_1 import stg_censos_censo_2026_1

from utilities.transformations.yes_no_to_boolean import yes_no_to_boolean
from utilities.transformations.process_marcas import process_marcas, classify_marcas
from utilities.transformations.text_cleaning import clean_text

def int_censos_censo_2026_1():

    stg_censos_2_df = stg_censos_censo_2026_1()

    # 1. Column Renamming
    rename_dict = {
        "ID Cliente": "local_id",
        "cliente": "razon_social",
        "Dirección": "direccion",
        "Región": "region",
        "Comuna": "comuna",
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
        '¿CUALES DE ESTAS MARCAS SE VENDEN EN SCHOP?': "marcas"
    }
    df = stg_censos_2_df.rename(columns=rename_dict)

    # 2. Basic Data Types
    df["local_id"] = df["local_id"].astype("str")

    # 3. Brand Processing and Classification
    if "marcas" in df.columns:
        df["marcas"] = df["marcas"].apply(process_marcas)
        df = classify_marcas(df)

    # 4. Value Transformations
    df = yes_no_to_boolean(df, "tiene_schoperas")
    
    # 5. Period and Metadata
    df["periodo"] = "2026-S1"
    df["fecha"] = pd.to_datetime("2026-02-01").date()
    
    # 6. Calculated Columns (Total outputs)
    # Total outputs (salidas) is the sum of salidas across all machine columns
    df["salidas"] = 0
    for i in range(1, 7):
        col_name = f"SCHOPERA CCU {i} - NÚMERO DE SALIDAS"
        if col_name in stg_censos_2_df.columns:
            df["salidas"] += pd.to_numeric(stg_censos_2_df[col_name], errors='coerce').fillna(0)

    # 7. Final Conversions to Int64 (nullable int)
    numeric_cols = ["salidas", "schoperas", "instalo", "disponibilizo"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

    # clean text values nombre_fantasia, direccion
    df = clean_text(df, ["nombre_fantasia", "direccion"], title=True)
    
    # 8. Final Column Selection
    selected_columns = [
        "local_id",
        "periodo",
        "fecha",
        "schoperas",
        "salidas",
        "instalo",
        "disponibilizo",
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras",
        # locales cols
        "razon_social",
        "direccion",
        "region",
        "comuna",
        "nombre_fantasia",
        # otros
        # "tiene_schoperas",
        # "observaciones",
        # "visitador",
        # "rut_visitador"
    ]
    
    return df[selected_columns]
