import streamlit as st
from time import sleep
from stqdm import stqdm

import os, json

from config import *
from main_functions import(
    start_render,
    get_scene_names,
    scenes2arg_scenes,
    scripts2string,

)


# Inforamtion about wich frames to render
# Taken from rendersettings.json for eqch .blend file
path = os.path.sep.join([MAIN_PATH, 'rendersettings.json'])
with open(path, 'r') as fp:
    config = json.load(fp)

render_frames = config['render_frames']



# Session State Variables
session_state_variables = {
    'new_files_counter' : 1,
    'all_correct' : False,
    'files_data' : {},

}

# Create session_state variables
for var, value in session_state_variables.items():
    if var not in st.session_state:
        st.session_state[var] = value





def draw_header(localization, language):
    """
    Draws Logo and a Title
    """

    logo = os.path.sep.join([MISC_PATH, "3Dev-sign.png"])
    col1, mid, col2 = st.columns([1,1,20])
    with col1:
        st.image(logo, width=60)
    with col2:
        st.title(localization['main_logo_1'][language])

    st.header(localization['main_title_1'][language])

def draw_main_container(localization, language):
    """
    Draws main frame with rows for new files to add,
    stores data for use in rendering process
    """

    with st.container(border=True):
        st.write('Add files to render')
        for count in range(st.session_state['new_files_counter']):

            # Container with Add button
            if st.session_state['new_files_counter'] - count <= 1:
                add_file_container_bt = st.container(border=False)
                with add_file_container_bt:
                    col1, col2, buff = st.columns([1,1,12])
                    
                    add_file_button = col1.button(label=':heavy_plus_sign:',
                                                on_click=add_file_container_bt_ac,  # on_click required to change session_state variable
                                                args=(count,))  # pass arguments to function here
            
                    remove_file_button = col2.button(label=':heavy_minus_sign:',
                                                on_click=remove_file_container_bt_ac,
                                                args=(count,))  
            
            # Containers with file data
            else:
                with st.container(border=True):
                    draw_file_data(localization, language, count)



    st.button('reset', on_click=reset_session_state)

def draw_file_data(localization, language, file_num):
    """
    Initialize files data in session_state
    Draws file path input, correct/wrong path input,

    """

    col1, col2, col3 = st.columns([1,1,30])
    with col1:
        st.subheader(file_num+1)

    with col3:
        file_path_input = st.text_input(
            label='Select file to render',
            placeholder=localization['file_render_select_file_1'][language],
            key=f'file_path_{file_num+1}',
        )
        st.session_state['files_data'][file_num+1]['path'] = file_path_input

    try:
        st.session_state['files_data'][file_num+1]['selected_scenes'] = []  # Clear after change in file_path input
        st.session_state['files_data'][file_num+1]['scenes'] = []  # Same
        st.session_state['files_data'][file_num+1]['correct_input'] = True

        scenes = get_scene_names(file_path_input)
        col2.write(':large_green_circle:')

        col1, buf, col2 = st.columns([5,1,15])
        with col1:
            draw_scene_selector(localization, language, file_num, scenes)
            if st.session_state['files_data'][file_num+1]['all_scenes']:
                selected_scenes = scenes
            else:
                selected_scenes = st.session_state['files_data'][file_num+1]['selected_scenes']

            arg_scenes = scenes2arg_scenes(selected_scenes,render_frames)
            st.session_state['files_data'][file_num+1]['scenes'] = arg_scenes

        with col2:
            draw_render_settings(localization, language, file_num)

    except FileNotFoundError:
        st.write('Wrong path')
        col2.write(':red_circle:')
        st.session_state['files_data'][file_num+1]['correct_input'] = False

def draw_scene_selector(localization, language, file_num, scene_list):
    """
    Draws scene selector in a checkbox form,
    switches all_scenes session_state variable,
    adds selected scenes to session_state variable
    """

    all_scenes_toggle_chb = st.checkbox(label='All scenes',
                   value=True,
                   key=f'all_scenes_{file_num+1}'
                   )
    st.session_state['files_data'][file_num+1]['all_scenes'] = all_scenes_toggle_chb

    st.write('Select scenes')

    for scene in scene_list:
        if st.checkbox(scene, value=False, disabled=all_scenes_toggle_chb):
            if scene not in st.session_state['files_data'][file_num+1]['selected_scenes']:
                st.session_state['files_data'][file_num+1]['selected_scenes'].append(scene)
        else:
            if scene in st.session_state['files_data'][file_num+1]['selected_scenes']:
                st.session_state['files_data'][file_num+1]['selected_scenes'].remove(scene)


def draw_render_settings(localization, language, file_num):
    """
    Draws render settings,
    Selection of optional scripts
    """

    
    optional_scripts_input = st.text_input(
            label='Optional scripts to launch',
            placeholder=localization['optional_script_names_1'][language],
            key=f'opt_scripts_{file_num+1}'
        )
    
    optional_scripts = optional_scripts_input.split(', ')
    str_scripts = scripts2string(SCRIPTS_BEFORE,SCRIPTS_AFTER,optional_scripts)
    st.session_state['files_data'][file_num+1]['scripts'] = str_scripts

    with st.container(border=True):
        
        
        col1, col2 = st.columns([2,1])
        
        col1.subheader('Render Settings')
        col2.toggle(label='Overwrite')

        # 4 columns to display 2 parameters in 1 row
        col_param1, col_toggle1, col_param2, col_toggle2 = st.columns([5,3,5,3])

        # render_scheme
        parameters = {'label':'Render scheme', 'options':['OPTIX', 'CUDA'], 'key':'render_scheme'}
        render_settings_block(col_param1, col_toggle1, 'radio', parameters)

        # render_device
        parameters = {'label':'Render device', 'options':['GPU', 'CPU'], 'key':'render_device'}
        render_settings_block(col_param2, col_toggle2, 'radio', parameters)



    



def draw_render_button(localization, language):
    """
    Render button which starts rendering process
    """

    start_render_bt = st.button('Start Render')
    if start_render_bt:
        # Checking if all inputs are correct
        for file_data in st.session_state['files_data'].values():
            if file_data['correct_input'] == False:
                return st.write('Check file inputs. Something is wrong!')
  

        # if st.session_state['all_correct']:
        for index, file_data in stqdm(st.session_state['files_data'].items()):
            # Get data from Session_state dict
            blender = BLENDER_PATH
            blend_file = file_data['path']
            arg_blend_file = f'-b {blend_file}'
            scripts_str = file_data['scripts']
            arg_scripts = f'-P {scripts_str}'
            arg_scenes = file_data['scenes']

            console_command = f'{blender} {arg_blend_file} {arg_scripts} {arg_scenes}'
            st.write(console_command)
            start_render(console_command)
        

def render_settings_block(col_param, col_toggle, widget, kwargs):
    """
    Draws single render setting with desired widget
    """

    with st.container(border=True):
        with col_param:
            getattr(st, widget)(**kwargs)  # To draw any widget you pass to function
        with col_toggle:
            key = kwargs['key']
            unique_key = f'overwrite_{key}'
            st.checkbox(label='overwrite', label_visibility='hidden', key=unique_key)

def add_file_container_bt_ac(file_num):
    """
    Helper function, works with on_click,
    which is required to rerun when session_state is changed
    """
    
    st.session_state['new_files_counter'] += 1
    if file_num+1 not in st.session_state['files_data']:
        st.session_state['files_data'][file_num+1] = {}
        st.session_state['files_data'][file_num+1]['correct_input'] = False
        st.session_state['files_data'][file_num+1]['selected_scenes'] = []
        st.session_state['files_data'][file_num+1]['scenes'] = []
        st.session_state['files_data'][file_num+1]['scripts'] = ''
        st.session_state['files_data'][file_num+1]['render_settings'] = {}
        



def remove_file_container_bt_ac(file_num):
    """
    Helper function, works with on_click,
    which is required to rerun when session_state is changed
    """
    
    if st.session_state['new_files_counter'] >= 2:
        st.session_state['new_files_counter'] -= 1
    
    if file_num in st.session_state['files_data']:
        del st.session_state['files_data'][file_num]


def reset_session_state():
    """
    Helper function for Reset button, works with on_click,
    which is required to rerun when session_state is changed
    """
    
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)

# Needs tweaking but MUST DO
def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)
