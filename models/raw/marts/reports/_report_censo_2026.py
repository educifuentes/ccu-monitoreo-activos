import pandas as pd
from models.raw.marts._fct_censos import fct_censos_2026
from models.raw.marts._dim_locales import dim_locales

def report_censo_2026():
    """
    Data model that generates the final Censo 2026 report
    by joining the fact censos 2026 with dimensions and mapping
    to the final user-facing schema.
    """
    final_columns = [
        "AGENCIA",
        "ID CLIENTE",
        "NOMBRE FANTASÍA",
        "RAZÓN SOCIAL",
        "RUT",
        "REGIÓN",
        "COMUNA",
        "DIRECCIÓN",
        "Permite censo (SI/NO)",
        "[Si corresponde] Motivo por el que no pudo ser censado (local cerrado, no permite ingreso, etc)",
        "Presencia de schopera comodato de CCU (SI/NO)",
        "Número de salidas totales de schop en máquinas CCU",
        "Instala schopera adicional (Sí/No)",
        "Disponibiliza salidas en máquina schopera (0,1,2)",
        "CCH (Si/No)",
        "Kross (Si/No)",
        "Otras (indicar cuáles)",
        "Competencia en salida CCU (Sí/No)",
        "Indicar nombre de competidor en salida CCU",
        # extras nuevas
        "schoperas_total",
        "schoperas_ccu"
    ]

    COLUMN_MAPPING = {
        # agencia
        "AGENCIA": "agencia",
        # locales info
        "ID CLIENTE": "local_id",
        "NOMBRE FANTASÍA": "nombre_fantasia", 
        "RAZÓN SOCIAL": "razon_social",
        "RUT": "rut",
        "REGIÓN": "region",
        "COMUNA": "comuna",
        "DIRECCIÓN": "direccion",
        # censo metadta
        "Permite censo (SI/NO)": "permite_censo",
        # pending
        "[Si corresponde] Motivo por el que no pudo ser censado (local cerrado, no permite ingreso, etc)": "motivo_no_censo",
        # activos
        "Presencia de schopera comodato de CCU (SI/NO)": "schoperas",  
        "Número de salidas totales de schop en máquinas CCU": "salidas",
        # accion
        "Instala schopera adicional (Sí/No)": "instalo",
        "Disponibiliza salidas en máquina schopera (0,1,2)": "disponibilizo",
        # marcas
        "CCH (Si/No)": "marcas_abinbev",
        "Kross (Si/No)": "marcas_kross",
        "Otras (indicar cuáles)": "marcas_otras_listado",
        # marcas en salidas nuevas
        "Competencia en salida CCU (Sí/No)": "hay_competencia_en_salida", 
        "Indicar nombre de competidor en salida CCU": "marca_instalada_en_salida",
         # extras nuevas
        "schoperas_total": "schoperas_total",
        "schoperas_ccu": "schoperas_ccu"
    }

    df_fct_censos = fct_censos_2026()
    df_locales = dim_locales()

    # Ensure local_id has the same type
    df_fct_censos["local_id"] = df_fct_censos["local_id"].astype(str)
    df_locales["local_id"] = df_locales["local_id"].astype(str)

    # adapt
    df_fct_censos["instalo"] = df_fct_censos["instalo"] > 0
    

    # Drop duplicate local_ids from the lookup dataframe
    df_locales = df_locales.drop_duplicates(subset=["local_id"], keep="last")
    
    # Set index to local_id to align the update
    df_fct_censos = df_fct_censos.set_index('local_id')
    df_locales = df_locales.set_index('local_id')
    
    # Update only missing values
    missing_mask = df_fct_censos['razon_social'].isna()
    if missing_mask.any() and 'razon_social' in df_locales.columns:
        df_fct_censos.loc[df_fct_censos.index[missing_mask], 'razon_social'] = df_locales['razon_social']
        
    missing_mask_rut = df_fct_censos['rut'].isna()
    if missing_mask_rut.any() and 'rut' in df_locales.columns:
        df_fct_censos.loc[df_fct_censos.index[missing_mask_rut], 'rut'] = df_locales['rut']
    
    df_fct_censos = df_fct_censos.reset_index()
    
    # Initialize an empty DataFrame with our target columns
    out_df = pd.DataFrame(columns=final_columns)

    # transformations
    
    # Map the columns
    for final_col, source_col in COLUMN_MAPPING.items():
        if source_col == "PENDING" or source_col not in df_fct_censos.columns:
            # We don't have this mapping yet, leave it empty
            out_df[final_col] = None
        else:
            # Pull the data from the source column
            out_df[final_col] = df_fct_censos[source_col]

            
    return out_df