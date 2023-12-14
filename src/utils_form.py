import streamlit as st
import pandas as pd
from datetime import time, timedelta, datetime
import src.utils_gsheets as gs
from src.config import constants
import src.utils_styling as style

# init connection with google sheet
gs_manager = gs.GSheetsManager()

def create_user_form(data):
    # load in options for entry
    SLEEP_TYPE, SLEEP_START, SLEEP_STOP, SLEEP_QUALTIY = constants()
    
    # create the user input form
    with st.form(key='input_form'):
        # create field 1 for record date input
        record_date = st.date_input(label='Recording date*').strftime('%Y-%m-%d')
        
        # create field 2 for sleep type
        sleep_type = st.selectbox(label='Sleep Type*', options=SLEEP_TYPE, index=None)
        
        # create 2 columns for  field 3 and 4 for sleeping range
        col1, col2 = st.columns(2)
        
        with col1:
            st.write('Sleep Date*')
            sleep_start_date = st.date_input(label=':night_with_stars:')
        
        with col2:
            st.write('Sleep Time*')
            sleep_start_time = st.time_input(
                label=':sleeping_accommodation:',
                value=SLEEP_START + timedelta(hours=5.5),
                step=timedelta(minutes=5)
            )
        
        sleep_start = datetime.combine(sleep_start_date, sleep_start_time)
        
        with col1:
            st.write('Wake Up Date*')
            sleep_end_date = st.date_input(label=':sunrise:')
        
        with col2:
            st.write('Wake Up Time*')
            sleep_end_time = st.time_input(
                label=':dancer:',
                value=SLEEP_STOP - timedelta(hours=9.5),
                step=timedelta(minutes=5)
            )
        
        sleep_end = datetime.combine(sleep_end_date, sleep_end_time)
        
        # create field 5 for sleep grade
        sleep_quality = st.select_slider(label='Sleep Quality*', options=SLEEP_QUALTIY, value='C+')
        
        # create field 6 for user remarks
        remarks = st.text_area(label='Remarks')
        
        # mark mandatory fields
        style.markdown('*Required Fields')

        # create submit button
        submit_button = st.form_submit_button(label='Submit Sleep Details')
        
        # actions taken after form submission
        if submit_button:
            # tells the user how long they have slept
            sleep_time = sleep_end - sleep_start
            total_mins = sleep_time.total_seconds() / 60
            hours = int(total_mins // 60)
            mins = int(total_mins % 60)
            
            # convert sleep time into floats for form submission
            sleep_duration = round(sleep_time.total_seconds() / 3600, 1)
            
            user_form_submission(
                data=data,
                record_date=record_date,
                sleep_type=sleep_type,
                sleep_start_date=sleep_start_date,
                sleep_start_time=sleep_start_time,
                sleep_end_date=sleep_end_date,
                sleep_end_time=sleep_end_time,
                sleep_duration=sleep_duration,
                sleep_quality=sleep_quality,
                remarks=remarks
            )
            
            # inform user on their sleep duration after submission
            if sleep_type == 'Overnight':
                if hours >= 16:
                    style.write(f'Are you a polar bear? Because you have hibernated for {hours} hours and {mins} minutes.')
                elif hours >= 12:
                    style.write(f'Sleeping beauty are you. You have slept for {hours} hours and {mins} minutes.')
                elif hours >= 8:
                    style.write(f'Well Done! You have slept for {hours} hours and {mins} minutes.')
                elif hours <= 6:
                    style.write(f'Oh no... You are only rested for {hours} hours and {mins} mins.')
            elif sleep_type == 'Nap':
                if hours >= 5:
                    style.write(f'Did you went into a deep nap?! It has been {hours} hours and {mins} mins!')
                elif hours >= 3:
                    style.write(f'{hours} hours and {mins} mins is a loooooooooooong nap.')
                elif hours < 3:
                    style.write(f'Hope the {hours} hours and {mins} mins nap has been a great one!')
                    
            style.write('Thank you for using this web app. I hope you like it!')
            
            # clear cached data
            st.cache_data.clear()
                       
            
def user_form_submission(
    data,
    record_date,
    sleep_type,
    sleep_start_date,
    sleep_start_time,
    sleep_end_date,
    sleep_end_time,
    sleep_duration,
    sleep_quality,
    remarks
):
    # convert sleep times to proper hrs and mins
    sleep_start_time = sleep_start_time.strftime('%H:%M')
    sleep_end_time = sleep_end_time.strftime('%H:%M')
    
    # check if all fields are submitted
    if not sleep_type:
        st.warning('Please fill in all required fields.')
        st.stop()
        
    # check if the date is already recorded
    elif (data['Record Date'].astype(str) == record_date).any():
        # check the type of sleep
        if sleep_type == 'Overnight' and 'Overnight' in data[data['Record Date'] == record_date]['Type'].unique():
            st.warning(
                f'You have already recorded your details for an Overnight sleep on this date. '
                f'Head over to the Amend Details page if you will like to edit any of your details.'
            )
            st.stop()
        else:
            # allow entry of different sleep type for the same date
            sleep_data = pd.DataFrame(
                [
                    {
                        'Record Date': record_date,
                        'Type': sleep_type,
                        'Sleep Start Date': sleep_start_date,
                        'Sleep Start Time': sleep_start_time,
                        'Sleep End Date': sleep_end_date,
                        'Sleep End Time': sleep_end_time,
                        'Length': sleep_duration,
                        'Quality': sleep_quality,
                        'Remarks': remarks
                    }
                ]
            )
            
    # create dataframe for a totally new sleep details
    else:
        sleep_data = pd.DataFrame(
            [
                {
                    'Record Date': record_date,
                    'Type': sleep_type,
                    'Sleep Start Date': sleep_start_date,
                    'Sleep Start Time': sleep_start_time,
                    'Sleep End Date': sleep_end_date,
                    'Sleep End Time': sleep_end_time,
                    'Length': sleep_duration,
                    'Quality': sleep_quality,
                    'Remarks': remarks
                }
            ]
        )
    
    # add new entry to data
    updated_data = pd.concat([data, sleep_data], axis=0, ignore_index=True)
    
    # update google sheets with the updated_data
    gs_manager.update_data(updated_data=updated_data, worksheet_name='sleep')
    
    style.write('Sleep details submitted successfully!')
    

def user_amend_form(data):
    # create a dropdown menu to select a date to amend
    sorted_date = data['Record Date'].sort_values(ascending=False).unique()
    selected_date = st.selectbox('To amend details, select the date when you record your details.', sorted_date)
    
    style.write(f'Displaying details recorded on {selected_date}.')
    
    # retrieve the sleep details for the selected date
    amend_entry = (
        data
        .loc[(data['Record Date'] == selected_date), :]
        .fillna('NA')
    )
        
    # convert Sleep Start/End column to datetime format
    amend_entry['Sleep Start Date'] = pd.to_datetime(amend_entry['Sleep Start Date'])
    amend_entry['Sleep End Date'] = pd.to_datetime(amend_entry['Sleep End Date'])
    amend_entry['Sleep Start Time'] = pd.to_datetime(amend_entry['Sleep Start Time'], format='%H:%M').dt.time
    amend_entry['Sleep End Time'] = pd.to_datetime(amend_entry['Sleep End Time'], format='%H:%M').dt.time

    # load in options for entry
    SLEEP_TYPE, SLEEP_START, SLEEP_STOP, SLEEP_QUALITY = constants()

    # form changes based on the number of entries for the selected date
    if len(amend_entry) > 1:
        # table-like editor
        style.write('You have multiple entries during this date. Select the details of which you want to edit.')
        
        # convert Date column to datetime format
        amend_entry['Record Date'] = pd.to_datetime(amend_entry['Record Date']).dt.date
        
        amended_entry = st.data_editor(
            data=amend_entry,
            use_container_width=True,
            column_order=(
                'Type', 'Sleep Start Date', 'Sleep Start Time',
                'Sleep End Date', 'Sleep End Time', 'Quality',
                'Remarks'
            ),
            hide_index=True,
            num_rows='dynamic',
            column_config={
                'Type': st.column_config.SelectboxColumn(
                    label='Type*',
                    options=SLEEP_TYPE,
                    required=True
                ),
                'Sleep Start Date': st.column_config.DateColumn(
                    label='Sleep Start Date*',
                    required=True,
                ),
                'Sleep Start Time': st.column_config.TimeColumn(
                    label='Sleep Start Time*',
                    format='HH:ss',
                    step=60
                ),
                'Sleep End Date': st.column_config.DateColumn(
                    label='Sleep Start Date*',
                    required=True,
                ),
                'Sleep End Time': st.column_config.TimeColumn(
                    label='Sleep Start Time*',
                    format='HH:ss',
                    step=60
                ),
                'Quality': st.column_config.SelectboxColumn(
                    label='Quality*',
                    options=SLEEP_QUALITY,
                    required=True
                ),
                'Remarks': st.column_config.TextColumn()
            }
        )
        
        style.markdown('*Required Fields')
        
        # calculate sleep duration
        amended_entry['Sleep Start Date'] = amended_entry['Sleep Start Date'].astype(str)
        amended_entry['Sleep End Date'] = amended_entry['Sleep End Date'].astype(str)
        amended_entry['Sleep Start Time'] = amended_entry['Sleep Start Time'].apply(lambda x: x.strftime('%H:%M'))
        amended_entry['Sleep End Time'] = amended_entry['Sleep End Time'].apply(lambda x: x.strftime('%H:%M'))
        
        sleep_start = pd.to_datetime(amended_entry['Sleep Start Date'] + ' ' + amended_entry['Sleep Start Time'])
        sleep_end = pd.to_datetime(amended_entry['Sleep End Date'] + ' ' + amended_entry['Sleep End Time'])
        
        amended_entry['Length'] = ((sleep_end - sleep_start) / pd.Timedelta(seconds=3600)).round(2)
        
        # submit the amended entry
        submit_button = st.button('Submit Your New Sleep Details')
        
        if submit_button:
            user_amend_form_submission(
                data=data,
                entry_date=selected_date,
                new_entry=amended_entry,
            )
            
            # clear cached data
            st.cache_data.clear()
            
    # when there is only 1 entry for the selected date
    else:       
        # display a form pre-filled with original entry details for modification
        with st.form(key='amend_form'):
            # create field 1 for sleep type amendment
            new_sleep_type = st.selectbox(
                'Sleep Type*',
                options=SLEEP_TYPE,
                index=SLEEP_TYPE.index(amend_entry['Type'].iloc[0])
            )
            
            # create 2 columns for  field 3 and 4 for sleeping range amendment
            col1, col2 = st.columns(2)
            
            with col1:
                st.write('Sleep Date*')
                new_sleep_start_date = st.date_input(
                    label=':night_with_stars:',
                    value=amend_entry['Sleep Start Date'].iloc[0]
                )
            
            with col2:
                st.write('Sleep Time*')
                new_sleep_start_time = st.time_input(
                    label=':sleeping_accommodation:',
                    value=amend_entry['Sleep Start Time'].iloc[0],
                    step=timedelta(minutes=5)
                )
                
            new_sleep_start = datetime.combine(new_sleep_start_date, new_sleep_start_time)
                
            with col1:
                st.write('Wake Up Date*')
                new_sleep_end_date = st.date_input(
                    label=':sunrise:',
                    value=amend_entry['Sleep End Date'].iloc[0]
                )
        
            with col2:
                st.write('Wake Up Time*')
                new_sleep_end_time = st.time_input(
                    label=':dancer:',
                    value=amend_entry['Sleep End Time'].iloc[0],
                    step=timedelta(minutes=5)
                )
                
            new_sleep_end = datetime.combine(new_sleep_end_date, new_sleep_end_time)
                
            # create field 3 for sleep quality amendment
            new_sleep_quality = st.select_slider(
                label='Sleep Quality*',
                options=SLEEP_QUALITY,
                value=amend_entry['Quality'].iloc[0]
            )
            
            # create field 5 for user remarks
            new_remarks = st.text_area(label='Remarks', value=amend_entry['Remarks'].iloc[0])
            
            # mark mandatory fields
            style.markdown('*Required Fields')
            
            # calculate new sleep duration
            new_sleep_length = new_sleep_end - new_sleep_start
                       
            # convert sleep time into floats for form submission
            new_sleep_length = round(new_sleep_length.total_seconds() / 3600, 2)
            
            # put amended details into a dictionary
            amended_entry = {
                'Record Date': selected_date,
                'Type': new_sleep_type,
                'Sleep Start Date': new_sleep_start_date,
                'Sleep Start Time':new_sleep_start_time.strftime('%H:%M'),
                'Sleep End Date': new_sleep_end_date,
                'Sleep End Time':new_sleep_end_time.strftime('%H:%M'),
                'Length': new_sleep_length,
                'Quality': new_sleep_quality,
                'Remarks': new_remarks,
            }
            
            # create submit button
            submit_button = st.form_submit_button(label='Submit Your New Sleep Details')
                
            # action taken after form submission
            if submit_button:
                user_amend_form_submission(
                    data=data,
                    entry_date=selected_date,
                    new_entry=amended_entry,
                )
                
                # clear cached data
                st.cache_data.clear()
            
                
def user_amend_form_submission(data, entry_date, new_entry):
    
    # check datatype of new_entry
    if type(new_entry) == pd.DataFrame:
        
        # convert columns to similar datatypes
        new_entry['Record Date'] = new_entry['Record Date'].astype(str)
        
        # filter away old_entry from data using entry_date
        data = data[data['Record Date'] != entry_date]
        
        # concat new_entry to data
        data = (
            pd
            .concat([data, new_entry], axis=0, ignore_index=True)
            .sort_values(by='Record Date', ascending=True)
        )

    elif type(new_entry) == dict:

        # convert dictionary to dataframe
        new_entry = pd.DataFrame(new_entry, index=[0])
        
        # update the selected_date entry with new_entry
        data[data['Record Date'] == entry_date] = new_entry.iloc[0].values
    
    # update google sheets
    gs_manager.update_data(updated_data=data, worksheet_name='sleep')
    
    style.write('New sleep details amended successfully!')
    