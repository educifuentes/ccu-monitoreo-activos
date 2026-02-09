import pandas as pd

from models.marts.gsheets.gsheets_tables import censos

from models.marts.metrics.clasification_censo import clasify_censo

def bi_censos():
    """
    Uses the classification logic defined in models.marts.metrics.clasification_censo.
    """
    # 1. Data Loading and Integration
    df = censos()
    
    # 2. Classification Logic (Moved to metrics layer)
    df = clasify_censo(df)

    return df
