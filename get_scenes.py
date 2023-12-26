import bpy
import sys, json, os
from pathlib import Path

from ...config import TEMP_PATH

def get_scene_names():
    scenes = {}
    for scene in bpy.data.scenes:
        scenes[scene.name] = {}
        
    return scenes


if __name__ == "__main__":

    # get_scene_names()
    main_dir = str(Path(__file__).parents[2])

    # path = os.path.sep.join([os.path.abspath(TEMP_PATH), 'get_scenes.py'])
    # with open()
    


    print(main_dir)
