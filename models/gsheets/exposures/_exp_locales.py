from models.gsheets.staging.gsheets_tables import locales  

def exp_locales():

    df = locales()

    # new columns
    df["cerrado"] = False

    return df
