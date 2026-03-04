import pandas as pd
import numpy as np

from utilities.yaml_loader import load_yaml_config

def stg_censos_censo_2026_1():
    # Define file path
    file_path = "seeds/censos/CCU2026 PK - CCU_2026_29_V34.csv"
    
    # Load CSV using the second row as header
    df = pd.read_csv(file_path)
    return df

