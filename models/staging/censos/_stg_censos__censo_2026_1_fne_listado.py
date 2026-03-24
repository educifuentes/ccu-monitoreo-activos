import pandas as pd
import numpy as np

from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.utilities.load_source import load_source

def stg_censos__censo_2026_1_fne_listado():
    # Fetch file path from metadata
    file_path = get_source_metadata(
        "censo_2026_1_fne_listado",
        "models/sources/_src_censos__censo_2026_1.yml"
    )
    
    # Load CSV using the second row as header
    df = load_source(file_path)
    return df
