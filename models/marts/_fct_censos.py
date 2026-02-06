import pandas as pd
from models.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.intermediate._int_base_norm_censo_1 import int_base_norm_censo_1


# unir data de censo 1 y de censo 2

def fct_censos():
    int_censos_1_df = int_base_norm_censo_1()
    int_censos_2_df = int_censos_censo_2()

    # Align columns before concat
    # Censo 1 missing columns
    int_censos_1_df["instalo"] = None
    int_censos_1_df["disponibilizo"] = None
    

    selected_columns = [
        # censo info
        "local_id",
        "periodo",
        "fecha",    
        # activos cantidades
        "schoperas_ccu",
        "salidas_ccu",
        "instalo",
        "disponibilizo",
        # marcas
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_otras"
    ]

    int_censos_1_df = int_censos_1_df[selected_columns]
    int_censos_2_df = int_censos_2_df[selected_columns]

    union_df = pd.concat([int_censos_1_df, int_censos_2_df], ignore_index=True)



    return union_df