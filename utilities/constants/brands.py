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

BRAND_GROUP = [
    "marcas_ccu",
    "marcas_abinbev",
    "marcas_kross",
    "marcas_otras"
]

BRANDS_MAPPING = {
    "CRISTAL": BRAND_GROUP[0],
    "DORADA": BRAND_GROUP[0],
    "ESCUDO": BRAND_GROUP[0],
    "MORENITA": BRAND_GROUP[0],
    "ROYAL GUARD": BRAND_GROUP[0],
    "STONES": BRAND_GROUP[0],
    "IMPERIAL": BRAND_GROUP[0],
    "BLUE MOON": BRAND_GROUP[0],
    "COORS": BRAND_GROUP[0],
    "HEINEKEN": BRAND_GROUP[0],
    "SOL": BRAND_GROUP[0],
    "AUSTRAL": BRAND_GROUP[0],
    "D'OLBEK": BRAND_GROUP[0],
    "GUAYACÁN": BRAND_GROUP[0],
    "KUNSTMANN": BRAND_GROUP[0],
    "PATAGONIA": BRAND_GROUP[0],
    "SZOT": BRAND_GROUP[0],
    "CORONA": BRAND_GROUP[1],
    "BECKER": BRAND_GROUP[1],
    "STELLA ARTOIS": BRAND_GROUP[1],
    "BUDWEISER": BRAND_GROUP[1],
    "CUSQUEÑA": BRAND_GROUP[1],
    "CORONITA": BRAND_GROUP[1],
    "BALTICA": BRAND_GROUP[1],
    "MALTA DEL SUR": BRAND_GROUP[1],
    "PILASE": BRAND_GROUP[1],
    "PACEÑA": BRAND_GROUP[1],
    "QUILMES": BRAND_GROUP[1],
    "PILSEN DEL SUR": BRAND_GROUP[1],
    "MODELO": BRAND_GROUP[1],
    "BECKS": BRAND_GROUP[1],
    "KILOMETRO 24,7": BRAND_GROUP[1],
    "GOOSE ISLAND": BRAND_GROUP[1],
    "HOEGAARDEN": BRAND_GROUP[1],
    "BUD LIGHT": BRAND_GROUP[1],
    "LEFFE": BRAND_GROUP[1],
    "BUSCH": BRAND_GROUP[1],
    "BRAHMA": BRAND_GROUP[1],
    "MICHELOB ULTRA": BRAND_GROUP[1],
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
