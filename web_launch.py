import os, json, signal
import streamlit as st
import time

from config import *
from main_functions import (
    createParser,
    is_blender_running,
    start_render,
    stop_render
)

from web_ui import (
    draw_header,
    draw_main_container,
    draw_render_button,
    draw_stop_button,
    draw_message
)

# Session State Variables
session_state_variables = {
    'new_files_counter' : 1,
    'all_correct' : False,
    'is_rendering' : False,
    'render_process' : None,
    'files_data' : {},
}

# Create session_state variables
for var, value in session_state_variables.items():
    if var not in st.session_state:
        st.session_state[var] = value


# Open localization json
path = os.path.sep.join([MAIN_PATH, 'localization.json'])
with open(path, encoding='utf-8') as localiz:
    localiz_dict = json.load(localiz)

cur_language = 'en'


if __name__ == '__main__':

    message = 'An instance of Blender is already running on the server! Rendering 2 projects at once might not be a good idea..'
    # draw_message(is_blender_running(), message, 'WARNING')
    draw_header(localiz_dict, cur_language)

    draw_main_container(localiz_dict, cur_language)

    # Rendering cycle
    draw_render_button(localiz_dict, cur_language)
    # if st.session_state['is_rendering']:
    draw_stop_button(localiz_dict, cur_language,
                        st.session_state['render_process'])


            

    

    # st.write(st.session_state)
