from enum import Enum
import streamlit as st
from _webappp.assets.app_definitions import PageDataFormat


class PagesData(Enum):
    HOME       = PageDataFormat("page_home.py",      
                                "Home")

    AXIS_1     = PageDataFormat("page_axis_1.py",     
                                "Axis 1: What Is Considered Funny?", 
                                "515.jpg")

    AXIS_2     = PageDataFormat("page_axis_2.py",     
                                "Axis 2: Professions, Politics, and Power", 
                                "545.jpg")

    AXIS_3     = PageDataFormat("page_axis_3.py",     
                                "Behind the Punchline: The representation of gender", 
                                "582.jpg")
    
    ABOUTUS    = PageDataFormat("page_aboutus.py",   
                                "About Us")


myPages = {
    "ADACore42 navigation bar:": [
        PagesData.HOME.value.get_page(),
        PagesData.AXIS_1.value.get_page(),
        PagesData.AXIS_2.value.get_page(),
        PagesData.AXIS_3.value.get_page(),
        PagesData.ABOUTUS.value.get_page(),

    ]
}




# ---------------------------
# PAGE DESCRIPTIONS 
# ---------------------------

PagesData.HOME.value.description = """
Welcome to ADAcore42!  
This page introduces the project, navigation structure, and quick links.
""".strip()

PagesData.AXIS_1.value.description = """
Axis 1 explores what is considered funny through caption analysis, ..
""".strip()

PagesData.AXIS_2.value.description = """
Axis 2 focuses on political themes, professions, and power dynamics in humor.
""".strip()

PagesData.AXIS_3.value.description = """
Axis 3 study the representation of gender in captions and ... 
""".strip()

PagesData.ABOUTUS.value.description = """
Information about the ADAcore42 team, project goals, methodology, 
and contributors.
""".strip()






