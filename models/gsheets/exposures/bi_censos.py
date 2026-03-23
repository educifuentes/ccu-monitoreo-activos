import pandas as pd

from models.gsheets.staging.gsheets_tables import censos
from models.gsheets.exposures.bi_locales import bi_locales

from models.raw.marts.metrics.clasification_censo import clasify_censo

def bi_censos():
    """
    Uses the classification logic defined in models.raw.marts.metrics.clasification_censo.
    """
    # 1. Data Loading and Integration
    df = censos()
    
    # 2. Classification Logic (Moved to metrics layer)
    df = clasify_censo(df)

    # add region column
    df = df.merge(bi_locales(), on='local_id', how='left')

    return df
