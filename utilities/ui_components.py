import streamlit as st

def display_compliance_badge(clasificacion):
    """Displays a formatted st.badge based on the classification."""
    if clasificacion == "En regla":
        st.badge("En regla", icon="✅")
    elif clasificacion == "No en regla":
        st.badge("No en regla", icon="⚠️")
    elif clasificacion == "No aplica":
        st.badge("No aplica", icon="⚪")
    elif clasificacion == "Sin comodato o terminado":
        st.badge("Sin comodato o terminado", icon="🚫")
    else:
        st.badge(clasificacion, icon="🔍")
