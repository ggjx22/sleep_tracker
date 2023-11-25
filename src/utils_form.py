import streamlit as st
import pandas as pd
import src.utils_gsheets as gs
import src.config as constants
import src.utils_styling as style

def create_user_form(data):
    # create the user input form
    with st.form(key='input_form'):
        # create field 1 for date input
        date = st.date_input(label='Date Recorded in YYYY-MM-DD')
        date = date.strftime('%Y-%m-%d')
        
        # create field 3 for sleep type
        sleep_type = st.selectbox('Sleep Type*', options=constants.SLEEP_TYPE, index=None)
        
        # create field 2 for sleep length
        sleep_duration = st.selectbox('Sleep Duration*', options=constants.SLEEP_HOURS, index=None)
        
        # create field 4 for sleep quality
        sleep_quality = st.selectbox('Sleep Quality*', options=constants.SLEEP_QUALITY, index=None)
        
        # create field 5 for sleep grade
        sleep_grade = st.selectbox('Sleep Grade*', options=constants.SLEEP_GRADE, index=None)
        
        # create field 6 for user remarks
        remarks = st.text_area(label='Remarks')
        
        # mark mandatory fields
        style.markdown('**Required Fields')

        # create submit button
        submit_button = st.form_submit_button(label='Submit Sleep Details')
        
        # actions taken after form submission
        if submit_button:
            user_form_submission(
                data=data,
                date=date,
                sleep_type=sleep_type,
                sleep_duration=sleep_duration,
                sleep_quality=sleep_quality,
                sleep_grade=sleep_grade,
                remarks=remarks
            )
            
            
def user_form_submission(data, date, sleep_type, sleep_duration, sleep_quality, sleep_grade, remarks):   
    # check if all fields are submitted
    if not sleep_type or not sleep_duration or not sleep_quality or not sleep_grade:
        st.warning('Please fill in all required fields.')
        st.stop()
        
    # check if the date is already recorded
    elif (data['Date'].astype(str) == date).any():
        # check the type of sleep
        if sleep_type == data[data['Date'] == date]['Type'].iloc[0]:
            st.warning(
                f'Similar sleep details for this date already recorded. '
                f'Head over to the Amend Sleep Details page if you will like to edit your details.'
            )
            st.stop()
        else:
            # allow entry of different sleep type for the same date
            sleep_data = pd.DataFrame(
            [
                {
                    'Date': date,
                    'Type': sleep_type,
                    'Length': sleep_duration,
                    'Quality': sleep_quality,
                    'Overall': sleep_grade,
                    'Remarks': remarks
                }
            ]
        )
            
    # append the new sleep data to the existing data
    else:
        sleep_data = pd.DataFrame(
            [
                {
                    'Date': date,
                    'Type': sleep_type,
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
    
    # retrieve the sleep details for the selected date
    selected_entry = data[data['Date'] == selected_date].iloc[0]
    
    # fill empty entries with 'NA' to avoid code break in st.form()
    selected_entry.fillna('NA', inplace=True)
    
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
        # create field 2 for sleep length amendment
        new_sleep_duration = st.selectbox(
            'Sleep Duration*',
            options=constants.SLEEP_HOURS,
            index=constants.SLEEP_HOURS.index(original_entry['Length'])
        )
        
        # create field 3 for sleep quality amendment
        new_sleep_quality = st.selectbox(
            'Sleep Quality*',
            options=constants.SLEEP_QUALITY,
            index=constants.SLEEP_QUALITY.index(original_entry['Quality'])
        )
        
        # create field 4 for sleep grade amendment
        new_sleep_grade = st.selectbox(
            'Sleep Grade*',
            options=constants.SLEEP_GRADE,
            index=constants.SLEEP_GRADE.index(original_entry['Overall'])
        )
        
        # create field 5 for user remarks
        new_remarks = st.text_area(label='Remarks', value=original_entry['Remarks'])
        
        # mark mandatory fields
        style.markdown('**Required Fields')
        
        # create submit button
        submit_button = st.form_submit_button(label='Submit Your New Sleep Details')
        
        # action taken after form submission
        if submit_button:
            user_amend_form_submission(
                old_entry=original_entry,
                data=data,
                date=selected_date,
                sleep_duration=new_sleep_duration,
                sleep_quality=new_sleep_quality,
                sleep_grade=new_sleep_grade,
                remarks=new_remarks
            )
            

def user_amend_form_submission(old_entry, data, date, sleep_duration, sleep_quality, sleep_grade, remarks):
    # make a duplicate copy of data
    amended_data = old_entry.copy()
    
    # update the amended data with the new sleep details
    amended_data['Length'] = sleep_duration
    amended_data['Quality'] = sleep_quality
    amended_data['Overall'] = sleep_grade
    amended_data['Remarks'] = remarks
        
    # convert the amended_data dictionary to a dataframe
    amended_sleep_data = pd.DataFrame(amended_data, index=[0])
    
    # update the selected_date entry with amended_sleep_data
    data[data['Date'] == date] = amended_sleep_data.iloc[0].values
    
    # establish a google sheets connection
    conn = gs.init_connection()
    
    # update google sheets with amended_sleep_data
    conn.update(worksheet='Sheet1', data=data)
    
    st.write('Sleep details amended successfully!')
    