import pandas as pd

from models.marts._fct_censos import fct_censos
from models.marts._fct_bases_ccu import fct_bases_ccu

from models.gsheets.staging.gsheets_tables import bases_ccu, censos


# unir data de censo 1 y de censo 2

def bi_activos():
    """
    Unir data de conteo de activos de censos con data reportes ccu.
    """

    # # local version
    # fct_censos_df = fct_censos()
    # fct_bases_ccu_df = fct_bases_ccu()

    # gsheets version
    fct_bases_ccu_df = bases_ccu()
    fct_censos_df = censos()


    # new column
    fct_censos_df["fuente"] = "Censo"
    fct_bases_ccu_df["fuente"] = "CCU"
    
    

    selected_columns = [
        # row level identifiers
        "local_id",
        "periodo",
        "fecha",    
        "fuente",
        # activos cantidades
        "schoperas",
        "salidas",
        "coolers",
        # locales info
    ]

    union_df = pd.concat([fct_censos_df, fct_bases_ccu_df], ignore_index=True)



    return union_df[selected_columns]