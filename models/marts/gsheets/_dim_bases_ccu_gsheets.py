from helpers.utilities.load_gsheets import load_gsheets_worksheet

def dim_bases_ccu_gsheets():
    """Return DataFrame for bases_ccu worksheet."""
    return load_gsheets_worksheet("bases_ccu")
