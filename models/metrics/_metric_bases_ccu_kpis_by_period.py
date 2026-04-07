from models.marts._fct_bases_ccu import fct_bases_ccu


def metrics_bases_ccu_kpis_by_period():
    """
    Calcula los KPIs de bases CCU por periodo:
    """
    df = fct_bases_ccu()

    # --- Pre-calculate boolean flags ---
    df["es_local_imagen"] = df["es_local_imagen"].fillna(False).astype(bool)

    # --- Aggregate by period ---
    agg_df = (
        df.groupby("periodo")
        .agg(
            clientes=("cliente_id", "count"),
            clientes_local_imagen=("es_local_imagen", "sum"),
        )
        .reset_index()
    )

    # --- Calculate new clients vs previous period ---
    # Sort periods; periods are strings like "2026-Q1", "2025-Q4", etc.
    # We sort descending so that for each period we can look up its predecessor.
    all_periods = sorted(df["periodo"].unique(), reverse=True)

    def get_previous_period_clients(current_period):
        """
        Returns the set of cliente_ids from the most recent period
        that is strictly earlier than current_period.
        """
        # Periods after sorting descending: [2026-Q1, 2025-Q4, 2025-Q3, ...]
        # Find the first period in the sorted list that is less than current_period
        for p in all_periods:
            if p < current_period:
                return set(df.loc[df["periodo"] == p, "cliente_id"])
        return set()

    def count_new_clients(current_period):
        current_ids = set(df.loc[df["periodo"] == current_period, "cliente_id"])
        previous_ids = get_previous_period_clients(current_period)
        if not previous_ids:
            # No prior period — all clients are considered new
            return len(current_ids)
        return len(current_ids - previous_ids)

    agg_df["clientes_nuevos"] = agg_df["periodo"].apply(count_new_clients)

    # --- Sort descending by period ---
    agg_df.sort_values(by="periodo", ascending=False, inplace=True)

    # --- Human-friendly names ---
    agg_df = agg_df.rename(
        columns={
            "periodo": "periodo",
            "clientes": "N Clientes",
            "clientes_local_imagen": "N Clientes Local Imagen",
            "clientes_nuevos": "N Clientes Nuevos",
        }
    )

    # --- Format display columns ---
    for col in agg_df.columns:
        if col.startswith("N "):
            agg_df[col] = agg_df[col].fillna(0).apply(lambda x: f"{int(x):,}".replace(",", "."))

    return agg_df
