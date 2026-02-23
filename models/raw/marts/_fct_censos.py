import pandas as pd

from models.raw.intermediate._int_censos_censo_2 import int_censos_censo_2

from models.raw.intermediate._int_base_norm_censo_1 import int_base_norm_original_censo_2024


def fct_censos():
    """
    Combines Censo 1 and Censo 2 data into a single fact table.
    Standardizes columns across both datasets to ensure a consistent schema.
    """
    # 1. Load intermediate models
    df_censo_2024 = int_base_norm_original_censo_2024()
    df_censo_2025 = int_censos_censo_2()


    # 5. Union and Final Processing
    df = pd.concat([df_censo_2024, df_censo_2025], ignore_index=True)

    return df