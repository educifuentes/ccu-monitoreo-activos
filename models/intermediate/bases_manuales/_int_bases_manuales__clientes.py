from models.staging.bases_manuales._stg_bases_manuales__clientes import stg_bases_manuales__clientes
from models.intermediate.bases_ccu._int_bases_ccu__base_2026_q1 import int_bases_ccu__base_2026_q1_locales

from utilities.transformations.text_cleaning import clean_text


def int_bases_manuales__clientes():
    base_norm_clientes_df = stg_bases_manuales__clientes()

    # data types
    base_norm_clientes_df["cliente_id"] = base_norm_clientes_df["cliente_id"].astype(str)


    # clean and titleize
    title_cols = ["razon_social", "direccion", "region", "ciudad", "nombre_fantasia"]
    base_norm_clientes_df = clean_text(base_norm_clientes_df, title_cols, title=True)
    base_norm_clientes_df = clean_text(base_norm_clientes_df, ["rut"], title=False)


    return base_norm_clientes_df  

    










    