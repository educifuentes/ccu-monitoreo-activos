import pandas as pd

REGION_MAP = {
    # 1 - Tarapacá
    "Tarapacá": "1 - Tarapaca",
    "Tarapaca": "1 - Tarapaca",

    # 2 - Antofagasta
    "Antofagasta": "2 - Antofagasta",

    # 3 - Atacama
    "Atacama": "3 - Atacama",

    # 4 - Coquimbo
    "Coquimbo": "4 - Coquimbo",

    # 5 - Valparaíso
    "Valparaíso": "5 - Valparaiso",
    "Valparaiso": "5 - Valparaiso",

    # 6 - O’Higgins
    "O'Higgins": "6 - O'Higgins",
    "Libertador Bernardo O'Higgins": "6 - O'Higgins",

    # 7 - Maule
    "Maule": "7 - Maule",

    # 8 - Biobío
    "Biobío": "8 - Biobio",
    "Biobio": "8 - Biobio",
    "Bio Bio": "8 - Biobio",

    # 9 - La Araucanía
    "La Araucanía": "9 - La Araucania",
    "Araucanía": "9 - La Araucania",
    "La Araucania": "9 - La Araucania",

    # 10 - Los Lagos
    "Los Lagos": "10 - Los Lagos",

    # 11 - Aysén
    "Aysén": "11 - Aysen",
    "Aysen": "11 - Aysen",

    # 12 - Magallanes
    "Magallanes": "12 - Magallanes",
    "Magallanes Y De La Antártica Chilena": "12 - Magallanes",

    # 13 - Metropolitana
    "Metropolitana": "13 - Metropolitana",
    "Metropolitana De Santiago": "13 - Metropolitana",

    # 14 - Los Ríos
    "Los Ríos": "14 - Los Rios",
    "Los Rios": "14 - Los Rios",

    # 15 - Arica y Parinacota
    "Arica Y Parinacota": "15 - Arica y Parinacota",
    "Arica y Parinacota": "15 - Arica y Parinacota",

    # 16 - Ñuble
    "Ñuble": "16 - Ñuble",
}

def clean_region(df):
    """
    Cleans the region column in a DataFrame using the REGION_MAP.
    Ensures NaN values are transformed to None.
    """
    if "region" not in df.columns:
        return df

    # Replace using map
    df["region"] = df["region"].replace(REGION_MAP)
    
    # Convert NaN to None
    df["region"] = df["region"].where(df["region"].notna(), None)
    
    return df