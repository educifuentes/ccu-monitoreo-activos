import pandas as pd
import numpy as np

def stg_base_normalizada__censo_2024_2():
    # Define file path
    file_path = "seeds/base_normalizada/base_normalizada - censo_2024_2.csv"
    
    # Load CSV
    df = pd.read_csv(file_path)
        
    return df