
import pandas as pd

from models.gsheets.staging.gsheets_tables import contratos

def exp_contratos():

    df = contratos()


    return df
