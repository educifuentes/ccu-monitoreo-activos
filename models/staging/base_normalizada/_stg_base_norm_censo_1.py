import pandas as pd
import numpy as np

def stg_base_norm_censo_1():
    # Define file path
    file_path = "seeds/base_normalizada/base_normalizada - censo_1.csv"
    
    # Load CSV
    df = pd.read_csv(file_path)
        
    return df