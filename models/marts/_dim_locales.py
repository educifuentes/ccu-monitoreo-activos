import pandas as pd

from models.intermediate._int_base_norm_locales import int_base_norm_locales
from models.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1_locales


def updatate_with_base_ccu_2026_q1():
    """ Actualiza loclaes ocn info de base 2026 Q1 """


    int_reportes_ccu_base_2026_q1_locales_df = int_reportes_ccu_base_2026_q1_locales()


    int_base_norm_locales_df = int_base_norm_locales()

    # rebuild

    df = int_base_norm_locales_df.merge(int_reportes_ccu_base_2026_q1_locales_df, on="local_id", how="left")

    return df
    

def dim_locales():
    """
    Locales con info consolidada de censos y contratos.
    """

    locales_df = int_base_norm_locales()

   
    return locales_df
