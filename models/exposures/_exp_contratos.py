
import pandas as pd

from models.marts._fct_contratos import fct_contratos

def exp_contratos():

    df = fct_contratos()


    return df
