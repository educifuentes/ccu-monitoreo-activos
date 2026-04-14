import streamlit as st
from helpers.utilities.check_environment import get_environment

def check_password():
    """Returns True if the user has entered the correct password in this session."""

    # Bypass authentication if not in production
    if get_environment() != "production":
        return True

    if st.session_state.get("password_correct", False):
        return True

    # Center the login input
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Ingrese contraseñ", type="password", key="temp_password")
        
        if password:
            if password == st.secrets["password"]:
                st.session_state["password_correct"] = True
                # Clear the temporary password from state
                del st.session_state["temp_password"]
                # Refresh the app to authenticated view
                st.rerun()
            else:
                st.error("😕 Password incorrect")
                
    return False
