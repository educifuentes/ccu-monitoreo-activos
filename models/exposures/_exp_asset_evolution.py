from models.exposures._exp_activos_ccu_y_censos import exp_activos_ccu_y_censos

def exp_asset_evolution():
    """
    Evolution of assets per cliente_id ordered by fecha descending.
    Includes schoperas_ccu and the difference with the following row (previous date).
    Equivalent to SQL: 
        PARTITION BY cliente_id ORDER BY fecha DESC
        schoperas_ccu - LEAD(schoperas_ccu) OVER (PARTITION BY cliente_id ORDER BY fecha DESC)
    """
    df = exp_activos_ccu_y_censos()

    # Sort descending by fecha within each cliente_id
    df = df.sort_values(by=["cliente_id", "fecha"], ascending=[True, False])

    # Window function: LEAD(schoperas_ccu) partitioned by cliente_id, ordered by fecha DESC
    # i.e. the next row in the sorted order = the row with the older fecha
    for col in ["schoperas_ccu", "salidas", "coolers", "schoperas_competencia"]:
        df[f"{col}_prev"] = df.groupby("cliente_id")[col].shift(-1)
        df[f"{col}_diff"] = df[col] - df[f"{col}_prev"]
        df = df.drop(columns=[f"{col}_prev"])

    selected_columns = [
        "cliente_id",
         "fuente",
        "periodo",
        "fecha",
        "schoperas_ccu",
        "schoperas_ccu_diff",
        "schoperas_competencia",
        "schoperas_competencia_diff",
        "salidas",
        "salidas_diff",
        "coolers",
        "coolers_diff",
    ]

    return df[selected_columns]