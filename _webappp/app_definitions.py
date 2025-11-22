from enum import Enum
import streamlit as st






class Tovarisch:
    def __init__(self, title: str, image: str, description: str):
        self.title = title
        self.image = image
        self.description = description





class PageDataFormat:
    TITLE_IMG_DIR = "_webappp/assets/title_img/"
    TitleImageWidth = 400

    def __init__(self, path: str, title: str, pathTitleImg: str = "", description: str = ""):
        self.path = path
        self.title = title
        self.titleImagePath = self.TITLE_IMG_DIR + pathTitleImg 
        self.description = description

    def get_page(self):
        return st.Page(self.path, title=self.title)
    
    def get_titleImage(self, width: int = 400):
        return st.image(self.titleImagePath, width=width)
    
    def get_title(self):
        return st.title(self.title)
    


    def page_firstBlock(self):
        st.title(self.title)
        col1, col2 = st.columns([1, 3], vertical_alignment="center")
        with col1:
            st.image(self.titleImagePath, self.TitleImageWidth)
        with col2:
            st.write(self.description)
        st.divider()
    
