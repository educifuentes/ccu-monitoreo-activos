import pandas as pd

from models.exposures._exp_censos import exp_censos
from models.exposures._exp_bases_ccu import exp_bases_ccu

# unir data de censo 1 y de censo 2

def exp_activos_ccu_y_censos():
    """
    Unir data de conteo de activos de censos con data reportes ccu.
    """

    # # cliente version
    censos_df = exp_censos()
    bases_ccu_df = exp_bases_ccu()


    # ajusten coolers en censos
    censos_df["coolers"] = censos_df["tiene_coolers"]
    # Map boolean to int for coolers
    censos_df["coolers"] = censos_df["tiene_coolers"].fillna(False).astype(int)

    # new columns before concat
    censos_df["fuente"] = "Censo"
    bases_ccu_df["fuente"] = "CCU"

    bases_ccu_df["schoperas_competencia"] = None


    
    selected_columns = [
        # keys
        "cliente_id",
        "fuente",
        "periodo",
        "fecha",    
        # activos 
        "schoperas_ccu",
        "schoperas_competencia",
        "salidas",
        "coolers",
    ]

    union_df = pd.concat([censos_df, bases_ccu_df], ignore_index=True)


    return union_df[selected_columns]