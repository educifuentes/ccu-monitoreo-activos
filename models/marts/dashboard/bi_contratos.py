
import pandas as pd

from models.gsheets.staging.gsheets_tables import contratos

def bi_contratos():

    df = contratos()


    return df
