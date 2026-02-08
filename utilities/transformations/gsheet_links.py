import pandas as pd

def add_gsheet_link(df, gid, row_index=None):
    """
    Adds a column with a direct link to the corresponding row in Google Sheets.
    Uses 'row_index' argument to point to the specific row.
    """
    if not gid:
        return df
        
    df = df.copy()
    
    base_url = f"https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit#gid={gid}"
    
    if row_index is not None:
        # Range A{row_index} makes the link point directly to the row/cell
        df["ir a gsheet"] = row_index.apply(lambda x: f"{base_url}&range=A{x}" if pd.notna(x) else base_url)
    else:
        df["ir a gsheet"] = base_url
        
    return df
