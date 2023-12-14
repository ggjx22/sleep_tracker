import streamlit as st
from streamlit_gsheets import GSheetsConnection

class GSheetsManager:
    def __init__(self):
        self.conn = self.init_connection()
        
    def init_connection(self):
        return st.connection('gsheets', type=GSheetsConnection)
    
    def fetch_data(self, worksheet_name=None):
        if worksheet_name is None:
            raise ValueError('Please provide a worksheet name.')
        
        data = self.conn.read(worksheet=worksheet_name, usecols=list(range(9)))
        data = data.dropna(how='all')
        
        return data
    
    def update_data(self, updated_data, worksheet_name=None):
        if worksheet_name is None:
            raise ValueError('Please provide a worksheet name.')
        
        self.conn.update(worksheet=worksheet_name, data=updated_data)