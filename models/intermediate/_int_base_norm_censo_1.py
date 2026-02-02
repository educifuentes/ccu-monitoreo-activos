from models.staging._stg_base_norm_censo_1 import stg_base_norm_censo_1
import pandas as pd


def process_marcas(val):
    if pd.isna(val) or val == "":
        return None
    
    brands = [
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
    
    found_brands = []
    val_upper = str(val).upper()
    
    for brand in brands:
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


def int_base_norm_censo_1():

    df = stg_base_norm_censo_1()

    # Apply brand processing
    brands_col = "CCU/ABINBEV/OTRAS MARCAS COMPETENCIA"
    if brands_col in df.columns:
        df["marcas"] = df[brands_col].apply(process_marcas)

    # # rename
    rename_dict = {
        "id": "local_id",
        "CATEGORÍA CENSO 1": "categoria",
        "CANTIDAD DE SCHOPERAS CCU": "schoperas_ccu",
        "CANTIDAD DE SALIDAS": "salidas_totales",
        "CANTIDAD DE SHOPERAS COMPETENCIA ": "schoperas_competencia"
    }

    df.rename(columns=rename_dict, inplace=True)


    selected_columns = [
        "local_id",
        "salidas_totales",
        "schoperas_ccu",
        "schoperas_competencia",
        "marcas"
    ]

    # Filter columns that exist
    selected_columns = [col for col in selected_columns if col in df.columns]

    # 3. Output Information
    # print("--- DataFrame Head ---")
    # print(df.iloc[:, :5].head())

    print("\n--- List of Column Names ---")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")

    df = df[selected_columns]
        
    return df