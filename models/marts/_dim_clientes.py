import pandas as pd

from models.intermediate.base_normalizada._int_base_normalizada__clientes import int_base_normalizada__clientes
from models.intermediate.bases_ccu._int_bases_ccu__base_2026_q1 import int_bases_ccu__base_2026_q1_locales
from models.intermediate.censos._int_censos__censo_2026_1 import int_censos__censo_2026_1_agencia_pk

from models.intermediate.censos._int_censos__censo_2026_1_fne_listado import int_censos__censo_2026_1_fne_listado


from utilities.transformations.text_cleaning import clean_text
from utilities.transformations.clean_region import clean_region


def update_with_base_ccu_2026_q1():
    """ 
    Consolidates clientes by prioritizing the 2026 CCU report.
    Adds records from the normalized base that are missing in the 2026 report.
    """
    # load df
    df_norm = int_base_normalizada__clientes()
    df_ccu = int_bases_ccu__base_2026_q1_locales()

    # columns
    locales_columns = ["cliente_id", "razon_social", "rut", "direccion", "region", "ciudad", "comuna", "nombre_fantasia"]

    df_norm["comuna"] = None
    df_norm = df_norm[locales_columns]

    # Load both sources
    df_norm = df_norm[locales_columns]
    df_ccu = df_ccu[locales_columns]

    # 1. Start with CCU 2026 records
    df_ccu["fuente"] = "Base CCU 2026"
    
    # 2. Find records in base_norm that are NOT in base_ccu_2026
    missing_ids = df_norm[~df_norm["cliente_id"].isin(df_ccu["cliente_id"])].copy()
    missing_ids["fuente"] = "Base Normalizada"
    print(f"Clientes en base_norm no presentes en CCU 2026: {len(missing_ids)}")

    # 3. Concatenate (Union)
    df_final = pd.concat([df_ccu, missing_ids], ignore_index=True)

    return df_final

def _new_locales_censo_2026_1():
    """
    Extracts clientes from the 2026-1 Census that are NOT currently in the base dataframe.
    """
    df = update_with_base_ccu_2026_q1()
        
    censo_2026_1 = int_censos__censo_2026_1_agencia_pk()

    # Define standard columns
    locales_columns = ["cliente_id", "razon_social", "rut", "direccion", "region", "ciudad", "comuna", "nombre_fantasia"]

    # Add empty columns that don't exist in census to match standard layout
    if "rut" not in censo_2026_1.columns:
        censo_2026_1["rut"] = pd.NA
    if "ciudad" not in censo_2026_1.columns:
        censo_2026_1["ciudad"] = pd.NA

    censo_2026_1 = censo_2026_1[locales_columns]

    # Find census clientes missing from our main df
    missing_ids = censo_2026_1[~censo_2026_1["cliente_id"].isin(df["cliente_id"])].copy()
    missing_ids["fuente"] = "Censo 2026-1"
    
    print(f"Clientes en censo_2026_1 no presentes en info base: {len(missing_ids)}")

    # add missing info from fne listado
    fne_df = int_censos__censo_2026_1_fne_listado()
    
    # Keep only necessary columns from the right side for the join
    fne_df_subset = fne_df[['cliente_id', 'razon_social', 'rut']].drop_duplicates(subset=['cliente_id'])
    
    # Drop existing 'razon_social' and 'rut' to replace them entirely with FNE data
    missing_ids = missing_ids.drop(columns=['razon_social', 'rut'])
    
    # Perform left join to bring in reasonably clean FNE data
    missing_ids = missing_ids.merge(fne_df_subset, on='cliente_id', how='left')

    # clean
    missing_ids = clean_text(missing_ids, ["razon_social"], title=True)

    # reorder columns
    missing_ids = missing_ids[locales_columns]

    return missing_ids
    

def dim_clientes():
    """
    Clientes con info consolidada de censos y contratos.
    Se hace clean de valores.
    """

    df = update_with_base_ccu_2026_q1()

    # add new clientes from censo 2026-1 (23 clientes)
    df_censo = _new_locales_censo_2026_1()
    
    df = pd.concat([df, df_censo], ignore_index=True)

    # 1. Standardize and clean text columns
    # clean_text now handles:
    # - Conversion to "string" dtype (modern pandas nullable strings)
    # - Stripping whitespace
    # - Title casing (propagates pd.NA correctly)
    # - Converting empty strings to pd.NA
    title_cols = ["razon_social", "direccion", "region", "ciudad", "comuna", "nombre_fantasia"]
    df = clean_text(df, title_cols, title=True)
    df = clean_text(df, ["rut"], title=False)
    
    # 2. Normalize regions using the dedicated mapper
    df = clean_region(df)

    # 3. Final cleanups
    df["nombre_fantasia"] = df["nombre_fantasia"].replace("0", pd.NA)

    # replace cliente_id wuth "nan" to None
    df["cliente_id"] = df["cliente_id"].replace("nan", pd.NA)

    return df
