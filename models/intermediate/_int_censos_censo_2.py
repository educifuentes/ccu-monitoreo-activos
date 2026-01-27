import sys, os
sys.path.append(os.getcwd())

from models.staging._stg_censos_censo_2 import model as stg_model

def intermediate_model():
    df = stg_model()

    cols_to_select = [
        'ID PK',
        'tipo_de_local',
        'ID CCU',
        'Punto',
        'Inicio'
    ]
    
    df = df[cols_to_select].copy()
    
    print("\n--- Intermediate Model Output (First 5 columns selected) ---")
    print(df.head())
    
    return df

if __name__ == "__main__":
    intermediate_model()
