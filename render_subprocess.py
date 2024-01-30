import json, subprocess

from config import (
    BLENDER_PATH,
)

from main_functions import (
    scenes2arg_scenes,
)

# RENDERING CYCLE
# Get data from temp json file
with open('temp_render_file_data.json') as file:
    temp_json = json.load(file)

for index, file_data in temp_json.items():

    use_sid = file_data['use_sid']

    # Saves to .json for scripts that run in blender to take data from
    with open('render_file_data.json', 'w+', encoding='utf-8') as dict:
        json.dump(file_data['render_settings'], dict, ensure_ascii=False, indent=4)

    # blender.exe
    blender = BLENDER_PATH
    #.blend file path
    blend_file = file_data['path']
    arg_blend_file = f'-b "{blend_file}"'
    # Scripts pathes
    arg_scripts = file_data['scripts']
    # Scenes
    arg_scenes = scenes2arg_scenes(file_data['render_settings']['selected_scenes'],
                                file_data['render_settings']['render']['render_type'],
                                file_data['render_settings']['render']['frame_range'])

    if not use_sid:
        console_command = f'"{blender}" {arg_blend_file} {arg_scripts} {arg_scenes}'
    else:
        string = '--python-expr "import bpy;bpy.ops.object.superimagedenoisetemporal_bg()"'
        console_command = f'"{blender}" {arg_blend_file} {arg_scripts}'

    process = subprocess.Popen(console_command,
                            #    stdout=subprocess.PIPE,
                            #    stderr=subprocess.STDOUT,
                            #    universal_newlines=True
                            )

    return_code = process.wait()
    # Ensure exit
    if return_code:
        raise subprocess.CalledProcessError(return_code, console_command)
