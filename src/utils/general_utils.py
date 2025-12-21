# General utilities
import warnings
import os
from PIL import Image
import streamlit as st
import pickle
import matplotlib.pyplot as plt
    
def absolute_index2contest_index(absolute_idx):
    """
    Fonction to obtain the contest index (e.g. 510) from the absolute index after preprocessing.

    Inputs : absolute index of the contest, obtained from precprocessing [0; 383]
    Outputs : index of the contest as given by The New Yorker Caption Contest [510; 895]

    Exceptions :
    - Contest 525 is suppressed : offset +1 from absolute index 15
    - Contest 540 is suppressed : offset +2 from absolute index 30
    """
    if 0 <= absolute_idx < 15:
        return 510 + absolute_idx
    elif 15 <= absolute_idx < 29:
        return 510 + absolute_idx + 1
    elif 29 <= absolute_idx <= 383:
        return 510 + absolute_idx + 2
    else:
        warnings.warn(f"Absolute index {absolute_idx} is out of valid range [0; 383]. Returning None.")
        return None



def contest_index2absolute_index(contest_idx):
    """
    Fonction to obtain the absolute index [0; 383] from the contest index [510; 895].
    Inputs: contest index as given by The New Yorker Caption Contest [510; 895]
    Outputs: absolute index of the contest, obtained from preprocessing [0; 383]
    Exceptions:
    - Contest 525 is suppressed : offset +1 from absolute index 15
    - Contest 540 is suppressed : offset +2 from absolute index 30
    """
    if contest_idx < 510 or contest_idx > 895:
        warnings.warn(f"Contest index {contest_idx} is out of valid range [510; 895]. Returning None.")
        return None

    if contest_idx < 525:
        return contest_idx - 510

    elif contest_idx < 540:
        return contest_idx - 510 - 1

    else:
        return contest_idx - 510 - 2
    
def drop_NaN(dataA, dataC):
    """
    This function finds the contests with no metadata and drop them in dataA
    and dataC
    Input: dataA, dataC
    Return: dataA_removed, dataC_removed
    """
    dataC_copy = dataC.copy(deep=True)

    # find the where there are no NaN's are in the metadata
    NaN_in_rows = dataC_copy[dataC_copy['image_descriptions'].isna()].index
    # remove them in dataC
    dataC_copy.dropna(subset=['image_descriptions'], inplace=True)
    # Remove the corresponding contests in dataA
    dataA_removed = [x for i, x in enumerate(dataA) if i not in NaN_in_rows]

    return dataA_removed, dataC_copy

def get_contest_id(idx, dataC):
    """
    Find the contest id based on the index of one element of dataA
    Return: contest_id
    """
    contest_id = dataC.iloc[idx]['contest_id']
    return contest_id

def plot_cartoon(contest_id, root):
    cartoon_path = os.path.join("data", "newyorker_caption_contest_virgin", "images", f"{contest_id}.jpg")
    path = os.path.join(root, cartoon_path)
    img = Image.open(path)
    img.show()

def plot_html(path, height=450):
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(html_content, height=height, scrolling=False)

def plot_html_version2(path, height=600):
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(html_content,height=height/2,scrolling=True,)
def plot_html_3(path, height=450, width=800):
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(html_content, height=height, width = width, scrolling=False)


def plot_jpg(path, width=600):
    st.image(path, width=width)


def plot_wordcloud(path, graph_name, word_type, gender):
    with open(path, "rb") as f:
        data = pickle.load(f)
    wc = data[graph_name]  # WordCloud object

    # Créer figure matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(f"Top {word_type} in {gender} gendered captions", fontsize=16)

    # Afficher dans Streamlit
    st.pyplot(fig)