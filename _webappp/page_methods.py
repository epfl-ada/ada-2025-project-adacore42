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
from _webappp.assets.app_definitions import *
from _webappp.assets.app_design import *



st.markdown(
    """
    <style>
    /* Justify ALL markdown text in Streamlit */
    div[data-testid="stMarkdown"] p,
    div[data-testid="stMarkdown"] li {
        text-align: justify !important;
        text-justify: inter-word !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)








st.title("Methods")

"""
Welcome to this section, where we present the methods in more details.
"""

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Home main structure in containers
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

dataset_c = st.container()
procpip_c = st.container()
funisco_c = st.container()
statistics_c = st.container()




# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Home main structure in containers definitions
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


with dataset_c:
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


    #st.subheader("Dataset and Pipeline Overview")







with procpip_c:
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














with funisco_c:

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
            BERTopic is a topic modeling framework that combines transformer-based language representations with clustering 
            techniques to identify latent themes in textual data. It is designed to address limitations of traditional probabilistic 
            topic models, particularly when applied to short texts or documents with limited word co-occurrence.

            The method begins by transforming each document into a dense vector representation using a pre-trained sentence-level transformer model. 
            These embeddings encode semantic relationships between documents in a high-dimensional space. To facilitate efficient clustering, dimensionality 
            reduction is applied, commonly using Uniform Manifold Approximation and Projection (UMAP), which preserves local and global structure while 
            reducing computational complexity.

            Clustering is then performed on the reduced embeddings, typically using a density-based algorithm such as HDBSCAN. 
            This approach allows the model to identify clusters of varying sizes and to label documents that do not belong to any coherent cluster as outliers, 
            rather than forcing all documents into topics.

            For topic representation, BERTopic employs a class-based Term Frequency–Inverse Document Frequency (c-TF–IDF) scheme. In this step, all documents 
            assigned to a given cluster are treated as a single aggregated document, and TF–IDF scores are computed to identify terms that are both frequent 
            within the cluster and distinctive relative to other clusters. These terms are used to characterize and interpret each topic.
            """
            )

    with st.expander("**Vader's Sentiment Analysis**", expanded=AP.expanders):
        st.write(
            """
            VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool designed to analyse sentiments in social media contexts. It is very effective for short texts, such as tweets, comments, and captions,as it looks for informal language, punctuation and emojis if any. While we have removed emojis and punctuation in our preprocessing steps, VADER remains a robust choice for sentiment analysis due to its ability with spoken language and short texts.

            VADER operates on a pre-compiled lexicon of words and phrases that are associated with specific sentiment scores. Each word in the lexicon is assigned a valence score. The tool also incorporates rules to account for the intensity of sentiment based on factors such as capitalised words, punctuation, modifiers (e.g., "very", "extremely"), and negations.

            When analysing a piece of text, VADER tokenizes the input into individual words and phrases, looks up their corresponding sentiment scores in the lexicon, and applies the defined rules to adjust these scores based on context. The final output includes four sentiment metrics: positive, negative, neutral, and compound scores. The compound score is a normalised value ranging from -1 (most extreme negative) to +1 (most extreme positive).
            """
            )
        
with statistics_c:
    with st.expander("**Whitney U Test**", expanded=AP.expanders):
        st.write(
            """
            The Mann-Whitney U test is a non-parametric statistical test used to determine whether there is a significant difference between the distributions of two independent groups. It is useful when the data does not meet the assumptions required for parametric tests like a t-test (for example normality of data). Importantly, we need that the two groups being compared are independent and that there is some ordinal or continuous measurement scale.

            The test works by ranking all the observations from both groups together, then comparing the sum of ranks between the two groups. The U statistic is calculated based on these rank sums, and it reflects the number of times observations from one group are larger than observations from the other group in the ranked list. 

            The null hypothesis of the Mann-Whitney U test states that there is no difference in the distributions of the two groups. If the observed U statistic is unlikely under this assumption, we reject the null hypothesis and conclude that there is a statistically significant difference between the groups. A significant result indicates that one group tends to receive higher or lower values (no known direction, for that we need another measure) than the other, but it does not indicate how large or practically meaningful that difference is.
            """)
        
    with st.expander("**Cliff's Delta**", expanded=AP.expanders):
        st.markdown(
            r"""
            Cliff's Delta is a non-parametric effect size measure that quantifies the degree of overlap
            between two independent groups. It is calculated by considering all possible pairs of
            observations from the two groups and determining the proportion of pairs where one group's
            observation is greater than, less than, or equal to the other group's observation.

            The formula for Cliff's Delta ($d$) is given by:

            $$
            d = \frac{n_{\text{greater}} - n_{\text{less}}}{n_{\text{total}}}
            $$

            The value of Cliff's Delta ranges from $-1$ to $1$, where:
            - $d = 1$ indicates that all observations in group A are greater than those in group B.
            - $d = -1$ indicates that all observations in group A are less than those in group B.
            - $d = 0$ indicates complete overlap between the two groups.

            Common benchmarks for interpretation are:
            - Small effect: $|d| < 0.147$
            - Medium effect: $0.147 \le |d| < 0.33$
            - Large effect: $|d| \ge 0.33$

            Cliff's Delta is particularly useful for assessing practical significance in non-parametric
            tests such as the Mann–Whitney U test.
            """
        )




