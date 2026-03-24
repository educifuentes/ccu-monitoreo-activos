import pandas as pd
import numpy as np
from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.utilities.load_source import load_source

def stg_bases_ccu__base_2024_q1():
    # Fetch configuration from YAML
    file_path = get_source_metadata("base_normalizada_clientes", "models/sources/_src_base_normalizada.yml")

    # Load CSV
    df = load_source(file_path)

    return df



