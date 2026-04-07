import pandas as pd

from helpers.utilities.load_gsheets import load_gsheets_worksheet

def fct_bases_ccu_gsheets():
    """Return DataFrame for bases_ccu worksheet."""
    df = load_gsheets_worksheet("bases_ccu")

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
        # metadata
        "row_index"
    ]

    df = df[selected_columns]
    
    # Cast cliente_id and periodo to str to avoid TypeError on sorting
    df["cliente_id"] = df["cliente_id"].astype(str).str.replace(r'\.0$', '', regex=True).replace("nan", pd.NA)
    df["periodo"] = df["periodo"].astype(str)

    # Cast fecha to date only (not datetime)
    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"], errors='coerce').dt.date

    # Cast asset counts to Int64
    numeric_cols = ["schoperas_ccu", "salidas", "coolers"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

    return df
