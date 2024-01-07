import os, json, time, psutil
import streamlit as st

from config import *
from main_functions import (
    is_blender_running,
    search_sort_log
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
    'completed_successfull' : False,
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
    # Display only on other instances of blender, not rendering by this process
    if not psutil.pid_exists(st.session_state['render_process'].pid):
        message = 'An instance of Blender is already running on the server! Rendering 2 projects at once might not be a good idea..'
        draw_message(is_blender_running(), message, 'WARNING')

    draw_header(localiz_dict, cur_language)

    draw_main_container(localiz_dict, cur_language)

    # Rendering cycle
    draw_render_button(localiz_dict, cur_language)
    
    draw_stop_button(localiz_dict, cur_language,
                        st.session_state['render_process'])
    
    # Render log
    if st.session_state['is_rendering']:
        st.write(f'Render started at: {st.session_state["start_render_time"]}')
        render_data = search_sort_log('render_log.txt')
        if render_data != None:
            st.write(render_data.strip())

            # st.write(f"Curent frame: {render_data['frame']}")
            # st.write(f"Elapsed time: {render_data['time']}")
            # st.write(f"Remaining time: {render_data['remaining']}")

        # Check if render process is running and if complited successfully
        if not psutil.pid_exists(st.session_state['render_process'].pid):
            st.session_state['is_rendering'] = False
        if st.session_state['render_process'].poll() != None:
            st.session_state['completed_successfull'] = True
    
        time.sleep(3)
        st.rerun()

    # If render process completed successfully
    if st.session_state['completed_successfull']:
        st.session_state['completed_successfull'] = False
        draw_message(True, 'Rendering was successfull.', 'SUCCESS')
        st.write(f'Render started at: {st.session_state["start_render_time"]}')
        st.write(f'Render finished at: {time.strftime("%H:%M:%S")}')



