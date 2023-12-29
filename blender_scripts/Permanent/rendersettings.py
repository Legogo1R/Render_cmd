import bpy
import json

with open('f:\\Library\\Blender_Work\\3Devision\\Scripts\\Render_cmd\\render_file_data.json', 'r') as fp:
    config = json.load(fp)

render_settings = {
    'render_scheme' : config['render_settings']['render_scheme'],
    'render_device' : config['render_settings']['render_device'],
    'render_samples' : config['render_settings']['render_samples'],
    'render_noice_threshold' : config['render_settings']['render_noice_threshold'],
    'render_denoice' : config['render_settings']['render_denoice'],
    'render_resolution_percentage' : config['render_settings']['render_resolution_percentage'],
    # 'light_paths' : config['render_settings']['light_paths'],
    'color_managment' : config['render_settings']['color_managment'],
    'render_output_location' : config['render_settings']['render_output_location'],
    'file_format' : config['render_settings']['file_format'],
}

def change_rendersettings(scene, settings):
    """Function cycles through most common Render properties
    and overwrites them if needed.
    """

    # Device, samples, noice, denoice
    if settings['render_device']['overwrite']:
        scene.cycles.device = settings['render_device']['value']

    if settings['render_samples']['overwrite']:
        scene.cycles.samples = settings['render_samples']['value']

    if settings['render_noice_threshold']['overwrite']:
        scene.cycles.use_adaptive_sampling = True
        scene.cycles.adaptive_threshold = settings['render_noice_threshold']['value']

    if settings['render_noice_threshold']['overwrite']:
        scene.cycles.use_denoising = settings['render_denoice']['value']
        scene.cycles.denoiser = 'OPTIX'
        scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
  
    # Resolution
    scene.render.use_border = False
    if settings['render_resolution_percentage']['overwrite']:
        scene.render.resolution_percentage = settings['render_resolution_percentage']['value']

    # LightPaths
    # if settings['light_paths']['overwrite']:
    #     scene.cycles.max_bounces = settings['light_paths']['channels']['total']
    #     scene.cycles.diffuse_bounces = settings['light_paths']['channels']['diffuse']
    #     scene.cycles.glossy_bounces = settings['light_paths']['channels']['glossy']
    #     scene.cycles.transmission_bounces = settings['light_paths']['channels']['transmission']
    #     scene.cycles.volume_bounces = settings['light_paths']['channels']['volume']
    #     scene.cycles.transparent_max_bounces = settings['light_paths']['channels']['transparent']
    
    #Clamping
#    scene.cycles.sample_clamp_direct = 0
#    scene.cycles.sample_clamp_indirect = 80
    
    #Performance
    if settings['render_scheme'] == 'OPTIX':
        scene.cycles.use_auto_tile = False
        scene.cycles.tile_size = 1536
    else:
        scene.cycles.use_auto_tile = True
        scene.cycles.tile_size = 128
    
    # scene.cycles.debug_use_spatial_splits = False
    # scene.cycles.debug_use_hair_bvh = True
    # scene.render.use_persistent_data = False
    
    #Color Management
    if settings['color_managment']['overwrite']:
        scene.view_settings.view_transform = settings['color_managment']['view_transform']
        scene.view_settings.look = settings['color_managment']['look']
        scene.sequencer_colorspace_settings.name = settings['color_managment']['colorspace']
    
    """Output Properties"""
    
    #Frame Range
#    scene.frame_start = 1
#    scene.frame_end = 3
    
    #Post Processing
    scene.render.use_compositing = True
    scene.render.use_sequencer = True


def change_output(scene, settings):
    """Function cycles through most common Output properties
    and overwrites them if needed.
    """

    #Output
    if settings['render_output_location']['overwrite']:
        scene.render.filepath = settings['render_output_location']['value']
        scene.render.use_file_extension = True

        # Output in output nodes
        for node in scene.node_tree.nodes:
            if node.type == 'OUTPUT_FILE':
                cur_path = node.base_path

                if 'renders' in cur_path.lower():
                    tmp_path = cur_path.split('\\', 1)[1]
                    new_path = f"{settings['render_output_location']['value']}\{tmp_path}"
                else:
                    tmp_path = cur_path.split('//', 1)[1]
                    new_path = f"{settings['render_output_location']['value']}\{tmp_path}"
                node.base_path = new_path

    # Format
    if settings['file_format']['overwrite']:
        scene.render.image_settings.file_format = settings['file_format']['format']
        scene.render.image_settings.color_mode = settings['file_format']['color_mode']
        scene.render.use_overwrite = settings['file_format']['overwrite_files']

        if settings['file_format']['format'] == 'PNG':
            scene.render.image_settings.color_depth = '8'
            scene.render.image_settings.compression = 50
        if settings['file_format']['format'] == 'JPEG':
            scene.render.image_settings.quality = 90
        else:
            pass

        # Format in output nodes
        for node in scene.node_tree.nodes:
            if node.type == 'OUTPUT_FILE':
                node.format.file_format = settings['file_format']['format']
                node.format.color_mode = settings['file_format']['color_mode']
                
                if settings['file_format']['format'] == 'PNG':
                    node.format.color_depth = '8'
                    node.format.compression = 50
                if settings['file_format']['format'] == 'JPEG':
                    node.format.quality = 90
                else:
                    pass

if __name__ == "__main__":

    #Use 'CUDA' or 'OPTIX' to change render scheme
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = render_settings['render_scheme']['value']

    for scene in bpy.data.scenes:
        change_rendersettings(scene, render_settings)
        change_output(scene, render_settings)