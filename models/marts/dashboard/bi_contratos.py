
import pandas as pd

from models.staging.gsheets.gsheets_tables import contratos

def bi_contratos():

    df = contratos()


    return df
