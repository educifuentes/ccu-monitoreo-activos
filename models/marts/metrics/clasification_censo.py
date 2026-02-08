import pandas as pd
import numpy as np
import math

def clasify_censo(df):
    """
    Applies censo classification business rules to the provided DataFrame.
    
    Business Rules:
    - Applicability: The rule applies if 'salidas' > 3.
    - Target: 1 outlet for competition for every 4 CCU outlets (floor(salidas / 4)).
    - Compliance: (instalo + disponibilizo) >= Target.
    """
    
    # 1. Critical Column Pre-processing
    # Ensure numeric types and handle NaNs for calculation columns
    calc_cols = ['salidas', 'instalo', 'disponibilizo']
    for col in calc_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0

    # 2. Rule Applicability
    # The regulation applies only to locals with more than 3 CCU outlets
    df['aplica_regla'] = df['salidas'] > 3

    # 3. Target Calculation (Cuota)
    # Target is floor(salidas / 4) for applicable rows, otherwise 0
    df['salidas_objetivo'] = 0.0
    mask_applies = df['aplica_regla']
    df.loc[mask_applies, 'salidas_objetivo'] = (df.loc[mask_applies, 'salidas'] / 4).apply(math.floor)

    # 4. Competition Results and Compliance
    # Real outlets dedicated to competition
    df["salidas_competencia"] = df["instalo"] + df["disponibilizo"]

    # Compliance flag for applicable locals
    df['cumple_cuota'] = False
    df.loc[mask_applies, 'cumple_cuota'] = df.loc[mask_applies, 'salidas_competencia'] >= df.loc[mask_applies, 'salidas_objetivo']

    # 5. Final Classification
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
