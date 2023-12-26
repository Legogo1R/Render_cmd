import bpy
import sys, json, os

MAIN_PATH = 'f:\\Library\\Blender_Work\\3Devision\\Scripts\\Render_cmd'

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
    file_name = os.path.sep.join([MAIN_PATH,'.temp', 'scenes.json'])

    with open(file_name, 'w+', encoding='utf-8') as txt:
        json.dump(scenes, txt, ensure_ascii=False, indent=4)

