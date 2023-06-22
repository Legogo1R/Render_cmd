import os, sys, subprocess, argparse, psutil
import re

scripts_path = 'f:\\Library\\Blender_Work\\3Devision\\Scripts\\Render_cmd\\Scripts\\'
scene_name_generator = f'-P {scripts_path}scene_name_generator_for_cmd.py'
rendersettings = f'-P {scripts_path}rendersettings.py'
viewlayers_use_for_rendering = f'-P {scripts_path}viewlayers_use_for_rendering_from_every_scene.py'
active_layers_printer = f'-P {scripts_path}active_layers_printer.py'

#Create example of a class to parse arguments from comand line
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--blend', nargs = '+', required = True, help = 'type a name(names) and extension of a .blend file(files) you want to render in any order')
    parser.add_argument('-s', '--script', nargs = '+', default = '',  help = '(Optional) type a name(names) and extension of .py script(scripts) you want to launch, in order they should be executed')
    parser.add_argument('-L', action='store_true', help = '(Optional) if you want to render certain scenes. Then you will be asked to select cirtain scenes from a given list')
    return parser

if __name__ == '__main__':
    #Checks if blender is already running
    if 'blender.exe'  in (p.name() for p in psutil.process_iter()):
        answer = input('Another instance of Blender is already running! Are you sure you want to start render now?\n(Type y/n)\n')
        if answer == 'y':
            pass
        else:
            print('Render aborted!')
            exit()
    parser = createParser()
    args = parser.parse_args(sys.argv[1:])
    scene_names_string = ''
    scripts_before = f'{rendersettings} {viewlayers_use_for_rendering}'
    scripts_after = f'{active_layers_printer}'
    script = [f'-P {scripts_path}{script_name}' for script_name in args.script]
    script = " ".join(script)
    blender = 'blender.exe'
    print('\n..Getting scene names from .blend files..')
    #Getting scene names cycle
    scene_names_dict = {}
    for file_number, bl in enumerate(args.blend):
        blend = f'-b {bl}'
        #First launch of blender to get scene names
        scene_names = subprocess.run(
            f'{blender} {blend} {scene_name_generator}',
            shell = True,
            capture_output=True
        )
        scene_names_dict[file_number] = scene_names.stderr.strip().decode("utf-8")
        print(f'\n..{bl} Done! [{file_number+1}/{len(args.blend)}]..')

    if args.L == True:
        #Working with scene names to print(scene to index : scene column), input(index), print(selected scenes)
        for i in range(len(args.blend)):
            print(f'\n..Type in Indexes of Scenes you want to render for {args.blend[i]}, enumerated through \'space\'..\n\
- Hit "Enter" to render no scenes\n\
- Type in "a" to render all scenes\n')
            splited_list = re.split(r"(\s+-a\s+|\s+-a|\s-f\s+\d\s+|\s-f\s+\d|\s-f\s+\d..\d\s+|\s-f\s+\d..\d|\s-f\s+\d,\d\s+|\s-f\s+\d,\d)", scene_names_dict[i])
            del splited_list[-1]
            scene_names_list = []
            scenes = [] #For printing only selected '-S Scene'
            number_of_scenes = []
            for index in range(len(splited_list)//2):
                number_of_scenes.append(str(index))
                scene_names_list.append(f"{splited_list[2*index]}{splited_list[2*index + 1]}")
                temp_str = f"{splited_list[2*index]}"
                scenes.append(f"{splited_list[2*index]} ")
                print(f'{index} : {temp_str}')
            # Waits for input of scene's indexes and then append them to script string
            scenes_index_list = input()
            temp_scene_names_list = []
            temp_scenes = '' #For printing only selected '-S Scene'
            while all(
                scenes_index_list == 'a'
                or scenes_index_list == ''
                or x in number_of_scenes for x in scenes_index_list.split(' ')
                ) == False:
                scenes_index_list = input('Wrong input\n')
            else:
                if scenes_index_list == 'a':
                    temp_scenes = 'All Scenes to render'
                elif scenes_index_list == '':
                    scene_names_dict[i] = ""
                    temp_scenes = '0 Scenes to render'
                else:
                    scenes_index_list = scenes_index_list.split(' ')
                    for index in scenes_index_list:
                        temp_scene_names_list.append(scene_names_list[int(index)])
                        scene_names_dict[i] = " ".join(temp_scene_names_list)
                        temp_scenes += scenes[int(index)]
            print(f'..You have selected {temp_scenes}..')
    else:
        pass
    # Rendering cycle
    for file_number, bl in enumerate(args.blend):
        blend = f'-b {bl}'
        scenes_to_render = scene_names_dict[file_number]
        print(f'###################\n{blender} {blend} {scripts_before} {script} {scripts_after} {scenes_to_render}\n###################')

        # Second launch of blender to render
        render = subprocess.run(
            f'{blender} {blend} {scripts_before} {script} {scripts_after} {scenes_to_render}',
            shell = True
        )