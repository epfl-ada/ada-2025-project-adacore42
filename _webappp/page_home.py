import streamlit as st
from _webappp.assets.app_definitions import HomePageAxis_C
from _webappp.assets.app_content import PagesData as PD
from _webappp.assets.app_definitions import AppParams as AP

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Intro 
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


st.title("Humor as a Mirror")

"The New Yorker Captions as Reflections of Society, Politics, and Stereotypes"
st.divider()

st.write(
    """
    This web app analyses thousands of captions from the *New Yorker* Caption Contest 
    to understand what people find funny, and how humor reflects patterns in society.  
    Using large-scale statistics, NLP tools, and semantic embeddings, we explore how
    jokes encode stereotypes, power dynamics, and cultural norms.
    """
)

st.divider()


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Home main structure in containers
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


dataNpipeline_c = st.container ()
methodsNglance_c = st.container ()
axisContent_c = st.container()



# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Containers definition 
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


with dataNpipeline_c:
    st.subheader("Dataset and Pipeline Overview")

    col_1, col_2 = st.columns (2)

    with col_1:
        with st.expander("**Data sources**", expanded=AP.expanders):
            st.write(
                """
                - 380+ caption contests  
                - CSV caption tables, metadata JSON  
                - Occupation list (≈33k curated roles)  
                - Gendered lexicon from *Jailbreak the Patriarchy*  
                """
            )

    with col_2:
        with st.expander("**Processing pipeline**", expanded=AP.expanders):
            st.write(
                """
                1. Centralised path + loading utilities  
                2. Data cleaning and consistency checks  
                3. Construction of a robust *funny score*  
                4. Tokenisation and lemmatisation (optional)  
                5. Models for similarity, clustering and gender analysis  
                """
            )

    st.divider()


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

with methodsNglance_c:
    st.subheader("Methods at a Glance")

    "**Funny Score**"  
    st.info("A composite metric combining funny/unfunny ratios with vote weighting and z-score standardisation to identify reliably funny captions.")

    "**Semantic Similarity & Clustering** "
    st.info("SBERT embeddings (all-MiniLM-L6-v2), K-means clusters, UMAP projections, and cluster quality evaluation via intra- vs inter-cluster similarity.")

    "**Occupation & Gender Lexicons**"
    st.info("Built to detect job references and gender indicators in captions and metadata.")



    st.divider()


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

with axisContent_c:

    st.subheader("Content")

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




st.info(
    "This app shows not just which captions win — "
    "but what our jokes reveal about culture, bias, and how society laughs."
)


