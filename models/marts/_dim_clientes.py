import pandas as pd

from models.staging.bases_manuales._stg_bases_manuales__clientes_ghsheets_2026_03 import stg_bases_manuales__clientes_ghsheets_2026_03

    

def dim_clientes():

    df = stg_bases_manuales__clientes_ghsheets_2026_03()

    df.rename(columns={
        "local_id": "cliente_id"
    }, inplace=True)


    # DATA TYPES
    df["cliente_id"] = df["cliente_id"].replace("nan", pd.NA)

    selected_columns = ["cliente_id",
                        "razon_social",
                        "rut",
                        "direccion",
                        "region",
                        "ciudad",
                        "comuna",
                        "nombre_fantasia"]
    df = df[selected_columns]

    return df
