from models.staging.base_normalizada._stg_base_norm_locales import stg_base_norm_locales
from models.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1_locales

from utilities.transformations.text_cleaning import clean_text


def int_base_norm_locales():
    base_norm_locales_df = stg_base_norm_locales()

    # data types
    base_norm_locales_df["local_id"] = base_norm_locales_df["local_id"].astype(str)


    # clean and titleize
    title_cols = ["razon_social", "direccion", "region", "ciudad", "nombre_fantasia"]
    base_norm_locales_df = clean_text(base_norm_locales_df, title_cols, title=True)
    base_norm_locales_df = clean_text(base_norm_locales_df, ["rut"], title=False)


    return base_norm_locales_df  

    










    