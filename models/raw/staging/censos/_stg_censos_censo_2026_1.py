import pandas as pd
import numpy as np

from utilities.yaml_loader import load_yaml_config
from utilities.load_sources import load_source

SOURCE_YAML_PATH = "models/raw/sources/_src_censos__censo_2026_1.yml"


def stg_censos_censo_2026_1():
    df = load_source(
        name="censo_2026",
        src_yaml_path=SOURCE_YAML_PATH
    )
    return df

def stg_censos_censo_2026_1_agencia_nueva():
    df = load_source(
        name="censo_2026_1 agencia nueva",
        src_yaml_path=SOURCE_YAML_PATH
    )

    return df

def stg_censos_censo_2026_1_corregido():
    df = load_source(
        name="censo_2026_1 corregido",
        src_yaml_path=SOURCE_YAML_PATH
    )

    return df

