import os, sys, subprocess, argparse, psutil
import re, json

from config import *
from main_functions import (
    createParser,
    is_blender_running,
    scripts2string,
    get_scene_names,
    create_arg_scenes,
    start_render
)


# Inforamtion about wich frames to render
# Taken from rendersettings.json for eqch .blend file
path = os.path.sep.join([MAIN_PATH, 'rendersettings.json'])
with open(path, 'r') as fp:
    config = json.load(fp)

render_frames = config['render_frames']



if __name__ == '__main__':

    if is_blender_running:
        answer = input('Another instance of Blender is already running! Are you sure you want to start render now?\n(Type y/n)\n')
        if answer.lower() == 'y':
            pass
        else:
            print('Render aborted!')
            exit()

    # Creating parser to pass parameters to
    parser = createParser()
    args = parser.parse_args(sys.argv[1:])

    # Arguments for rendering througch command line
    blend_file = args.blend[0]
    arg_blend_file = f'-b {blend_file}'
    arg_scripts = scripts2string(SCRIPTS_BEFORE,SCRIPTS_AFTER,args.script)


    print('\n..Getting scene names from .blend files..')
    scenes = get_scene_names(blend_file)
    arg_scenes = create_arg_scenes(scenes, render_frames)

    
    # Rendering cycle
    start_render(arg_blend_file, arg_scripts, arg_scenes)