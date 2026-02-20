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
        "total_contratos_imagen": bi_contratos_df['local_id'].nunique()
    }
    
    
    return metrics

def get_latest_classification(local_id, bi_censos_df):
    """
    Retrieves the latest business classification for a specific local_id based on census data.
    """
    local_bi_censos = bi_censos_df[bi_censos_df['local_id'] == local_id].sort_values('periodo', ascending=False)
    
    if local_bi_censos.empty:
        return "Sin Datos"
        
    return local_bi_censos.iloc[0]['clasificacion']
