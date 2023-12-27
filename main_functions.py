import os, sys, subprocess, argparse, psutil
import re, json

import blendfile
from config import (
    SCRIPT_PATH,
    PERM_SCRIPTS_PATH,
    BLENDER_PATH,
    MAIN_PATH
)


def createParser():
    """
    Create instanse of a class to parse arguments from comand line
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--blend', nargs = '+', required = True, help = 'type a name(names) and extension of a .blend file(files) you want to render in any order')
    parser.add_argument('-s', '--script', nargs = '+', default = '',  help = '(Optional) type a name(names) and extension of .py script(scripts) you want to launch, in order they should be executed')
    parser.add_argument('-L', action='store_true', help = '(Optional) if you want to render certain scenes. Then you will be asked to select cirtain scenes from a given list')
    return parser

def is_blender_running():
    """
    Check if blender is already oppened on the server
    """
    
    return 'blender.exe'  in (p.name() for p in psutil.process_iter())

def scripts2string(scrits_before, scripts_after, scripts_optional):
    """
    Converts scripts' pathes to single string needed as a command line argument
    """

    # Permanent scripts that should be run before and after optional scripts
    if scrits_before:
        tmp_lst = []
        for script_name in scrits_before:
            tmp_lst.append(os.path.sep.join([MAIN_PATH, PERM_SCRIPTS_PATH, script_name]))
        arg_scripts_before = " ".join(tmp_lst)  # Needs to be as 1 string
    
    if scripts_after:
        tmp_lst = []
        for script_name in scripts_after:
            tmp_lst.append(os.path.sep.join([MAIN_PATH, PERM_SCRIPTS_PATH, script_name]))
        arg_scripts_after = " ".join(tmp_lst)  # Needs to be as 1 string

    # Optional scripts that can be passed as arguments, will be run in between
    if scripts_optional:
        tmp_lst = []
        for script_name in scripts_optional:
            tmp_lst.append(os.path.sep.join([MAIN_PATH, SCRIPT_PATH, script_name]))
        arg_optional_scripts = " ".join(tmp_lst)  # Needs to be as 1 string

    return f'-P {arg_scripts_before} {arg_optional_scripts} {arg_scripts_after}'

# Unbeliveable shit below.. who could have guessed that you can do that..
def get_scene_names(blend_file):
    """
    Get scene names from a blend file without even opening it ! WHAAAT?!
    """

    def get_id_name(block):
        name = block[b'id', b'name'].decode()
        return name[2:]

    bf = blendfile.open_blend(blend_file)
    scene_block = bf.find_blocks_from_code(b'SC')
    scenes = [get_id_name(sc) for sc in scene_block]
    print(scenes)
    bf.close()

    return scenes

def create_arg_scenes(scenes, render_frames):

    tmp_scenes = []
    if render_frames['render'] == 'f':
        for scene in scenes:
            tmp_scenes.append(f'-S {scene} -f {render_frames["frames"]}')
    if render_frames['render'] == 'a':
        for scene in scenes:
            tmp_scenes.append(f'-S {scene} -a')
    
    arg_scenes = " ".join(tmp_scenes)  # Needs to be as 1 string
    return arg_scenes


def start_render(arg_blend_file, arg_scripts, arg_scenes):
    """ 
    Runs blender through command line to render with desired settings
    """

    blender = BLENDER_PATH
    render = subprocess.run(
            f'{blender} {arg_blend_file} {arg_scripts} {arg_scenes}',
            shell = True
        )