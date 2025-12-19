import streamlit as st
import pandas as pd
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html

st.markdown("# Behind the Punchline: The representation of gender")

# pageData = PagesData.AXIS_3.value 

# pageData.page_firstBlock()

# st.markdown("# Big title")
# st.markdown("## Section title")
# st.markdown("### Subsection")
# st.markdown("Normal paragraph")

st.markdown(
    """
    What if your understanding of gender came from a single source: 
    The New Yorker Caption Contest?

    No textbooks. No surveys. Just cartoons, captions, and punchlines.
    Would men and women appear equal? Different? Stereotyped? Modern?

    In this section, we treat the contest as a cultural lens and ask what kind of
    gendered world it quietly sketches. Humor often looks harmless — but jokes rely
    on shared assumptions. And those assumptions can tell us a lot.""",
    text_alignment= 'justify')

st.markdown(
    """
    To guide this investigation, we focus on two questions:

    1. How are men and women depicted in cartoons and captions, and do these depictions
    reflect traditional gender roles or stereotypes?

    2. How does audience response relate to gendered content — do captions about one
    gender receive more positive attention than the other?
    """,
    text_alignment= 'justify'
)

st.image("data/newyorker_caption_contest_virgin/images/582.jpg", width=700)
st.markdown(
    "<h3 style='text-align: center;'>Yes, I see the train but I think we can beat it.</h3>",
    unsafe_allow_html=True
)

st.divider()

st.markdown("## 1. Setting the Scene: Who Appears in the Contest?")

st.markdown("### A simple method")

st.markdown("""
    Before diving into our scientific investigation, it's important to define the method to find gender in the
    cartoon descriptions and captions. It is rather simple actually, we created two big dictionnaries; one for
    women labeled word and one for men. It contains common english names, occupations, pronouns...
    With these dictionnaries, we can do some simple gender detection: iterate through the image descriptions 
    and captions, and annotate it as 'men', 'women', 'both' or 'neutral' depending on the presence of 
    gendered words.
    """,
    text_alignment= 'justify'
    )

st.markdown("### The results")

st.markdown("""
    We applied this simple method and got these plots, and guess what? We already found something intersting!
    Almost 50% of the cartoons are related only to men. Also women are present alone only in 8% of the cartoons
    and are more often mentioned alongside men. And, as expected, this imbalance is translated to the captions,
    where men references clearly dominates. If captions were our only window into the world, we would already
    conclude that men occupy far more narrative space.""",
    text_alignment= 'justify'
    )
# If possible, I would like to have a button were you can select which plot you see: either the one for the 
# cartoons or the one for the captions. I put the two plot next.
# plot_html(r"_webappp/assets/graph/counts_cartoons.html")
# plot_html(r"_webappp/assets/graph/counts_captions.html")

plot_choice = st.radio(
    "Select which distribution to display:",
    ["Cartoons", "Captions"],
    horizontal=True
)

if plot_choice == "Cartoons":
    plot_html(r"_webappp/assets/graph/counts_cartoons.html", height=450)
else:
    plot_html(r"_webappp/assets/graph/counts_captions.html", height=450)

st.divider()

# There is a big gap in the website here idk why

st.markdown("## 2. Behind the Scene: How Gender Is Depicted")

st.markdown("""
    Presence, however, is only part of the story. Now we have to investigate how
    are men and women are portrayed once they appear.""",
    text_alignment= 'justify')
    


st.markdown("### Words Matter")
st.markdown("""
    One way to examine depiction is to look at language itself.
    Which words tend to surround men? Which describe women?

    We extracted verbs and adjectives from gender-labeled captions and counted how
    often they appeared. The result is a set of word clouds showing the 50 most
    frequent descriptive words for each gender.

    Word size reflects frequency; color is purely aesthetic.
    """,
    text_alignment= 'justify')

# # Insert wordclouds. Man and Women wordcloud next to each other with a 
# # button where you can choose if you want to see the verbs or adjectives
# # The image appears blurry, idk why

wc_type = st.radio(
    "Choose your word type:",
    ["Verbs", "Adjectives"],
    horizontal=True
)

if wc_type == "Verbs":
    st.image(r"_webappp/assets/graph/wordclouds_verbs.png", width=700)
else:
    st.image(r"_webappp/assets/graph/wordclouds_adjs.png", width=700)

st.markdown("""
    At first glance, the clouds look similar, men and women seem to share
    much of the same vocabulary. But when we look closer, we see
    a more intersting story.
         
    **TO COMPLETE**
    """,
    text_alignment= 'justify')

st.divider()

st.markdown("### Themes we keep coming back to")

st.markdown("""
    Individual words tell part of the story but humor often operates at the level
    of recurring situations and ideas. To uncover these patterns, we turn to topic modeling. 
    And yes, we used a model with a magical-sounding name: BERTopic. If you know it already, we invite you to 
    look at our beautiful graph that shows our findings. If you don't, well we made you a simple explanation next. 
    """,
    text_alignment= 'justify')

# If possible have a sort of markdown and when you click on "The magic of BERTopic" it shows the explanation

with st.expander("The magic of BERTopic"):  
    st.markdown("""       
        BERTopic is a topic modeling method that groups captions based on meaning, not just word frequency. Instead 
        of counting how often words appear, it first turns each caption into a 
        numerical representation, called an embedding, using a language model trained to understand context.
            
        Captions with similar meanings end up close to each other in this embedding space. BERTopic then clusters 
        these captions and assigns each cluster a topic label based on the most representative words.

        In short: BERTopic doesn’t ask “Which words appear together?” but rather “Which captions are saying roughly 
        the same thing?”
        """,
    text_alignment= 'justify')

st.divider()

st.markdown("""
    Using this approach, we identified recurring topics and aggregated them into broader,
    interpretable themes.

    Because the dataset contains far more men-labeled captions than women-labeled ones,
    we focus on the themes that together cover 60% of captions for each gender. This keeps
    the analysis centered on the most representative patterns.

    In the interactive graph below, each rectangle corresponds to a theme. Clicking on one
    reveals the words that define it. You can switch between genders to explore how these
    themes differ along with a few fun observations.
    """,
    text_alignment= 'justify')

# ## Insert treemap for both gender. with a button to select which one to show. When you select the men, it also
# ## shows the fun facts about men. Same for women

gender_choice = st.radio(
    "Select gender:",
    ["Men", "Women"],
    horizontal=True
)

if gender_choice == "Men":
    plot_html(r"_webappp/assets/graph/topic_male.html", height=450)
    st.markdown("***Men eat… a lot***")
    st.markdown(
        """ 
        Food-related theme take up a surprisingly large share of male-labeled captions, but not the wholesome kind. 
        Think alcohol, junk food, dinner menus, and indulgent eating. The humor paints men as enthusiastic consumers, 
        always one drink or snack away from the punchline.""",
        text_alignment= 'justify')

    st.markdown("***Politics, but it is in fact Trump***")
    st.markdown("""
        Political humor does appear in male captions, but with no diversity: it’s Trump, Trump, and… Trump again. 
        Apparently, when men enter politics in New Yorker cartoons, they do so wearing a red tie and making headlines.
    """,
    text_alignment= 'justify'
    )
    
    st.markdown("***Only men get the full life arc.***")
    st.markdown("""    
    Certain themes appear exclusively in male-labeled captions: transportation, death, arts & music, and pop culture. 
    According to these cartoons, only men take the subway, play guitars, play some baseball, watch Edward Scissorhands, contemplate mortality 
    and... eventually die. A complete journey, really.
    ...
    """,
    text_alignment= 'justify')
else:
    plot_html(r"_webappp/assets/graph/topic_female.html")
    st.markdown("***Karen is… just a name. Or is it?***")
    st.markdown("""
    If you knew gender only through these captions, you might think Karen is simply a very popular female name. In reality, 
    it’s doing a lot of cultural heavy lifting. “Karen” has become shorthand for a specific stereotype: demanding, entitled, 
    complaining, often middle-aged, and usually unhappy with the manager. What looks like a neutral name quietly carries a 
    full personality without the need of a backstory.
    """,
    text_alignment='justify') 
    

    st.markdown("***Women in politics: meet Hillary. That’s it.***")
    st.markdown("""
    Political themes do appear for women, but almost exclusively through Hillary Clinton. If New Yorker captions were your 
    only source of information, you might reasonably conclude that American politics briefly included a woman once, and then moved on. 
    The absence of other female political figures is striking... and telling...
    """, 
    text_alignment='justify') 

st.divider()  

st.markdown("### So what did we learn?")

st.markdown("""
    If the New Yorker Caption Contest were our only source of knowledge about gender, we might start forming some… very specific ideas.

    Based on the dominant themes and recurring topics, a typical woman in this cartoon universe is rarely defined on her own terms. 
    She is most often introduced through her relationships: she is a mother, a sister, a wife, sometimes a bride, and occasionally an ex-wife. 
    Her actions revolve around the private sphere: she feeds and follows recipes. When romance enters the picture, it often does so in extremes: 
    she becomes a trophy wife, only for the story to end in divorce. Her appearance matters. She wears dresses, worries about fashion. 
    Outside the home, she is gently anchored to nature and time passing: seasons, gardens, and quiet domestic landscapes.
         
    The typical man, by contrast, appears less as a relative and more as a role. He is a man, a boss, a guy, a salesman, a lawyer, an officer, 
    an archetype before he is an individual. He does not cook, he drinks. Alcohol, junk food, dinners, and menus surround him. His meal is 
    served to him. He works, and his work matters. He wears suits and ties, occupies offices and institutions, and moves easily through public 
    spaces. He rides the subway, travels, performs music, engages with politics, and even confronts death. Where women are tied to cycles and care, 
    men are tied to action, authority, and consequence.
    """,
    text_alignment='justify')

st.divider()

st.markdown("## 3. Does Gender Win the Crowd?")

st.markdown("### Are gendered captions funnier?")

st.markdown(
    """To compare how the audience responds to gendered captions, we relied on two complementary statistical tools: the Mann–Whitney U test and Cliff’s delta. 
    Together, they answer two different questions: Is there a difference? and Does that difference actually matter?
    If you don't know any of these tests, don't worry we included explanations for both of them.""",
    text_alignment='justify')

# just as for BERTopic, include a sort of markdown that when you click on 
# the definition for the test appears

with st.expander("Mann–Whitney U Test or *“Are these scores different at all”*?"):

    st.markdown(
        """
        The Mann–Whitney U test is a non-parametric statistical test used to compare two independent samples.
        It evaluates whether observations from one group tend to have larger or smaller values than observations from another group.

        Unlike a t-test, it does not assume normality or equal variances. Instead of comparing means directly, it operates on the rank ordering of all 
        observations across both groups. The test statistic U reflects how often values from one group precede values from the other in this ranking.

        Formally, the null hypothesis is: The two groups are drawn from the same distribution.

        In practice, a significant result indicates a systematic shift between the distributions (e.g., one group tends to receive higher scores), 
        but it does not specify the magnitude of this shift.""",
        text_alignment = 'justify')
    
with st.expander("Cliff’s delta or *“How big is the difference, really?”*"):
    st.markdown(
        """
        Because our dataset contains many more men-labeled captions than women-labeled ones, we rely on 
        non-parametric, rank-based methods that are robust to both skewed distributions and sample-size imbalance.

        **Cliff’s delta** is an effect-size measure that tells us how large a difference is, independently of how many data points we have. 
        Unlike p-values, it is not inflated by large datasets and therefore helps distinguish *statistical significance* from 
        *practical relevance*.

        **How it works**

        Cliff’s delta measures the probability that a randomly chosen caption from one group (e.g., men-labeled) has a higher score 
        than a randomly chosen caption from the other group (e.g., women-labeled). It answers the question: 
        *If we randomly pick one caption from each gender, how often does one outperform the other?*

        It ranges from **–1 to +1**:
        - **0** → complete overlap between groups  
        - **Positive values** → higher scores tend to come from the first group  
        - **Negative values** → higher scores tend to come from the second group  

        **Interpretation guide**

        - |δ| < 0.147 → Negligible effect
        - 0.147 ≤ |δ| < 0.33 → Small effect 
        - 0.33 ≤ |δ| < 0.47 → Medium effect 
        - |δ| ≥ 0.47 → Large effect 
        
        """,
        unsafe_allow_html=True
    )

st.markdown("### What about the top and worst captions?")

st.markdown(""" **TO CHANGE**
    Since we did not see a significant difference when looking at the whole set of captions, we decided to dig deeper.
    We decided to focus on the top and worst 5% of caption of each gender to see if they were laughed at differently.
    """)

plot_html(r"_webappp\assets\graph\evolution_funny_score.html")

plot_html(r"_webappp\assets\graph\funniness_distrib_by_gender.html")

plot_html(r"_webappp\assets\graph\funny_score_distrib_5.html")

st.divider()

st.markdown("## 4. So What’s the Joke, Really?")
"**Conclusion**"
