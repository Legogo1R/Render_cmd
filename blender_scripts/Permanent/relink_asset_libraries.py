import bpy
import os, sys, glob

sys.path.insert(1, os.environ['Render_cmd'])

from config import ASSET_LIBRARY_PATH


def find_missing_file(folder, file):
    """
    Recursively find path in a given folder
    to given file name
    """

    for file_path in glob.glob(f'{folder}/**/{file}', recursive=True):
        return file_path

for linked_file in bpy.data.libraries:

    split = linked_file.name.rsplit('.', 1)
    if split[-1] == 'blend':
        file_name = linked_file.name
    else:
        file_name = split[0]

    file_path = find_missing_file(ASSET_LIBRARY_PATH, file_name)
    if file_path != None:
        print(file_path)
        linked_file.filepath = file_path

    try:
        bpy.data.libraries[linked_file.name].reload()
    except:
        pass