import pandas as pd

BRANDS = [
        "BUDWEISER",
        "STELLA ARTOIS",
        "KROSS",
        "CRISTAL",
        "ROYAL GUARD",
        "GUAYACAN",
        "HEINEKEN",
        "PATAGONIA",
        "AUSTRAL",
        "KUNTSMANN",
    ]

BRANDS_MAPPING = {
        "BUDWEISER": "marcas_abinbev",
        "STELLA ARTOIS": "marcas_abinbev",
        "KROSS": "marcas_kross",
        "CRISTAL": "marcas_ccu",
        "ROYAL GUARD": "marcas_ccu",
        "GUAYACAN": "marcas_ccu",
        "HEINEKEN": "marcas_ccu",
        "PATAGONIA": "marcas_ccu",
        "AUSTRAL": "marcas_ccu",
        "KUNTSMANN": "marcas_ccu"
    }

def process_marcas(val):
    if pd.isna(val) or val == "":
        return None
    
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
    ordered_brands = [b[1] for b in found_brands]
    
    # Remove duplicates if any (maintaining order)
    unique_brands = list(dict.fromkeys(ordered_brands))
    
    return ", ".join(unique_brands) if unique_brands else None


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

# classify marcas