import pandas as pd

# from models.intermediate.bases_ccu._int_bases_ccu__base_2024_q1 import int_reportes_ccu_base_2024_q1
from models.intermediate.bases_ccu._int_bases_ccu__base_2026_q1 import int_reportes_ccu_base_2026_q1


def fct_bases_ccu():
   # inputs
   # int_reportes_ccu_base_2024_q1_df = int_reportes_ccu_base_2024_q1()
    df_ccu_2026_1 = int_reportes_ccu_base_2026_q1()

    # new columns
    df_ccu_2026_1["periodo"] = "2026-Q1"
    df_ccu_2026_1["fecha"] = df_ccu_2026_1["mes_cambio"]


    selected_columns = [
        # keys
        "cliente_id",
        "periodo",
        "fecha",
        # local info
        "razon_social",
        "rut",
        "direccion",
        "region",
        "ciudad",
        "comuna",
        "nombre_fantasia",
        # activos
        "schoperas_ccu",
        "salidas",
        "coolers",
        # contratos
        "folio",
        "es_local_imagen",
        "fecha_suscripcion_comodato",
        "fecha_termino_contrato",
        # variacion activos
        "activos_entregados",
        "cantidad_total_salidas_schop",
        "modificacion",
        "mes_cambio",
    ]

    df = df_ccu_2026_1[selected_columns]

    # to string type
    df["periodo"] = df["periodo"].astype(str)


    return df