import streamlit as st
from pages_data import PagesData

pageData = PagesData.AXIS_3.value 


pageData.page_firstBlock()
 



# Toggle state stored in session
if "cy_toggle" not in st.session_state:
    st.session_state.cy_toggle = False

# One toggle button
if st.button("Appuie ici, Cyrielle", type="primary"):
    st.session_state.cy_toggle = not st.session_state.cy_toggle

# Output
if st.session_state.cy_toggle:
    st.write("Ce bouton est pour toi!")
else:
    st.write("En attente du appuyage...")