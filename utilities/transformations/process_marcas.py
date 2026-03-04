import pandas as pd

from utilities.constants.brands import BRANDS, BRANDS_MAPPING, FREE_TEXT_MAPPINGS, IGNORE_FREE_TEXT
import re

def _extract_brands_list(val):
    if pd.isna(val) or val == "":
        return []
    
    found_brands = []
    val_upper = str(val).upper()
    
    for brand in BRANDS:
        pos = val_upper.find(brand)
        if pos != -1:
            # Store (position, TitleizedBrand)
            found_brands.append((pos, brand.title()))
    
    # Sort by position to preserve original order
    found_brands.sort()
    
    # Extract only the names
    return [b[1] for b in found_brands]

def _extract_free_text_brands(val):
    if pd.isna(val) or val == "":
        return []
    
    val = str(val).lower().strip()
    if val in IGNORE_FREE_TEXT:
        return []
    
    # Split by comma or " y "
    tokens = re.split(r",|\sy\s", val)
    found = []
    for t in tokens:
        t = t.strip()
        if not t: continue
        if t in IGNORE_FREE_TEXT: continuef
        
        # Check mapping
        if t in FREE_TEXT_MAPPINGS:
            found.append(FREE_TEXT_MAPPINGS[t].title())
        else:
            # Generic title case for unmapped brands
            found.append(t.title())
            
    return found

def process_marcos_texto_libre(df):
    if "marcas_texto_libre" not in df.columns:
        return df
    
    df["marcas_texto_libre"] = df["marcas_texto_libre"].apply(_extract_free_text_brands)
    
    return df

def process_marcas(df):
    """
    Process the 'marcas' column by extracting known brands, searching both 
    the 'marcas' column and 'marcas_texto_libre' if it exists.
    Consolidates the result into a single 'marcas' column.
    """
    if "marcas" not in df.columns:
        return df

    # Extract lists of brands from the main column
    extracted_marcas = df["marcas"].apply(_extract_brands_list)
    
    # If free text column exists, extract and combine
    if "marcas_texto_libre" in df.columns:
        # We assume process_marcos_texto_libre might have already run, or we run it directly
        extracted_libre = df["marcas_texto_libre"].apply(_extract_free_text_brands)
        combined_brands = extracted_marcas + extracted_libre
    else:
        combined_brands = extracted_marcas

    # Remove duplicates (maintaining order) and join into a comma-separated string
    df["marcas"] = combined_brands.apply(
        lambda brands: ", ".join(list(dict.fromkeys(brands))) if brands else None
    )
    
    return df


def classify_marcas(df, marcas_col="marcas"):
    """
    Categorize entries in the marcas column into boolean columns based on corporate parent.
    """
    if marcas_col not in df.columns:
        return df
        
    # Setup: Initialize columns as False
    df["marcas_abinbev"] = False
    df["marcas_kross"] = False
    df["marcas_ccu"] = False
    df["marcas_otras"] = False
    


    # Classification Logic
    marcas_upper = df[marcas_col].astype(str).str.upper()
    
    for brand, col in BRANDS_MAPPING.items():
        mask = marcas_upper.str.contains(brand, regex=False, na=False)
        df.loc[mask, col] = True

    # Identify "OTRAS": if marcas is not null but none of the mapped columns is True
    # Or more precisely, if there's a brand in the comma-separated list that isn't in the mapping keys
    def check_otras(val):
        if pd.isna(val) or val == "":
            return False
        brands_in_row = [b.strip().upper() for b in str(val).split(",")]
        for b in brands_in_row:
            if b not in BRANDS_MAPPING:
                return True
        return False

    df["marcas_otras"] = df[marcas_col].apply(check_otras)
    
    return df

