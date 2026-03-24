import pandas as pd
import numpy as np
from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.utilities.load_source import load_source

def stg_bases_manuales__censo_2024_2():
    # Define file path
    file_path = get_source_metadata("censo_2024_2", "models/sources/_src_bases_manuales.yml")
    
    # Load CSV
    df = load_source(file_path)
        
    return df