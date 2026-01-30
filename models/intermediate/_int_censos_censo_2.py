from models.staging._stg_censos_censo_2 import stg_censos_censo_2
from utilities.data_transformations import yes_no_to_boolean

def int_censos_censo_2():
    stg_censos_2_df = stg_censos_censo_2()

    rename_dict = {
        "ID PK": "local_id",
        "tipo_de_local": "tipo_de_local",
        "Visitador": "visitador",
        "rut Visitador": "rut_visitador",
        "Observaciones": "observaciones",
        "EL LOCAL CUENTA CON MAQUINAS SHOPERAS?": "tiene_schoperas",
        "NÚMERO DE MÁQUINAS SCHOPERAS DE CCU(ASUMIR QUE LA SCHOPERA ES CCU SI LA MAYORÍA DE LAS MARCAS SON CCU - REVISAR TARJETERO DE APOYO)": "schoperas_ccu",
        "CUANTAS SHOPERAS PARA DISPONIBILIZAR NUEVAS INSTALO CCU ?": "instalo",
        'CUANTAS SALIDAS DEJO LIBRE CCU EN TOTAL? s ': "disponibilizo",
    }

    # rename columns
    int_censos_censo_2_df = stg_censos_2_df.rename(columns=rename_dict)

    # transfortm re parsing
    int_censos_censo_2_df = yes_no_to_boolean(int_censos_censo_2_df, "tiene_schoperas")
    

    # new columns
    int_censos_censo_2_df["periodo"] = "2025-S2"
    int_censos_censo_2_df["salidas_ccu"] = stg_censos_2_df["SCHOPERA CCU 1 - NÚMERO DE SALIDAS"] + stg_censos_2_df["SCHOPERA CCU 2 - NÚMERO DE SALIDAS"] + stg_censos_2_df["SCHOPERA CCU 3 - NÚMERO DE SALIDAS"] + stg_censos_2_df["SCHOPERA CCU 4 - NÚMERO DE SALIDAS"] + stg_censos_2_df["SCHOPERA CCU 5 - NÚMERO DE SALIDAS"] + stg_censos_2_df["SCHOPERA CCU 6 - NÚMERO DE SALIDAS"]
    

    selected_columns = [
        "local_id",
        "periodo",
        "tipo_de_local",
        "visitador",
        "rut_visitador",
        "observaciones",
        "tiene_schoperas",
        "schoperas_ccu",
        "instalo",
        "disponibilizo",
        "salidas_ccu"
    ]
    
    return int_censos_censo_2_df[selected_columns]

if __name__ == "__main__":
    print(int_censos_censo_2().head())
