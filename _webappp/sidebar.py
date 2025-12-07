import streamlit as st
from _webappp.assets.app_content import myPages 
from _webappp.assets.app_definitions import AppParams as AP


def render():

    with st.sidebar:


        AP.expanders = st.toggle("Expand ALL expanders")

        return st.navigation(myPages)

   