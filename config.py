import os

SCRIPT_PATH = "Scripts"
PERM_SCRIPTS_PATH = os.path.sep.join([SCRIPT_PATH, "Permanent"])
BLENDER_PATH = 'c:\App\Blender\stable\blender-4.0.0+stable.878f71061b8e\blender.exe'



SCRIPTS_BEFORE = [
    'rendersettings.py',
    'viewlayers_use_for_rendering'
]

SCRIPTS_AFTER = [
    'active_layers_printer.py',

]


