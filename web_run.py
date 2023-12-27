import os, json
import streamlit as st

from config import MAIN_PATH, MISC_PATH
from ui import (
    draw_header,
    draw_files2render
)

# Open localization json
path = os.path.sep.join([MAIN_PATH, 'localization.json'])
with open(path, encoding='utf-8') as localiz:
    localiz_dict = json.load(localiz)

cur_language = 'en'

session_state_variables = {
    'new_files_counter' : 1,
    
}

# Create session_state variables
for var, value in session_state_variables.items():
    if var not in st.session_state:
        st.session_state[var] = value

draw_header(localiz_dict, cur_language)

draw_files2render(localiz_dict, cur_language)

st.write(st.session_state)





