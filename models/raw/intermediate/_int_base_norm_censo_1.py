import pandas as pd

from models.raw.staging.base_normalizada._stg_base_norm_censo_1 import stg_base_norm_censo_1
from models.raw.staging.base_normalizada._stg_base_norm_original import stg_base_norm_original_censo_2024

from utilities.transformations.process_marcas import process_marcas, classify_marcas

def clean_base_norm_original_censo_2024():
    df = stg_base_norm_original_censo_2024()

    # clean
    # drop rows based on  where CATEGORÍA CENSO 1 column:  "NO CENSADO" , None or NaN, and CCU/Cuestionados 
    df = df[df["CATEGORÍA CENSO 1"] != "NO CENSADO"]
    df = df[df["CATEGORÍA CENSO 1"] != "CCU/Cuestionados"]
    df = df.dropna(subset=["CATEGORÍA CENSO 1"])

    # drop wrows here column Censo 1 is "SIN CENSO"
    df = df[df["Censo 1"] != "SIN CENSO"]

    # drop local_ids none or nan
    df = df.dropna(subset=["ID CLIENTE"])

    return df



def int_base_norm_original_censo_2024():
    df = clean_base_norm_original_censo_2024()

    # rename
    rename_dict = {
        "ID CLIENTE": "local_id",
        "CATEGORÍA CENSO 1": "categoria_censo_1",
        "Censo 1": "censo_1",
        "CANTIDAD DE SCHOPERAS CCU": "schoperas",
        "CANTIDAD DE SALIDAS": "salidas",
        "CCU/ABINBEV/OTRAS MARCAS COMPETENCIA": "marcas"
    }

    df = df.rename(columns=rename_dict)

    # new columns
    df["periodo"] = "2024-S2"
    df["fecha"] = pd.to_datetime("2024-10-01").date()

    # dummy creates
    df["instalo"] = pd.NA
    df["disponibilizo"] = pd.NA

    # data types
    df["salidas"] = pd.to_numeric(df["salidas"], errors='coerce').astype("Int64")
    df["schoperas"] = pd.to_numeric(df["schoperas"], errors='coerce').astype("Int64")

    # apply brand processing
    brands_col = "marcas"
    if brands_col in df.columns:
        df["marcas"] = df[brands_col].apply(process_marcas)
        df = classify_marcas(df)

    selected_columns = [
        "local_id",
        "periodo",
        "fecha",  
        # activos  
        "schoperas",
        "salidas",
        "instalo",
        "disponibilizo",
        # marcas
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras"
    ]

    df = df[selected_columns]

    return df


def clean_df_summary_censo_2024():
    df = stg_base_norm_original_censo_2024()
    summary_data = []

    initial_len = len(df)
    
    step1_df = df[df["CATEGORÍA CENSO 1"] != "NO CENSADO"]
    summary_data.append({"Filtro": "CATEGORÍA CENSO 1 == 'NO CENSADO'", "Filas Eliminadas": initial_len - len(step1_df)})
    initial_len = len(step1_df)
    
    step2_df = step1_df[step1_df["CATEGORÍA CENSO 1"] != "CCU/Cuestionados"]
    summary_data.append({"Filtro": "CATEGORÍA CENSO 1 == 'CCU/Cuestionados'", "Filas Eliminadas": initial_len - len(step2_df)})
    initial_len = len(step2_df)
    
    step3_df = step2_df.dropna(subset=["CATEGORÍA CENSO 1"])
    summary_data.append({"Filtro": "CATEGORÍA CENSO 1 es NA", "Filas Eliminadas": initial_len - len(step3_df)})
    initial_len = len(step3_df)
    
    step4_df = step3_df[step3_df["Censo 1"] != "SIN CENSO"]
    summary_data.append({"Filtro": "Censo 1 == 'SIN CENSO'", "Filas Eliminadas": initial_len - len(step4_df)})
    initial_len = len(step4_df)
    
    step5_df = step4_df.dropna(subset=["ID CLIENTE"])
    summary_data.append({"Filtro": "ID CLIENTE es NA", "Filas Eliminadas": initial_len - len(step5_df)})

    return pd.DataFrame(summary_data)


def int_base_norm_censo_1():
    df = stg_base_norm_censo_1()

    # Apply brand processing
    brands_col = "CCU/ABINBEV/OTRAS MARCAS COMPETENCIA"
    if brands_col in df.columns:
        df["marcas"] = df[brands_col].apply(process_marcas)
        df = classify_marcas(df)

    # # rename
    rename_dict = {
        "id": "local_id",
        "CATEGORÍA CENSO 1": "categoria",
        "CANTIDAD DE SCHOPERAS CCU": "schoperas_ccu",
        "CANTIDAD DE SALIDAS": "salidas_ccu",
        "CANTIDAD DE SHOPERAS COMPETENCIA ": "schoperas_competencia"
    }

    df.rename(columns=rename_dict, inplace=True)

    # data types
    df["salidas_ccu"] = pd.to_numeric(df["salidas_ccu"], errors='coerce').astype("Int64")
    df["schoperas_ccu"] = pd.to_numeric(df["schoperas_ccu"], errors='coerce').astype("Int64")
    df["schoperas_competencia"] = pd.to_numeric(df["schoperas_competencia"], errors='coerce').astype("Int64")

    # note: I've updated the data type conversion to use pd.to_numeric with errors='coerce'. This will turn any invalid strings (like '2o5') into NaN, which are then correctly handled by the "Int64" type.

    # new columns
    df["periodo"] = "2024-S2"
    df["fecha"] = pd.to_datetime("2024-10-01").date()

    selected_columns = [
        "local_id",
        "periodo",
        "fecha",
        # activos cantidades
        "schoperas_ccu",
        "schoperas_competencia",
        "salidas_ccu",
        # marcas
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras"
    ]

    # Filter columns that exist
    selected_columns = [col for col in selected_columns if col in df.columns]

    print("\n--- List of Column Names ---")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")

    df = df[selected_columns]
        
    return df