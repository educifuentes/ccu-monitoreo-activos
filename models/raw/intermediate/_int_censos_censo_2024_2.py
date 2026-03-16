from models.raw.staging.censos._stg_censos_censo_2024_2 import stg_censos_censo_2024_2
from models.raw.staging.base_normalizada._stg_base_norm_censo_2024_2 import stg_base_norm_censo_2024_2
from models.raw.staging.base_normalizada._stg_base_norm_original import stg_base_norm_original_censo_2024

from utilities.transformations.process_marcas import process_marcas, classify_marcas
from utilities.transformations.yes_no_to_boolean import yes_no_to_boolean
import pandas as pd

# nota
# se usa finalmente int_base_norm_original_censo_2024

def int_censos_censo_2024_2():
    # viene de l censo base orignal que no se uso

    stg_censos_1_df = stg_censos_censo_2024_2()

    rename_dict = {
        "SbjNum": "local_id",
        "NOMBRE LOCAL": "nombre_local",
        "REGIÓN:": "region",
        "COMUNA": "comuna",
        "DIRECCIÓN": "direccion",
        "TIPO DE LOCAL:": "tipo_de_local",
        "¿EL LOCAL SE ENCUENTRA...?": "estado_local",
        "COMENTARIO": "observaciones",
        "Srvyr": "visitador",
        "NÚMERO TOTAL DE MÁQUINAS SCHOPERAS EN EL LOCAL": "schoperas_total",
        "NÚMERO DE MÁQUINAS SCHOPERAS DE CCU\n(ASUMIR QUE LA SCHOPERA ES CCU SI LA MAYORÍA DE LAS MARCAS SON CCU - REVISAR TARJETERO DE APOYO)": "schoperas_ccu",
    }

    # rename columns
    int_censos_censo_2024_2_df = stg_censos_1_df.rename(columns=rename_dict)

    # new columns
    int_censos_censo_2024_2_df["periodo"] = "2024-S2"
    int_censos_censo_2024_2_df["fecha"] = pd.to_datetime("2024-10-01")

    # Transform boolean-like columns
    # In Censo 1 we don't have a direct "tiene_schoperas" Yes/No question for the whole local
    # but we can derive it from schoperas_total or use other questions if they fit the pattern.
    
    # We can use the cooler questions as examples of yes_no_to_boolean
    int_censos_censo_2024_2_df = yes_no_to_boolean(int_censos_censo_2024_2_df, 'INSPECCIÓN VISUAL PARA VER Y REGISTRAR SI EXISTEN COOLERS O REFRIGERADORES VERTICALES (CON VIDRIO) PARA ENFRIAR CERVEZAS.\n(EN CASO QUE LOS COOLERS NO SE ENCUENTREN VISIBLES DEBERÁ PEDIR PERMISO AL DEPENDIENTE/ADMINISTRADOR/PROPIETARIO PARA OBSERVARLOS Y FOTOGRAFIARLOS)\n\n¿HAY COOLERS O REFRIGERADORES VERTICALES (CON VIDRIO) PARA ENFRIAR CERVEZAS?')
    
    # Create "tiene_schoperas" based on schoperas_total
    int_censos_censo_2024_2_df["tiene_schoperas"] = int_censos_censo_2024_2_df["schoperas_total"] > 0
    
    # Add period
    int_censos_censo_2024_2_df["periodo"] = "2024-S2" # Assuming this is the previous period

    # Calculate total outputs (salidas) by summing machines 1 to 12
    int_censos_censo_2024_2_df["salidas"] = 0
    for i in range(1, 13):
        col_name = f"NÚMERO DE SALIDAS TOTALES DE SCHOPERAS\nMÁQUINA SCHOPERA {i}:"
        col_name_alt = f"NÚMERO DE SALIDAS TOTALES DE SCHOPERAS \nMÁQUINA SCHOPERA {i}:"
        
        if col_name in int_censos_censo_2024_2_df.columns:
            int_censos_censo_2024_2_df["salidas"] += pd.to_numeric(int_censos_censo_2024_2_df[col_name], errors='coerce').fillna(0)
        elif col_name_alt in int_censos_censo_2024_2_df.columns:
            int_censos_censo_2024_2_df["salidas"] += pd.to_numeric(int_censos_censo_2024_2_df[col_name_alt], errors='coerce').fillna(0)

    selected_columns = [
        "local_id",
        # metadata
        "periodo",
        "fecha",
        # "estado_local",
        # "observaciones",
        # "tiene_schoperas",
        # activos
        "schoperas_ccu",
        "schoperas_total",
        "salidas"
    ]
    
    # Ensure all selected columns exist (some might have been dropped if empty)
    available_columns = [col for col in selected_columns if col in int_censos_censo_2024_2_df.columns]
    
    return int_censos_censo_2024_2_df[available_columns]




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
        "CATEGORÍA CENSO 1": "categoria_censo_2024_2",
        "Censo 1": "censo_2024_2",
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
        df["marcas"] = df[brands_col]
        df = process_marcas(df)
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


def int_base_norm_censo_2024_2():
    df = stg_base_norm_censo_2024_2()

    # Apply brand processing
    brands_col = "CCU/ABINBEV/OTRAS MARCAS COMPETENCIA"
    if brands_col in df.columns:
        df["marcas"] = df[brands_col]
        df = process_marcas(df)
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
        "salidas_ccu",
        # marcas
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras"
    ]

    df = df[selected_columns]
        
    return df