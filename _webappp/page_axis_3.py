import streamlit as st
import pandas as pd
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_treemap_html, plot_wordcloud

pageData = PagesData.AXIS_3.value 

pageData.page_firstBlock()

plot_wordcloud(r"_Other\amelie_analysis\wordcloud.pkl", "male_adj", "adjectives", "male")
plot_wordcloud(r"_Other\amelie_analysis\wordcloud.pkl", "female_adj", "adjectives", "female")
 
plot_treemap_html(r"_Other\amelie_analysis\topic_male.html")

plot_treemap_html(r"_Other\amelie_analysis\topic_female.html")


"Ouais c'est mon plot let's goooooooooooo"