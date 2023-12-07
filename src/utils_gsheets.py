import streamlit as st
from streamlit_gsheets import GSheetsConnection

def init_connection():
    # establishing a google sheets connection
    conn = st.connection('gsheets', type=GSheetsConnection)
    
    return conn
    
def fetch_data():
    # establishing a google sheets connection
    conn = init_connection()

    # fetch existing sleep data from google sheets
    existing_data = conn.read(worksheet='Sheet1', usecols=list(range(7)))
    existing_data = existing_data.dropna(how='all')
    
    return existing_data