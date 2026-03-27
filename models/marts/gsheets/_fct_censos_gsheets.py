import pandas as pd

from helpers.utilities.load_gsheets import load_gsheets_worksheet

def fct_censos_gsheets():
    """Return DataFrame for censos worksheet."""
    df = load_gsheets_worksheet("censos")

    selected_columns = [
        # keys
        "cliente_id",
        "periodo",
        "fecha",
        # clientes info
        "razon_social",
        "direccion",
        "rut",
        "region",
        "comuna",
        "nombre_fantasia",
        # censo metadata
        "agencia",
        "permite_censo",
        "motivo_no_censo",
        # activos
        "schoperas_total",
        "schoperas_ccu",
        "salidas",
        "tiene_coolers",
        # accion
        "instalo",
        "disponibilizo",
        # marcas
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras",
        # listados
        "marcas",
        "marcas_otras_listado",
        # competencia
        "hay_competencia_en_salida",
        "marca_instalada_en_salida",
    ]

    df = df[selected_columns]
    
    # Cast cliente_id and periodo to str to avoid TypeError on sorting
    df["cliente_id"] = df["cliente_id"].astype(str)
    df["periodo"] = df["periodo"].astype(str)
    
    # Cast asset counts to Int64
    numeric_cols = ["schoperas_total", "schoperas_ccu", "salidas", "instalo", "disponibilizo"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

    df.sort_values(by=["periodo"], ascending=False, inplace=True)

    return df
