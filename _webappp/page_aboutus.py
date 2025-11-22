import streamlit as st
from app_definitions import Tovarisch
import os

BASE = os.path.dirname(__file__)
tovarischs = [
    Tovarisch("Amélie Menoud", 
              os.path.join(BASE, "assets/profile_img/profile_image.jpeg"), 
              "Short description of t 1. Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description "),
    Tovarisch("András Horkay", 
              os.path.join(BASE, "assets/profile_img/profile_image.jpeg"), 
              "Short description of t 2. Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description "),
    Tovarisch("Cyrielle Manissadjian", 
              os.path.join(BASE, "assets/profile_img/profile_image.jpeg"), 
              "Short description of t 3. Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description "),
    Tovarisch("Dominic Stratila", 
              os.path.join(BASE, "assets/profile_img/profile_image.jpeg"), 
              "Short description of t 4. Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description "),
    Tovarisch("Katia Todorov", 
              os.path.join(BASE, "assets/profile_img/profile_image.jpeg"), 
              "Short description of t 5. Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description "),
]



st.title("J'ai mis mon chat comme placeholder, enjoy 🐱")

for t in tovarischs:
    st.subheader(t.title)
    col1, col2 = st.columns([1, 4], vertical_alignment="top")
    col1.image(t.image, width=100)        
    col2.write(t.description)
    st.divider()