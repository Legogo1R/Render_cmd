import os, json, sys
import streamlit as st

from config import *
from main_functions import (
    createParser,
    is_blender_running,
    start_render
)

from web_ui import (
    draw_header,
    draw_main_container,
    draw_render_button
)


# Open localization json
path = os.path.sep.join([MAIN_PATH, 'localization.json'])
with open(path, encoding='utf-8') as localiz:
    localiz_dict = json.load(localiz)

cur_language = 'en'


if __name__ == '__main__':

    draw_header(localiz_dict, cur_language)

    draw_main_container(localiz_dict, cur_language)

    # Rendering cycle
    draw_render_button(localiz_dict, cur_language)

    st.write(st.session_state)
