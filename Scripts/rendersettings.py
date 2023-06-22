import bpy
import json

with open('f:\\Library\\Blender_Work\\3Devision\\Scripts\\Render_cmd\\config.json', 'r') as fp:
    config = json.load(fp)

render_settings = {
    'use_rendersettings_overwrite' : config['rendersettings']['use_rendersettings_overwrite'],
    'render_scheme' : config['rendersettings']['render_scheme'],
    'samples' : config['rendersettings']['samples'],
    'resolution_x' : config['rendersettings']['resolution_x'],
    'resolution_y' : config['rendersettings']['resolution_y'],
    'resolution_percentage' : config['rendersettings']['resolution_percentage'],
    'use_render_output_overwrite' : config['rendersettings']['use_render_output_overwrite'],
    'render_output' : config['rendersettings']['render_output'],
    'file_format' : config['rendersettings']['file_format'],
    'color_mode' : config['rendersettings']['color_mode']
}

def change_rendersettings(settings):

    #Use 'CUDA' or 'OPTIX' to change render scheme
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = settings['render_scheme']
    # bpy.context.preferences.addons['cycles'].preferences.devices[0].use = True
    # bpy.context.preferences.addons['cycles'].preferences.devices[1].use = False

    for scene in bpy.data.scenes:
        
        """Render Properties"""
        # scene.render.engine = "CYCLES"
        # scene.cycles.device = "GPU"
        
        #Sampling
        scene.cycles.use_adaptive_sampling = True
        scene.cycles.adaptive_threshold
        scene.cycles.samples = settings['samples']
        scene.cycles.adaptive_min_samples = 0
        scene.cycles.time_limit = 0
        scene.cycles.use_denoising = True
        if settings['render_scheme'] == 'OPTIX':
            scene.cycles.denoiser = 'OPTIX'
            scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
        else:
            scene.cycles.denoiser = 'OPENIMAGEDENOISE'
            scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'

        #Format
        scene.render.resolution_x = settings['resolution_x']
        scene.render.resolution_y = settings['resolution_y']
        scene.render.resolution_percentage = settings['resolution_percentage']
        scene.render.use_border = False

        #LightPaths
        #  scene.cycles.max_bounces = 32
        #  scene.cycles.diffuse_bounces = 12
        #  scene.cycles.glossy_bounces = 12
        #  scene.cycles.transmission_bounces = 12
        #  scene.cycles.volume_bounces = 12
        #  scene.cycles.transparent_max_bounces = 12
        
        #Clamping
    #    scene.cycles.sample_clamp_direct = 0
    #    scene.cycles.sample_clamp_indirect = 80
        
        #Caustics
        scene.cycles.blur_glossy = 1
        scene.cycles.caustics_reflective = True
        scene.cycles.caustics_refractive = True
        
        #Simplify
        scene.render.use_simplify = False
        
        #Performance
        if settings['render_scheme'] == 'OPTIX':
            scene.cycles.use_auto_tile = False
            scene.cycles.tile_size = 1536
        else:
            scene.cycles.use_auto_tile = True
            scene.cycles.tile_size = 128
        
        scene.cycles.debug_use_spatial_splits = False
        scene.cycles.debug_use_hair_bvh = True
        scene.render.use_persistent_data = False
        
        #Color Management
        scene.view_settings.view_transform = 'Filmic'
        scene.view_settings.look = 'High Contrast'
        # scene.view_settings.exposure = 0
        scene.view_settings.gamma = 1
        scene.sequencer_colorspace_settings.name = 'sRGB'
        
        
        """Output Properties"""
        
        #Frame Range
    #    scene.frame_start = 1
    #    scene.frame_end = 3
        
        

        
        #Post Processing
        scene.render.use_compositing = True
        scene.render.use_sequencer = True

def change_output(settings):

    #Output
    scene.render.filepath = settings['render_output']
    scene.render.use_file_extension = True
    scene.render.image_settings.file_format = settings['file_format']

    #Use 'PNG' or 'JPEG' to change file format
    if settings['file_format'] == 'PNG':
        scene.render.image_settings.color_mode = settings['color_mode']
        scene.render.image_settings.color_depth = '8'
        scene.render.image_settings.compression = 50
        scene.render.use_overwrite = True
    if settings['file_format'] == 'JPEG':
        scene.render.image_settings.color_mode = settings['color_mode']
        scene.render.image_settings.quality = 90
        scene.render.use_overwrite = True
    else:
        pass

    for scene in bpy.data.scenes:
        scene.render.filepath = settings['render_output']
        for node in scene.node_tree.nodes:
            if node.type == 'OUTPUT_FILE':
                temp_path = node.base_path.rsplit('\\', 2)
                new_path = f"{settings['render_output']}{temp_path[1]}\\"
                node.base_path = new_path
                node.format.file_format = settings['file_format']
                if settings['file_format'] == 'PNG':
                    node.format.color_mode = settings['color_mode']
                    node.format.color_depth = '8'
                    node.format.compression = 50
                if settings['file_format'] == 'JPEG':
                    node.format.color_mode= settings['color_mode']
                    node.format.quality = 90
                else:
                    pass

if __name__ == "__main__":
    if render_settings['use_render_output_overwrite'] == True:
        change_output(render_settings)
    if render_settings['use_rendersettings_overwrite'] == True:
        change_rendersettings(render_settings)