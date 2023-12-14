import streamlit as st
from streamlit_gsheets import GSheetsConnection

class GSheetsManager:
    '''
    Class to interact with google sheets.
    '''
    def __init__(self):
        self.conn = self.init_connection()
        
    def init_connection(self):
        '''
        Method that initializes connection with google sheets.
        '''
        return st.connection('gsheets', type=GSheetsConnection)
    
    def fetch_data(self, worksheet_name=None):
        '''
        Method that fetch data from google sheets.
        
        Parameters:
        worksheet_name (str): Name of the worksheet to fetch data from.
        
        Returns:
        data (DataFrame): Dataframe containing the data from the worksheet.
        
        Raises:
        ValueError: If worksheet_name is not provided.
        '''
        if worksheet_name is None:
            raise ValueError('Please provide a worksheet name.')
        
        data = self.conn.read(worksheet=worksheet_name, usecols=list(range(9)))
        data = data.dropna(how='all')
        
        return data
    
    def update_data(self, updated_data, worksheet_name=None):
        '''
        Method that updates data in google sheets.
        
        Parameters:
        updated_data (DataFrame): Dataframe containing the updated data.
        worksheet_name (str): Name of the worksheet to update data in.
        
        Raises:
        ValueError: If worksheet_name is not provided.
        '''
        if worksheet_name is None:
            raise ValueError('Please provide a worksheet name.')
        
        self.conn.update(worksheet=worksheet_name, data=updated_data)