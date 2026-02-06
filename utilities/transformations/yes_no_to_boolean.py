import pandas as pd

def yes_no_to_boolean(df, column):
    """
    Convierte una columna con valores 'Sí'/'No' (o 'Yes'/'No') a booleanos True/False.
    Maneja variaciones de mayúsculas/minúsculas y espacios en blanco.
    """
    if column not in df.columns:
        return df
        
    # Crear un mapeo para normalizar los valores
    # Usamos str.strip().str.lower() para mayor robustez
    mapping = {
        'si': True,
        'sí': True,
        'yes': True,
        'no': False,
    }
    
    # Aplicar la transformación de forma segura
    df[column] = df[column].astype(str).str.strip().str.lower().map(mapping)
    
    return df