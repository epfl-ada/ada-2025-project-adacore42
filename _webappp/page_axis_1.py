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

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Version Tabs
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# """
# Looking back at the two captions, the first noticeable difference between them is length: the funnier one is shorter.
# Could it be a general pattern? 
# """




# def additionalComponent_1():  
#     st.write(
#         """
#         Let’s find out by comparing the funniest and least funny captions, using the 
#         extreme quantiles of our funny score distribution (0.9999 and 0.0001). This gives us two balanced groups of about 230 captions each.

#         We compared several features such as length and punctuation and assessed the statistical significance of the results using a Student’s t-test.

#         The results show that only subjectivity is significantly different, with funny captions being more objective.
#         For the other features, the distributions are quite similar, although more variability is found in polarity for the not-funny group.

#         Overall, there are no clear differences in word count or punctuation.
            

#         Was our first intuition wrong? Well maybe not totally, because when we look at the composition of our not funny group we discover that all captions comes from only four contest, very close in time, 
#         suggesting that our results may be bias toward the specific themes or styles of these contests rather than reflecting general trends. So let's approach the task with another angle.
#         """
#     )


# def additionalComponent_2():
#     st.write(
#         """
#         We will now compare the best and worth captions for each contest!
#         This give us a dataset with 384 captions for each group.

#         The results now show a significant difference between the two groups in terms of word count and punctuation usage. The least funny captions tend to be longer and contain more punctuation.

#         Subjectivity, on the other hand, is no longer significantly different between the groups, and sentiment polarity follows very similar distributions. This suggests that using more positive or negative words does not, by itself, influence the perception of funniness.

#         A first conclusion we can draw here is that it appear there is a difference in the surface features of funnier cpations and not funny captions. Especially in the number of words and number of punctiations.
#         We can now turn to another question : what are these captions actually talking about?
#         """
#     )



# TwoTabGraph_C(  
#     label_1="Angle",  
#     path_1="_webappp/assets/graph/plotfunny_vs_not_funny_2.html",
#     label_2="An other angle",
#     path_2="_webappp/assets/graph/plotbest_vs_worst_captions_2.html",
#     center_ratio=CENTER_RATIO+50,
#     isImage=False,
#     height=600,
#     additionalComponent_1=additionalComponent_1,
#     additionalComponent_2=additionalComponent_2
# )




# st.divider()


#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Version Tabs
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––




st.markdown(
    """
    Looking back at the two captions, the first noticeable difference between them is length: the funnier one is shorter.
    Could it be a general pattern? 
    """
)
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        """
        <div style="
            display: flex;
            align-items: center;
            height: 600px;
        ">
            <p style="font-size:16px; line-height:1.6;">
            Let’s find out by comparing the funniest and least funny captions, using the 
            extreme quantiles of our funny score distribution (0.9999 and 0.0001). This gives us two balanced groups of about 230 captions each.
            <br><br>
            We compared several features such as length and punctuation and assessed the statistical significance of the results using a Student’s t-test.
            <br><br>
            The results show that only subjectivity is significantly different, with funny captions being more objective.
            For the other features, the distributions are quite similar, although more variability is found in polarity for the not-funny group.
            <br><br>
            Overall, there are no clear differences in word count or punctuation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
        text_alignment="justify"
    )

with col2:
    plot_html(
        r"_webappp/assets/graph/plotfunny_vs_not_funny_2.html",
        height=600
    )

st.markdown(
    """
    Was our first intuition wrong? Well maybe not totally, because when we look at the composition of our not funny group we discover that all captions comes from only four contest, very close in time, 
    suggesting that our results may be bias toward the specific themes or styles of these contests rather than reflecting general trends. So let's approach the task with another angle.
    """
)
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        """
        <div style="
            display: flex;
            align-items: center;
            height: 600px;
        ">
            <p style="font-size:16px; line-height:1.6;">
            We will now compare the best and worth captions for each contest!
            This give us a dataset with 384 captions for each group.
            <br><br>
            The results now show a significant difference between the two groups in terms of word count and punctuation usage. The least funny captions tend to be longer and contain more punctuation.
            <br><br>
            Subjectivity, on the other hand, is no longer significantly different between the groups, and sentiment polarity follows very similar distributions. This suggests that using more positive or negative words does not, by itself, influence the perception of funniness.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
        text_alignment="justify"
    )

with col2:
    plot_html(
        r"_webappp/assets/graph/plotbest_vs_worst_captions_2.html",
        height=600
    )

st.markdown(
    """
    A first conclusion we can draw here is that it appear there is a difference in the surface features of funnier cpations and not funny captions. Especially in the number of words and number of punctiations.
    We can now turn to another question : what are these captions actually talking about?
    """)


st.divider()






























st.header("Are some topics inherently funnier than others, and do they increase your chances of winning?")



"""
We will now dive into an analysis of caption topics. To do so, we will first cluster captions according to their topics, using a BERTtopic model, analyse if some topics create more fun than others, and then examine where the winning captions stand.

To illustrate this, we will focus on a single contest, the one from May 23, 2022, featuring the cartoon below. Let’s see what we can discover!
"""


with st.expander("What is the difference between crowd-sourced top-rated caption and The New Yorker's winner ?", expanded=AP.expanders): 
    st.write(
        """
        There are two winning captions: one chosen by the public vote (referenced in <span style="color: orange;">orange</span>), and the other selected by the The New Yorker editorial team (referenced in <span style="color: blue;">blue</span>).
        """
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
We start by grouping captions together according to what they talk about.
Using the BERTtopic embeddings and HDBSCAN clustering algorithm, we detect common themes across all submitted captions for this cartoon.
The algorithm initially produces dozens of clusters, we manually analyse them and aggregated into a few meaningful ones.
Human inspections allows us to control the results, where humoristics captions are really hard to clusterize automatically, because of all things that makes humour so particular, almost indescribable...
"""



"""
We can meaningfully talk about “topics” in this contest, let's see what topic have been identified from this cartoon !

"""


topics = [
    ("checkmate_win_lose", "🏁", "Winning, losing, and the final “it’s over” moment."),
    ("chess_mechanics_pieces", "♟️", "Nerdy chess stuff: pieces, moves, and tiny tactics."),
    ("death_grim_reaper_afterlife", "💀", "Dark humor: death and endlife humor."),
    ("time_endgame_clock", "⏳", "Time pressure, endgame panic, and ticking clocks."),
    ("pop_culture", "🎬", "References to movies, politics, trends."),
    ("bureaucracy_taxes_insurance", "📄", "taxes & death, insurance."),
    ("deals_bets_rematches", "🤝", "Side deals, bets, rematches... negotiation mode on."),
    ("body_parts", "🖐️", "Hands, faces, bodies, bones... physical comedy and weird details."),
    ("emotional_reactions", "😳", "Big reactions: ‘haha’, ‘oh no’, ‘don’t you dare’."),
    ("color_choice_white_black", "⚪⚫", "White vs black: choices, sides, and subtle symbolism."),
    ("chess_life_game", "🎲", "Chess as life: fate, strategy, and existential metaphors."),
    ("misc", "🌀", "Unclassifiable outliers (a.k.a. the creative chaos)."),
]
cols = st.columns(3, gap="small")

for i, (key, emoji, desc) in enumerate(topics):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div style="
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 10px;
                padding: 8px 10px;
                background: rgba(255,255,255,0.025);
                box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                min-height: 78px;
            ">
              <div style="font-size: 15px; font-weight: 600; margin-bottom: 4px;">
                {emoji}
                <span style="
                    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                ">
                {key}
                </span>
              </div>
              <div style="opacity: 0.85; font-size: 12px; line-height: 1.25;">
                {desc}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )



with st.expander("Clustering quality assessment"):
    data = {
    "min_topic_size": [30],
    "coherence": [0.49],
    "diversity": [0.72],
    "silhouette": [0.079],
    "outlier_rate": [0.25],
    "n_topics": [37],
}
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    """This clustering shows an acceptable coherence and diversity, with a moderate outlier rate (expected for creative humorous text)."""

with st.expander("Why separating bureaucracy, taxes, and insurance from pop culture"):
    "Although this topic appear to belong to pop culture, the results obtained were significantly different from other pop culture references. Keeping it separate helps highlight its strong performance, which would otherwise be diluted within the broader pop-culture category."





st.subheader("Comparing funny score of all topics""")


"""
Now that we have topics, we compare how funny captions are perceived within each one.




**Visualizing humor distributions by topic :**

This graph shows distribution of standardized humor scores for each topic identified in the cartoon of May 23, 2022. Each theme is represented in a sub-graph, with two elements:
- Histogram: illustrates the relative frequency of scores.
- KDE (Kernel Density Estimation) curve: indicates the relative probability that a score will take a certain value. The higher the curve, the more likely it is that the scores will fall within that range. KDE allows us to see the overall shape of the distribution, regardless of the exact number of measurements.
"""

col_l, col_ccc, col_r = st.columns([1,8, 1])
with col_ccc:
    st.image("_webappp/assets/graph/distribution_funnyscore_kde_topics_289.jpg")

"""   
All topic distributions observed (except for one) show significant positive asymmetry (statistically significant skewness, p < 0.05), which means that scores tend to be concentrated at lower values with awith a long right tail of very funny captions. This results in a medians relatively similar across topics, and escpecially low (around 25/100). This distribution arises from the fact that we aggregated together all topics from the cartoon, and there is a lot with low funny score values, with only a few of outstanding funny ones.

Statistical tests confirm this:
- Skewness is significant for all topics (p < 0.05)
- Pairwise Mann–Whitney tests (with Bonferroni correction) reveal several significant differences



One topic stands out clearly: Bureaucracy, Taxes & Insurance.
This topic’s humor-score distribution differs significantly from most others. A smaller but notable effect is also observed for Time, Endgame & Clocks.
"""



"""
**A Synthetic View with Boxplots :** 
To summarize these distributions, we use boxplots per topic. Outliers correspond to captions that have received very high ratings.
"""

if "plot_winners1" not in st.session_state:
    st.session_state.plot_winners1 = False

if st.button(
    "Show winning captions in topics",
    key="btn_plot_winners1"
):
    st.session_state.plot_winners1 = not st.session_state.plot_winners1

if st.session_state.plot_winners1:
    plot_html("_webappp/assets/graph/boxplot_topics_with_winners_289.html", height=600)
else:
    plot_html("_webappp/assets/graph/boxplot_topics_289.html", height=600)
    

st.caption(
    "Interactive detail: By hovering over outliers, we can read the actual captions of the outliers"
)

"""
What we observe : 
- Very close medians between topics: No theme clearly dominates on average.

- Strong right-hand asymmetry for all topics: visual confirmation of the long-tail distribution already discussed.

- Very different variability depending on the topic: some have few outliers but a compact box, others (notably bureaucracy/taxes/insurance) show many very high outliers.

- Overrepresentation of certain topics, with a topic size varying from 39 to 1086 captions (excluding misc. topic) : some themes simply generate more proposals than others. There is a preponderant type of jokes done by people.

Being able to hover over outliers to read the captions is crucial: we can immediately see that the best captions are not “best on average,” but radically different.

This graph perfectly illustrates why the question “Which topic is the funniest?” is poorly phrased. The median obscures the important information: a topic's ability to produce brilliant exceptions. This box plot confirms that humorous performance is not determined by the average, but by the right tail of the distribution.
"""









"""
**Long-tail distribution bias of humour**:

We saw that humor scores follow a long-tail distribution. Indeed, if each topic clustered contains many mediocre captions and a few exellent ones, the average will flatten everything, resulting in a very low average score per topic. Therefore, we need to look beyond the average.

**So instead of asking: “Which topic is funniest on average?” we ask ourselves this question: “Which topics produce the most excellent captions?”**

We can use two differetn point of view to answer this question:

*Method 1. Isolate the top 10% and the baseline average range (40–60%). We then compute an enrichment score: How much more represented is a topic in the top captions compared to the average pool? This shows if whether certain topics are over-represented in the top rankings versus the average baseline (=top proportion vs. overall baseline proportion).*

*Method 2. Calculate the success rate (defined a score above a score threshold : 30/100 for the funny_score_scaled*



Let's see how does that changes our topic analysis...
"""





def additionalComponent_1():
    st.write(
        """
        This scatterplot directly answers the question: “Which topics are over-represented among the very best captions?”

        The vertical axis represents the enrichment score:
        the ratio between the presence of a topic in the top 10% of captions and its presence in the middle range (40–60%).
        A score > 1 indicates qualitative overperformance.

        Results :
        
        - The theme of bureaucracy/taxes/insurance is about 2.5 times more prevalent in the top 10%, making it by far the topic that “produces excellence” the most.
        - Emotional reactions show about 2 times enrichment; these are often powerful captions that surely have more potential to create humor.
        - The majority of other topics have an enrichment score close to 1: they are neither over- nor under-represented in the top 10%.
        
        This graph specifically addresses the bias identified earlier: it ignores the mass of mediocre captions and focuses solely on a topic's ability to generate hits. Hits win less often than some others, but when they do, they win big. This is a key distinction for understanding competitive humor.
        """
    )


def additionalComponent_2():
    st.write(
        """
        Here, we change perspective again. We no longer look at the top 10%, but at the probability that a caption will exceed the average score. The threshold corresponds to: 30/100 for funny_score_scaled for this cartoon from May 23, 2022.

        Results:
        - Bureaucracy / Taxes / Insurance : This topic stands out, with the highest proportion of “successful” captions, reaching around 20% above the success threshold (30/100). It is not only capable of producing a few exceptional captions, but also a relatively high number of consistently funny ones.
        - Death / Grim Reaper / Afterlife : This topic also shows a solid success rate, which makes sense given the cartoon itself. The theme fits very well with the image, making it easier for captions to connect with the audience. About 8% of captions exceed the success threshold.
        - Pop culture: In this contest, pop culture performs quite poorly overall. While some references work very well (like the “death and taxes” idea), many others do not. References to topics such as the Supreme Court, COVID, or specific movies lead to a lot of low-scoring captions.
        - The rest of the topics are below 7% of caption score above 30/100.

        This graph helps clarify the previous results: a topic can produce a few very strong captions (high enrichment score), but still be risky overall.
        
        
        """
    )

TwoTabGraph_C(
    label_1="Method 1 - Enrichment score",
    path_1="_webappp/assets/graph/enrichment_289.html",
    label_2="Method 2 - Proportion of captions above 30/100",
    path_2="_webappp/assets/graph/prop_above_thresh_289.html",
    toggle_btn_label="Show winning captions in topics",
    toggle_path_2="_webappp/assets/graph/prop_above_thresh_with_winners_289.html",
    center_ratio=CENTER_RATIO,
    isImage=False,
    height=600,
    additionalComponent_1=additionalComponent_1,
    additionalComponent_2=additionalComponent_2,
)



st.subheader("Discussion about above 2 results")

"""
Is the winning topic also the one that outperforms overall ? In this case not at all ! The most successful topic is not necessarily the one that wins.

Why ? Because contests reward captions according to many non-statisticall arguments: originality within a topic, subtle timing and phrasing, ... Not just statistical dominance.



The topic that generally outperforms is about Bureaucracy, Taxes & Insurance. It is a direct echo of the american statesman Benjamin Franklin's idiom :
*'Our new Constitution is now established, and has an appearance that promises permanency; but in this world nothing can be said to be certain, except death and taxes.'*
Taxes are a very familiar cultural reference, often linked to frustration, unfairness, and a sense of inevitability — a bit like a losing chess game, or even death itself. This idea fits the cartoon really well, while also adding a slightly uncanny and darker twist compared to the image alone. Because this reference is so deeply rooted in American culture, most people immediately get it, which likely explains why captions using this theme tend to work better and be appreciated by a wider audience.

Pop culture references, on the other hand, are much more unpredictable. When people get the reference, they can be very funny, but when they do not, the caption often falls flat. This makes pop culture a much riskier choice in a contest where humor is judged by a broad audience.


Limitations of our analysis : The topic assignment is imperfect, the humor perception is subjective and cultural references don’t resonate equally.
A promising next step would be to analyze outliers, and what makes the top 1-2 captions within a topic radically different from the rest ? That’s where the real secret of humor may lie.
"""






st.divider()

st.subheader("Conclusion de l'axe 1")

"""
Yes, some topics are statistically better at producing excellent captions. But winning is less about choosing the “best” topic, and the best sentence length - and more about finding a singular, surprising idea inside it.
“High-performing” topics increase the chances of producing a good caption, but they do not guarantee success in the The New Yorker Caption Contest.
"""


