import pandas as pd
import numpy as np
import math

from models.marts._fct_censos import fct_censos
from models.marts._dim_locales import dim_locales

def bi_censo_locales():
    """
    Calculates the BI model for censos by integrating fact and dimension data.
    
    Business Rules:
    - Applicability: The rule applies if 'salidas' > 3.
    - Target: 1 outlet for competition for every 4 CCU outlets (floor(salidas / 4)).
    - Compliance: (instalo + disponibilizo) >= Target.
    """
    # 1. Data Loading and Integration
    df_facts = fct_censos()
    df_dim = dim_locales()
    
    # Merge on local_id (inner join to ensure we have both facts and locale info)
    df = pd.merge(df_facts, df_dim, on="local_id", how="inner")

    # 2. Critical Column Pre-processing
    # Ensure numeric types and handle NaNs for calculation columns
    calc_cols = ['salidas', 'instalo', 'disponibilizo']
    for col in calc_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0

    # 3. Rule Applicability
    # The regulation applies only to locals with more than 3 CCU outlets
    df['aplica_regla'] = df['salidas'] > 3

    # 4. Target Calculation (Cuota)
    # Target is floor(salidas / 4) for applicable rows, otherwise 0
    df['salidas_objetivo'] = 0.0
    mask_applies = df['aplica_regla']
    df.loc[mask_applies, 'salidas_objetivo'] = (df.loc[mask_applies, 'salidas'] / 4).apply(math.floor)

    # 5. Competition Results and Compliance
    # Real outlets dedicated to competition
    df["salidas_competencia"] = df["instalo"] + df["disponibilizo"]

    # Compliance flag for applicable locals
    df['cumple_cuota'] = False
    df.loc[mask_applies, 'cumple_cuota'] = df.loc[mask_applies, 'salidas_competencia'] >= df.loc[mask_applies, 'salidas_objetivo']

    # 6. Final Classification
    # Use vectorized selection for performance and clarity
    conditions = [
        (~df['aplica_regla']),                                      # Case 1: Regulation doesn't apply
        (df['aplica_regla'] & df['cumple_cuota']),                  # Case 2: Applies and complies
        (df['aplica_regla'] & ~df['cumple_cuota'])                  # Case 3: Applies and fails
    ]
    choices = [
        "No aplica",
        "En regla",
        "No en regla"
    ]
    df['clasificacion'] = np.select(conditions, choices, default="Sin datos")

    return df
