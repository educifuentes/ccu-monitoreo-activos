import pandas as pd
from models.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.intermediate._int_censos_censo_1 import int_censos_censo_1


# unir data de censo 1 y de censo 2

def fct_censos():
    int_censos_1_df = int_censos_censo_1()
    int_censos_2_df = int_censos_censo_2()
    
    return pd.concat([int_censos_1_df, int_censos_2_df], ignore_index=True)