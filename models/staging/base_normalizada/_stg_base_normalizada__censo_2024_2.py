import pandas as pd
import numpy as np
from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.utilities.load_source import load_source

def stg_base_normalizada__censo_2024_2():
    # Define file path
    file_path = get_source_metadata("censo_2024_2", "models/sources/_src_base_normalizada.yml")
    
    # Load CSV
    df = load_source(file_path)
        
    return df