import pandas as pd
from models.staging._stg_censos_censo_2 import stg_censos_censo_2
from utilities.data_transformations import yes_no_to_boolean
from utilities.transformations.process_marcas import process_marcas

def int_censos_censo_2():
    stg_censos_2_df = stg_censos_censo_2()

    rename_dict = {
        "ID PK": "id_pk",
        "ID CCU": "local_id",
        "tipo_de_local": "tipo_de_local",
        "Visitador": "visitador",
        "rut Visitador": "rut_visitador",
        "Observaciones": "observaciones",
        "EL LOCAL CUENTA CON MAQUINAS SHOPERAS?": "tiene_schoperas",
        "NÚMERO DE MÁQUINAS SCHOPERAS DE CCU(ASUMIR QUE LA SCHOPERA ES CCU SI LA MAYORÍA DE LAS MARCAS SON CCU - REVISAR TARJETERO DE APOYO)": "schoperas_ccu",
        "CUANTAS SHOPERAS PARA DISPONIBILIZAR NUEVAS INSTALO CCU ?": "instalo",
        'CUANTAS SALIDAS DEJO LIBRE CCU EN TOTAL? s ': "disponibilizo",
        '¿CUALES DE ESTAS MARCAS SE VENDEN EN SCHOP?': "marcas"
    }

    # rename columns
    int_censos_censo_2_df = stg_censos_2_df.rename(columns=rename_dict)

    # data types        
    int_censos_censo_2_df["local_id"] = int_censos_censo_2_df["local_id"].astype("str")

    # Apply brand processing
    if "marcas" in int_censos_censo_2_df.columns:
        int_censos_censo_2_df["marcas"] = int_censos_censo_2_df["marcas"].apply(process_marcas)

    # transfortm re parsing
    int_censos_censo_2_df = yes_no_to_boolean(int_censos_censo_2_df, "tiene_schoperas")
    

    # new columns
    int_censos_censo_2_df["periodo"] = "2025-S2"
    int_censos_censo_2_df["fecha"] = pd.to_datetime("2025-10-01")
    
    # Calculate total outputs (salidas_ccu) by summing machines
    int_censos_censo_2_df["salidas_ccu"] = 0
    for i in range(1, 7): # check 1 to 6
        col_name = f"SCHOPERA CCU {i} - NÚMERO DE SALIDAS"
        if col_name in stg_censos_2_df.columns:
            int_censos_censo_2_df["salidas_ccu"] += pd.to_numeric(stg_censos_2_df[col_name], errors='coerce').fillna(0)
    

    selected_columns = [
        "local_id",
        "periodo",
        "fecha",
        # "tipo_de_local",
        # "visitador",
        # "rut_visitador",
        # "observaciones",
        # "tiene_schoperas",
        "schoperas_ccu",
        "salidas_ccu",
        "instalo",
        "disponibilizo",
        "marcas"
    ]
    
    return int_censos_censo_2_df[selected_columns]

if __name__ == "__main__":
    print(int_censos_censo_2().head())
