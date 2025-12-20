from enum import Enum
import streamlit as st
from src.utils.general_utils import plot_html



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












class ImageCaptionCenter_C:
    def __init__(self, image_path, caption, center_ratio=2):
        """
        center_ratio: relative width of the middle column
        """
        self.center_ratio = center_ratio
        self.image_path = image_path
        self.caption = caption
        self.render()


    def render(self):
        col_l, col_c, col_r = st.columns([1, self.center_ratio, 1])

        with col_c:
            st.image(
                self.image_path,
                use_container_width=True
            )

            st.markdown(
                f"""
                <div style="text-align:center; margin-top: 0.75rem;">
                    <h5>{self.caption}</h5>
                </div>
                """,
                unsafe_allow_html=True
            )



















class TwoTabGraph_C:
    def __init__(
        self,
        label_1,
        path_1,
        label_2,
        path_2,
        center_ratio=3,
        height=450,
        isImage=False,
        additionalComponent_1=None,
        additionalComponent_2=None,
    ):
        self.label_1 = label_1
        self.path_1 = path_1
        self.label_2 = label_2
        self.path_2 = path_2
        self.center_ratio = center_ratio
        self.height = height
        self.isImage = isImage
        self.additionalComponent_1 = additionalComponent_1
        self.additionalComponent_2 = additionalComponent_2

        self.render()

    def render(self):
        st.markdown(
            """
            <style>
            div[data-testid="stTabs"] div[data-baseweb="tab-list"]{
                display: flex !important;
                justify-content: center !important;
                width: 100% !important;
            }
            div[data-testid="stTabs"] {
                width: 100% !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        tab1, tab2 = st.tabs([self.label_1, self.label_2])

        with tab1:
            col_l, col_c, col_r = st.columns([1, self.center_ratio, 1])
            with col_c:
                if self.isImage:
                    st.image(self.path_1, width=1000)
                else:
                    plot_html(self.path_1, height=self.height)

                if callable(self.additionalComponent_1):
                    self.additionalComponent_1()

        with tab2:
            col_l, col_c, col_r = st.columns([1, self.center_ratio, 1])
            with col_c:
                if self.isImage:
                    st.image(self.path_2, width=1000)
                else:
                    plot_html(self.path_2, height=self.height)

                if callable(self.additionalComponent_2):
                    self.additionalComponent_2()