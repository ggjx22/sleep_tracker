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

# print(existing_data['Date'].apply(type))

# search_date = '2023-11-20'
# result = any(existing_data['Date'].str.contains(search_date))

# print(result)


# list out dropdown options for user entry
SLEEP_HOURS = list(np.arange(0, 24+0.5, 0.5))
SLEEP_QUALITY = list(np.arange(0, 10+1, 1))
SLEEP_GRADE = [
    'A+', 'A', 'A-',
    'B+', 'B', 'B-',
    'C+', 'C', 'C-',
    'D', 'E', 'F', 'NA'
]

# create the user input form
with st.form(key='input_form'):
    date = st.date_input(label='Date Recorded in YYYY-MM-DD')
    date = date.strftime('%Y-%m-%d')
    sleep_duration = st.selectbox('Sleep Duration*', options=SLEEP_HOURS, index=None)
    sleep_quality = st.selectbox('Sleep Quality*', options=SLEEP_QUALITY, index=None)
    sleep_grade = st.selectbox('Sleep Grade*', options=SLEEP_GRADE, index=None)
    remarks = st.text_area(label='Remarks')
    
    # mark mandatory fields
    st.markdown('**Required Fields*')
    
    submit_button = st.form_submit_button(label='Submit Sleep Details')
    
    # display a message when submit buttom is clicked
    if submit_button:
        # check if all fields are submitted
        if not sleep_duration or not sleep_quality or not sleep_grade:
            st.warning('Please fill in all required fields.')
            st.stop()
            
        # check if the date is already recorded
        elif (existing_data['Date'].astype(str) == date).any():
            st.warning('Sleep details for this date already recorded.')
            st.stop()
            
        # append the new sleep data to the existing data
        else:
            sleep_data = pd.DataFrame(
                [
                    {
                        'Date': date,
                        'Length': sleep_duration,
                        'Quality': sleep_quality,
                        'Overall': sleep_grade,
                        'Remarks': remarks
                    }
                ]
            )
            
            # add new sleep_data to existing_data
            updated_data = pd.concat([existing_data, sleep_data], ignore_index=True)
            
            # update google sheets with the updated_data
            conn.update(worksheet='Sheet1', data=updated_data)
            
            st.write('Sleep details submitted successfully!')