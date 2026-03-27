from helpers.utilities.load_gsheets import load_gsheets_worksheet

def dim_clientes__gsheets():
    """Return DataFrames for given worksheet names."""

    df = load_gsheets_worksheet("clientes")
    
    return df