# def int_base_norm_censo_1():

# df = stg_base_norm_censo_1()

# # Apply brand processing

# brands_col = "CCU/ABINBEV/OTRAS MARCAS COMPETENCIA"

# if brands_col in df.columns:

# df["marcas"] = df[brands_col].apply(process_marcas)

# df = classify_marcas(df)

# # # rename

# rename_dict = {

# "id": "local_id",

# "CATEGORÍA CENSO 1": "categoria",

# "CANTIDAD DE SCHOPERAS CCU": "schoperas_ccu",

# "CANTIDAD DE SALIDAS": "salidas_ccu",

# "CANTIDAD DE SHOPERAS COMPETENCIA ": "schoperas_competencia"

# }

# df.rename(columns=rename_dict, inplace=True)

# # data types

# df["salidas_ccu"] = pd.to_numeric(df["salidas_ccu"], errors='coerce').astype("Int64")

# df["schoperas_ccu"] = pd.to_numeric(df["schoperas_ccu"], errors='coerce').astype("Int64")

# df["schoperas_competencia"] = pd.to_numeric(df["schoperas_competencia"], errors='coerce').astype("Int64")

# # note: I've updated the data type conversion to use pd.to_numeric with errors='coerce'. This will turn any invalid strings (like '2o5') into NaN, which are then correctly handled by the "Int64" type.

# # new columns

# df["periodo"] = "2024-S2"

# df["fecha"] = pd.to_datetime("2024-10-01").date()

# selected_columns = [

# "local_id",

# "periodo",

# "fecha",

# # activos cantidades

# "schoperas_ccu",

# "schoperas_competencia",

# "salidas_ccu",

# # marcas

# "marcas",

# "marcas_abinbev",

# "marcas_kross",

# "marcas_ccu",

# "marcas_otras"

# ]

# # Filter columns that exist

# selected_columns = [col for col in selected_columns if col in df.columns]

# print("\n--- List of Column Names ---")

# for i, col in enumerate(df.columns):

# print(f"{i}: {col}")

# df = df[selected_columns]

# return df
