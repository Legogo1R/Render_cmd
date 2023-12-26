import os, json
import streamlit as st
from config import MAIN_PATH

# Open localization json
path = os.path.sep.join([MAIN_PATH, 'localization.json'])
with open(path, encoding='utf-8') as localiz:
    localiz_dict = json.load(localiz)

cur_language = 'en'

st.title(localiz_dict['main_title_1'][cur_language])