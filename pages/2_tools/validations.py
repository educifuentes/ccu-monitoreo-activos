import streamlit as st
import pandas as pd
from models.marts.dim_locales import dim_locales

st.header("📊 Validaciones de Datos Maestros")
st.markdown("Chequeos de calidad sobre la tabla Locales")

# Cargar datos
df = dim_locales()

# -----------------------------------------------------------------------------
# VALIDACIONES DE IDENTIDAD
# -----------------------------------------------------------------------------
st.subheader("1. Identidad y Unicidad")

# Unicidad de local_id
total_filas = len(df)
locales_unicos = df['local_id'].nunique()
has_dupes_id = locales_unicos < total_filas

if not has_dupes_id:
    st.success("✅ IDs Únicos")
else:
    st.error(f"❌ {total_filas - locales_unicos} IDs duplicados")

# Unicidad de RUT
ruts_unicos = df['rut'].nunique()
has_dupes_rut = ruts_unicos < total_filas

if not has_dupes_rut:
    st.success("✅ RUTs Únicos")
else:
    st.warning(f"⚠️ {total_filas - ruts_unicos} RUTs duplicados")

# Valores Nulos en columnas críticas
nulos_id = df['local_id'].isna().sum()
nulos_rut = df['rut'].isna().sum()

if nulos_id == 0 and nulos_rut == 0:
    st.success("✅ Sin nulos en IDs/RUT")
else:
    st.error(f"❌ Nulos detectados ({nulos_id} ID, {nulos_rut} RUT)")

# -----------------------------------------------------------------------------
# COMPLETITUD DE ATRIBUTOS
# -----------------------------------------------------------------------------
st.subheader("2. Atributos Descriptivos")

cols_desc = ['razon_social', 'direccion', 'region', 'ciudad']
nulos_desc = df[cols_desc].isna().sum()

# Mostrar métricas de nulos por columna (lista vertical)
for col in cols_desc:
    val = nulos_desc[col]
    label = col.replace("_", " ").title()
    if val == 0:
        st.write(f"✅ **{label}**: Completo (0 nulos)")
    else:
        st.write(f"⚠️ **{label}**: {val} nulos")



# Mostrar tabla de posibles duplicados por Razón Social
st.subheader("4. Posibles Duplicados (Razón Social)")
dupes_name = df[df.duplicated('razon_social', keep=False)].sort_values('razon_social')
if not dupes_name.empty:
    st.warning(f"Se encontraron {len(dupes_name)} filas con Razón Social compartida.")
    st.dataframe(dupes_name)
else:
    st.success("No se encontraron Razones Sociales duplicadas.")


