import pandas as pd

def clean_text(df, columns, title=True):
    """
    Strips whitespace from specified columns in a DataFrame.
    Optionally applies title casing.
    
    Args:
        df (pd.DataFrame): The DataFrame to process.
        columns (list): List of column names to clean.
        title (bool): Whether to apply .str.title(). Defaults to True.
        
    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            if title:
                df[col] = df[col].str.title()
    return df
