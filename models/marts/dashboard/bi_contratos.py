
import pandas as pd

from models.staging.gsheets.gsheets_tables import contratos

def bi_contratos():

    df = contratos()

    # new columns
    df["contrato_vigente"] = False

    # Calculate if contract is still active
    if "fecha_termino" in df.columns:
        # We consider today as valid (vencimiento happens at end of day)
        today = pd.Timestamp.today().date()
        df["contrato_vigente"] = df["fecha_termino"].apply(lambda x: x >= today if x is not None else False)
    else:
        df["contrato_vigente"] = False


    return df
