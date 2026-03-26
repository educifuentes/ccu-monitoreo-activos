import pandas as pd
from models.staging.censos._stg_censos__censo_2026_1_agencia_pk import stg_censos__censo_2026_1_agencia_pk
from helpers.transformations.yes_no_to_boolean import yes_no_to_boolean
from helpers.transformations.process_marcas import process_marcas, classify_marcas, correct_brand_names
from helpers.transformations.text_cleaning import clean_text
from helpers.transformations.clean_region import clean_region

def int_censos__censo_2026_1_agencia_pk():

    # 1. Load Data
    df = stg_censos__censo_2026_1_agencia_pk()

    # 2. Column Renaming
    rename_dict = {
        "ID Cliente": "cliente_id",
        "Dirección": "direccion",
        "Región": "region",
        "Comuna": "comuna", 
        "Nombre fantasía": "nombre_fantasia",
        "Visitador": "visitador",
        "rut Visitador": "rut_visitador",
        "Observaciones": "observaciones",
        # activos
        "EL LOCAL CUENTA CON MAQUINAS SHOPERAS?": "tiene_schoperas",
        "NÚMERO TOTAL DE MÁQUINAS SCHOPERAS EN EL LOCAL": "schoperas_total",
        "NÚMERO DE MÁQUINAS SCHOPERAS DE CCU(ASUMIR QUE LA SCHOPERA ES CCU SI LA MAYORÍA DE LAS MARCAS SON CCU - REVISAR TARJETERO DE APOYO)": "schoperas_ccu",
        "¿TIENE ALGÚN EQUIPO COOLER ENTREGADO POR CCU?": "tiene_coolers",
        # accion
        "CUANTAS SHOPERAS NUEVAS INSTALO CCU PARA MARCAS ARTESANALES?": "instalo",
        'CUANTAS SALIDAS DEJO LIBRE CCU PARA MARCAS ARTESANALES? s ': "disponibilizo",
        # marcas
        '¿CUALES DE ESTAS MARCAS SE VENDEN EN SCHOP?': "marcas",
        " OTRA MARCA, ESPECIFIQUE": "marcas_texto_libre",
        # competencia en salidas
        "¿HAY ALGUNA(S) MARCA(S) DE LA COMPETENCIA DE CCU, QUE ESTÉ INSTALADA EN ESA SALIDA(S) Y/ O SCHOPERA(S)  NUEVA(S)?": "hay_competencia_en_salida",
        "¿CUÁL(ES) MARCAS?": "marca_instalada_en_salida"
    }

    df = df.rename(columns=rename_dict)

    # 3. Basic Data Types and Standard Columns
    df["cliente_id"] = df["cliente_id"].astype("str")
    df["rut"] = None
    df["razon_social"] = None
    df["accion_ccu"] = None

    # 4. Period and Metadata
    df["periodo"] = "2026-S1"
    df["fecha"] = pd.to_datetime("2026-02-01").date()
    df["agencia"] = "pk"
    df["permite_censo"] = None
    df["motivo_no_censo"] = None

    # 5. Brand Processing and Classification
    if "marcas" in df.columns:
        df = process_marcas(df)
        df = classify_marcas(df)

    if "marca_instalada_en_salida" in df.columns:
        df["marca_instalada_en_salida"] = correct_brand_names(df["marca_instalada_en_salida"])
        df["marca_instalada_en_salida"] = df["marca_instalada_en_salida"].str.title()

    # 6. Value Transformations
    if "hay_competencia_en_salida" in df.columns:
        df["hay_competencia_en_salida"] = yes_no_to_boolean(df["hay_competencia_en_salida"])
    if "tiene_schoperas" in df.columns:
        df["tiene_schoperas"] = yes_no_to_boolean(df["tiene_schoperas"])

    df["tiene_coolers"] = yes_no_to_boolean(df["tiene_coolers"])
    
    # Text and region cleaning
    df = clean_text(df, ["nombre_fantasia", "direccion"], title=True)
    df = clean_region(df)
    
    # 7. Calculated Columns
    # Total outputs (salidas) is the sum of salidas across all machine columns
    df["salidas"] = 0
    for i in range(1, 7):
        col_name = f"SCHOPERA CCU {i} - NÚMERO DE SALIDAS"
        if col_name in df.columns:
            df["salidas"] += pd.to_numeric(df[col_name], errors='coerce').fillna(0)

    numeric_cols = ["salidas", "schoperas", "instalo", "disponibilizo"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")
    
    # 8. Final Column Selection
    selected_columns = [
        "cliente_id",
        # clientes cols
        "razon_social",
        "nombre_fantasia",
        "rut",
        "direccion",
        "region",
        "comuna",
        # censo metadata
        "periodo",
        "fecha",
        "permite_censo",
        "motivo_no_censo",
        "agencia",
        # activos
        "schoperas_total",
         "schoperas_ccu",
        "salidas",
        "tiene_coolers",
        # accion
        "accion_ccu",
        "instalo",
        "disponibilizo",
        # marcas
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras",
        # listados
        "marcas_abinbev_listado",
        "marcas_kross_listado",
        "marcas_ccu_listado",
        "marcas_otras_listado",
        # competencia en salida
        "hay_competencia_en_salida",
        "marca_instalada_en_salida"
    ]
    
    return df[selected_columns]
