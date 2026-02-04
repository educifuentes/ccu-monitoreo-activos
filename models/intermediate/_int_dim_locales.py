# from models.staging._stg_censos_censo_2 import stg_censos_censo_2

from models.staging._stg_base_norm_locales import stg_base_norm_locales
from models.staging._src_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1


def int_base_norm_locales():
    base_norm_locales_df = stg_base_norm_locales()

    # clean and titleize
    base_norm_locales_df["razon_social"] = base_norm_locales_df["razon_social"].str.strip().str.title()
    base_norm_locales_df["rut"] = base_norm_locales_df["rut"].str.strip()
    base_norm_locales_df["direccion"] = base_norm_locales_df["direccion"].str.strip().str.title()
    base_norm_locales_df["region"] = base_norm_locales_df["region"].str.strip().str.title()
    base_norm_locales_df["ciudad"] = base_norm_locales_df["ciudad"].str.strip().str.title()
    base_norm_locales_df["nombre_fantasia"] = base_norm_locales_df["nombre_fantasia"].str.strip().str.title()

    return base_norm_locales_df   

def int_reportes_ccu_locales():
    locales_columns = ['local_id', 'razon_social', 'rut', 'direccion', 'region', 'ciudad', 'comuna', 'nombre_fantasia']

    # base_norm_locales_df = stg_base_norm_locales()[locales_columns]
    reportes_ccu_base_2026_q1_df = stg_reportes_ccu_base_2026_q1()[locales_columns]

    return reportes_ccu_base_2026_q1_df






    