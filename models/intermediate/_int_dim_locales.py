# from models.staging._stg_censos_censo_2 import stg_censos_censo_2

from models.staging._stg_base_norm_locales import stg_base_norm_locales
from models.staging._stg_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1


def int_base_norm_locales():
    base_norm_locales_df = stg_base_norm_locales()

    # data types


    # clean and titleize
    base_norm_locales_df["razon_social"] = base_norm_locales_df["razon_social"].str.strip().str.title()
    base_norm_locales_df["rut"] = base_norm_locales_df["rut"].str.strip()
    base_norm_locales_df["direccion"] = base_norm_locales_df["direccion"].str.strip().str.title()
    base_norm_locales_df["region"] = base_norm_locales_df["region"].str.strip().str.title()
    base_norm_locales_df["ciudad"] = base_norm_locales_df["ciudad"].str.strip().str.title()
    base_norm_locales_df["nombre_fantasia"] = base_norm_locales_df["nombre_fantasia"].str.strip().str.title()

    base_norm_locales_df["local_id"] = base_norm_locales_df["local_id"].astype(str)

    return base_norm_locales_df   

def int_reportes_ccu_locales():
    locales_columns = ['local_id', 'razon_social', 'rut', 'direccion', 'region', 'ciudad', 'comuna', 'nombre_fantasia']

    # base_norm_locales_df = stg_base_norm_locales()[locales_columns]
    reportes_ccu_base_2026_q1_df = stg_reportes_ccu_base_2026_q1()[locales_columns]

    reportes_ccu_base_2026_q1_df["local_id"] = reportes_ccu_base_2026_q1_df["local_id"].astype(str)

    return reportes_ccu_base_2026_q1_df


def compare_locales_df():
    # Load dataframes
    base_norm_df = int_base_norm_locales()
    reportes_ccu_df = int_reportes_ccu_locales()
    
    # Inner join on local_id, with _ccu suffix for the right side
    comparison_df = base_norm_df.merge(
        reportes_ccu_df, 
        on="local_id", 
        how="inner", 
        suffixes=("", "_ccu")
    )

    # Reorder columns to see them side-by-side
    ordered_columns = [
        'local_id',
        'razon_social', 'razon_social_ccu',
        'rut', 'rut_ccu',
        'direccion', 'direccion_ccu',
        'nombre_fantasia', 'nombre_fantasia_ccu',
        'region', 'region_ccu',
        'ciudad', 'ciudad_ccu',
        'comuna', 'comuna_ccu'
    ]
    
    # Filter to only existing columns and return
    return comparison_df[[c for c in ordered_columns if c in comparison_df.columns]]






    