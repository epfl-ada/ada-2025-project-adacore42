import streamlit as st
import plotly.graph_objects as go
import numpy as np
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html
from src.utils.general_utils import plot_cartoon
from _webappp.assets.app_definitions import get_absolute_project_root
get_absolute_project_root()
from src.utils.web_app_plots.app_plots import PWA
from _webappp.assets.app_definitions import AppParams as AP

st.title("Methods")
st.write(
    """
    Welcome to this section, where we present the methods in more details.
    """
)
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Home main structure in containers
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––



with st.container ():
    #st.subheader("Dataset and Pipeline Overview")


    with st.expander("**Dataset**", expanded=AP.expanders):
        st.write(
            """
            - 380+ caption contests  
            - CSV caption tables, metadata JSON 
            - Additionnal dataset : 
                - Occupation list (≈33k curated roles)  
                - Gendered lexicon from *Jailbreak the Patriarchy*  
            """
        )


    with st.expander("**Processing pipeline**", expanded=AP.expanders):
        st.write(
            """
            1. Centralised path + loading utilities  
            2. Data cleaning and consistency checks 
                2.1 Concatenate all 385 CSV in a list of CSV
                2.2 Remove redundant columns (index and rank)
                2.3 Consistency verification 
            3. Construction of a robust *funny score*  
            4. Tokenisation and lemmatisation 
            5. Models for similarity, clustering and gender analysis  
            """
        )

    with st.expander("**Funny score**", expanded=AP.expanders):
        st.write(
            """
            In order to capture how the effect of numbers of votes we decided to develop a new funny metric :   
            """
        )

    with st.expander("**BERTtopic**", expanded=AP.expanders):
        st.write(
            """
            ... 
            """
        )
    st.divider()


