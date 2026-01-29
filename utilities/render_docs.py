import streamlit as st
import yaml
import os

def render_model_docs(yaml_path):
    """
    Lee un archivo YAML de documentación (formato dbt) y lo renderiza
    con un diseño limpio y profesional en Streamlit.
    """
    if not os.path.exists(yaml_path):
        st.error(f"⚠️ Archivo no encontrado: `{yaml_path}`")
        return

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo YAML: {e}")
        return

    if not data or 'models' not in data:
        st.warning("No se encontró información de modelos en el archivo.")
        return

    for model in data.get('models', []):
        model_name = model.get('name', 'Sin Nombre')
        description = model.get('description', 'Sin descripción disponible.')
        
        with st.container():
            st.subheader(f"📊 Modelo: {model_name}")
            st.info(description)
            
            if 'columns' in model:
                st.markdown("#### Detalle de Columnas")
                
                # Preparar datos para la tabla
                table_content = "| Columna | Descripción | Tests |\n| :--- | :--- | :--- |\n"
                for col in model['columns']:
                    name = f"`{col.get('name', '')}`"
                    desc = col.get('description', '---')
                    tests = col.get('data_tests', [])
                    tests_str = ", ".join([f"`{t}`" for t in tests]) if tests else "---"
                    table_content += f"| {name} | {desc} | {tests_str} |\n"
                
                st.markdown(table_content)
            
            st.divider()
