import pandas as pd

from models.marts._fct_censos import fct_censos
from models.marts._fct_bases_ccu import fct_bases_ccu

# unir data de censo 1 y de censo 2

def activos_ccu_y_censos():
    """
    Unir data de conteo de activos de censos con data reportes ccu.
    """

    # # cliente version
    fct_censos_df = fct_censos()
    fct_bases_ccu_df = fct_bases_ccu()

    # new column
    fct_censos_df["fuente"] = "Censo"
    fct_bases_ccu_df["fuente"] = "CCU"
    
    fct_censos_df["schoperas_no_ccu"] = fct_censos_df["schoperas_total"] - fct_censos_df["schoperas_ccu"]
    fct_bases_ccu_df["schoperas_no_ccu"] = fct_bases_ccu_df["schoperas_total"] - fct_bases_ccu_df["schoperas_ccu"]

    # ---

    selected_columns = [
        # keys
        "cliente_id",
        "fuente",
        "periodo",
        "fecha",    
        # activos 
        "schoperas_ccu",
        "schoperas_total",
        "salidas",
        "coolers",
        "schoperas_no_ccu"
    ]

    union_df = pd.concat([fct_censos_df, fct_bases_ccu_df], ignore_index=True)


    return union_df[selected_columns]