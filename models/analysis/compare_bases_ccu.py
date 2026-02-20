import pandas as pd
from models.raw.intermediate._int_base_norm_locales import int_base_norm_locales
from models.raw.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1_locales, int_reportes_ccu_base_2026_q1_activos

def compare_locales_df():
    # Load dataframes
    base_norm_df = int_base_norm_locales()
    reportes_ccu_df = int_reportes_ccu_base_2026_q1_locales()
    int_reportes_ccu_base_2026_q1_activos_df = int_reportes_ccu_base_2026_q1_activos()
    
    # Inner join on local_id, with _ccu suffix for the right side
    comparison_df = base_norm_df.merge(
        reportes_ccu_df, 
        on="local_id", 
        how="inner", 
        suffixes=("", "_ccu")
    )

    # Reorder columns to see them side-by-side
    ordered_columns = [
        'local_id',
        'razon_social', 'razon_social_ccu',
        'rut', 'rut_ccu',
        'direccion', 'direccion_ccu',
        'nombre_fantasia', 'nombre_fantasia_ccu',
        'region', 'region_ccu',
        'ciudad', 'ciudad_ccu',
        'comuna', 'comuna_ccu'
    ]
    
    # Filter to only existing columns and return
    return comparison_df[[c for c in ordered_columns if c in comparison_df.columns]]

def compare_activos_df():
    # Load dataframes
    base_norm_df = int_base_norm_locales()
    int_reportes_ccu_base_2026_q1_activos_df = int_reportes_ccu_base_2026_q1_activos()
    
    # Inner join on local_id, with _ccu suffix for the right side
    comparison_df = base_norm_df.merge(
        int_reportes_ccu_base_2026_q1_activos_df, 
        on="local_id", 
        how="inner", 
        suffixes=("_2024", "_2026")
    )

    # Reorder columns to see them side-by-side
    ordered_columns = [
        'local_id',
        'schoperas_2024', 'schoperas_2026',
        'salidas_2024', 'salidas_2026',
        'coolers_2024', 'coolers_2026'
    ]
    
    # Filter to only existing columns and return
    return comparison_df[[c for c in ordered_columns if c in comparison_df.columns]]
