import json, subprocess, time
import streamlit as st

from config import (
    BLENDER_PATH,
)

from main_functions import (
    scenes2arg_scenes,
)

# RENDERING CYCLE
# Get data from temp json file
print('########')
with open('temp_render_file_data.json') as file:
    temp_json = json.load(file)

for index, file_data in temp_json.items():

    # Saves to .json for scripts that run in blender to take data from
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

    process = subprocess.Popen(console_command,
                            #    stdout=subprocess.PIPE,
                            #    stderr=subprocess.STDOUT,
                            #    universal_newlines=True
                            )
    process.wait()
