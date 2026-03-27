from helpers.utilities.load_gsheets import load_gsheets_worksheet

def dim_censos_gsheets():
    """Return DataFrame for censos worksheet."""
    return load_gsheets_worksheet("censos")
