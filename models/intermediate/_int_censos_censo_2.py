from models.staging._stg_censos_censo_2 import stg_censos_censo_2

def int_censos_2():
    df = stg_censos_censo_2()

    # cols_to_select = [
    #     'ID PK',
    #     'tipo_de_local',
    #     'ID CCU',
    #     'Punto',
    #     'Inicio'
    # ]
    
    # df = df[cols_to_select].copy()
    
    # print("\n--- Intermediate Model Output (First 5 columns selected) ---")
    # print(df.head())
    
    return df

if __name__ == "__main__":
    print(int_censos_2().head())
