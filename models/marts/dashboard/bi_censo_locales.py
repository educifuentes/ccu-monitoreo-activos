import pandas as pd
import numpy as np
import math
from models.marts.fct_censos import fct_censos
from models.marts.dim_locales import dim_locales

def assign_clasificacion(row):
    """
    Categoriza el cumplimiento del local basado en las reglas de negocio.
    Maneja valores nulos para evitar errores de ambigüedad.
    """
    # Si aplica_regla es nulo o Falso, no aplica
    if pd.isna(row['aplica_regla']) or not row['aplica_regla']:
        return "No aplica"
    
    # Si es nulo, tratamos como No en regla por defecto o podrías agregar un estado "Sin Datos"
    if pd.isna(row['cumple_cuota']):
        return "Sin datos"
        
    if row['cumple_cuota']:
        return "En regla"
    
    return "No en regla"

def bi_censo_locales():
    """
    Calcula el BI de censos integrando datos de hechos y dimensiones, 
    aplicando la lógica de cuotas para marcas externas.
    """
    # 1. Carga y cruce de datos
    df = pd.merge(fct_censos(), dim_locales(), on="local_id")

    # Asegurar que las columnas críticas no tengan nulos para los cálculos
    df['salidas_ccu'] = df['salidas_ccu'].fillna(0)
    df['instalo'] = df['instalo'].fillna(0)
    df['disponibilizo'] = df['disponibilizo'].fillna(0)

    # 2. Definición de Aplicabilidad
    # La regla aplica si el local tiene más de 3 salidas de CCU.
    df['aplica_regla'] = df['salidas_ccu'] > 3

    # 3. Cálculo de Cuota (Target)
    # Según la normativa, por cada 4 salidas de CCU, se debe disponibilizar 1 para la competencia.
    df['salidas_objetivo'] = 0.0
    mask = df['aplica_regla']
    df.loc[mask, 'salidas_objetivo'] = (df.loc[mask, 'salidas_ccu'] / 4).apply(math.floor)

    # 4. Cálculo de Salidas Reales para Competencia
    df["salidas_reales_otras"] = df["instalo"] + df["disponibilizo"]

    # 5. Verificación de Cumplimiento
    df['cumple_cuota'] = False
    df.loc[mask, 'cumple_cuota'] = df.loc[mask, 'salidas_reales_otras'] >= df.loc[mask, 'salidas_objetivo']

    # 6. Clasificación Final
    df['clasificacion'] = df.apply(assign_clasificacion, axis=1)

    return df
