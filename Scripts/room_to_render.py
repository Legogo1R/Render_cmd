import bpy

C = bpy.context
D = bpy.data
room = 'Room_'
room1_name = 'Room_v1'
room2_name = 'Room_v2'
room3_name = 'Room_v3'
room4_name = 'Room_v4'

set = room1_name

for scene in bpy.data.scenes:
    
    # Setting active camera
    scene_name = scene.name
    scene_bath = scene_name

    set_number = set

    camera_name = scene_bath + '_' + set
    print(camera_name)
    
    scene.camera = bpy.data.objects[camera_name]
    
    # Changing output folder
    for node in scene.node_tree.nodes:
        if node.type in ['OUTPUT_FILE']:
            node.base_path += f'_{set}'
           


    for layer in scene.view_layers:
        
        # Кривой выбор нужных коллекций и их children с простановкой галочек
        for collection in  layer.layer_collection.children:      
            if room in collection.name:
                collection.exclude = True
                
                if set in collection.name:
                    collection.exclude = False         
                        
                    for child in collection.children:
                        child.exclude = False

                        for child in child.children:
                            child.exclude = False
                            
                            for child in child.children:
                                child.exclude = False
                                
                                for child in child.children:
                                    child.exclude = False
                                    
                                    for child in child.children:
                                        child.exclude = False
                                        
                                        for child in child.children:
                                            child.exclude = False