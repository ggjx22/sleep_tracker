import streamlit as st
import numpy as np

@st.cache_data
def constants():
    # list out dropdown options for user entry
    SLEEP_HOURS = list(np.arange(0, 24+0.5, 0.5)) + ['NA']

    SLEEP_QUALITY = list(np.arange(0, 10+0.5, 0.5)) + ['NA']

    SLEEP_GRADE = [
        'A+', 'A', 'A-',
        'B+', 'B', 'B-',
        'C+', 'C', 'C-',
        'D', 'E', 'F', 'NA'
    ]

    SLEEP_TYPE = ['Overnight', 'Nap']
    
    return SLEEP_HOURS, SLEEP_QUALITY, SLEEP_GRADE, SLEEP_TYPE