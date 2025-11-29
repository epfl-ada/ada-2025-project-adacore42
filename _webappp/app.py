import os
import streamlit as st
from app_definitions import *
import sidebar as sidebar
import page_home, page_axis_1, page_axis_2 , page_axis_3, page_aboutus, pages_data

myPages = pages_data.myPages

# Base folder of app.py
BASE = os.path.dirname(__file__)

# Correct full path to CSS file
css_path = os.path.join(BASE, "assets/app_design.css")

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS BEFORE rendering UI
load_css(css_path)









st.sidebar.title("ADAcore42")


st.set_page_config(
    page_title="ADACore42",
    layout="wide",
)

# -------------------------------------------------------
# -------------------------------------------------------

pg = st.navigation(myPages, position="top")

pg.run()
# =======================================================
# SIDEBAR (ADVANCED)
# =======================================================
with st.sidebar:
    sidebar.render()