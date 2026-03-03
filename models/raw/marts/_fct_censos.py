import pandas as pd

from models.raw.intermediate._int_censos_censo_2025_2 import int_censos_censo_2025_2
from models.raw.intermediate._int_censos_censo_2026_1 import int_censos_censo_2026_1

from models.raw.intermediate._int_base_norm_censo_2024_2 import int_base_norm_original_censo_2024


def fct_censos():
    """
    Combines Censo 1 and Censo 2 data into a single fact table.
    Standardizes columns across both datasets to ensure a consistent schema.
    """
    # 1. Load intermediate models
    df_censo_2024_2 = int_base_norm_original_censo_2024()
    df_censo_2025_2 = int_censos_censo_2025_2()
    df_censo_2026_1 = int_censos_censo_2026_1()

    selected_columns = [
        "local_id",
        "periodo",
        "fecha",
        "schoperas",
        "salidas",
        "instalo",
        "disponibilizo",
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras"
        # # quizas mas adelante agregar
        # "tiene_schoperas",
        # "observaciones",
        # "visitador",
        # "rut_visitador"
    ]

    # 5. Union and Final Processing
    df = pd.concat([df_censo_2024_2, df_censo_2025_2, df_censo_2026_1], ignore_index=True)

    df = df[selected_columns]

    return df