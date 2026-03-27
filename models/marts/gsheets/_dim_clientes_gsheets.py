from helpers.utilities.load_gsheets import load_gsheets_worksheet

import pandas as pd

def dim_clientes_gsheets():
    """Return DataFrames for given worksheet names."""

    df = load_gsheets_worksheet("clientes")

    # DATA TYPES
    df["cliente_id"] = df["cliente_id"].astype(str).replace("nan", pd.NA)

    selected_columns = [
                        "cliente_id",
                        "razon_social",
                        "rut",
                        "direccion",
                        "region",
                        "ciudad",
                        "comuna",
                        "nombre_fantasia", "fuente", "row_index"]
    
    df = df[selected_columns]
    
    return df