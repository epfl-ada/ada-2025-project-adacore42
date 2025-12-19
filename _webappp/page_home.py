import streamlit as st
from _webappp.assets.app_definitions import HomePageAxis_C
from _webappp.assets.app_content import PagesData as PD
from _webappp.assets.app_definitions import AppParams as AP

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Title and Header 
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


#st.title("Humor as a Mirror")
st.markdown(
    "<h1 style='text-align: center;'>Humor as a Mirror</h1>",
    unsafe_allow_html=True
)
#"The New Yorker Captions as Reflections of Society, Politics, and Stereotypes"
#"A reflection of society through comedy
st.markdown(
    "<h3 style='text-align: center;'>A reflection of Society, Politics, and Stereotypes</h3>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 3, 1]) # pour centrer 
with col2:
    st.image("data/newyorker_caption_contest_virgin/images/733.jpg", width=700)

#"They don't hate us because we're wolves; they hate us because we're lawyers."
st.markdown(
    "<h5 style='text-align: center;'>They don't hate us because we're wolves; they hate us because we're lawyers.</h5>",
    unsafe_allow_html=True)
st.divider()

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Intro 
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

st.subheader("Introduction")
st.write(
    """
    Humor is a universal yet complex form of expression. The more we think about it and the more complexes it appear! There are numerous genres of humor, and it can be used in almost every life context. Humor can even serve serious purposes, such as addressing sensitive or difficult topics and easing social tensions.

    With this in mind, this project aim to investigate how jokes reflect societal traits and values. We will begin by examining what is generally perceived as “funny” and “unfunny,” and then explore how humor operates on two main topic : politics and gender. 

    In order to answer this questions, we will analyze thousands of captions from the *New Yorker* Caption Contest. In this contest, a cartoon is published weekly or biweekly without a caption, and readers are invited to submit their own humorous responses. Other participants then vote on whether each caption is funny, somewhat funny, or unfunny. This process provides a rich dataset that captures public humor preferences and social attitudes, a perfect opportunity to explore how humor reflects societal norms!
    """
)

st.divider()


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Home main structure in containers
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––



#dataNpipeline_c = st.container ()
methodsNglance_c = st.container ()
axisContent_c = st.container()

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

with methodsNglance_c:
    st.subheader("Methods at a Glance")

    "**Funny Score**"  
    st.info("A composite metric combining funny/unfunny ratios with vote weighting and z-score standardisation to identify reliably funny captions.")

    "**Semantic Similarity & Clustering** "
    st.info("SBERT embeddings (all-MiniLM-L6-v2), K-means clusters, UMAP projections, and cluster quality evaluation via intra- vs inter-cluster similarity.")

    "**Occupation & Gender Lexicons**"
    st.info("Built to detect job references and gender indicators in captions and metadata.")


    st.write(
    """
    If you are interested by learning more about the dataset, the processing pipeline and methods used, please check the sections below.
    """
    )
    ### PLEASE FIX :
    #st.page_link("page_methods.py", label="Go to Methods Page", icon="➡️") # do not work yet PLEASE FIX
    HomePageAxis_C(
        title=PD.METHODS.value.title,
        description=PD.METHODS.value.description,
        axisPath=PD.METHODS.value.path)

    st.divider()


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

with axisContent_c:

    st.subheader("Axes of analysis")

    HomePageAxis_C(
        title=PD.AXIS_1.value.title,
        description=PD.AXIS_1.value.description,
        axisPath=PD.AXIS_1.value.path)
    HomePageAxis_C(
        title=PD.AXIS_2.value.title,
        description=PD.AXIS_2.value.description,
        axisPath=PD.AXIS_2.value.path)
    HomePageAxis_C(
        title=PD.AXIS_3.value.title,
        description=PD.AXIS_3.value.description,
        axisPath=PD.AXIS_3.value.path)
    






    
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# End 
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


st.divider()
st.subheader("Conclusion")
st.write(
    """
    Conclusion : ...
        - This app shows not just which captions win — "
        - but what our jokes reveal about culture, bias, and how society laughs."

    We hope you enjoyed exploring societal reflections through humour with us! Now it's time to travel back home for hollidays. Merry christmas and don't forget your towel !
    """
)
col1, col2, col3 = st.columns([1, 3, 1]) # pour centrer 
with col2:
    st.image("data/newyorker_caption_contest_virgin/images/606.jpg", width=600)
#"They don't hate us because we're wolves; they hate us because we're lawyers."
    st.markdown(
    "<h5 style='text-align: center;'>Is this Part 2 of Hitchhikers Guide to The Galaxy?</h5>",
    unsafe_allow_html=True)



