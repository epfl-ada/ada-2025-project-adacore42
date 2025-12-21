import streamlit as st
from _webappp.assets.app_definitions import Tovarisch
import os

BASE = os.path.dirname(__file__)
tovarischs = [
    Tovarisch("Amélie Menoud", 
              os.path.join(BASE, "assets/profile_img/profile_image.jpeg"), 
              "BSc in Civil Enginnering, MA in Mobility and Transport with a minor in Computer Science. For this project, I was the gender analyst. In general, you can find me playing volleyball at a low level, or on the top lane as Garen."),
    Tovarisch("András Horkay", 
              os.path.join(BASE, "assets/profile_img/profile_image.jpeg"), 
              "Short description of t 2. Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description "),
    Tovarisch("Cyrielle Manissadjian", 
              os.path.join(BASE, "assets/profile_img/864.jpg"), 
              "BSc in Environmental Sciences and Engineering, MA in Climate Change Anticipation and Adaptation.\nFavorite cartoon caption : “Maybe cut the line about following your instincts.”"),
    Tovarisch("Dominic Stratila", 
              os.path.join(BASE, "assets/profile_img/profile_image.jpeg"), 
              "BSc in Microtechnique, MA Robotics with minor in Electrical Engineering. As hobby I love doing pretty same things: 3d prototyping-printing, coding. Recently assembled my personal drone. I also like doing Via Ferratas or climbing."),
    Tovarisch("Katia Todorov", 
              os.path.join(BASE, "assets/profile_img/profile_image.jpeg"), 
              "Short description of t 5. Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description Short description "),
]



st.title("J'ai mis mon chat comme placeholder, enjoy 🐱")
"""
Comme idee vous pouvez mettre: BCs in ..., MA ---, My hobbys..., votre cartoon préféré!
"""
for t in tovarischs:
    st.subheader(t.title)
    col1, col2 = st.columns([1, 4], vertical_alignment="top")
    col1.image(t.image, width=100)        
    col2.write(t.description)
    st.divider()