import pandas as pd
from models.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.intermediate._int_base_norm_censo_1 import int_base_norm_censo_1
from models.staging._stg_reportes_ccu_base_2024_q1 import stg_reportes_ccu_base_2024_q1
from models.staging._stg_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1


# unir data de censo 1 y de censo 2

def fct_activos():

    # censos
    int_censos_1_df = int_base_norm_censo_1()
    int_censos_2_df = int_censos_censo_2()
    # reportes ccu
    stg_reportes_ccu_base_2024_q1_df = stg_reportes_ccu_base_2024_q1()
    stg_reportes_ccu_base_2026_q1_df = stg_reportes_ccu_base_2026_q1()


    # rename
    # int_censos_1_df.rename(columns={"N° Columnas (Schoperas)": "schoperas_ccu"}, inplace=True)
    # int_censos_1_df.rename(columns={"N° Salidas Schop CCU": "salidas_ccu"}, inplace=True)

    # new column
    int_censos_1_df["fuente"] = "Censo"
    int_censos_2_df["fuente"] = "Censo"
    stg_reportes_ccu_base_2024_q1_df["fuente"] = "CCU"
    stg_reportes_ccu_base_2026_q1_df["fuente"] = "CCU"
    
    

    selected_columns = [
        # row level identifiers
        "local_id",
        "periodo",
        "fecha",    
        # activos cantidades
        "schoperas_ccu",
        "salidas_ccu",
        "coolers"
    ]

    int_censos_1_df = int_censos_1_df[selected_columns]
    int_censos_2_df = int_censos_2_df[selected_columns]

    union_df = pd.concat([int_censos_1_df, int_censos_2_df], ignore_index=True)



    return union_df