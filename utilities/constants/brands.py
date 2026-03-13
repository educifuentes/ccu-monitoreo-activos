BRANDS = [
    "AUSTRAL",
    "BALTICA",
    "BECKER",
    "BUDWEISER",
    "CORONA",
    "CRISTAL",
    "CUELLO NEGRO",
    "CUSQUEÑA",
    "D'OLBEK",
    "ERDINGER",
    "ESCUDO",
    "ESTRELLA DE GALICIA",
    "GOOSE ISLAND",
    "GUAYACÁN",
    "HEINEKEN",
    "HOEGAARDEN",
    "KILOMETRO 24,7",
    "KROSS",
    "KUNSTMANN",
    "LOA",
    "MESTRA",
    "PATAGONIA",
    "QUILMES",
    "ROYAL GUARD",
    "STELLA ARTOIS",
    "TOTEM",
]

BRAND_GROUP = [
    "marcas_ccu",
    "marcas_abinbev",
    "marcas_kross",
    "marcas_otras"
]

BRANDS_MAPPING = {
    "AUSTRAL": BRAND_GROUP[0],
    "BALTICA": BRAND_GROUP[1],
    "BECKER": BRAND_GROUP[1],
    "BUDWEISER": BRAND_GROUP[1],
    "CORONA": BRAND_GROUP[1],
    "CRISTAL": BRAND_GROUP[0],
    "CUELLO NEGRO": BRAND_GROUP[3],
    "CUSQUEÑA": BRAND_GROUP[1],
    "D'OLBEK": BRAND_GROUP[0],
    "ERDINGER": BRAND_GROUP[3],
    "ESCUDO": BRAND_GROUP[0],
    "ESTRELLA DE GALICIA": BRAND_GROUP[3],
    "GOOSE ISLAND": BRAND_GROUP[1],
    "GUAYACÁN": BRAND_GROUP[0],
    "HEINEKEN": BRAND_GROUP[0],
    "HOEGAARDEN": BRAND_GROUP[1],
    "KILOMETRO 24,7": BRAND_GROUP[1],
    "KROSS": BRAND_GROUP[2],
    "KUNSTMANN": BRAND_GROUP[0],
    "LOA": BRAND_GROUP[3],
    "MESTRA": BRAND_GROUP[3],
    "PATAGONIA": BRAND_GROUP[0],
    "QUILMES": BRAND_GROUP[1],
    "ROYAL GUARD": BRAND_GROUP[0],
    "STELLA ARTOIS": BRAND_GROUP[1],
    "TOTEM": BRAND_GROUP[3],
}

BRAND_GROUPS_COLORS = {
    BRAND_GROUP[0]: "#2ca02c",  # Green (CCU)
    BRAND_GROUP[1]: "#d62728",  # Red (Abinbev)
    BRAND_GROUP[2]: "#ff7f0e",  # Orange (Kross)
    BRAND_GROUP[3]: "#7f7f7f"   # Gray (Otras)
}

BRAND_COLORS = [
    BRAND_GROUPS_COLORS.get(BRANDS_MAPPING.get(brand), BRAND_GROUPS_COLORS[BRAND_GROUP[3]])
    for brand in BRANDS
]

FREE_TEXT_MAPPINGS = {
    "bloomon": "BLUE MOON",
    "bluemoon": "BLUE MOON",
    "blue moon": "BLUE MOON",
    "chester beer artesanal": "CHESTER",
    "chester beer": "CHESTER",
    "chester": "CHESTER",
    "kross": "KROSS",
    "estrella damn": "ESTRELLA DAMM",
    "estrella damm": "ESTRELLA DAMM",
    "estrella": "ESTRELLA DAMM",
    "mahou": "MAHOU",
    "mahon": "MAHOU",
    "peroni": "PERONI",
    "peronni": "PERONI",
    "peruani": "PERONI",
    "tubiinger": "TUBINGER",
    "tubinger": "TUBINGER",
    "alambra": "ALHAMBRA",
    "alhambra": "ALHAMBRA",
    "tropera": "TROPERA",
    "las troperas": "TROPERA",
}

IGNORE_FREE_TEXT = {
    "no", "ninguna", "ninguna otra", "sin comentario", "ninguna otra marca",
    "0", "no hay otra", "no tienen cervezas a la venta , estan solo las maquinas",
    "no hay", "ok", ".", "no tiene", "si. comentarios"
}
