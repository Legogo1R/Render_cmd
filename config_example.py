BLENDER_PATH = r'path/to/blender.exe'
MAIN_PATH = r'path/to/repository'
SCRIPT_PATH = 'blender_scripts'
PERM_SCRIPTS_PATH = 'Permanent'
MISC_PATH = 'misc'
RSYNC_FOLDER_PATH = r''
ASSET_LIBRARY_PATH = r''

# Scripts will be executed from top - down
# Scripts to run before Optional(Extra) sripts
SCRIPTS_BEFORE = [
    'relink_asset_libraries.py',  # Permanent (Don't remove)
    'rendersettings.py',  # Permanent (Don't remove)
]

# Scripts to run after Optional(Extra) sripts
SCRIPTS_AFTER = [

]