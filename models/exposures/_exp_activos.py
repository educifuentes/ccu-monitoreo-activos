import pandas as pd

from models.marts._fct_censos import fct_censos
from models.marts._fct_bases_ccu import fct_bases_ccu

# unir data de censo 1 y de censo 2

def exp_activos():
    """
    Unir data de conteo de activos de censos con data reportes ccu.
    """

    # # cliente version
    fct_censos_df = fct_censos()
    fct_bases_ccu_df = fct_bases_ccu()



    # new column
    fct_censos_df["fuente"] = "Censo"
    fct_bases_ccu_df["fuente"] = "CCU"
    
    

    selected_columns = [
        # row level identifiers
        "cliente_id",
        "periodo",
        "fecha",    
        "fuente",
        # activos cantidades
        "schoperas",
        "salidas",
        "coolers",
        # clientes info
    ]

    union_df = pd.concat([fct_censos_df, fct_bases_ccu_df], ignore_index=True)



    return union_df[selected_columns]