import pandas as pd

from models.raw.intermediate._int_reportes_ccu_base_2024_q1 import int_reportes_ccu_base_2024_q1
from models.raw.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1


def fct_bases_ccu():
    # dfs inputs by period
    int_reportes_ccu_base_2024_q1_df = int_reportes_ccu_base_2024_q1()
    int_reportes_ccu_base_2026_q1_df = int_reportes_ccu_base_2026_q1()

    select_columns_base_2026 = [
        "local_id",
        "periodo",
        "fecha",
        # activos
        "schoperas",
        "salidas",
        "coolers",
        # fechas
        "fecha_suscripcion_comodato",
        "fecha_termino_contrato",
        "activos_entregados"
    ]



    int_reportes_ccu_base_2026_q1_df = int_reportes_ccu_base_2026_q1_df[select_columns_base_2026]

    df = pd.concat([int_reportes_ccu_base_2024_q1_df, int_reportes_ccu_base_2026_q1_df], ignore_index=True)   

    df.sort_values(by=["local_id", "periodo"], ascending=[True, True], inplace=True)



    return df