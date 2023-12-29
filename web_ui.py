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

## SESION_STATE VARIABLES NEED TO BE IN LAUNCH FILE

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

    with st.container(border=False):
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
            placeholder='path\\to\\file.blend',
            key=f'file_path_{file_num+1}',
        )
        st.session_state['files_data'][file_num+1]['path'] = file_path_input

    try:
        st.session_state['files_data'][file_num+1]['selected_scenes'] = []  # Clear after change in file_path input
        st.session_state['files_data'][file_num+1]['scenes'] = []  # Same
        st.session_state['files_data'][file_num+1]['correct_input'] = True

        scenes = get_scene_names(file_path_input)
        col2.write(':large_green_circle:')

        col1, buf, col2 = st.columns([4,1,15])
        with col1:
            draw_scene_selector(localization, language, file_num, scenes)

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

    # st.session_state['files_data'][file_num+1]['selected_scenes'] = []  # Clear after change in file_path input

    all_scenes_toggle_chb = st.checkbox(label='All scenes',
                   value=True,
                   key=f'all_scenes_{file_num+1}'
                   )
    st.session_state['files_data'][file_num+1]['all_scenes'] = all_scenes_toggle_chb
    st.write('Select scenes')

    for scene in scene_list:
        scene_cbx = st.checkbox(scene, value=False,
                                disabled=all_scenes_toggle_chb, key=f'cbx_{scene}_{file_num+1}')
        if scene_cbx:
            if scene not in st.session_state['files_data'][file_num+1]['selected_scenes']:
                st.session_state['files_data'][file_num+1]['selected_scenes'].append(scene)
        else:
            if scene in st.session_state['files_data'][file_num+1]['selected_scenes']:
                st.session_state['files_data'][file_num+1]['selected_scenes'].remove(scene)

    # Working with 'All scenes' switch
    
    if st.session_state['files_data'][file_num+1]['all_scenes']:
        st.session_state['files_data'][file_num+1]['selected_scenes'] = scene_list

def draw_render_settings(localization, language, file_num):
    """
    Draws render settings,
    Selection of optional scripts
    """

    
    optional_scripts_input = st.text_input(
            label='Optional scripts to launch',
            placeholder='script1.py, script2.py',
            key=f'opt_scripts_{file_num+1}'
        )
    
    optional_scripts = optional_scripts_input.split(', ')
    str_scripts = scripts2string(SCRIPTS_BEFORE,SCRIPTS_AFTER,optional_scripts)
    st.session_state['files_data'][file_num+1]['scripts'] = str_scripts

    # Render Settings
    render_settings_container = st.container(border=True)
    with render_settings_container:
        
        col1, col2 = st.columns([2,1])      
        col1.subheader('Render Settings')
        overwrite_toggle = col2.toggle(label='Overwrite',  # Important toggle that switches on/off all settings' overwrite
                                       key=f'render_settings_overwrite_{file_num+1}')

        col1, col2 = st.columns([9,2])
        # render_output_location
        kwargs = {'label':'Output location',  # widget function arguments
                      'placeholder':'Enter output folder',
                      'value':'//Renders',
                      'key':f'render_output_location_{file_num+1}'}
        param, toggle = render_settings_block(col1, col2, 'text_input', kwargs,  # draw widget
                              checkbox_default=True, settings_toggle=overwrite_toggle)
        parameters = {'overwrite':toggle,  # parameters to store in session_state rendersettings 
                      'value':param}
        store_rendersettings(file_num, 'render_output_location', **parameters)  # store parameters

        # 4 columns to display 2 parameters in 1 row BECAUSE F** Streamlit can't allow multipple columns inside collumns
        col_param1, col_toggle1, col_param2, col_toggle2 = st.columns([5,3,5,3])

        # render_scheme
        kwargs = {'label':'Render scheme', 'options':['OPTIX', 'CUDA'],
                  'index':0,
                  'key':f'render_scheme_{file_num+1}'}
        param, toggle = render_settings_block(col_param1, col_toggle1, 'radio', kwargs,
                                              settings_toggle=overwrite_toggle)
        parameters = {'overwrite':toggle,
                      'value':param}
        store_rendersettings(file_num, 'render_scheme', **parameters)

        # render_device
        kwargs = {'label':'Render device', 'options':['GPU', 'CPU'],
                  'index':0,
                  'key':f'render_device_{file_num+1}'}
        param, toggle = render_settings_block(col_param2, col_toggle2, 'radio', kwargs,
                                              settings_toggle=overwrite_toggle)
        parameters = {'overwrite':toggle,
                      'value':param}
        store_rendersettings(file_num, 'render_device', **parameters)

        # render_samples
        kwargs = {'label':'Render samples', 'step':1,
                  'value':256,
                  'step':256,
                  'min_value': 0,                 
                  'key':f'render_samples_{file_num+1}'}
        param, toggle = render_settings_block(col_param1, col_toggle1, 'number_input', kwargs,
                              checkbox_default=True, settings_toggle=overwrite_toggle)
        parameters = {'overwrite':toggle,
                      'value':param}
        store_rendersettings(file_num, 'render_samples', **parameters)

        # render_noice_threshold
        kwargs = {'label':'Render noice threshold',
                  'value':0.01,
                  'min_value': 0.0,
                #   'format':'%0.3f',
                  'key':f'render_noice_threshold_{file_num+1}'}
        param, toggle = render_settings_block(col_param1, col_toggle1, 'number_input', kwargs,
                                              settings_toggle=overwrite_toggle)
        parameters = {'overwrite':toggle,
                      'value':param}
        store_rendersettings(file_num, 'render_noice_threshold', **parameters)

        # render_resolution_percentage
        kwargs = {'label':'Render resolution, %',
                  'value':100,
                  'step':25,
                  'min_value': 0,
                  'max_value': 100,                                    
                  'key':f'render_resolution_percentage_{file_num+1}'}
        param, toggle = render_settings_block(col_param2, col_toggle2, 'number_input', kwargs,
                              checkbox_default=True, settings_toggle=overwrite_toggle)
        parameters = {'overwrite':toggle,
                      'value':param}
        store_rendersettings(file_num, 'render_resolution_percentage', **parameters)

        # render_denoice
        kwargs = {'label':'Denoice',
                  'value': True,
                  'key':f'render_denoice_{file_num+1}'}
        param, toggle = render_settings_block(col_param2, col_toggle2, 'toggle', kwargs,
                                              settings_toggle=overwrite_toggle)
        parameters = {'overwrite':toggle,
                      'value':param}
        store_rendersettings(file_num, 'render_denoice', **parameters)

        # color_managment
        col1, col2 = st.columns([2,1])      
        col1.write('Color managment')
        overwrite_toggle = col2.toggle(label='Overwrite', value=False, key=f'color_managment_{file_num+1}')

        col_param1, col_toggle1, col_param2, col_toggle2, = st.columns([10,1,10,1])
    
        # view_transform
        kwargs = {'label':'View Transform','options':['Filmic', 'AgX', 'Raw', 'Standart'],
                  'index':1,
                  'key':f'view_transform_{file_num+1}'}
        view_transform, toggle = render_settings_block(col_param1, col_toggle1, 'selectbox', kwargs,
                                              checkbox=False, settings_toggle=overwrite_toggle)

        # look
        # Stupid AgX has diffetent names for look. pff.. Now we need 'if' statement cause of that..
        if view_transform == 'AgX':
            kwargs = {'label':'Look','options':['None', 'AgX - Punchy',
                                                'AgX - Greyscale', 'AgX - Very High Contrast',
                                                'AgX - High Contrast', 'AgX - Medium High Contrast',
                                                'AgX - Base Contrast', 'AgX - Medium Low Contrast',
                                                'AgX - Low Contrast', 'AgX - Very Low Contrast'],
                      'index':4,                      
                      'key':f'look_{file_num+1}'}
        else:
            kwargs = {'label':'Look','options':['None', 'Very High Contrast',
                                                'High Contrast', 'Medium High Contrast',
                                                'Medium Contrast', 'Medium Low Contrast',
                                                'Low Contrast', 'Very Low Contrast'],
                      'index':2,                                                  
                      'key':f'look_{file_num+1}'}
        look, toggle = render_settings_block(col_param2, col_toggle2, 'selectbox', kwargs,
                                                checkbox=False, settings_toggle=overwrite_toggle)
        
        parameters = {'overwrite':toggle,
                      'view_transform':view_transform,
                      'look':look}
        store_rendersettings(file_num, 'color_managment', **parameters)
        
    # Render Frames/Animation
    with st.container(border=True):
        st.subheader('Render')

        # file_format
        col1, col2 = st.columns([2,1])      
        col1.write('File format')
        overwrite_toggle = col2.toggle(label='Overwrite', value=False, key=f'file_format_{file_num+1}')

        col_param1, col_toggle1, col_param2, col_toggle2, = st.columns([10,1,10,1])

        # format
        kwargs = {'label':'Format','options':['PNG', 'JPEG'],
                  'index':0,
                  'key':f'format_{file_num+1}'}
        format, format_toggle = render_settings_block(col_param1, col_toggle1, 'radio', kwargs,
                                              checkbox=False, settings_toggle=overwrite_toggle)
        
        # color_mode
        if format == 'PNG':
            kwargs = {'label':'Color mode','options':['BW', 'RGB', 'RGBA'],
                      'index':1,                      
                      'key':f'color_mode_{file_num+1}'}
        elif format == 'JPEG':
            kwargs = {'label':'Color mode','options':['BW', 'RGB'],
                      'index':1,                       
                      'key':f'color_mode_{file_num+1}'}
        color_mode, toggle = render_settings_block(col_param2, col_toggle2, 'selectbox', kwargs,
                                                checkbox=False, settings_toggle=overwrite_toggle)
        
        # film_transparent
        kwargs = {'label':'Film transparent',
                  'value':False,
                  'key':f'film_transparent_{file_num+1}'}
        film_transparent, toggle = render_settings_block(col_param1, col_toggle1, 'toggle', kwargs,
                                                checkbox=False, settings_toggle=overwrite_toggle)
        
        # overwrite_files
        kwargs = {'label':'Overwrite files',
                  'value':True,
                  'key':f'overwrite_files_{file_num+1}'}
        overwrite_files, toggle = render_settings_block(col_param2, col_toggle2, 'toggle', kwargs,
                                                checkbox=False, settings_toggle=overwrite_toggle)
        
        parameters = {'overwrite':toggle,
                      'format':format,
                      'color_mode':color_mode,
                      'film_transparent':film_transparent,
                      'overwrite_files':overwrite_files}
        store_rendersettings(file_num, 'file_format', **parameters)
 
        col_param1, col_toggle1 = st.columns([9,1])

        # render_type
        kwargs = {'label':'Render type', 'options':['Frames', 'Animation'],
                      'horizontal':True,
                      'label_visibility':'collapsed',
                      'key':f'render_type_{file_num+1}'}
        render_scheme, toggle = render_settings_block(col_param1, col_toggle1, 'radio', kwargs,
                              checkbox=False)
        
        if render_scheme == 'Frames':
            enabled = True
        elif render_scheme == 'Animation':
            enabled = False
        # frame_range
        kwargs = {'label':'Frame range',
                    'placeholder':'1,3..7,9,10',
                    'key':f'frame_range_{file_num+1}'}
        frame_range, toggle = render_settings_block(col_param1, col_toggle1, 'text_input', kwargs,
                              checkbox=False, settings_toggle=enabled)
        parameters = {'render_type':render_scheme,
                      'frame_range':frame_range,}
        store_rendersettings(file_num, 'render', **parameters)



def render_settings_block(col_param, col_toggle, widget, kwargs,
                          checkbox_default=False, checkbox=True,
                          settings_toggle=True):
    """
    Helperfunction for draw_render_settings()
    Draws single render setting with desired widget,
    Saves parameters to session_state files_data render_settings
    """

    if checkbox:
        with col_toggle:
            key = kwargs['key']
            unique_key = f'overwrite_{key}'
            toggle = st.checkbox(label='overwrite', value=checkbox_default,
                                disabled=not settings_toggle,
                                label_visibility='hidden', key=unique_key)
        if not settings_toggle:
            toggle = settings_toggle
    else:
        toggle = True
        if not settings_toggle:
            toggle = settings_toggle
    with col_param:
        param = getattr(st, widget)(disabled=not toggle, **kwargs)  # To draw any widget you pass to function

    return param, toggle
    
def store_rendersettings(file_num, state_param, **kwargs):
    """
    Helperfunction for draw_render_settings()
    Stores session_state files_data rendersettings
    """

    st.session_state['files_data'][file_num+1]['render_settings'][state_param]= {}
    for key, value in kwargs.items():
        st.session_state['files_data'][file_num+1]['render_settings'][state_param][key] = value

def draw_stop_button(localization, language):
    """
    Stop button which stops rendering process
    """

    stop_render_bt = st.button('Stop Render')
    if stop_render_bt:
        st.stop()

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
            elif file_data['render_settings']['render']['render_type'] == 'Frames' and file_data['render_settings']['render']['frame_range'] == '':
                return st.write('Input frame range!')
  
        # RENDERING CYCLE
        # Get data from Session_state dict
        for index, file_data in st.session_state['files_data'].items():

            # Saves to .json for other scripts to take data from
            with open('render_file_data.json', 'w+', encoding='utf-8') as dict:
                json.dump(file_data['render_settings'], dict, ensure_ascii=False, indent=4)

            # blender.exe
            blender = BLENDER_PATH
            #.blend file path
            blend_file = file_data['path']
            arg_blend_file = f'-b {blend_file}'
            # Scripts pathes
            scripts_str = file_data['scripts']
            arg_scripts = f'-P {scripts_str}'
            # Scenes
            arg_scenes = scenes2arg_scenes(file_data['selected_scenes'],
                                           file_data['render_settings']['render']['render_type'],
                                           file_data['render_settings']['render']['frame_range'])

            console_command = f'{blender} {arg_blend_file} {arg_scripts} {arg_scenes}'
            # st.write(console_command)
            start_render(console_command)
        
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

# Needs tweaking but MUST DO
def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

