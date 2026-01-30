import streamlit as st
from pathlib import Path

st.header("Requerimientos")

req_file = Path("text_notes/requerimientos.md")
if req_file.exists():
    md_content = req_file.read_text()
    # Replace markdown checkboxes with emojis for clearer rendering in Streamlit
    md_content = md_content.replace("- [x]", "✅").replace("- [ ]", "⬜")
    st.markdown(md_content)
else:
    st.warning(f"No se encontró el archivo '{req_file}'")