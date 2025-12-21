import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import random

from src.utils.general_utils import plot_html, plot_jpg, plot_cartoon

from _webappp.assets.app_content import PagesData
from _webappp.assets.app_definitions import *
from _webappp.assets.app_design import *

from _webappp.assets.app_definitions import AppParams as AP
from _webappp.assets.app_content import PagesData as PD

from _webappp.assets.app_definitions import get_absolute_project_root
get_absolute_project_root()
from src.utils.web_app_plots.app_plots import PWA

PWA.set_root_path()
plots = PWA.load_plots()






st.title("What is considered funny?")

"""
Welcome to this section where we explore some of the mechanisms behind humor !
"""

"""
Let’s take a first glance at the two cartoons and their captions below. Which one do you find funnier?
Take a moment to trust your first reaction before going any further.
"""

col1, col2 = st.columns(2)

with col1:
    ImageCaptionCenter_C(
        image_path="data/newyorker_caption_contest_virgin/images/592.jpg",
        caption="We're not getting Shakespeare, but about every three minutes we get a presidential tweet.",
        center_ratio=CENTER_RATIO_FULL
    )

with col2:
    ImageCaptionCenter_C(
        image_path="data/newyorker_caption_contest_virgin/images/665.jpg",
        caption="Lunch is on me.",
        center_ratio=CENTER_RATIO_FULL
    )



st.space('small')


"""
The two captions you just read are the very best and very worst of all captions combined in eight years of contests. 
The first one was unanimously voted not funny with 6 467 votes while the second received 15 232 votes for funny.
Are you surprised by this large difference?

If yes, you are already experiencing one key result of this study : humor is hard to predict. What one person finds hilarious, another may find dull or even offensive. 
Humor is subjective and influenced by various factors, including personal experiences, cultural background, and social context.
Quantifying absolute funniness is therefore an elusive goal. In this work, we focus instead on studying the structure of humor in the specific case of written captions for English-speaking audiences between 2016 and 2024. Let’s keep this in mind to avoid drawing broad conclusions too quickly!
"""

st.divider()












































st.header("Let's study what makes captions funny")


"""
Looking back at the two captions, the first noticeable difference between them is length: the funnier one is shorter.
Could it be a general pattern? 
"""




def additionalComponent_1():  
    st.write(
        """
        Let’s find out by comparing the funniest and least funny captions, using the 
        extreme quantiles of our funny score distribution (0.9999 and 0.0001). This gives us two balanced groups of about 230 captions each.

        We compared several features such as length and punctuation and assessed the statistical significance of the results using a Student’s t-test.

        The results show that only subjectivity is significantly different, with funny captions being more objective.
        For the other features, the distributions are quite similar, although more variability is found in polarity for the not-funny group.

        Overall, there are no clear differences in word count or punctuation.
            

        Was our first intuition wrong? Well maybe not totally, because when we look at the composition of our not funny group we discover that all captions comes from only four contest, very close in time, 
        suggesting that our results may be bias toward the specific themes or styles of these contests rather than reflecting general trends. So let's approach the task with another angle.
        """
    )


def additionalComponent_2():
    st.write(
        """
        We will now compare the best and worth captions for each contest!
        This give us a dataset with 384 captions for each group.

        The results now show a significant difference between the two groups in terms of word count and punctuation usage. The least funny captions tend to be longer and contain more punctuation.

        Subjectivity, on the other hand, is no longer significantly different between the groups, and sentiment polarity follows very similar distributions. This suggests that using more positive or negative words does not, by itself, influence the perception of funniness.

        A first conclusion we can draw here is that it appear there is a difference in the surface features of funnier cpations and not funny captions. Especially in the number of words and number of punctiations.
        We can now turn to another question : what are these captions actually talking about?
        """
    )



TwoTabGraph_C(  
    label_1="Angle",  
    path_1="_webappp/assets/graph/plotfunny_vs_not_funny_2.html",
    label_2="An other angle",
    path_2="_webappp/assets/graph/plotbest_vs_worst_captions_2.html",
    center_ratio=CENTER_RATIO+50,
    isImage=False,
    height=1150,
    additionalComponent_1=additionalComponent_1,
    additionalComponent_2=additionalComponent_2
)




st.divider()







































st.header("Are there best topics to be funny and win the contest ?")



"""
We will now dive into an analysis of caption topics. To do so, we will first cluster captions according to their topics, using a BERTtopic model, analyse if some topics create more fun than others, and then examine where the winning captions stand.

To illustrate this, we will focus on a single contest, the one from May 23, 2022, featuring the cartoon below. Let’s see what we can discover!
"""


with st.expander("What is the difference between crowd-sourced top-rated caption and The New Yorker's winner ?", expanded=AP.expanders): 
    st.write(
        """
        There are two winning captions: one chosen by the public vote (referenced in <span style="color: orange;">orange</span>), and the other selected by the The New Yorker editorial team (referenced in <span style="color: blue;">blue</span>).
        """,
        unsafe_allow_html=True
    )


with st.expander("The magic of BERTopic", expanded=AP.expanders): 
    st.write("""       
        BERTopic is a topic modeling method that groups captions based on meaning, not just word frequency. Instead of counting how often words appear, it first turns each caption into a numerical representation, called an embedding, using a language model trained to understand context.
            
        Captions with similar meanings end up close to each other in this embedding space. BERTopic then clusters these captions and assigns each cluster a topic label based on the most representative words.

        In short: BERTopic doesn’t ask “Which words appear together?” but rather “Which captions are saying roughly the same thing?”
        
        For more technical details about this model, see the Methods.
        """
        )
    if st.button("Go to Methods →"):
        st.switch_page(PD.METHODS.value.path)
        


ImageCaptionCenter_C(
    image_path="data/newyorker_caption_contest_virgin/images/801.jpg",
    caption=[
        "Contest number 801 - Published May 23, 2022.",
    ],
)






@st.cache_data
def load_captions():
    df = pd.read_csv("_webappp/assets/csv/dataA_topics_289.csv")
    # Exclure misc / -1
    df = df[df["aggregated_topic"] != "misc"]
    return df

df_captions = load_captions()

if "random_caption_idx" not in st.session_state:
    st.session_state.random_caption_idx = random.randint(0, len(df_captions) - 1)

row = df_captions.iloc[st.session_state.random_caption_idx]




st.subheader("Caption example:")

col_11, col_22 = st.columns([1, 1])
with col_11:
    st.write(row['caption'])
    st.write(f"*Topic: {row['aggregated_topic']}*")

with col_22:
    if st.button("Want to see another caption ?", type="primary"):
        new_idx = st.session_state.random_caption_idx
        while new_idx == st.session_state.random_caption_idx:
            new_idx = random.randint(0, len(df_captions) - 1)
        st.session_state.random_caption_idx = new_idx









st.markdown(
    """
    <h3 style="text-align:center;">
        <em style="color: orange;">
            Crowd Top Rated caption:'What do you mean I don’t have time for another game?'
        </em>
    </h3>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style="text-align:center;">
        <em style="color: steelblue;">
            The New Yorker's winner: 'I thought you’d be better at the endgame.'
        </em>
    </h3>
    """,
    unsafe_allow_html=True
)




st.divider()


































st.subheader("Identify common topics among all captions")

"""
Using the BERTtopic embeddings and HDBSCAN clustering algorithm, we identify common topics of differents captions within a contest.
This gives a dozen of different clusters, we manually analyse them and aggregated into a few meaningful ones.
Human inspections allows us to control the results, where humoristics captions are really hard to clusterize automatically, because of all things that makes humour so particular, almost indescribable...


Let's see what topic have been identified from this cartoon, and the relative appreciation of people for them !
"""








st.subheader("Comparing funny score of all topics""")


if "plot_winners1" not in st.session_state:
    st.session_state.plot_winners1 = False

if st.button(
    "Show winning captions in topics",
    key="btn_plot_winners1"
):
    st.session_state.plot_winners1 = not st.session_state.plot_winners1

if st.session_state.plot_winners1:
    plot_html("_webappp/assets/graph/boxplot_topics_with_winners_289.html", height=1250)
else:
    plot_html("_webappp/assets/graph/boxplot_topics_289.html", height=1250)
    



"""
Don't you see a problem here ? ... Yes perfectly ! All topics seems to have almost the same median, and furthermore this median is low ! Around 25/100... Are the jokes that bad ??
NO. This result arises from the fact that we aggregated together ................ This will be addressed in the next section. 

Now, let's talk about the distribution of caption's scores within each topics. Some have more elements than others, some have more variance than others, some have more outliers than others (you can pass your mouse on the outliers to see the corresponding caption, have fun with it !)................

Another unexpected thing arised from this topic detection : Bureaucracy ? Taxes ? Insurrance ? We investigated here and ..............

Were does lie our two winning captions in those topics ?
"""


with st.expander("See more about the distribution of our topics", expanded=AP.expanders):
    plot_jpg("_webappp/assets/graph/distribution_funnyscore_kde_topics_289.jpg")
    """
    This graph shows how standardized humor scores (funny_score_scaled) are distributed across different themes. Each theme is represented in a sub-graph, with two elements:
    - Histogram: illustrates the relative frequency of scores.
    - KDE (Kernel Density Estimation) curve: indicates the relative probability that a score will take a certain value. The higher the curve, the more likely it is that the scores will fall within that range. KDE allows us to see the overall shape of the distribution, regardless of the exact number of measurements.
    
    
    All distributions observed show significant positive asymmetry (statistically significant skewness, p < 0.05), which means that scores tend to be concentrated at lower values with a tail extending towards higher values.
    """







"""
**Long-tail distribution bias**:
Those boxplots per topic allow us to see the distributions of caption scores within each topic, but as we saw, there is an issue of "smoothing all captions scores" with this simple plot. Indeed, if each topic clustered contains many mediocre captions and a few exellent ones, the average will flatten everything, resulting in a very low average score per topic. Therefore, we need to look beyond the average. We can :

*1. Isolates the top X% and the average range (40–60) and compare whether certain topics are over-represented in the top rankings versus the average. To do this, we calculate the 'enrichment per topic' (=top proportion vs. overall proportion). This allows us to answer the question "Which topics produce the most excellent captions?" without using the average. This will be called the 'enrichment score'.*

*2. Instead of looking at "which topic is the funniest on average", we look at: "which topics produce the most excellent captions?" by calculating the success rate (defined a score above the average score : 1.5/3 for the mean score, 50/100 for the funny_score_scaled) rather than the average score.*

Let's see how does that changes our topic analysis...
"""





def additionalComponent_1():
    st.write(
        """
        LALALA, interpréter le graphique. Taxes sont en moyenne 2.5 fios plus rpz dans le top 10% que dans la masse (40-60%)., emotionnal reactions (with haha!, don't you dare, ....) sont 2 fois plus rpz, les autres sont en moyenne autant treprésentées dans le top 10 que dans le reste des propositions.

        **Concerning the proportion of captions with a score higher than 30/100** :
        """
    )


def additionalComponent_2():
    st.write(
        """
        Blablabla commenter le graph ........... Commenter about taxes, about death_grim_reaper_afterlife, faire une remarque sur le topic pop_culture.
        
        Were does lie our two winning captions, do they belong to a topic where there is a high percentage of more funny captions ?

        Is the winning topic also the one that outperforms overall ? In this case not at all ! The topic that generally outperforms is the one refering to Taxes, and to the famous idiom of the american statesman Benjamin Franklin:

        'Our new Constitution is now established, and has an appearance that promises permanency; but in this world nothing can be said to be certain, except death and taxes.'

        Commenter encore sur celaaaa .................
        """
    )

TwoTabGraph_C(
    label_1="Enrichment score",
    path_1="_webappp/assets/graph/enrichment_289.html",
    label_2="Proportion of captions above 30/100",
    path_2="_webappp/assets/graph/prop_above_thresh_289.html",
    toggle_btn_label="Show winning captions in topics",
    toggle_path_2="_webappp/assets/graph/prop_above_thresh_with_winners_289.html",  # <- ton fichier
    center_ratio=CENTER_RATIO,
    isImage=False,
    height=1150,
    additionalComponent_1=additionalComponent_1,
    additionalComponent_2=additionalComponent_2,
)



st.divider()


st.subheader("Conclusion de l'axe 1")



