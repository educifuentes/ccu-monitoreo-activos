import pandas as pd
import numpy as np

from utilities.yaml_loader import get_table_config

def stg_base_norm_original():
    # Fetch configuration from YAML
    config = get_table_config(
        source_name="base normalizada", 
        table_name="base_normalizada_original", 
        yaml_path="models/raw/sources/_src_base_normalizada.yml"
    )
    file_path = config.get('path')

    # drop columns encuestada unificada
    
    
    # Load CSV
    df = pd.read_csv(file_path, skiprows=1)

    # Drop columns encuestada unificada
    columns_to_drop_encuestada_unificada = [
        "NUEVO TELÉFONO",
        "DUEÑO/ADMINISTRADOR/JEFE DE LOCAL",
        "¿CONOCE EL ACUERDO CCU CON LA FISCALÍA NACIONAL ECONÓMICA?",
        "¿A QUÉ PROVEEDORES LE COMPRAN SHOP?",
        "CCU",
        "ABINVED",
        "OTRO (PONER CUAL)",
        "¿CUÁNTAS SCHOPERAS DE CCU TIENEN EN EL LOCAL ACTUALMENTE?",
        "¿CCU HA DEJADO PROACTIVAMENTE EN SUS SHOPERAS ALGUNA SALIDA LIBRE DISPONIBLE PARA OTRO PROVEEDOR? SI/NO",
        "¿CCU HA INSTALADO PROACTIVAMENTE ALGUNA MAQUINA SHOPERA ADICIONAL PARA SER USADA POR OTRO PROVEEDOR? SI/NO",
        "¿EN LOS ULTIMOS 6 MESES, HA INCORPORADO UD. UN NUEVO PROVEEDOR DE SCHOP EN ALGUNA SALIDA DE LAS SHOPERAS? SI/NO",
        "¿CUÁL?"
    ]
    df = df.drop(columns=columns_to_drop_encuestada_unificada, errors='ignore')



    return df

def stg_base_norm_original_base_ccu_2024():
    df = stg_base_norm_original()
    selected_columns = ["ID CLIENTE", "N° Coolers", "N° Columnas", "N° Salidas Schop CCU"]
    
    # Drop rows where all three activos columns are null or none
    activos_cols = ["N° Coolers", "N° Columnas", "N° Salidas Schop CCU"]
    df = df.dropna(subset=activos_cols, how='all')


    df = df[selected_columns]
    return df

def stg_base_norm_original_censo_2024():
    df = stg_base_norm_original()

    selected_columns = [
        "ID CLIENTE", 
        "CATEGORÍA CENSO 1",
        "Censo 1",
        "CANTIDAD DE SCHOPERAS CCU",
        "CANTIDAD DE SALIDAS",
        "CANTIDAD DE SHOPERAS COMPETENCIA ",
        "CCU/ABINBEV/OTRAS MARCAS COMPETENCIA"
    ]    

    df = df[selected_columns]
    return df