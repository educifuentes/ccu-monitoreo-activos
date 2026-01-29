from models.staging._stg_censos_censo_2 import stg_censos_censo_2

def load_locales_from_censo_2():
    stg_censos_2_df = stg_censos_censo_2()

    rename_dict = {
        "ID PK": "local_id",
        "ID CCU": "ccu_id",
        "Dirección": "direccion",
        "Comuna": "comuna",
        "Región": "region",
        "Latitud": "latitud",
        "Longitud": "longitud",
        "NOMBRE LOCAL FANTASIA": "nombre_fantasia",
    }

    stg_censos_2_df.rename(columns=rename_dict, inplace=True)

    selected_columns = [
        "local_id",
        "ccu_id",
        "direccion",
        "comuna",
        "region",
        "latitud",
        "longitud",
        "nombre_fantasia",
    ]

    return stg_censos_2_df[selected_columns]

if __name__ == "__main__":
    print(load_locales_from_censo_2().head())
