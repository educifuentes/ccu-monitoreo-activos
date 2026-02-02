import pandas as pd

BRANDS = [
        "BUDWEISER",
        "STELLA ARTOIS",
        "CRISTAL",
        "ROYAL GUARD",
        "GUAYACAN",
        "HEINEKEN",
        "PATAGONIA",
        "AUSTRAL",
        "KUNTSMANN",
    ]

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
