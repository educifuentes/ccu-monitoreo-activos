from utilities.load_sources import load_source

SOURCE_YAML_PATH = "models/raw/sources/_src_censos__censo_2026_1.yml"

def stg_censos__censo_2026_1_agencia_pk():
    df = load_source(
        name="censo_2026_1_agencia_pk",
        src_yaml_path=SOURCE_YAML_PATH
    )
    return df
