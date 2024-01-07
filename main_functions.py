import os, sys, subprocess, argparse, signal, psutil

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
    tmp_lst = []
    for script_name in scrits_before:
        if script_name != '':  # Checks for empty strings, but still elements of a list
            tmp_lst.append(os.path.sep.join([MAIN_PATH, SCRIPT_PATH, PERM_SCRIPTS_PATH, script_name]))
    str_scripts_before = " ".join(filter(None, tmp_lst))  # Needs to be as 1 string
    
    tmp_lst = []
    for script_name in scripts_after:
        if script_name != '': 
            tmp_lst.append(os.path.sep.join([MAIN_PATH, SCRIPT_PATH, PERM_SCRIPTS_PATH, script_name]))
    str_scripts_after = " ".join(filter(None, tmp_lst))  # Needs to be as 1 string

    # Optional scripts that can be passed as arguments, will be run in between
    tmp_lst = []
    for script_name in scripts_optional:
        if script_name != '':
            tmp_lst.append(os.path.sep.join([MAIN_PATH, SCRIPT_PATH, script_name]))
    str_optional_scripts = " ".join(filter(None, tmp_lst))  # Needs to be as 1 string

    # Concatenate in a single string
    arg_scripts = " ".join(filter(None, (str_scripts_before,str_optional_scripts,str_scripts_after)))
    return arg_scripts


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
    bf.close()

    return scenes

def scenes2arg_scenes(scenes, render_type, frame_range):

    tmp_scenes = []
    if render_type == 'Frames':
        for scene in scenes:
            tmp_scenes.append(f'-S {scene} -f {frame_range}')
    if render_type == 'Animation':
        for scene in scenes:
            tmp_scenes.append(f'-S {scene} -a')
    
    arg_scenes = " ".join(tmp_scenes)  # Needs to be as 1 string
    return arg_scenes


def start_render():
    """ 
    Runs blender through command line to render with desired settings
    """

    # -u for real time printing stdout (not using buffer)
    command = [sys.executable, '-u', 'render_subprocess.py']
    with open ('render_log.txt', 'w') as f:  # Redirect stdout to .txt, to display in streamlit
        process = subprocess.Popen(command,
                            stdout=f,
                            # stderr=subprocess.STDOUT,
                            # universal_newlines=True
                            )

    return process
    
def kill_render(process):
    """ 
    Kills current rendering by terminating subprocess group
    """

    parent = psutil.Process(process.pid)
    children = parent.children(recursive=True)
    for child in children:
        # child.kill()
        os.kill(child.pid, signal.SIGINT)  # SIGINT looks safer then kill(), but i dunno..
    # gone, still_alive = psutil.wait_procs(children, timeout=2)
    # parent.kill()
    os.kill(parent.pid, signal.SIGINT)
    parent.wait(3)

def search_sort_log(file):
    """
    Extract data from log
    """

    # extracted_data = {}
    # extracted_data['valid'] = False
    # extracted_data['frame'] = 'N/A'
    # extracted_data['time'] = 'N/A'
    # extracted_data['remaining'] = 'N/A'
    # extracted_data['scene'] = 'N/A'
    # extracted_data['viewlayer'] = 'N/A'

    with open (file, 'rb') as f:
            # Take last line from file
            try:  # catch OSError in case of a one line file 
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()
            if last_line.startswith('Fra:'):
                return last_line
            return None
                # extracted_data['valid'] = True
                # frame_start_idx = 4
                # frame_end_idx = last_line.find('Mem:')
                # extracted_data['frame'] = int(last_line[frame_start_idx:frame_end_idx])

                # time_idx = last_line.find('Time:') + 5
                # extracted_data['time'] = last_line[time_idx:time_idx+8]

                # remainig_idx = last_line.find('Remaining:') + 5
                # if remainig_idx != -1:
                #     extracted_data['remaining'] = last_line[remainig_idx:remainig_idx+8]

                # Not so easy to get Scene and Viewlayer, so a bit of stuff down below..
                # tmp_idx = [i for i in range(len(last_line)) if last_line.startswith('M', i)]
                # scene_start_idx = tmp_idx[5] + 4
                # if last_line.find()
                # if scene_idx != -1:
                #     extracted_data['scene'] = last_line[scene_idx:scene_idx+8]

                # viewlayer_idx = last_line.find('Remaining:') + 5
                # if viewlayer_idx != -1:
                #     extracted_data['viewlayer'] = last_line[viewlayer_idx:viewlayer_idx+8]

    # return extracted_data