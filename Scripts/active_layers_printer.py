import bpy

unmuted_nodes = []

print('\n..View Layers that has "Use for rendering" chekbox..')

for scene in bpy.data.scenes:
    if scene.use_nodes == True:
        for node in scene.node_tree.nodes:
            if node.type == 'R_LAYERS' and node.mute == False:
                unmuted_nodes.append(node.layer)

    #Prints Layers per scene that will be rendered
    print(f'{scene.name}\n{unmuted_nodes}\n###################')
    unmuted_nodes.clear()