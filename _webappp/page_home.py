import streamlit as st
from _webappp.assets.app_definitions import HomePageAxis_C
from _webappp.assets.app_content import PagesData as PD
from _webappp.assets.app_definitions import AppParams as AP
from _webappp.assets.app_design import *
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Definition style button page 
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––



# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Title and Header 
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

with st.container():
    st.markdown(
        """
        <div style="text-align:center;">
            <h1>Humor as a Mirror</h1>
            <h3>A reflection of Society, Politics, and Stereotypes</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.image(
            "data/newyorker_caption_contest_virgin/images/733.jpg",
            use_container_width=True
        )

    st.markdown(
        """
        <div style="text-align:center; margin-top: 0.75rem;">
            <h5>
            They don't hate us because we're wolves; they hate us because we're lawyers.
            </h5>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Intro 
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

st.subheader("Introduction")
st.write(
    """
    Humor is a universal yet complex form of expression. The more we think about it and the more complexes it appear! There are numerous genres of humor, and it can be used in almost every life context. Humor can even serve serious purposes, such as addressing sensitive or difficult topics and easing social tensions.

    With this in mind, this project aim to investigate how jokes reflect societal traits and values. We will begin by examining what is generally perceived as “funny” and “unfunny”, and then explore how humor operates on two main topic : politics and gender. 

    In order to cover this subject, we will analyze thousands of captions from the *New Yorker* Caption Contest. In this contest, a cartoon is published weekly or biweekly without a caption, and readers are invited to submit their own humorous responses. Other participants then vote on whether each caption is funny, somewhat funny, or unfunny. This process provides a rich dataset that captures public humor preferences and social attitudes, a perfect opportunity to explore how humor reflects societal norms!
    """
)

st.divider()


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Home main structure in containers
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


st.subheader("Methods at a Glance")



with st.container():

    col_1, col_2, col_3 = st.columns([1, 1.8, 1])
    with col_1:
        "**Funny Score**"  
        st.info("We built a metric that captures what most people find funny and not funny.")

    with col_2:
        "**Semantic Similarity & Clustering** "
        st.info("SBERT embeddings (all-MiniLM-L6-v2), K-means clusters, UMAP projections, and cluster quality evaluation via intra- vs inter-cluster similarity.")
    
    with col_3:
        "**Occupation & Gender Lexicons**"
        st.info("Built to detect job references and gender indicators in captions and metadata.")
        

    "*If you are interested by learning more about the dataset, the processing pipeline and methods used, please check the sections below.*"



    if st.button("Go to Methods →"):
        st.switch_page(PD.METHODS.value.path)

    st.divider()


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

with st.container():

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
    


st.divider()




    
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# End 
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


with st.container():
    st.markdown(
        """
        <div style="text-align:center;">
            <h2>Conclusion</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align:center; max-width: 2000px; margin: 0 auto;">
            <p>
                This app shows not just which captions win —
                but what our jokes reveal about culture, bias, and how society laughs.
            </p>
            <p>
                We hope you enjoyed exploring societal reflections through humour with us.
                Now it's time to travel back home for holidays.
                Merry Christmas — and don’t forget your towel!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_l, col_c, col_r = st.columns([1, 1, 1])
    with col_c:
        st.image(
            "data/newyorker_caption_contest_virgin/images/606.jpg",
            use_container_width=True
        )

    st.markdown(
        """
        <div style="text-align:center; margin-top: 0.75rem;">
            <h5>Is this Part 2 of The Hitchhiker’s Guide to the Galaxy?</h5>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()