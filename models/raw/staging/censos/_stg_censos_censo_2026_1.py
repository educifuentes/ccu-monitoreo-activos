import pandas as pd
import numpy as np

from utilities.yaml_loader import load_yaml_config
from utilities.load_sources import load_source
from utilities.transformations.clean_column_names import clean_column_name

SOURCE_YAML_PATH = "models/raw/sources/_src_censos__censo_2026_1.yml"


def stg_censos_censo_2026_1_agencia_pkl():
    df = load_source(
        name="censo_2026_1_agencia_pk",
        src_yaml_path=SOURCE_YAML_PATH
    )
    return df

def stg_censos_censo_2026_1_agencia_pkl_agencia_corpa():
    df = load_source(
        name="censo_2026_1_agencia_corpa",
        src_yaml_path=SOURCE_YAML_PATH
    )

    df = clean_column_name(df)

    return df

def stg_censos_censo_2026_1_agencia_corpa_sistematizado():
    df = load_source(
        name="censo_2026_1_agencia_corpa_sistematizado",
        src_yaml_path=SOURCE_YAML_PATH
    )

    df = clean_column_name(df)

    return df

