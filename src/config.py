import streamlit as st
import numpy as np
from datetime import datetime, timedelta

@st.cache_data
def constants():
    # list out dropdown options for user entry
    # SLEEP_HOURS = list(np.arange(0, 24+0.5, 0.5)) + ['NA']

    SLEEP_QUALITY = list(np.arange(0, 10+0.5, 0.5)) + ['NA']

    SLEEP_GRADE = [
        'A+', 'A', 'A-',
        'B+', 'B', 'B-',
        'C+', 'C', 'C-',
        'D', 'E', 'F', 'NA'
    ]

    SLEEP_TYPE = ['Overnight', 'Nap']
    
    # current date
    current_date = datetime.now().date()

    # set initial time with current date
    SLEEP_START = datetime.combine(current_date, datetime.strptime('18:00', '%H:%M').time())
    SLEEP_STOP = SLEEP_START + timedelta(days=1)
    
    return SLEEP_QUALITY, SLEEP_GRADE, SLEEP_TYPE, SLEEP_START, SLEEP_STOP
