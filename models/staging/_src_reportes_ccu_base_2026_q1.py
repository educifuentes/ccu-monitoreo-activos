import pandas as pd
import numpy as np

def stg_reportes_ccu_base_2026_q1():
    # Define file path
    file_path = "seeds/reportes_ccu/base_solicitada.xlsx"
    
    # Load CSV
    df = pd.read_excel(file_path)

    # rename
    rename_dict = {
        "id": "local_id",
        "numero de schoperas": "schoperas",
        "numero de salidas": "num_salidas",
        "numero de coolers": "num_coolers",
        "¿es local imagen?": "es_local_imagen",
        "Fecha de suscripción del comodato": "marcas",
        "Fecha de término del contrato (de aplicar)": "fecha_termino_contrato",
        "Activos entregados": "activos_entregados",
        "Cantidad total de salidas de schop": "salidas_totales",
    }

    # df.rename(columns=rename_dict, inplace=True)

    # selected_columns = [
    #     "local_id",
    #     "razon_social",
    #     "rut",
    #     "direccion",
    #     "region",
    #     "ciudad",
    #     "nombre_fantasia" ]

    # 3. Output Information
    # print("--- DataFrame Head ---")
    # print(df.iloc[:, :5].head())

    print("\n--- List of Column Names ---")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")

    # df = df[selected_columns]
        
    return df