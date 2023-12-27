import os, json, sys
import streamlit as st

from config import *
from main_functions import (
    createParser,
    is_blender_running,
    scripts2string,
    get_scene_names,
    create_arg_scenes,
    start_render
)

from ui import (
    draw_header,
    draw_main_container,
    draw_render_button
)


# Open localization json
path = os.path.sep.join([MAIN_PATH, 'localization.json'])
with open(path, encoding='utf-8') as localiz:
    localiz_dict = json.load(localiz)

cur_language = 'en'

# Inforamtion about wich frames to render
# Taken from rendersettings.json for eqch .blend file
path = os.path.sep.join([MAIN_PATH, 'rendersettings.json'])
with open(path, 'r') as fp:
    config = json.load(fp)

render_frames = config['render_frames']

if __name__ == '__main__':

    draw_header(localiz_dict, cur_language)

    draw_main_container(localiz_dict, cur_language)

    # draw_render_button(localiz_dict, cur_language)

    st.write(st.session_state)

    # Creating parser to pass parameters to
    parser = createParser()
    args = parser.parse_args(sys.argv[1:])

    # Arguments for rendering througch command line
    
    # arg_blend_file = f'-b {blend_file}'
    # arg_scripts = scripts2string(SCRIPTS_BEFORE,SCRIPTS_AFTER,scripts)
    # arg_scenes = create_arg_scenes(scenes, render_frames)

    # Rendering cycle

    # start_render(arg_blend_file, arg_scripts, arg_scenes)


