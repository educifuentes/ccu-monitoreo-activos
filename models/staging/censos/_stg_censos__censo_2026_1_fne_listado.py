import pandas as pd
import numpy as np

from utilities.yaml_loader import load_yaml_config

def stg_censos__censo_2026_1_fne_listado():
    # Define file path
    file_path = "seeds/censos/Listado Final_to_supervisoraENTREGADO POR FNE.xlsx - Visita supervisora.csv"
    
    # Load CSV using the second row as header
    df = pd.read_csv(file_path)
    return df
