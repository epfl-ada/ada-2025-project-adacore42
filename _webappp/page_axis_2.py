import streamlit as st
from pages_data import PagesData, dataA

pageData = PagesData.AXIS_2.value

pageData.page_firstBlock()



# Prepare only the two columns we need
plot_df = dataA[0][["votes", "funny"]].copy()

# Show line chart
plot_df