import sys
import bpy
import json

with open('F:\\Library\\Blender_Work\\3Devision\\Scripts\\Render_cmd\\config.json', 'r') as fp:
    config = json.load(fp)

animation_or_frames = config['scene_name_generator_for_cmd']['animation_or_frames']
frame_range = config['scene_name_generator_for_cmd']['frame_range']

#If you need only one frame, make frame_start = frame_end
#"a" for animation, "f" for set of frames
def scene_names_generator():
    scene_names_for_cmd = ""
    if animation_or_frames == "a":
        for scene in bpy.data.scenes:
            scene_names_for_cmd += "-S {} -{} ".format(scene.name, animation_or_frames)
    else:
        for scene in bpy.data.scenes:
            scene_names_for_cmd += "-S {} -{} {} ".format(scene.name, animation_or_frames, frame_range)
    return scene_names_for_cmd

if __name__ == "__main__":
    print(scene_names_generator(), file=sys.stderr)