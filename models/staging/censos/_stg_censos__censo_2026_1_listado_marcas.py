from utilities.load_sources import load_source

SOURCE_YAML_PATH = "models/sources/_src_censos__censo_2026_1.yml"

def stg_censos__censo_2026_1_agencia_corpa_listado_marcas():
    df = load_source(
        name="censo_2026_1_agencia_pk",
        src_yaml_path=SOURCE_YAML_PATH
    )

    # Convert column to string and drop null values
    marcas_col = df["¿CUALES DE ESTAS MARCAS SE VENDEN EN SCHOP?"].dropna().astype(str)
    
    # Split the pipe-separated string and expand/explode into separate rows
    marcas_explode = marcas_col.str.split('|').explode()
    
    # Clean trailing/leading spaces and convert to upper case
    marcas_clean = marcas_explode.str.strip().str.upper()
    
    # Remove empty strings resulting from trailing pipes or double pipes
    marcas_clean = marcas_clean[marcas_clean != '']
    marcas_clean = marcas_clean[~marcas_clean.isin(["LISTADO", "OTRAS", "NINGUNA", "NO APLICA"])]
    
    # Extract unique brand sequences as list
    unique_marcas = marcas_clean.unique().tolist()
    
    # Dictionary to standardise and map common typos to correct brand names
    typo_mapping = {
        "KUNTSMANN": "KUNSTMANN",
        "KUNTZMANN": "KUNSTMANN",
        "KUSTMANN": "KUNSTMANN",
        "KUNSTMAN": "KUNSTMANN",
        "KUNTSMAN": "KUNSTMANN",
        "HEINNEKEN": "HEINEKEN",
        "HENIEKEN": "HEINEKEN",
        "HEINENKEN": "HEINEKEN",
        "ESCUDOS": "ESCUDO",
        "AUSTRALS": "AUSTRAL",
        "ROYAL": "ROYAL GUARD",
        "CUELLONEGRO": "CUELLO NEGRO",
        "CUELLO  NEGRO": "CUELLO NEGRO",
        "CRISTALS": "CRISTAL",
        "CORONAS": "CORONA",
        "CUSQUENA": "CUSQUEÑA",
        "DOLBEK": "D'OLBEK",
        "GUAYACAN": "GUAYACÁN",
        "KILOMETRO 24.7": "KILOMETRO 24,7"
    }
    
    # Apply standardisation using dict and return as a set converted back to list for uniqueness
    standardized_marcas = sorted(list({typo_mapping.get(m, m) for m in unique_marcas}))
    
    return standardized_marcas
