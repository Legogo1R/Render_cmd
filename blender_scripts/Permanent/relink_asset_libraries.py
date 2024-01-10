import bpy
import os, sys

#os.environ['Render_cmd'] = r'f:\Library\Blender_Work\3Devision\Scripts\Render_cmd'

#sys.path.insert(1, os.environ['Render_cmd'])

#from config import ASSET_LIBRARY_PATH
#print(ASSET_LIBRARY_PATH)

bpy.ops.file.find_missing_files(directory=r'f:\Library\Blender_Work\3Devision\T124_SHORT_SOHO_SUITES')