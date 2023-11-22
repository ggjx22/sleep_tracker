import src.utils_gsheets as gs
import src.utils_form as ui_form
import streamlit as st

# display title and description
colT1,colT2 = st.columns([1,5])
with colT2:
    st.title('Sleep Tracker Web App')

st.markdown('Enter your sleep details below.')

# fetch data from google sheets
data = gs.fetch_data()

# create user form for input and submission into google drive
ui_form.create_user_form(data)