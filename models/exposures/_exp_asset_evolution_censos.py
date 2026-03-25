from models.exposures._exp_censos import exp_censos

def exp_asset_evolution_censos():
    """
    Evolution of censo assets per cliente_id ordered by fecha descending.
    Computes period-over-period differences for schoperas_total, schoperas_ccu, and salidas.
    Equivalent to SQL:
        PARTITION BY cliente_id ORDER BY fecha DESC
        col - LEAD(col) OVER (PARTITION BY cliente_id ORDER BY fecha DESC)
    """
    df = exp_censos()

    # Sort descending by fecha within each cliente_id
    df = df.sort_values(by=["cliente_id", "fecha"], ascending=[True, False])

    # Window function: LEAD(schoperas_ccu) partitioned by cliente_id, ordered by fecha DESC
    # i.e. the next row in the sorted order = the row with the older fecha
    for col in ["schoperas_total", "schoperas_ccu", "schoperas_competencia", "salidas"]:
        df[f"{col}_prev"] = df.groupby("cliente_id")[col].shift(-1)
        df[f"{col}_diff"] = df[col] - df[f"{col}_prev"]
        df = df.drop(columns=[f"{col}_prev"])

    selected_columns = [
        "cliente_id",
        "periodo",
        "fecha",
        "schoperas_total",
        "schoperas_total_diff",
        "schoperas_ccu",
        "schoperas_ccu_diff",
        "schoperas_competencia",
        "schoperas_competencia_diff",
        "salidas",
        "salidas_diff",
    ]

    return df[selected_columns]