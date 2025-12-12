import streamlit as st
import pandas as pd
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import afficher_treemap_html

pageData = PagesData.AXIS_3.value 

pageData.page_firstBlock()
 
afficher_treemap_html("treemap_interactif.html")


"Ouais c'est mon plot let's goooooooooooo"