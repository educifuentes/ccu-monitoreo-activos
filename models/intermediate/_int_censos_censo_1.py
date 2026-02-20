from models.staging.censos._stg_censos_censo_1 import stg_censos_censo_1
from models.staging.base_normalizada._stg_base_norm_censo_1 import stg_base_norm_censo_1

from utilities.transformations.yes_no_to_boolean import yes_no_to_boolean
import pandas as pd

def int_censos_censo_1():
    stg_censos_1_df = stg_censos_censo_1()

    rename_dict = {
        "SbjNum": "local_id",
        "NOMBRE LOCAL": "nombre_local",
        "REGIÓN:": "region",
        "COMUNA": "comuna",
        "DIRECCIÓN": "direccion",
        "TIPO DE LOCAL:": "tipo_de_local",
        "¿EL LOCAL SE ENCUENTRA...?": "estado_local",
        "COMENTARIO": "observaciones",
        "Srvyr": "visitador",
        "NÚMERO TOTAL DE MÁQUINAS SCHOPERAS EN EL LOCAL": "total_schoperas",
        "NÚMERO DE MÁQUINAS SCHOPERAS DE CCU\n(ASUMIR QUE LA SCHOPERA ES CCU SI LA MAYORÍA DE LAS MARCAS SON CCU - REVISAR TARJETERO DE APOYO)": "schoperas_ccu",
    }

    # rename columns
    int_censos_censo_1_df = stg_censos_1_df.rename(columns=rename_dict)

    # new columns
    int_censos_censo_1_df["periodo"] = "2024-S2"
    int_censos_censo_1_df["fecha"] = pd.to_datetime("2024-10-01")

    # Transform boolean-like columns
    # In Censo 1 we don't have a direct "tiene_schoperas" Yes/No question for the whole local
    # but we can derive it from total_schoperas or use other questions if they fit the pattern.
    
    # We can use the cooler questions as examples of yes_no_to_boolean
    int_censos_censo_1_df = yes_no_to_boolean(int_censos_censo_1_df, 'INSPECCIÓN VISUAL PARA VER Y REGISTRAR SI EXISTEN COOLERS O REFRIGERADORES VERTICALES (CON VIDRIO) PARA ENFRIAR CERVEZAS.\n(EN CASO QUE LOS COOLERS NO SE ENCUENTREN VISIBLES DEBERÁ PEDIR PERMISO AL DEPENDIENTE/ADMINISTRADOR/PROPIETARIO PARA OBSERVARLOS Y FOTOGRAFIARLOS)\n\n¿HAY COOLERS O REFRIGERADORES VERTICALES (CON VIDRIO) PARA ENFRIAR CERVEZAS?')
    
    # Create "tiene_schoperas" based on total_schoperas
    int_censos_censo_1_df["tiene_schoperas"] = int_censos_censo_1_df["total_schoperas"] > 0
    
    # Add period
    int_censos_censo_1_df["periodo"] = "2024-S2" # Assuming this is the previous period

    # Calculate total outputs (salidas) by summing machines 1 to 12
    int_censos_censo_1_df["salidas_total"] = 0
    for i in range(1, 13):
        col_name = f"NÚMERO DE SALIDAS TOTALES DE SCHOPERAS\nMÁQUINA SCHOPERA {i}:"
        col_name_alt = f"NÚMERO DE SALIDAS TOTALES DE SCHOPERAS \nMÁQUINA SCHOPERA {i}:"
        
        if col_name in int_censos_censo_1_df.columns:
            int_censos_censo_1_df["salidas_total"] += pd.to_numeric(int_censos_censo_1_df[col_name], errors='coerce').fillna(0)
        elif col_name_alt in int_censos_censo_1_df.columns:
            int_censos_censo_1_df["salidas_total"] += pd.to_numeric(int_censos_censo_1_df[col_name_alt], errors='coerce').fillna(0)

    selected_columns = [
        "local_id",
        "periodo",
        "fecha",
        # "estado_local",
        # "observaciones",
        # "tiene_schoperas",
        "schoperas_ccu",
        "total_schoperas",
        "salidas_total"
    ]
    
    # Ensure all selected columns exist (some might have been dropped if empty)
    available_columns = [col for col in selected_columns if col in int_censos_censo_1_df.columns]
    
    return int_censos_censo_1_df[available_columns]

