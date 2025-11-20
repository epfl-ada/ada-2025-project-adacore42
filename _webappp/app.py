import streamlit as st
from app_definitions import *
import app_sidebar
import app_home, app_axis1, app_axis2, app_aboutus



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