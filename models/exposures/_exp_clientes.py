from models.marts._dim_clientes import dim_clientes

def exp_clientes():

    df = dim_clientes()  

    return df
