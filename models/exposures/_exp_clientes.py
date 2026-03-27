from models.marts.gsheets._dim_clientes_gsheets import dim_clientes_gsheets

def exp_clientes():

    df = dim_clientes_gsheets()  

    return df
