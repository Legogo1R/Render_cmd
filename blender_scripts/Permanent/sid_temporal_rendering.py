import bpy
import os, json

# Need to add repositoriy path to env variable first
#path = os.path.sep.join([os.environ['Render_cmd'], 'render_file_data.json'])
path = r'f:\Library\Blender_Work\3Devision\Scripts\Render_cmd\render_file_data.json'

with open(path, 'r') as fp:
    config = json.load(fp)

sid_settings = {
    'selected_scenes' : config['selected_scenes'],
    'denoiser_type' : config['sid_settings']['denoiser_type'],
    'quality' : config['sid_settings']['quality'],
    'working_directory' : config['sid_settings']['working_directory'],
    'overscan' : config['sid_settings']['overscan'],
    'frame_compensation' : config['sid_settings']['frame_compensation'],
    'smaller_exr_files' : config['sid_settings']['smaller_exr_files'],
    'overwrite_existing_files' : config['sid_settings']['overwrite_existing_files'],
    'denoice_file_format' : config['sid_settings']['denoice_file_format'],
    'file_format_video' : config['sid_frames_to_animation']['value'],
}



# Setting desired settings
for scene in bpy.data.scenes:
   if scene.name in sid_settings['selected_scenes']:

        # Settings
        # Denoicer type
        scene.sid_settings.denoiser_type = sid_settings['denoiser_type']

        # Quality
        scene.sid_settings.quality = sid_settings['quality']

        # Passes to denoice
        bpy.ops.superimagedenoiser.detectpasses()  # Auto detect

        # Working directory
#        scene.sid_settings.working_directory = sid_settings['working_directory']

        # Advanced Settings
        scene.sid_settings.overscan = sid_settings['overscan']
        scene.sid_settings.frame_compensation = sid_settings['frame_compensation']

        # Step 1. Render
        scene.sid_settings.smaller_exr_files = sid_settings['smaller_exr_files']
        scene.render.use_overwrite = sid_settings['overwrite_existing_files']

        # Step 2. Denoice
        # File extension
        scene.sid_settings.file_format = sid_settings['denoice_file_format']

        # Step 3. Frames to Animation
        scene.sid_settings.file_format_video = sid_settings['file_format_video']
    
        context_override = bpy.context.copy()
        context_override["scene"] = bpy.data.scenes['Temporal_Test']
        with bpy.context.temp_override(**context_override):
            bpy.ops.superimagedenoiser.sidtrender()