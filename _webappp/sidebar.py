import streamlit as st
import _webappp.assets.app_content as app_content
myPages = app_content.myPages

def render():
     # Title FIRST
    with st.sidebar:

        return st.navigation(myPages)

   