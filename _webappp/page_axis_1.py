import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import random
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html
from src.utils.general_utils import plot_cartoon
from _webappp.assets.app_definitions import get_absolute_project_root
get_absolute_project_root()
from src.utils.web_app_plots.app_plots import PWA
PWA.set_root_path()

plots = PWA.load_plots()


#pageData = PagesData.AXIS_1.value

#pageData.page_firstBlock()
st.title("What is considered funny?")
st.markdown(
    """
    Welcome to this section, where we explore some of the mechanisms behind humor.
    """
)
st.divider()

st.markdown(
    """
    Let’s take a first glance at the two cartoons and their captions below. Which one do you find funnier?
    Take a moment to trust your first reaction before going any further.
    """
)
col1, col2 = st.columns(2)

with col1:
    st.markdown("")
    st.image("data/newyorker_caption_contest_virgin/images/592.jpg", width=650)
    #st.markdown("'We're not getting Shakespeare, but about every three minutes we get a presidential tweet.'")
    st.markdown(
    "<h3 style='text-align: center;'>We're not getting Shakespeare, but about every three minutes we get a presidential tweet.</h3>",
    unsafe_allow_html=True)

with col2:
    st.markdown("")
    st.image("data/newyorker_caption_contest_virgin/images/665.jpg", width=650)
    st.markdown(
    "<h3 style='text-align: center;'>Lunch is on me.</h3>",
    unsafe_allow_html=True)




st.divider()

st.markdown(
    """
    The two captions you just read are the very best and very worst of all captions combined in eight years of contests. 
    The first one was unanimously voted not funny with 6 467 votes while the second received 15 232 votes for funny.
    Are you surprised by this large difference?

    If yes, you are already experiencing one key result of this study : humor is hard to predict. What one person finds hilarious, another may find dull or even offensive. 
    Humor is subjective and influenced by various factors, including personal experiences, cultural background, and social context.
    Quantifying absolute funniness is therefore an elusive goal. In this work, we focus instead on studying the structure of humor in the specific case of written captions for English-speaking audiences between 2016 and 2024. Let’s keep this in mind to avoid drawing broad conclusions too quickly!
    """
)

st.divider()
st.subheader("Let's study what makes captions funny")

st.markdown(
    """
    Looking back at the two captions, the first noticeable difference between them is length: the funnier one is shorter.
    Could it be a general pattern? Let’s find out by comparing the funniest and least funny captions, using the 
    extreme quantiles of our funny score distribution (0.9999 and 0.0001). This gives us two balanced groups of about 230 captions each. We compared several features and assessed the statistical significance of the results using a Student’s t-test. The results are shown in the following figures. 
    Both groups use mostly neutral words, although the least funny captions show more variability.
    Subjectivity differs significantly: funny captions tend to be more objective. 
    No clear differences in word count, punctuation.
    """
)
plot_html(r"_webappp/assets/graph/plotfunny_vs_not_funny.html")
st.markdown(
    """
    Was our first intuition wrong? well maybe not totally, if we look at our unfunny group we discover that all captions comes from only 4 contest, very close in time, suggesting that image context may strongly influence voting behavior and could affect our analyses.
    So let's approach the task with another angle : compare best and worth captions for each contest! 
    And the result indeed changes as presented in the following figure. Subjectivity is no longer significant, but word count and punctuation become important. The funniest captions are indeed shorter, with a median length of around 10 words. 
    """
)

plot_html(r"_webappp/assets/graph/plotbest_vs_worst_captions.html")




st.divider()


st.subheader("Are there any topics to best create funniness and win the contest ?")
st.markdown(
    """
    Now that we have tried to analyse what elements makes a joke funnier, we will dive into caption-topics clustering, to try to see if there is some topics better than other, some that creates more fun.
    An interesting question is to see if winning captions, according to the crowd-sourced ranking, and accorded to The New Yorker, corresponds to those 'best-winning' topics... See further the answer !
    """)

with st.expander("What is the difference between crowd-sourced top-rated caption and The New Yorker's winner ?"): 
    """
    a redigeeeeer
    """


st.markdown(
    """
    <div style="text-align: center;">
        <br>
        <strong>Contest number 801 - Published May 23, 2022.</strong>
        <br>
    </div>
    """,
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.markdown("")


with col2:
    st.markdown("")
    st.image("data/newyorker_caption_contest_virgin/images/801.jpg", width=650)

with col3:
    st.markdown("")




st.divider()

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


st.markdown(
    f"""
    <div style="text-align: center; padding: 20px;">
        <h9>Some proposed captions of this contest</h9>
        <p style="font-size: 26px;"><i>"{row['caption']}"</i></p>
        <p style="font-size: 20px; color: gray;">
            Topic: <b>{row['aggregated_topic']}</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


if st.button("See another joke ?"):
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



st.markdown(
    """
    **Identify common topics among all captions**

    Using HDBSCAN clustering algorithm and BERTtopic embeddings [SOURCE], we will try to identify common topics of differents captions within a contest, and here are the results.
    We manually aggregated the found clusters into a few aggregated ones, to retrieve meaning of those results.
    It took a lot of time to do it by hand, but isn't it better to analyse a douzain of topics than hundreds, no ? :)
    Human inspections allows us to control the results, where humoristics captions are really hard to clusterize automatically, because of all things that makes humour so particular, almost indescribable...
    
    
    Let's see what topic have been identified from this cartoon, and the relative appreciation of people for them !
    """
    )




st.divider()


st.markdown(
    """
    **Comparing funny score of all topics**
    """
)


if "plot_winners1" not in st.session_state:
    st.session_state.plot_winners1 = False

if st.button(
    "Show winning captions in topics",
    key="btn_plot_winners1"
):
    st.session_state.plot_winners1 = not st.session_state.plot_winners1

if st.session_state.plot_winners1:
    plot_html("_webappp/assets/graph/boxplot_topics_with_winners_289.html")
else:
    plot_html("_webappp/assets/graph/boxplot_topics_289.html")
    


st.markdown(
    """
    Don't you see a problem here ? ... Yes perfectly ! All topics seems to have almost the same median, and furthermore this median is low ! Around 25/100... Are the jokes that bad ??
    NO. This result arises from the fact that we aggregated together ................ This will be addressed in the next section. 

    Now, let's talk about the distribution of caption's scores within each topics. Some have more elements than others, some have more variance than others, some have more outliers than others (you can pass your mouse on the outliers to see the corresponding caption, have fun with it !)................
    
    Another unexpected thing arised from this topic detection : Bureaucracy ? Taxes ? Insurrance ? We investigated here and ..............
    
    Were does lie our two winning captions in those topics ?
    """
)



st.markdown(
    """
    The *The New Yorker* winning caption *"I thought you’d be better at the endgame."* corresponds to the *Time, Clock, and Engame* topic, [TODO : EXPLAIN HUMOUR].
    The *crowd-sourced ranking* winning caption *"What do you mean I don’t have time for another game?"* corresponds to the *Chess game or Life game* topic, [TODO : EXPLAIN HUMOUR].
    """
)



st.markdown(
    """
    **Long-tail distribution bias**:
    Those boxplots per topic allow us to see the distributions of caption scores within each topic, but as we saw, there is an issue of "smoothing all captions scores" with this simple plot. Indeed, if each topic clustered contains many mediocre captions and a few exellent ones, the average will flatten everything, resulting in a very low average score per topic. Therefore, we need to look beyond the average. We can :

    1) Isolates the top X% and the average range (40–60) and compare whether certain topics are over-represented in the top rankings versus the average. To do this, we calculate the 'enrichment per topic' (=top proportion vs. overall proportion). This allows us to answer the question "Which topics produce the most excellent captions?" without using the average. This will be called the 'enrichment score'.

    2) Instead of looking at "which topic is the funniest on average", we look at: "which topics produce the most excellent captions?" by calculating the success rate (defined a score above the average score : 1.5/3 for the mean score, 50/100 for the funny_score_scaled) rather than the average score.
    
    Let's see how does that changes our topic analysis...
    """
)
plot_html(r"_webappp/assets/graph/enrichment_289.html")

st.markdown(
    """
    LALALA, interpréter le graphique. Taxes sont en moyenne 2.5 fios plus rpz dans le top 10% que dans la masse (40-60%)., emotionnal reactions (with haha!, don't you dare, ....) sont 2 fois plus rpz, les autres sont en moyenne autant treprésentées dans le top 10 que dans le reste des propositions.

    **Concerning the proportion of captions with a score higher than 30/100** :
    """
)



if "plot_winners2" not in st.session_state:
    st.session_state.plot_winners2 = False

if st.button(
    "Show winning captions in topics",
    key="btn_plot_winners2"
):
    st.session_state.plot_winners2 = not st.session_state.plot_winners2

if st.session_state.plot_winners2:
    plot_html("_webappp/assets/graph/prop_above_thresh_with_winners_289.html")
else:
    plot_html("_webappp/assets/graph/prop_above_thresh_289.html")





st.markdown(
    """
    Blablabla commenter le graph ........... Commenter about taxes, about death_grim_reaper_afterlife, faire une remarque sur le topic pop_culture.
    
    Were does lie our two winning captions, do they belong to a topic where there is a high percentage of more funny captions ?
    """
)

st.markdown(
    """
    LA AUSSI FAUDRAIT METTRE UN BOUTON POUR FAIRE POP LE GRAPHIQUE CI DESSOUS, A LA PLACE DE L'ANCIEN
    """
)




st.markdown(
    """
    Is the winning topic also the one that outperforms overall ? In this case not at all ! The topic that generally outperforms is the one refering to Taxes, and to the famous idiom of the american statesman Benjamin Franklin:

    'Our new Constitution is now established, and has an appearance that promises permanency; but in this world nothing can be said to be certain, except death and taxes.'

    Commenter encore sur celaaaa .................
    """
)








st.divider()
st.markdown(
    """

    """
)



# Un exemple de coment plotter un plot a l'aide de plotly
if plots:
    plot = plots[0]

    # Plotly line figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=plot.Y_data,
            y=plot.X_data,
            mode="lines",
            line=dict(width=1),
            name=plot.title,
        )
    )

    fig.update_layout(
        title=plot.title,
        xaxis_title=plot.X_label,
        yaxis_title=plot.Y_label,
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40),
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("No stored plots found.")

