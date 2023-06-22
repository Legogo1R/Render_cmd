import bpy

D = bpy.data
view_layer_names = []

for scene in D.scenes:
    if scene.use_nodes == True:
        for node in scene.node_tree.nodes:
            if node.type == 'R_LAYERS':
                node.mute = False
                view_layer_names.append(node.layer)

        for vl in scene.view_layers:
                if vl.name in view_layer_names:
                    vl.use = True