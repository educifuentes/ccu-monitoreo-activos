import pandas as pd

from models.marts._fct_censos import fct_censos
from models.marts._dim_locales import dim_locales
from models.marts.metrics.clasification_censo import clasify_censo

def bi_censos():
    """
    Calculates the BI model for censos by integrating fact and dimension data.
    Uses the classification logic defined in models.marts.metrics.clasification_censo.
    """
    # 1. Data Loading and Integration
    df_facts = fct_censos()
    df_dim = dim_locales()
    
    # Merge on local_id (inner join to ensure we have both facts and locale info)
    df = pd.merge(df_facts, df_dim, on="local_id", how="inner")
    
    # 2. Classification Logic (Moved to metrics layer)
    df = clasify_censo(df)

    return df
