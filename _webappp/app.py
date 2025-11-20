import os
import streamlit as st
from app_definitions import *
import app_sidebar
import app_home, app_axis1, app_axis2, app_aboutus

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
# Top-level navigation (PRIMARY NAVBAR)
# -------------------------------------------------------
main_tabs = st.tabs([tab.value.name for tab in MainTabs])

# =======================================================
with main_tabs[MainTabs.HOME.value.id]:
    app_home.render()

with main_tabs[MainTabs.AXIS_1.value.id]:
    app_axis1.render()

with main_tabs[MainTabs.AXIS_2.value.id]:
    app_axis2.render()

with main_tabs[MainTabs.ABOUTUS.value.id]:
    app_aboutus.render()

# =======================================================
# SIDEBAR (ADVANCED)
# =======================================================
with st.sidebar:
    app_sidebar.render()