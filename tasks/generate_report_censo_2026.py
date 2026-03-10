import os
import sys

# Add project root to sys.path so we can import models from the tasks folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.raw.marts._fct_censos import fct_censos_2026
import pandas as pd

final_columns = [
    "ID CLIENTE",
    "NOMBRE FANTASÍA",
    "RAZÓN SOCIAL",
    "RUT",
    "REGIÓN",
    "COMUNA",
    "DIRECCIÓN",
    "Permite censo (SI/NO)",
    "[Si corresponde] Motivo por el que no pudo ser censado (local cerrado, no permite ingreso, etc)",
    "Presencia de schopera comodato de CCU (SI/NO)",
    "Número de salidas totales de schop en máquinas CCU",
    "Instala schopera adicional (Sí/No)",
    "Disponibiliza salidas en máquina schopera (0,1,2)",
    "CCH (Si/No)",
    "Kross (Si/No)",
    "Otras (indicar cuáles)",
    "Competencia en salida CCU (Sí/No)",
    "Indicar nombre de competidor en salida CCU"
]

COLUMN_MAPPING = {
    # locales info
    "ID CLIENTE": "local_id",
    "NOMBRE FANTASÍA": "nombre_fantasia", 
    "RAZÓN SOCIAL": "razon_social",
    "RUT": "rut",
    "REGIÓN": "region",
    "COMUNA": "comuna",
    "DIRECCIÓN": "direcion",
    # censo metadta
    "Permite censo (SI/NO)": "PENDING",
    "[Si corresponde] Motivo por el que no pudo ser censado (local cerrado, no permite ingreso, etc)": "PENDING",
    # activos
    "Presencia de schopera comodato de CCU (SI/NO)": "schoperas",  # Might need boolean transformation
    "Número de salidas totales de schop en máquinas CCU": "salidas",
    # accion
    "Instala schopera adicional (Sí/No)": "instalo",
    "Disponibiliza salidas en máquina schopera (0,1,2)": "disponibilizo",
    # marcas
    "CCH (Si/No)": "marcas_abinbev",
    "Kross (Si/No)": "marcas_kross",
    "Otras (indicar cuáles)": "marcas_otras",
    "Competencia en salida CCU (Sí/No)": "PENDING",  # Assuming abinbev/otras means competence
    "Indicar nombre de competidor en salida CCU": "PENDING"
}

def generate_report(output_filename="tasks/outputs/censo_2026_report.csv"):
    df_fct = fct_censos_2026()
    
    # Initialize an empty DataFrame with our target columns
    out_df = pd.DataFrame(columns=final_columns)
    
    # Map the columns
    for final_col, source_col in COLUMN_MAPPING.items():
        if source_col == "PENDING" or source_col not in df_fct.columns:
            # We don't have this mapping yet, leave it empty
            out_df[final_col] = None
        else:
            # Pull the data from the source column
            out_df[final_col] = df_fct[source_col]
            
    # Export to CSV
    out_df.to_csv(output_filename, index=False, encoding="utf-8-sig")
    print(f"Report successfully generated and saved to: {output_filename}")

if __name__ == "__main__":
    generate_report()