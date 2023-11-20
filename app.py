import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np

# display title and description
st.title('Sleep Tracker Web App')
st.markdown('Enter your sleep details below.')

# establishing a google sheets connection
conn = st.connection('gsheets', type=GSheetsConnection)

# fetch existing sleep data from google sheets
existing_data = conn.read(worksheet='Sheet1', usecols=list(range(5)), ttl=5)
existing_data = existing_data.dropna(how='all')

# list out dropdown options
HOURS = list(np.arange(0, 24+0.5, 0.5))

# # display existing sleep data
# st.dataframe(existing_data)