import pandas as pd

from models.staging.bases_ccu._stg_bases_ccu__base_2026_q1 import stg_bases_ccu__base_2026_q1

from helpers.transformations.yes_no_to_boolean import yes_no_to_boolean
from helpers.transformations.date_parsing import parse_spanish_month_year



def int_reportes_ccu_base_2026_q1():

    df = stg_bases_ccu__base_2026_q1()

    # rename
    rename_dict = {
        "local_id": "cliente_id",
        # local info
        "razon_social": "razon_social",
        "rut": "rut",
        "direccion": "direccion",
        "region": "region",
        "ciudad": "ciudad",
        "comuna": "comuna",
        "nombre_fantasia": "nombre_fantasia",
        # activos
        "numero de schoperas": "schoperas_ccu",
        "numero de salidas": "salidas",
        "numero de coolers": "coolers",
        # contratos
        "¿es local imagen?": "es_local_imagen",
        "Folio": "folio",
        "Fecha de suscripción del comodato": "fecha_suscripcion_comodato",
        "Fecha de término del contrato (de aplicar)": "fecha_termino_contrato",
        # variacion activos
        "Activos entregados": "activos_entregados",
        "Cantidad total de salidas de schop": "cantidad_total_salidas_schop",
        "Modificacion": "modificacion",
        "Mes cambio": "mes_cambio",
    }

    df.rename(columns=rename_dict, inplace=True)

    # data types
    df["cliente_id"] = df["cliente_id"].astype(str)

    df["schoperas_ccu"] = df["schoperas_ccu"].astype("Int64")
    df["salidas"] = df["salidas"].astype("Int64")
    df["coolers"] = df["coolers"].astype("Int64")

    df["es_local_imagen"] = yes_no_to_boolean(df["es_local_imagen"])

    df["modificacion"] = df["modificacion"].astype("category")

    df["fecha_suscripcion_comodato"] = parse_spanish_month_year(df["fecha_suscripcion_comodato"])
    df["fecha_termino_contrato"] = parse_spanish_month_year(df["fecha_termino_contrato"])
    df["mes_cambio"] = parse_spanish_month_year(df["mes_cambio"])



    selected_columns = [
        # keys
        "cliente_id",
        # cliente info
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
        "es_local_imagen",
        "folio",
        "fecha_suscripcion_comodato",
        "fecha_termino_contrato",
        # variacion activos
        "activos_entregados",
        "cantidad_total_salidas_schop",
        "modificacion",
        "mes_cambio"
    ]

    return df[selected_columns]