import pandas as pd
import numpy as np

from models.staging.censos._stg_censos__censo_2026_1_corregido_manual import stg_censos__censo_2026_1_corregido_manual
from helpers.transformations.yes_no_to_boolean import yes_no_to_boolean
from helpers.transformations.process_marcas import process_marcas, classify_marcas, correct_brand_names
from helpers.transformations.text_cleaning import clean_text
from helpers.transformations.clean_region import clean_region

def int_censos__censo_2026_1_corregido_manual():
    """
    Intermediate model for the manually corrected 2026-1 censo data.
    """
    # 1. Load Data
    df = stg_censos__censo_2026_1_corregido_manual()

    # 2. Column Renaming to match schema
    rename_dict = {
        "ID CLIENTE": "cliente_id",
        # cliente info
        "NOMBRE FANTASÍA": "nombre_fantasia",
        "RAZÓN SOCIAL": "razon_social",
        "RUT": "rut",
        "REGIÓN": "region",
        "COMUNA": "comuna",
        "DIRECCIÓN": "direccion",
        # censo metadata
        "Permite censo (SI/NO)": "permite_censo",
        "[Si corresponde] Motivo por el que no pudo ser censado (local cerrado, no permite ingreso, etc)": "motivo_no_censo",
        "Presencia de schopera comodato de CCU (SI/NO)": "presencia_schopera_ccu",
        # activos
        "Número de salidas totales de schop en máquinas CCU": "salidas",
        "schoperas_total": "schoperas_total",
        "schoperas_ccu": "schoperas_ccu",
        "schoperas competencia": "schoperas_competencia",
        # acciones
        "Instala schopera adicional (Sí/No)": "instalo",
        "Disponibiliza salidas en máquina schopera (0,1,2)": "disponibilizo",
        # marcas
        "CCH (Si/No)": "marcas_abinbev",
        "Kross (Si/No)": "marcas_kross",
        "Otras (indicar cuáles)": "marcas_otras_listado",
        # competencia
        "Competencia en salida CCU (Sí/No)": "hay_competencia_en_salida",
        "Indicar nombre de competidor en salida CCU": "marca_competidor_en_salida",
        # complementarios / auditoria
        "Local implementado según primer reporte (complementario)": "local_implementado_primer_reporte",
        "Local cuestionado por CCU según primer reporte (complementario)": "local_cuestionado_primer_reporte",
        "Local no implementado por CCU según primer reporte (complementario)": "local_no_implementado_primer_reporte",
        "Fue censado en julio de 2025": "censo_julio_2025",
        "Fue censado en julio de 2025 y sujeto a compromiso N°2": "censo_julio_2025_compromiso_2",
        "Unnamed: 21": "temp_unnamed_21",
    }

    df = df.rename(columns=rename_dict)

    # 3. Basic Data Types and Standard Columns
    df["cliente_id"] = df["cliente_id"].astype("str")


    # 5. Value Transformations
    df["permite_censo"] = yes_no_to_boolean(df["permite_censo"])

    # 6. Action transformations
    df["instalo"] = yes_no_to_boolean(df["instalo"]).apply(lambda x: 1 if x is True else pd.NA).astype("Int64")
    df["disponibilizo"] = pd.to_numeric(df["disponibilizo"], errors="coerce").astype("Int64")

    # 7. Text and Region Cleaning
    df = clean_text(df, ["nombre_fantasia", "direccion", "razon_social"], title=True)
    df = clean_region(df)
    
    if "marca_instalada_en_salida" in df.columns:
        df["marca_instalada_en_salida"] = correct_brand_names(df["marca_instalada_en_salida"])
        df["marca_instalada_en_salida"] = df["marca_instalada_en_salida"].str.title()


    # new column
    df["marcas_otras"] = False
    df["marcas_otras"] = df["marcas_otras_listado"].apply(lambda x: True if pd.notnull(x) and str(x).strip() != "" else False)


    selected_columns = [
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

    df = df[selected_columns]

    
    return df
