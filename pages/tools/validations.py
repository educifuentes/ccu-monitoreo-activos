import streamlit as st
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer
from models.staging._stg_censos_censo_2 import stg_censos_censo_2



# Load the data
df = stg_censos_censo_2()

# Use the StreamlitRenderer to embed the explorer
renderer = StreamlitRenderer(df)
renderer.explorer()