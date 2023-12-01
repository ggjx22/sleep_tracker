import streamlit as st
import pandas as pd
from datetime import time, timedelta, datetime
import src.utils_gsheets as gs
from src.config import constants
import src.utils_styling as style

def create_user_form(data):
    # load in options for entry
    SLEEP_TYPE, SLEEP_START, SLEEP_STOP, SLEEP_QUALTIY = constants()
    
    # create the user input form
    with st.form(key='input_form'):
        # create field 1 for date input
        date = st.date_input(label='Date Recorded in YYYY-MM-DD')
        date = date.strftime('%Y-%m-%d')
        
        # create field 2 for sleep type
        sleep_type = st.selectbox(label='Sleep Type*', options=SLEEP_TYPE, index=None)
        
        # create field 3 & 4 for sleep start/end 
        sleep_range = st.slider(
            label='Sleep Duration*',
            min_value=SLEEP_START,
            max_value=SLEEP_STOP,
            format='HH:mm',
            value=(
                SLEEP_START + timedelta(hours=5.5),   # default to 23:30
                SLEEP_STOP - timedelta(hours=9.5)     # default to 08:30
            ),
            step=timedelta(minutes=1)
        )
        
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
            sleep_end, sleep_start = sleep_range[1], sleep_range[0]
            sleep_time = sleep_end - sleep_start
            total_mins = sleep_time.total_seconds() / 60
            hours = int(total_mins // 60)
            mins = int(total_mins % 60)
            
            # convert sleep time into floats for form submission
            sleep_duration = round(sleep_time.total_seconds() / 3600, 1)
            
            user_form_submission(
                data=data,
                date=date,
                sleep_type=sleep_type,
                sleep_start=sleep_start,
                sleep_end=sleep_end,
                sleep_duration=sleep_duration,
                sleep_quality=sleep_quality,
                remarks=remarks
            )
            
            if hours >= 16:
                style.write(f'Are you a polar bear? Because you have hibernated for {hours} hours and {mins} minutes.')
            elif hours >= 12:
                style.write(f'Sleeping beauty are you. You have slept for {hours} hours and {mins} minutes.')
            elif hours >= 8:
                style.write(f'Well Done! You have slept for {hours} hours and {mins} minutes.')
            elif hours < 1:
                style.write(f'Hope you had a nice nap! You have napped for {mins} minutes.')
            else:
                style.write(f'Oh no... You are only rested for {hours} hours and {mins} mins.')
                       
            
@st.cache_data
def user_form_submission(data, date, sleep_type, sleep_start, sleep_end, sleep_duration, sleep_quality, remarks):
    # convert sleep times to proper hrs and mins
    sleep_start = sleep_start.strftime('%H:%M')
    sleep_end = sleep_end.strftime('%H:%M')
    
    # check if all fields are submitted
    if not sleep_type:
        st.warning('Please fill in all required fields.')
        st.stop()
        
    # check if the date is already recorded
    elif (data['Date'].astype(str) == date).any():
        # check the type of sleep
        if sleep_type == 'Overnight' and 'Overnight' in data[data['Date'] == date]['Type'].unique():
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
                        'Date': date,
                        'Type': sleep_type,
                        'Sleep Start': sleep_start,
                        'Sleep End': sleep_end,
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
                    'Date': date,
                    'Type': sleep_type,
                    'Sleep Start': sleep_start,
                    'Sleep End': sleep_end,
                    'Length': sleep_duration,
                    'Quality': sleep_quality,
                    'Remarks': remarks
                }
            ]
        )
    
    # add new entry to data
    updated_data = pd.concat([data, sleep_data], axis=0, ignore_index=True)

    # establish a google sheets connection
    conn = gs.init_connection()
    
    # update google sheets with the updated_data
    conn.update(worksheet='Sheet1', data=updated_data)
    
    style.write('Sleep details submitted successfully!')
    

def user_amend_form(data):
    # create a dropdown menu to select a date to amend
    sorted_date = data['Date'].sort_values(ascending=False).unique()
    selected_date = st.selectbox('Select a date to amend your details', sorted_date)
    
    style.write(f'Displaying your records for {selected_date}.')
    
    # retrieve the sleep details for the selected date
    selected_entry = (
        data
        .loc[(data['Date'] == selected_date), :]
        .fillna('NA')
    )
    
    # remove length column for amend form
    amend_entry = selected_entry.drop(columns=['Length'], axis=1)
    
    # convert Sleep Start/End column to datetime.time format
    amend_entry['Sleep Start'] = pd.to_datetime(amend_entry['Sleep Start']).dt.time
    amend_entry['Sleep End'] = pd.to_datetime(amend_entry['Sleep End']).dt.time

    # load in options for entry
    SLEEP_TYPE, SLEEP_START, SLEEP_STOP, SLEEP_QUALITY = constants()

    # form changes based on the number of entries for the selected date
    if len(amend_entry) > 1:
        # table-like editor
        style.write('You have multiple entries during this day. Select the details of which you want to edit.')
        
        # convert Date column to datetime format
        amend_entry['Date'] = pd.to_datetime(amend_entry['Date']).dt.date
        
        amended_entry = st.data_editor(
            data=amend_entry,
            use_container_width=True,
            hide_index=True,
            num_rows='dynamic',
            column_config={
                'Date': st.column_config.Column(
                    label='Date*',
                    disabled=True
                ),
                'Type': st.column_config.SelectboxColumn(
                    label='Type*',
                    options=SLEEP_TYPE,
                    required=True
                ),
                'Sleep Start': st.column_config.TimeColumn(
                    label='Sleep Start*',
                    required=True,
                    step=60
                ),
                'Sleep End': st.column_config.TimeColumn(
                    label='Sleep End*',
                    required=True,
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
        amended_entry['Sleep Start'] = pd.to_datetime(amended_entry['Sleep Start'], format='%H:%M:%S')
        amended_entry['Sleep End'] = pd.to_datetime(amended_entry['Sleep End'], format='%H:%M:%S')
        
        # attached the actual dates into Sleep Start/End
        sleep_date = pd.to_datetime(selected_date)
        amended_entry['Sleep Start'] = amended_entry['Sleep Start'].apply(
            lambda x: x.replace(year=sleep_date.year, month=sleep_date.month, day=sleep_date.day)
        )
        
        wake_date = (pd.to_datetime(selected_date) + pd.DateOffset(days=1)).date()
        amended_entry['Sleep End'] = amended_entry['Sleep End'].apply(
            lambda x: x.replace(year=wake_date.year, month=wake_date.month, day=wake_date.day)
        )
        
        amended_entry['Length'] = (
            amended_entry['Sleep End'] - amended_entry['Sleep Start']
        ).apply(lambda x: x.total_seconds() / 3600)
        
        # only keep date component of Sleep Start/End
        amended_entry['Sleep Start'] = amended_entry['Sleep Start'].dt.time
        amended_entry['Sleep End'] = amended_entry['Sleep End'].dt.time
        
        # rearrange columns
        amended_entry = amended_entry[
            ['Date', 'Type', 'Sleep Start', 'Sleep End', 'Length', 'Quality', 'Remarks']
        ]
        
        # submit the amended entry
        submit_button = st.button('Submit Your New Sleep Details')
        
        if submit_button:
            user_amend_form_submission(
                data=data,
                entry_date=selected_date,
                new_entry=amended_entry,
            )
            
            
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

            # create field 2 for sleep length amendment
            if amend_entry['Type'].iloc[0] == 'Overnight':
                # get original sleep days and time
                original_sleep_start = datetime.combine(pd.to_datetime(selected_date), amend_entry['Sleep Start'].iloc[0])
                original_sleep_end = datetime.combine(pd.to_datetime(selected_date), amend_entry['Sleep End'].iloc[0]) + timedelta(days=1)
                
                # define default sleep range for that day
                default_sleep_start = datetime.combine(pd.to_datetime(selected_date), SLEEP_START.time())
                default_sleep_stop = datetime.combine(pd.to_datetime(selected_date), SLEEP_STOP.time()) + timedelta(days=1)
                
                new_sleep_range = st.slider(
                    label='Sleep Duration*',
                    min_value=default_sleep_start,
                    max_value=default_sleep_stop,
                    format='HH:mm',
                    value=(original_sleep_start,original_sleep_end),
                    step=timedelta(minutes=1)
                )
                
            elif amend_entry['Type'].iloc[0] == 'Nap':
                # get original sleep days and time
                original_sleep_start = datetime.combine(pd.to_datetime(selected_date), amend_entry['Sleep Start'].iloc[0])
                original_sleep_end = datetime.combine(pd.to_datetime(selected_date), amend_entry['Sleep End'].iloc[0])
                
                # define default sleep range for that day 
                hours_before_day_start = pd.to_datetime(selected_date) - original_sleep_start
                default_sleep_start_adj = original_sleep_start + hours_before_day_start

                hours_before_day_end = pd.to_datetime(selected_date) + timedelta(days=1) - original_sleep_end
                default_sleep_end_adj = original_sleep_end + hours_before_day_end

                
                new_sleep_range = st.slider(
                    label='Sleep Duration*',
                    min_value=default_sleep_start_adj,
                    max_value=default_sleep_end_adj,
                    format='HH:mm',
                    value=(original_sleep_start,original_sleep_end),
                    step=timedelta(minutes=1)
                )
                
            else:
                st.warning(f'{amend_entry.iloc[0]} is not a valid Sleep Type.')
                st.stop()
                
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
            
            # calculate sleep duration
            new_sleep_end, new_sleep_start = new_sleep_range[1], new_sleep_range[0]
            sleep_time = new_sleep_end - new_sleep_start
            new_sleep_duration = round(sleep_time.total_seconds() / 3600, 1)
            
            # put amended details into a dictionary
            amended_entry = {
                'Date': selected_date,
                'Type': new_sleep_type,
                'Sleep Start': new_sleep_start.strftime('%H:%M'),
                'Sleep End': new_sleep_end.strftime('%H:%M'),
                'Length': new_sleep_duration,
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
                
                
@st.cache_data
def user_amend_form_submission(data, entry_date, new_entry):
    
    # check datatype of new_entry
    if type(new_entry) == pd.DataFrame:
        # ensure date column is in datetime format
        data['Date'] = data['Date'].astype('str')
        new_entry['Date'] = new_entry['Date'].astype('str')

        # filter away old_entry from data using entry_date
        data = data[data['Date'] != entry_date]
        
        # concat new_entry to data
        data = (
            pd
            .concat([data, new_entry], axis=0, ignore_index=True)
            .sort_values(by='Date', ascending=True)
        )
        
    elif type(new_entry) == dict:
        # convert dictionary to dataframe
        new_entry = pd.DataFrame(new_entry, index=[0])
        
        # update the selected_date entry with amended_sleep_data
        data[data['Date'] == entry_date] = new_entry.iloc[0].values
        
    # establish a google sheets connection
    conn = gs.init_connection()
    
    # update google sheets
    conn.update(worksheet='Sheet1', data=data)
    
    style.write('New sleep details amended successfully!')
    