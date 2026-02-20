import pandas as pd


path = "seeds/gsheets_snapshots/2026-02-20 - Activos CCU.xlsx"

def reprocess_sheets():
    """Clean the sheets."""
    
    df = pd.read_excel(path, sheet_name="locales")
    print(df.head())
    