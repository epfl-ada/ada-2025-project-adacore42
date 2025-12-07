import os
import streamlit as st
from _webappp.assets.app_definitions import *
import sidebar as sidebar
import _webappp.assets.app_content as app_content

myPages = app_content.myPages

# Base folder of app.py
BASE = os.path.dirname(__file__)

# Correct full path to CSS file
css_path = os.path.join(BASE, "assets/app_design.css")

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS BEFORE rendering UI
load_css(css_path)

st.set_page_config(page_title="ADAcore42", layout="wide")


sidebar.render().run()

