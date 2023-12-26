import bpy
import sys, json, os

from config import TEMP_PATH

def get_scene_names():
    """
    Runs inside blender file to dump json file with names
    of all scenes in that blender file
    """

    scenes = {}
    for scene in bpy.data.scenes:
        scenes[scene.name] = {}
    return scenes


if __name__ == "__main__":

    scenes = get_scene_names()
    path = os.path.abspath(TEMP_PATH)

    with open(f'path\\scenes.json', 'w+', encoding='utf-8') as txt:
        json.dump(scenes, txt, ensure_ascii=False, indent=4)

