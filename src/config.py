import streamlit as st
import numpy as np
from datetime import datetime, timedelta

@st.cache_data
def constants():
    # list out dropdown options for user entry
    SLEEP_TYPE = ['Overnight', 'Nap']

    # current date
    current_date = datetime.now().date()

    # set initial time with current date
    SLEEP_START = datetime.combine(current_date, datetime.strptime('18:00', '%H:%M').time())
    SLEEP_STOP = SLEEP_START + timedelta(days=1)

    SLEEP_QUALTIY = [
        'A+', 'A', 'A-',
        'B+', 'B', 'B-',
        'C+', 'C', 'C-',
        'D', 'E', 'F', 'NA'
    ]

    return SLEEP_TYPE, SLEEP_START, SLEEP_STOP, SLEEP_QUALTIY
