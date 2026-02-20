import pandas as pd
import numpy as np

from utilities.yaml_loader import get_table_config

def stg_base_norm_original():
    # Fetch configuration from YAML
    config = get_table_config(
        source_name="base normalizada", 
        table_name="base_normalizada_original", 
        yaml_path="models/raw/sources/_src_base_normalizada.yml"
    )
    file_path = config.get('path')
    
    # Load CSV
    df = pd.read_csv(file_path, skiprows=1)

        
    return df