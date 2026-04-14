import os
import streamlit as st

def get_environment() -> str:
    """Returns the current environment ('local' or 'production')."""
    env = os.environ.get("ENVIRONMENT")
    if not env:
        env = st.secrets.get("ENVIRONMENT", "production")
    
    # Return exactly 'local' or 'production' as requested
    if env and env.lower() == "local":
        return "local"
    return "production"
