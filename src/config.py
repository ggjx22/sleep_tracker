import numpy as np

# list out dropdown options for user entry
SLEEP_HOURS = list(np.arange(0, 24+0.5, 0.5)) + ['NA']

SLEEP_QUALITY = list(np.arange(0, 10+0.5, 0.5)) + ['NA']

SLEEP_GRADE = [
    'A+', 'A', 'A-',
    'B+', 'B', 'B-',
    'C+', 'C', 'C-',
    'D', 'E', 'F', 'NA'
]