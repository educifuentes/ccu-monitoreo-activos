from models.marts.gsheets._fct_bases_ccu_gsheets import fct_bases_ccu_gsheets

def exp_asset_evolution_bases_ccu():
    """
    Evolution of Bases CCU assets per cliente_id ordered by fecha descending.
    Computes period-over-period differences for schoperas_ccu, salidas, and coolers.
    """
    df = fct_bases_ccu_gsheets()


    # Sort descending by fecha within each cliente_id
    df = df.sort_values(by=["cliente_id", "fecha"], ascending=[True, False])

    # Window function: LEAD(col) partitioned by cliente_id, ordered by fecha DESC
    # i.e. the next row in the sorted order = the row with the older fecha
    for col in ["schoperas_ccu", "salidas", "coolers"]:
        # We fillna(0) for calculations to avoid NaN results
        # but keep it in mind if the original column has NaNs.
        df[col] = df[col].fillna(0)
        df[f"{col}_prev"] = df.groupby("cliente_id")[col].shift(-1)
        df[f"{col}_diff"] = df[col] - df[f"{col}_prev"].fillna(0)
        df = df.drop(columns=[f"{col}_prev"])

    selected_columns = [
        "cliente_id",
        "periodo",
        "fecha",
        "schoperas_ccu",
        "schoperas_ccu_diff",
        "salidas",
        "salidas_diff",
        "coolers",
        "coolers_diff",
        "razon_social",
        "nombre_fantasia",
    ]

    return df[selected_columns]
