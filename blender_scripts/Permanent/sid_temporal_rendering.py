import bpy
import os, json

# Need to add repositoriy path to env variable first
#path = os.path.sep.join([os.environ['Render_cmd'], 'render_file_data.json'])
path = r'f:\Library\Blender_Work\3Devision\Scripts\Render_cmd\render_file_data.json'

with open(path, 'r') as fp:
    config = json.load(fp)

sid_settings = {
    'selected_scenes' : config['selected_scenes']
}



# Setting desired settings
for scene in bpy.data.scenes:
    if scene.name in sid_settings['selected_scenes']:

        # Quality
        scene.sid_settings.quality = 'High'
        
        # Passes to denoice
        bpy.ops.superimagedenoiser.detectpasses()  # Auto detect
    
        # Working directory
        scene.sid_settings.working_directory = '//Temporal/'
        
        # Advanced Settings
        scene.sid_settings.overscan = int('5')
        scene.sid_settings.frame_compensation = True
        
        scene.sid_settings.smaller_exr_files = True
        scene.render.use_overwrite = True
