import bpy

C = bpy.context
D = bpy.data


# Set of view_layer_names used in the compositor
view_layer_names = set()

for scene in D.scenes:
    
    if scene.use_nodes == True:
        # Turn off "Render single layer"
        scene.render.use_single_layer = False
            
        # Dictionary - render layer node : scene
        rl_comp = {}
        for node in scene.node_tree.nodes:
            if node.type == 'R_LAYERS' and node.mute == False:
                rl_comp[node] = node.scene.name_full
        
        # Gets view layers that will be rendered in every scene and put them in tupple
        rl_scene = [layr for layr, scn in rl_comp.items() if scn == scene.name]
            
        view_layer_names.clear() # Clears set()
        
        # Compares render_layer.names with selected layers to render
        for vl in scene.view_layers:
            if vl.name in set([l.layer for l in rl_scene]):
                view_layer_names.add(vl.name)
    
        # Set use property
        for vl in scene.view_layers:
            if vl.name in view_layer_names:
                vl.use = True
            else:
                vl.use = False
    else:
        view_layer_names.clear()

        for vl in scene.view_layers:
            if vl.use == True:
                view_layer_names.add(vl.name)

# if __name__ == "__main__":
#     print('\n..View Layers that has "Use for rendering" chekbox..')
#     for scene in D.scenes:
#         #Prints Layers per scene that will be rendered
#         print(f'{scene.name}\n{view_layer_names}\n###################')
