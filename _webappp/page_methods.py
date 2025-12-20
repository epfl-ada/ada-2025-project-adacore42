import streamlit as st
import plotly.graph_objects as go
import numpy as np
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html
from src.utils.general_utils import plot_cartoon
from _webappp.assets.app_definitions import get_absolute_project_root
get_absolute_project_root()
from src.utils.web_app_plots.app_plots import PWA
from _webappp.assets.app_definitions import AppParams as AP

st.title("Methods")
st.write(
    """
    Welcome to this section, where we present the methods in more details.
    """
)
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Home main structure in containers
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––



with st.container ():
    #st.subheader("Dataset and Pipeline Overview")


    with st.expander("**Dataset**", expanded=AP.expanders):
        st.write(
            """
            - 380+ caption contests  
            - CSV caption tables, metadata JSON 
            - Additionnal dataset : 
                - Occupation list (≈33k curated roles)  
                - Gendered lexicon from *Jailbreak the Patriarchy*  
            """
        )


    with st.expander("**Processing pipeline**", expanded=AP.expanders):
        st.write(
            """
            1. Centralised path + loading utilities  
            2. Data cleaning and consistency checks 

                2.1 Concatenate all 385 CSV in a list of CSV

                2.2 Remove redundant columns (index and rank)

                2.3 Consistency verification 

            3. Construction of a robust *funny score*  
            4. Tokenisation and lemmatisation 
            5. Models for similarity, clustering and gender analysis  
            """
        )

    with st.expander("**Funny score**", expanded=AP.expanders):
        st.markdown(
            r"""
        In order to capture the funny score according to the number of votes, we developed a new metric.

        First, we compute the **proportions of votes** for each caption:

        $$
        \text{props} = \frac{[\text{funny}, \text{somewhat\_funny}, \text{not\_funny}]}{\text{votes}}
        $$

        Then, we **weight each caption by the number of votes** it received using a logarithmic scaling factor. This ensures that captions with very large numbers of votes do not dominate, while still being given more importance:

        $$
        \text{props\_weighted} = \text{props} \times 5 \cdot \log(1 + \text{votes})
        $$

        Next, the **funny score** for each caption is calculated as a weighted combination of vote categories. We introduced scaling factors because the number of “funny” votes is much lower than the others, giving it more weight as it represents the aspect we are interested in:

        $$
        \text{funny\_score} = \text{funny} + 0.5 \cdot \text{somewhat\_funny} - 0.4 \cdot \text{not\_funny}
        $$

        Finally, we **rescale the score to a 0–100 range** to improve interpretability:

        $$
        \text{funny\_score\_scaled} = 100 \times \frac{\text{funny\_score} - \text{min}}{\text{max} - \text{min}}
        $$

        Where 0 corresponds to the least funny caption across all contests, and 100 corresponds to the funniest.
        """
        )


    with st.expander("**BERTtopic**", expanded=AP.expanders):
        st.write(
            """
            ... 
            """
        )
    st.divider()


