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
        "NOMBRE FANTASÍA": "nombre_fantasia",
        "RAZÓN SOCIAL": "razon_social",
        "RUT": "rut",
        "REGIÓN": "region",
        "COMUNA": "comuna",
        "DIRECCIÓN": "direccion",
        "Permite censo (SI/NO)": "permite_censo",
        "[Si corresponde] Motivo por el que no pudo ser censado (local cerrado, no permite ingreso, etc)": "motivo_no_censo",
        "Presencia de schopera comodato de CCU (SI/NO)": "tiene_schopera",
        "Número de salidas totales de schop en máquinas CCU": "salidas",
        "Instala schopera adicional (Sí/No)": "instalo",
        "Disponibiliza salidas en máquina schopera (0,1,2)": "disponibilizo",
        "Otras (indicar cuáles)": "marcas_texto_libre",
        "Competencia en salida CCU (Sí/No)": "hay_competencia_en_salida",
        "Indicar nombre de competidor en salida CCU": "marca_instalada_en_salida",
        # "schoperas_total": "schoperas_total", # Already matches or exists
        # "schoperas_ccu": "schoperas_ccu", # Already matches or exists
    }

    df = df.rename(columns=rename_dict)

    # 3. Basic Data Types and Standard Columns
    df["cliente_id"] = df["cliente_id"].astype("str")
    df["periodo"] = "2026-S1"
    df["fecha"] = pd.to_datetime("2026-03-11").date() # Based on filename date
    df["agencia"] = "definitiva_pilar"
    
    # User requested column: coolers (Solo hay que agregar columna de coolers)
    df["coolers"] = None

    # 4. Brand Consolidation (CCH, Kross, Otras)
    # Map CCH and Kross to marques if SI
    df["marcas_ccu_flag"] = yes_no_to_boolean(df["CCH (Si/No)"])
    df["marcas_kross_flag"] = yes_no_to_boolean(df["Kross (Si/No)"])
    
    # Reconstruct a marcas-like string for standard processing if possible, 
    # or manually handle it.
    # Let's manually create marcas_abinbev, marcas_kross, marcas_ccu, marcas_otras.
    # We use classify_marcas if we have a 'marcas' list.
    
    def build_marcas_list(row):
        marcas = []
        if row["marcas_ccu_flag"]: marcas.append("CCU")
        if row["marcas_kross_flag"]: marcas.append("KROSS")
        if pd.notnull(row["marcas_texto_libre"]) and str(row["marcas_texto_libre"]).strip() != "":
            marcas.append(str(row["marcas_texto_libre"]))
        return ", ".join(marcas)

    df["marcas"] = df.apply(build_marcas_list, axis=1)
    
    # Standard brand processing
    df = process_marcas(df)
    df = classify_marcas(df)

    # 5. Value Transformations
    df["permite_censo"] = yes_no_to_boolean(df["permite_censo"])
    df["hay_competencia_en_salida"] = yes_no_to_boolean(df["hay_competencia_en_salida"])
    if "tiene_schoperas" in df.columns:
        df["tiene_schoperas"] = yes_no_to_boolean(df["tiene_schoperas"])
    
    # 6. Action transformations
    df["instalo"] = yes_no_to_boolean(df["instalo"]).astype("Int64")
    df["disponibilizo"] = pd.to_numeric(df["disponibilizo"], errors="coerce").astype("Int64")

    # 7. Text and Region Cleaning
    df = clean_text(df, ["nombre_fantasia", "direccion", "razon_social"], title=True)
    df = clean_region(df)
    
    if "marca_instalada_en_salida" in df.columns:
        df["marca_instalada_en_salida"] = correct_brand_names(df["marca_instalada_en_salida"])
        df["marca_instalada_en_salida"] = df["marca_instalada_en_salida"].str.title()

    # 8. Numeric Conversions
    numeric_cols = ["salidas", "schoperas_total", "schoperas_ccu"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype("Int64")

    # 9. Final Column Selection
    selected_columns = [
        "cliente_id",
        "razon_social",
        "nombre_fantasia",
        "rut",
        "direccion",
        "region",
        "comuna",
        "periodo",
        "fecha",
        "permite_censo",
        "motivo_no_censo",
        "agencia",
        "schoperas_total",
        "schoperas_ccu",
        "salidas",
        "coolers", # Included as requested
        "instalo",
        "disponibilizo",
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras",
        "marcas_abinbev_listado",
        "marcas_kross_listado",
        "marcas_ccu_listado",
        "marcas_otras_listado",
        "hay_competencia_en_salida",
        "marca_instalada_en_salida"
    ]
    
    return df[selected_columns]
