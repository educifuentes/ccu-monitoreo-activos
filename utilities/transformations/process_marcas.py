import pandas as pd

BRANDS = [
    "CRISTAL",
    "DORADA",
    "ESCUDO",
    "MORENITA",
    "ROYAL GUARD",
    "STONES",
    "IMPERIAL",
    "BLUE MOON",
    "COORS",
    "HEINEKEN",
    "SOL",
    "AUSTRAL",
    "D'OLBEK",
    "GUAYACÁN",
    "KUNSTMANN",
    "PATAGONIA",
    "SZOT",
    "CORONA",
    "BECKER",
    "STELLA ARTOIS",
    "BUDWEISER",
    "CUSQUEÑA",
    "CORONITA",
    "BALTICA",
    "MALTA DEL SUR",
    "PILASE",
    "PACEÑA",
    "QUILMES",
    "PILSEN DEL SUR",
    "MODELO",
    "BECKS",
    "KILOMETRO 24,7",
    "GOOSE ISLAND",
    "HOEGAARDEN",
    "BUD LIGHT",
    "LEFFE",
    "BUSCH",
    "BRAHMA",
    "MICHELOB ULTRA",
]

BRAND_COLORS = [
    "#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6",
    "#E67E22", "#1ABC9C", "#34495E", "#E74C3C", "#2ECC71",
    "#3498DB", "#F39C12", "#8E44AD", "#D35400", "#16A085",
    "#2C3E50", "#E74C3C", "#27AE60", "#2980B9", "#F39C12",
    "#8E44AD", "#D35400", "#16A085", "#2C3E50", "#C0392B",
    "#27AE60", "#2980B9", "#F39C12", "#8E44AD", "#D35400",
    "#16A085", "#2C3E50", "#C0392B", "#27AE60", "#2980B9",
    "#F39C12", "#8E44AD", "#D35400", "#16A085"
]

BRANDS_MAPPING = {
    "CRISTAL": "marcas_ccu",
    "DORADA": "marcas_ccu",
    "ESCUDO": "marcas_ccu",
    "MORENITA": "marcas_ccu",
    "ROYAL GUARD": "marcas_ccu",
    "STONES": "marcas_ccu",
    "IMPERIAL": "marcas_ccu",
    "BLUE MOON": "marcas_ccu",
    "COORS": "marcas_ccu",
    "HEINEKEN": "marcas_ccu",
    "SOL": "marcas_ccu",
    "AUSTRAL": "marcas_ccu",
    "D'OLBEK": "marcas_ccu",
    "GUAYACÁN": "marcas_ccu",
    "KUNSTMANN": "marcas_ccu",
    "PATAGONIA": "marcas_ccu",
    "SZOT": "marcas_ccu",
    "CORONA": "marcas_abinbev",
    "BECKER": "marcas_abinbev",
    "STELLA ARTOIS": "marcas_abinbev",
    "BUDWEISER": "marcas_abinbev",
    "CUSQUEÑA": "marcas_abinbev",
    "CORONITA": "marcas_abinbev",
    "BALTICA": "marcas_abinbev",
    "MALTA DEL SUR": "marcas_abinbev",
    "PILASE": "marcas_abinbev",
    "PACEÑA": "marcas_abinbev",
    "QUILMES": "marcas_abinbev",
    "PILSEN DEL SUR": "marcas_abinbev",
    "MODELO": "marcas_abinbev",
    "BECKS": "marcas_abinbev",
    "KILOMETRO 24,7": "marcas_abinbev",
    "GOOSE ISLAND": "marcas_abinbev",
    "HOEGAARDEN": "marcas_abinbev",
    "BUD LIGHT": "marcas_abinbev",
    "LEFFE": "marcas_abinbev",
    "BUSCH": "marcas_abinbev",
    "BRAHMA": "marcas_abinbev",
    "MICHELOB ULTRA": "marcas_abinbev",
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