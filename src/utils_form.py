import streamlit as st
import pandas as pd
import src.utils_gsheets as gs
import src.config as constants

def create_user_form(data):
    # create the user input form
    with st.form(key='input_form'):
        # create field 1 for date input
        date = st.date_input(label='Date Recorded in YYYY-MM-DD')
        date = date.strftime('%Y-%m-%d')
        
        # create field 2 for sleep length
        sleep_duration = st.selectbox('Sleep Duration*', options=constants.SLEEP_HOURS, index=None)
        
        # create field 3 for sleep quality
        sleep_quality = st.selectbox('Sleep Quality*', options=constants.SLEEP_QUALITY, index=None)
        
        # create field 4 for sleep grade
        sleep_grade = st.selectbox('Sleep Grade*', options=constants.SLEEP_GRADE, index=None)
        
        # create field 5 for user remarks
        remarks = st.text_area(label='Remarks')
        
        # mark mandatory fields
        st.markdown('**Required Fields*')

        # create submit button
        submit_button = st.form_submit_button(label='Submit Sleep Details')
        
        # actions taken after form submission
        if submit_button:
            user_form_submission(
                data=data,
                date=date,
                sleep_duration=sleep_duration,
                sleep_quality=sleep_quality,
                sleep_grade=sleep_grade,
                remarks=remarks
            )
            
            
def user_form_submission(data, date, sleep_duration, sleep_quality, sleep_grade, remarks):
    # check if all fields are submitted
    if not sleep_duration or not sleep_quality or not sleep_grade:
        st.warning('Please fill in all required fields.')
        st.stop()
        
    # check if the date is already recorded
    elif (data['Date'].astype(str) == date).any():
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
    updated_data = pd.concat([data, sleep_data], ignore_index=True)
    
    # establish a google sheets connection
    conn = gs.init_connection()
    
    # update google sheets with the updated_data
    conn.update(worksheet='Sheet1', data=updated_data)
    
    st.write('Sleep details submitted successfully!')
    
    
def user_amend_form(data):
    # create a dropdown menu to select a date to amend
    sorted_date = data['Date'].sort_values(ascending=False)
    selected_date = st.selectbox('Select a date to amend your details', sorted_date)
    
    # selected_date = '2023-11-23'
    
    # retrieve the sleep details for the selected date
    selected_entry = data[data['Date'] == selected_date].iloc[0]
    
    # place original entry details in a dictionary
    original_entry = {
        'Date': selected_entry['Date'],
        'Length': selected_entry['Length'],
        'Quality': selected_entry['Quality'],
        'Overall': selected_entry['Overall'],
        'Remarks': selected_entry['Remarks']
    }
    
    # display a form pre-filled with original entry details for modification
    with st.form(key='amend_form'):
        # create field 1 for date amendment
        date = st.date_input(
            label='Date Recorded in YYYY-MM-DD',
            value=pd.to_datetime(original_entry['Date'])
        )
        # date = date.strftime('%Y-%m-%d')
        
        # create field 2 for sleep length amendment
        sleep_duration = st.selectbox(
            'Sleep Duration*',
            options=constants.SLEEP_HOURS,
            index=constants.SLEEP_HOURS.index(original_entry['Length'])
        )
        
        # create field 3 for sleep quality amendment
        sleep_quality = st.selectbox(
            'Sleep Quality*',
            options=constants.SLEEP_QUALITY,
            index=constants.SLEEP_QUALITY.index(original_entry['Quality'])
        )
        
        # create field 4 for sleep grade amendment
        sleep_grade = st.selectbox(
            'Sleep Grade*',
            options=constants.SLEEP_GRADE,
            index=constants.SLEEP_GRADE.index(original_entry['Overall'])
        )
        
        # create field 5 for user remarks
        remarks = st.text_area(label='Remarks', value=original_entry['Remarks'])