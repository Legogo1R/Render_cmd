#'render.py' program allows to simplify the process of batch rendering multiple .blend files with certain parameters from command line#

You need 'Python' isntalled and also 'psutil' library

#Caution!#
If you are updating script files, don't forget to change paths to external scripts inside certain scripts themselves

Use 'config.json' to change most common parameters of rendering
Scripts you want to use in this program should be in 'Scripts' folder in the same directory as 'render.py'

#How to#
1.
Open directory with .blend files you want to render
Example:
f: cd f:\Library\Blender_Work\3Devision\T93_Bathtubs_LS\
2.
Run 'render.py' with parameters in any order:
- '-b' or '--blend', then type a name(names) and extension of a .blend file(files) you want to render in any order
- '-s' or '--script'(Optional), then type a name(names) and extension of .py script(scripts) you want to launch, in order they should be executed
- ' -L' (Optional), if you want to render certain scenes. Then you will be asked to select cirtain scenes from a given list

Exmaple:
python f:\Library\Blender_Work\3Devision\Scripts\Render_cmd\render_launch.py -b T93_Bathtub_LS_G1_v3.blend T93_Bathtub_LS_G2_v3.blend T93_Bathtub_LS_G3_v3.blend -s some_script.py