import pandas as pd

from models.marts._fct_censos import fct_censos
from models.marts.marts._dim_locales import exp_locales

from models.marts.metrics.clasification_censo import clasify_censo

def exp_censos():
    """
    Uses the classification logic defined in models.marts.metrics.clasification_censo.
    """
    # 1. Data Loading and Integration
    df = fct_censos()
    
    # 2. Classification Logic (Moved to metrics layer)
    df = clasify_censo(df)

    # add region column
    df = df.merge(exp_locales(), on='local_id', how='left')

    return df
