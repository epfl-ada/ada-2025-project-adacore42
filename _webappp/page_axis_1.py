import streamlit as st
import plotly.graph_objects as go
import numpy as np
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html
from src.utils.general_utils import plot_cartoon
from _webappp.assets.app_definitions import get_absolute_project_root
get_absolute_project_root()
from src.utils.web_app_plots.app_plots import PWA
PWA.set_root_path()

plots = PWA.load_plots()


pageData = PagesData.AXIS_1.value

pageData.page_firstBlock()

st.write(
    """
    Welcome to this section, where we explore some of the mechanisms behind humor.
    Let’s take a first glance at the two cartoons and there captions below. Which one do you find funnier? 
    Take a moment to trust your first reaction before going any further.
    """
)

st.image("data/newyorker_caption_contest_virgin/images/592.jpg", width=700)
#st.write("'We're not getting Shakespeare, but about every three minutes we get a presidential tweet.'")
st.markdown(
    "<h3 style='text-align: center;'>We're not getting Shakespeare, but about every three minutes we get a presidential tweet.</h3>",
    unsafe_allow_html=True)
st.image("data/newyorker_caption_contest_virgin/images/665.jpg", width=700)
st.markdown(
    "<h3 style='text-align: center;'>Lunch is on me.</h3>",
    unsafe_allow_html=True)
st.divider()

st.write(
    """
    The two captions you just read are the very best and very worst of all captions combined in 10 years of contests. 
    The first one was unanimously voted not funny with 6 467 votes while the second one received 15 232 votes for funny.
    Are you surprised by this large difference?

    If yes, you are already experiencing one key result of this study: humor is hard to predict. What one person finds hilarious, another may find dull or even offensive. 
    Humor is subjective and influenced by various factors, including personal experiences, cultural background, and social context.
    Quantify absolute funniness is therefore an elusive goal. We are rather studying the structure of fun in the specific case of written captions with english speaking audiences between 2016 and 2024. 

    """
)

st.subheader("Let's study what makes captions funny")

st.write(
    """
    Looking at the two captions shown earlier, the first noticeable difference is length: the funnier one is shorter.
    Is this a general pattern? Let’s find out by comparing the very funniest and very least funny captions, using the 
    extreme quantiles (0.9999 and 0.0001). This gives us two balanced groups of about 230 captions each. We then 
    compare several features and the results are shown in the following figures. 
    Both groups use mostly neutral words, although the least funny captions show more variability.
    Subjectivity differs significantly: funny captions tend to be more objective. 
    No clear differences in word count, punctuation.
    """
)
plot_html(r"_Other/katia_analysis/plotfunny_vs_not_funny.html")
st.write(
    """
    Was our first intuition wrong? well maybe not totally, if we look at our unfunny group we discover that all captions comes from only 4 contest, very close in time, suggesting that image context may strongly influence voting behavior and could affect our analyses.
    So let's approach the task with another angle : compare best and worth captions for each contest! 
    And the result indeed changes as presented in the following figure. Subjectivity is no longer significant, but word count and punctuation become important. The funniest captions are indeed shorter, with a median length of around 10 words. 
    """
)

plot_html(r"_Other/katia_analysis/plotbest_vs_worst_captions.html")




st.divider()


st.subheader("Are there any topics to best create funniness and win the contest ?")
st.write(
    """
    Now that we have tried to analyse what elements makes a joke funnier, we will dive into caption-topics clustering, to try to see if there is some topics better than other, some that creates more fun.
    An interesting question is to see if winning captions, according to the crowd-sourced ranking, and accorded to The New Yorker, corresponds to those 'best-winning' topics... See further the answer !
    We will firstly build the pipeline analysing captions among one contest, and then generalize and perform statistical analysis to finally conclude about this question.
    """
)

st.image("data/newyorker_caption_contest_virgin/images/801.jpg", width=700)
st.markdown(
    """
    <div style="text-align: center;">
    <\br>**Contest number 801, published May 23, 2022**  <\br>
    <\br>*Top Rated caption*: "What do you mean I don’t have time for another game?"  <\br>
    <\br>*The New Yorker's winner*: "I thought you’d be better at the endgame."  <\br>
    <\br>*Number of votes*: 562,261<\br>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    """
    LALALA
    """
)
plot_html(r"_Other\cycy_analysis\saved_plots\boxplot_topics_289.html")
plot_html(r"_Other\cycy_analysis\saved_plots\boxplot_topics_with_winners_289.html")

st.write(
    """
    LALALA
    """
)
plot_html(r"_Other\cycy_analysis\saved_plots\enrichment.html")

st.write(
    """
    LALALA
    """
)
plot_html(r"_Other\cycy_analysis\saved_plots\prop_above_thresh_289.html")
st.write(
    """
    LALALA
    """
)
plot_html(r"_Other\cycy_analysis\saved_plots\prop_above_thresh_with_winners_289.html")




st.divider()
st.write(
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

