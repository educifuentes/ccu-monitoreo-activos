# from models.staging._stg_censos_censo_2 import stg_censos_censo_2

from models.staging._stg_base_norm_locales import stg_base_norm_locales


def dim_locales():
    locales_df = stg_base_norm_locales()

    # clean and titleize
    locales_df["razon_social"] = locales_df["razon_social"].str.strip().str.title()
    locales_df["rut"] = locales_df["rut"].str.strip()
    locales_df["direccion"] = locales_df["direccion"].str.strip().str.title()
    locales_df["region"] = locales_df["region"].str.strip().str.title()
    locales_df["ciudad"] = locales_df["ciudad"].str.strip().str.title()
    locales_df["nombre_fantasia"] = locales_df["nombre_fantasia"].str.strip().str.title()

    return locales_df
