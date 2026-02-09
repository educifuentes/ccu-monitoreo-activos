import pandas as pd

def calculate_general_metrics(bi_activos_df, bi_censos_2025_df, bi_contratos_df, bi_locales_df):
    """
    Calculates general KPIs for the dashboard based on active assets, 
    census classification, and contracts.
    """
    clasificacion_counts = bi_censos_2025_df['clasificacion'].value_counts()
    
    metrics = {
        "en_regla": clasificacion_counts.get("En regla", 0),
        "no_en_regla": clasificacion_counts.get("No en regla", 0),
        "sin_comodato": clasificacion_counts.get("Sin comodato o terminado", 0),
        "no_aplica": clasificacion_counts.get("No aplica", 0),
        "total_locales": bi_locales_df['local_id'].nunique(),
        "total_contratos_vigentes": bi_contratos_df['contrato_vigente'].sum()
    }
    
    return metrics
