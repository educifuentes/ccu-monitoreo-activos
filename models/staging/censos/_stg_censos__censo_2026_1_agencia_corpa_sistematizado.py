from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.utilities.load_source import load_source
from helpers.transformations.clean_column_names import clean_column_name

SOURCE_YAML_PATH = "models/sources/_src_censos__censo_2026_1.yml"

def stg_censos__censo_2026_1_agencia_corpa_sistematizado():
    file_path = get_source_metadata("censo_2026_1_agencia_corpa_sistematizado", SOURCE_YAML_PATH)
    df = load_source(file_path)

    df = clean_column_name(df)

    return df
