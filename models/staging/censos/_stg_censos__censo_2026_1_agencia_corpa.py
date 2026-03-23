from utilities.load_sources import load_source
from utilities.transformations.clean_column_names import clean_column_name

SOURCE_YAML_PATH = "models/sources/_src_censos__censo_2026_1.yml"

def stg_censos__censo_2026_1_agencia_corpa():
    df = load_source(
        name="censo_2026_1_agencia_corpa",
        src_yaml_path=SOURCE_YAML_PATH
    )

    df = clean_column_name(df)

    return df
