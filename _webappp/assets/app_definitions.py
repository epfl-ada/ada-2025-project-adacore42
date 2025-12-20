from enum import Enum
import streamlit as st



class AppParams:
    expanders = True
    

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
    


class HomePageAxis_C: 

    def __init__(self, title: str, description: str, axisPath):
        self.title = title
        self.description = description
        self.axisPath = axisPath
        self.render()
        
    def render(self):

        col1, col2 = st.columns([4, 3])
        with col1:
            # st.markdown(f"**{self.title}**")
            st.write(self.description)
            
        with col2:
            if st.button(self.title, key=self.axisPath, type="primary", width=500):
                st.switch_page(self.axisPath)



        



def get_absolute_project_root():
    import sys
    from pathlib import Path


    root = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    while root.parent != root:
        if ((root / ".git").exists() and 
            (root / "README.txt").exists() and 
            (root / "results.ipynb").exists()): break
        root = root.parent
    if str(root) not in sys.path: sys.path.insert(0, str(root))
    
    return root
