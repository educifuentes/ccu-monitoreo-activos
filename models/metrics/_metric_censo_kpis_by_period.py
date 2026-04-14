from models.exposures._exp_censos import exp_censos

def metrics_censo_kpis_by_period():
    """
    Calcula los kpis de censo por periodo
    """
    df = exp_censos()

    # Pre-calculate boolean flags
    df["hay_competencia"] = df["hay_competencia_en_salida"].fillna(False).astype(bool)
    df["instalo_gt_0"] = (df["instalo"] > 0).fillna(False)
    df["disponibilizo_gt_0"] = (df["disponibilizo"] > 0).fillna(False)
    df["sin_activos"] = (df["schoperas_ccu"].fillna(0) == 0)

    cols_to_agg = [
        "marcas_abinbev",
        "marcas_kross",
        "marcas_otras",
        "hay_competencia",
        "instalo_gt_0",
        "disponibilizo_gt_0",
        "permite_censo",
        "sin_activos"
    ]

    # Grouping and Aggregation
    agg_dict = {"cliente_id": "count"}
    for col in cols_to_agg:
        agg_dict[col] = ["sum", "mean"]

    metrics_df = df.groupby("periodo").agg(agg_dict)

    # Flatten multi-index columns
    metrics_df.columns = [f"{col}_{stat}" for col, stat in metrics_df.columns]

    # Human friendly names
    name_mapping = {
        "cliente_id_count": "N Clientes",
        "sin_activos_sum": "N Clientes Sin Activos",
        "sin_activos_mean": "% Clientes Sin Activos",
        "permite_censo_sum": "N Permite censos",
        "permite_censo_mean": "% Permite censos",
        "marcas_abinbev_sum": "N con AbInbev",
        "marcas_abinbev_mean": "% con AbInbev",
        "marcas_kross_sum": "N con Kross",
        "marcas_kross_mean": "% con Kross",
        "marcas_otras_sum": "N con Otras Marcas",
        "marcas_otras_mean": "% con Otras Marcas",
        "hay_competencia_sum": "N con Comp. en Salida",
        "hay_competencia_mean": "% con Comp. en Salida",
        "instalo_gt_0_sum": "N que Instalaron",
        "instalo_gt_0_mean": "% que Instalaron",
        "disponibilizo_gt_0_sum": "N que Disponibilizaron",
        "disponibilizo_gt_0_mean": "% que Disponibilizaron",
    }

    metrics_df = metrics_df.rename(columns=name_mapping).reset_index()

    # Reorder columns to put Total Clientes first
    cols = ["periodo", "N Clientes"] + [c for c in metrics_df.columns if c not in ["periodo", "N Clientes"]]
    metrics_df = metrics_df[cols]

    metrics_df.sort_values(by="periodo", ascending=False, inplace=True, key=lambda col: col.astype(str))

    # format display columns
    for col in metrics_df.columns:
        if col.startswith("%"):
            metrics_df[col] = (metrics_df[col] * 100).round(0).fillna(0).astype(int).astype(str) + "%"
        elif col.startswith("N "):
            metrics_df[col] = metrics_df[col].fillna(0).apply(lambda x: f"{int(x):,}".replace(",", "."))

    return metrics_df