#!/bin/sh

# Create the .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Check if the environment variable is set
if [ -z "$STREAMLIT_SECRETS_CONTENTS" ]; then
    echo "Warning: STREAMLIT_SECRETS_CONTENTS is not set. The app might fail if secrets are required."
else
    echo "Recreating secrets.toml from environment variable..."
    # Write the contents to the secrets.toml file
    echo "$STREAMLIT_SECRETS_CONTENTS" > .streamlit/secrets.toml
fi

# Start Streamlit
streamlit run app.py
