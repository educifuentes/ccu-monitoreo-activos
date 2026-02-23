
import pandas as pd
import numpy as np

from utilities.yaml_loader import get_table_config

def stg_reportes_ccu_base_2024_q1():
    # Fetch configuration from YAML
    file_path = "seeds/base_normalizada/base_normalizada - locales.csv"

    # Load CSV
    df = pd.read_csv(file_path)

    return df



