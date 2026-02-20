from models.staging.gsheets.gsheets_tables import locales  

def bi_locales():

    df = locales()

    # new columns
    df["cerrado"] = False

    return df
