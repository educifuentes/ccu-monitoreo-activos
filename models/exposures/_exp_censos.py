import pandas as pd

from models.marts._fct_censos import fct_censos
from models.exposures._exp_clientes import exp_clientes

from models.marts.metrics.clasification_censo import clasify_censo

def exp_censos():
    """
    censo con dim clientes
    """
    # 1. Data Loading and Integration
    df = fct_censos()
    clientes_df = exp_clientes()

    # Merge; clientes_df is the authoritative source for shared columns
    df = df.merge(clientes_df, on='cliente_id', how='left', suffixes=('_censos', ''))

    # Drop any _censos-suffixed duplicates (fct_censos copies of client columns)
    cols_to_drop = [c for c in df.columns if c.endswith('_censos')]
    df = df.drop(columns=cols_to_drop)

    # 2. Classification Logic (Moved to metrics layer)
    df = clasify_censo(df)

    return df
