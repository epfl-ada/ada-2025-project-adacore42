import streamlit as st
import pandas as pd
from _webappp.assets.app_content import PagesData
from _webappp.assets.app_content import PagesData as PD
from _webappp.assets.app_definitions import *
from src.utils.general_utils import plot_html
from _webappp.assets.app_design import *
from _webappp.assets.app_definitions import AppParams as AP

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Containered structure 
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

behind_the_punchline_0 = st.container()

setting_the_scene_1 = st.container()

behind_the_scene_2 = st.container()

gender_crowd_3 = st.container()

what_we_learned_4 = st.container()









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












# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Containers definitions
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

with behind_the_punchline_0:

    st.title("Behind the Punchline: The representation of gender")
    st.write(
        """
        What if your understanding of gender came from a single source: 
        The New Yorker Caption Contest? No textbooks. No surveys. Just cartoons, captions, and punchlines.
        Would men and women appear equal? Different? Stereotyped? Modern? In this section, we treat the contest as a cultural lens and investigate on what kind of
        gendered world it quietly sketches. Humor often looks harmless, but jokes rely
        on shared assumptions. And those assumptions can tell us a lot. 

        Why does this matter? Because humor is one of the quiet places where norms survive.
        The New Yorker is not fringe comedy: it is an elite cultural institution, widely read,
        widely imitated, and often taken as a barometer of “smart” humor. If gender stereotypes
        persist here, they are not accidents — they are assumptions shared between cartoonists,
        caption writers, editors, and readers. Studying these jokes is not about policing humor. It is about understanding which
        representations feel natural enough to be laughed at without explanation.
        """
        )

    st.write(
        """
        **To guide this investigation, we focus on two questions:**

        *1. How are men and women depicted in cartoons and captions, and do these depictions
        reflect traditional gender roles or stereotypes?*

        *2. How does audience response relate to gendered content — do captions about one
        gender receive more positive attention than the other?*
        """
    )







    ImageCaptionCenter_C(
        image_path="data/newyorker_caption_contest_virgin/images/582.jpg",
        caption="Yes, I see the train — but I think we can beat it.",
        center_ratio=1
        )

st.divider()



























with setting_the_scene_1:
        
    st.header("1. Setting the Scene: Who Appears in the Contest?")

    st.subheader("A simple method")

    st.write(
        """
        Before diving into our scientific investigation, it's important to define the method to find gender in the
        cartoon descriptions and captions. It is rather simple actually, we created two big dictionnaries; one for
        women labeled word and one for men. It contains common english names, occupations, pronouns...
        With these dictionnaries, we can do some simple gender detection: iterate through the image descriptions 
        and captions, and annotate it as 'men', 'women', 'both' or 'neutral' depending on the presence of 
        gendered words. 

        A note of caution before going further. Our gender detection relies on word-based
        dictionaries: names, pronouns, and gendered roles. This approach captures broad trends,
        but it cannot account for irony, ambiguous names, visual cues in cartoons, or
        non-binary identities. Some captions will inevitably be misclassified. Rather than precise individual labeling, this method is designed to surface large-scale
        patterns. The results should be read as tendencies, not absolutes.

        We applied this simple method and got these plots, and guess what? We already found something intersting!
        """
        )
    
    graph_choice = st.radio(
        "",
        ["Cartoons", "Captions"],
        horizontal=True,
        label_visibility='collapsed'
        )
    
    if graph_choice == 'Cartoons':
        plot_html(r"_webappp/assets/graph/counts_cartoons.html")
    else: 
        plot_html(r"_webappp/assets/graph/counts_captions.html")

    # TwoTabGraph_C(
    #     label_1="Cartoons",
    #     path_1="_webappp/assets/graph/counts_cartoons.html",
    #     label_2="Captions",
    #     path_2="_webappp/assets/graph/counts_captions.html",
    #     center_ratio=8,
    #     height=450)

    st.subheader("The results")

    st.write(
        """
        Almost 50% of the cartoons are related only to men. Also women are present alone only in 8% of the cartoons
        and are more often mentioned alongside men. And, as expected, this imbalance is translated to the captions,
        where men references clearly dominates. If captions were our only window into the world, we would already
        conclude that men occupy far more narrative space.
        """
        )
















































st.divider()

with behind_the_scene_2:
    st.header("2. Behind the Scene: How Gender Is Depicted")

    st.write(
        """
        Presence, however, is only part of the story. Now we investigate how
        are men and women are portrayed once they appear. To do this, we first look at which words are most 
        associated with each gender. Then, we look at the most reccuring topics. 
        """)
    

    st.subheader("Words Matter")
    
    
    st.write(
        """
        One way to examine depiction is to look at language itself.
        Which words tend to surround men? Which describe women?

        To do this, we analyse the words most strongly associated with each gender category. We computed word frequencies
        separately for men and women labeled captions. But directly comparing these frequencies would not be meaningful since
        we have six times for men labeled captions. So we computed a normalised score and associated it with each word.
        Below, you can find how we computed this score.
    
        """)
    
    with st.expander("The normalised score", expanded=AP.expanders):  

        st.write("Here is how we calculated it for the men related words. For the women, it's just one minus the men's score.")
        st.latex(
            r"""
            S_{w}^{\text{male}} =
            \frac{\tfrac{c_{w,m}}{N_m}}
            {\tfrac{c_{w,m}}{N_m} + \tfrac{c_{w,f}}{N_f}}
            """
        )

        st.markdown(
            """
            where:
            - $c_{w,m}$ is the count of word *w* in male-labeled captions  
            - $c_{w,f}$ is the count of word *w* in female-labeled captions  
            - $N_m$ and $N_f$ are the total number of tokens in male- and female-labeled captions, respectively  
        """)
        
    st.write("""
        With those frequencies computed, we can now show you the top 50 words associated words to each gender in the following
        wordcloud.
        """)
    
    # st.image(r"_webappp\assets\graph\wordcloud_gender.png")
    st.image(r"_webappp/assets/graph/wordcloud_gender.png")

    # TwoTabGraph_C(
    #     label_1="Verbs",
    #     path_1="_webappp/assets/graph/wordclouds_verbs.png",
    #     label_2="Adjectives",
    #     path_2="_webappp/assets/graph/wordclouds_adjs.png",
    #     center_ratio=3,
    #     isImage=True,
    #     height=450
    # )


    st.write(
        """
        On the men’s side, the most frequent words lean toward power and money. Words like stocks, reinvent, president, employee, king, and cop dominate. 
        Men appear embedded in institutions: finance, work, authority, and public life. Even when humor turns negative (abominable, fired), it often frames men as actors 
        within larger structures: bosses who fail, leaders who disappoint, systems that collapse. Men are doing things, running things or breaking things.

        The women’s word cloud, by contrast, pulls the reader closer to the appearance and relationships. Words like lipstick, divorce, ruffled, marry, beautiful, 
        and even 'monsieur' suggest women are framed through how they look, who they belong to, or what role they play for others. Even neutral word papers feel 
        contextualized by domestic or relational settings. There is even an insult, which was not the case for men. 
        Humor here leans less toward institutions and more toward personal identity and social expectation.

        So if this contest were our only window into gender, we might conclude this:
        men inhabit the world, while women inhabit the frame.
        """
        )

    st.subheader("Themes we keep coming back to")

    st.write(
        """
        Individual words tell part of the story but humor often operates at the level
        of recurring situations and ideas. To uncover these patterns, we turn to topic modeling. 
        And yes, we used a model with a magical-sounding name: BERTopic. If you know it already, we invite you to 
        look at our beautiful graph that shows our findings. If you don't, well we made you a simple explanation next. 
        """)

    with st.expander("The magic of BERTopic", expanded=AP.expanders):  
        st.write("""       
            BERTopic is a topic modeling method that groups captions based on meaning, not just word frequency. Instead 
            of counting how often words appear, it first turns each caption into a 
            numerical representation, called an embedding, using a language model trained to understand context. 
                 
            Captions with similar meanings end up close to each other in this embedding space. BERTopic then clusters 
            these captions and assigns each cluster a topic label based on the most representative words.

            In short: BERTopic doesn’t ask “Which words appear together?” but rather “Which captions are saying roughly 
            the same thing?”
                 
            For more detailled explanation, see Methods.
            """
        )
        if st.button("Go to Methods →"):
            st.switch_page(PD.METHODS.value.path)

    st.write("""
        Using this approach, we identified recurring topics and aggregated them into broader,
        interpretable themes.

        Because the dataset contains far more men-labeled captions than women-labeled ones,
        we focus on the themes that together cover 60% of captions for each gender. This keeps
        the analysis centered on the most representative patterns.

        In the interactive graph below, each rectangle corresponds to a theme. Clicking on one
        reveals the words that define it. You can switch between genders to explore how these
        themes differ along with a few fun observations.
        """
    )
    # ## Insert treemap for both gender. with a button to select which one to show. When you select the men, it also
    # ## shows the fun facts about men. Same for women




    # def additionalComponent_1():
        
    #     with st.expander("Men eat… a lot.", expanded=AP.expanders):
    #         st.write(
    #             """ 
    #             Food-related theme take up a surprisingly large share of male-labeled captions, but not the wholesome kind. 
    #             Think alcohol, junk food, dinner menus, and indulgent eating. The humor paints men as enthusiastic consumers, 
    #             always one drink or snack away from the punchline."""
    #     )
    #     with st.expander("Politics, but it is in fact Trump.", expanded=AP.expanders):
    #         st.write("""
    #             Political humor does appear in male captions, but with no diversity: it’s Trump, Trump, and… Trump again. 
    #             Apparently, when men enter politics in New Yorker cartoons, they do so wearing a red tie and making headlines.
    #         """
    #         )
        
    #     with st.expander("Only men get the full life arc.", expanded=AP.expanders):
    #         st.write("""    
    #         Certain themes appear exclusively in male-labeled captions: transportation, death, arts & music, and pop culture. 
    #         According to these cartoons, only men take the subway, play guitars, play some baseball, watch Edward Scissorhands, contemplate mortality 
    #         and... eventually die. A complete journey, really.
    #         ...
    #         """)



    # def additionalComponent_2():
    #     with st.expander("Karen is… just a name. Or is it?", expanded=AP.expanders):
    #         st.write("""
    #         If you knew gender only through these captions, you might think Karen is simply a very popular female name. In reality, 
    #         it’s doing a lot of cultural heavy lifting. “Karen” has become shorthand for a specific stereotype: demanding, entitled, 
    #         complaining, often middle-aged, and usually unhappy with the manager. What looks like a neutral name quietly carries a 
    #         full personality without the need of a backstory.
    #         """
    #     )
    #     with st.expander("Women in politics: meet Hillary. That’s it.", expanded=AP.expanders):

    #         st.write("""
    #         Political themes do appear for women, but almost exclusively through Hillary Clinton. If New Yorker captions were your 
    #         only source of information, you might reasonably conclude that American politics briefly included a woman once, and then moved on. 
    #         The absence of other female political figures is striking... and telling...
    #         """
    #         )

    gender_choice = st.radio(
    "",
    ["Men", "Women"],
    horizontal=True,
    label_visibility='collapsed'
    )
    

    if gender_choice == "Women":
        plot_html(r"_webappp/assets/graph/topic_female.html")
        with st.expander("Karen is… just a name. Or is it?", expanded=AP.expanders):
            st.write("""
            If you knew gender only through these captions, you might think Karen is simply a very popular female name. In reality, 
            it’s doing a lot of cultural heavy lifting. “Karen” has become shorthand for a specific stereotype: demanding, entitled, 
            complaining, often middle-aged, and usually unhappy with the manager. What looks like a neutral name quietly carries a 
            full personality without the need of a backstory.
            """
        )
        with st.expander("Women in politics: meet Hillary. That’s it.", expanded=AP.expanders):

            st.write("""
            Political themes do appear for women, but almost exclusively through Hillary Clinton. If New Yorker captions were your 
            only source of information, you might reasonably conclude that American politics briefly included a woman once, and then moved on. 
            The absence of other female political figures is striking... and telling...
            """
            )
    else:
        plot_html(r"_webappp/assets/graph/topic_male.html")
        with st.expander("Men eat… a lot.", expanded=AP.expanders):
            st.write(
                """ 
                Food-related theme take up a surprisingly large share of male-labeled captions, but not the wholesome kind. 
                Think alcohol, junk food, dinner menus, and indulgent eating. The humor paints men as enthusiastic consumers, 
                always one drink or snack away from the punchline."""
        )
        with st.expander("Politics, but it is in fact Trump.", expanded=AP.expanders):
            st.write("""
                Political humor does appear in male captions, but with no diversity: it’s Trump, Trump, and… Trump again. 
                Apparently, when men enter politics in New Yorker cartoons, they do so wearing a red tie and making headlines.
            """
            )
        
        with st.expander("Only men get the full life arc.", expanded=AP.expanders):
            st.write("""    
            Certain themes appear exclusively in male-labeled captions: transportation, death, arts & music, and pop culture. 
            According to these cartoons, only men take the subway, play guitars, play some baseball, watch Edward Scissorhands, contemplate mortality 
            and... eventually die. A complete journey, really.
            ...
            """)


    # TwoTabGraph_C(  
    # label_1="Men",  
    # path_1=r"_webappp/assets/graph/topic_male.html",
    # label_2="Women",
    # path_2=r"_webappp/assets/graph/topic_female.html",
    # center_ratio=CENTER_RATIO_FULL,
    # isImage=False,
    # height=500,
    # additionalComponent_1=additionalComponent_1,
    # additionalComponent_2=additionalComponent_2
    # )

    # plot_html(r"_webappp/assets/graph/topic_female copy.html") 

    st.subheader("So what did we learn?")

    st.write("""
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
        """)

    st.divider()












 











































with gender_crowd_3:
        

    st.header("3. Does Gender Win the Crowd?")

    st.subheader("Are gendered captions funnier?")

    st.write("""
        Now that we have explored how men and women are depicted in the contest, we turn to a different question: how does the audience respond to those depictions?
        In other words, does gendered humor actually land differently with readers? To get a first intuition, we start with two descriptive views of the funny score:
        
        *1. The evolution of the average funny score over time, shown with its variability*

        *2. The overall distribution of funny scores for men- and women-labeled captions*
                
        You can select which plot you want to see with the following buttons. Also, if you want to see the results
        better, you can select which gender you want to see by clicking on the legend of the plots.
        """)
    
    funny_choice = st.radio(
    "",
    ["Distribution", "Evolution over time"],
    horizontal=True,
    label_visibility='collapsed'
    )

    if funny_choice == 'Distribution':
        plot_html(r"_webappp/assets/graph/funniness_distrib_by_gender.html", height= 500)
    else:
        plot_html(r"_webappp/assets/graph/evolution_funny_score.html", height = 500)
    # TwoTabGraph_C(
    #     label_1="Distribution",
    #     path_1="_webappp/assets/graph/funniness_distrib_by_gender.html",
    #     label_2="Evolution",
    #     path_2="_webappp/assets/graph/evolution_funny_score.html",
    #     center_ratio=8,
    #     height=600
    # )


    st.write(
        """
        At first glance, the result is surprising: the curves are almost identical.
        Both over time and across the full distribution, men- and women-labeled captions appear to receive very similar audience scores.
        But visual similarity does not necessarily mean statistical equality.  We turn to statistical testing to verify it. 

        To compare how the audience responds to gendered captions, we relied on two complementary statistical tools: the Mann–Whitney U test and Cliff’s delta. 
        Together, they answer two different questions: Is there a difference? and Does that difference actually matter?
        If you don't know any of these tests, don't worry we included explanations for both of them in the methods. This button will redirect you.""")
    
    with st.container():
        if st.button("Go to Methods →", key= 1):
            st.switch_page(PD.METHODS.value.path)


    # with st.expander("Mann–Whitney U Test or *“Are these scores different at all”*?", expanded=AP.expanders):

    #     st.write(
    #         """
    #         The Mann–Whitney U test is a non-parametric statistical test used to compare two independent samples.
    #         It evaluates whether observations from one group tend to have larger or smaller values than observations from another group.

    #         Unlike a t-test, it does not assume normality or equal variances. Instead of comparing means directly, it operates on the rank ordering of all 
    #         observations across both groups. The test statistic U reflects how often values from one group precede values from the other in this ranking.

    #         Formally, the null hypothesis is: The two groups are drawn from the same distribution.

    #         In practice, a significant result indicates a systematic shift between the distributions (e.g., one group tends to receive higher scores), 
    #         but it does not specify the magnitude of this shift.""")
        
    # with st.expander("Cliff’s delta or *“How big is the difference, really?”*", expanded=AP.expanders):
    #     st.write(
    #         """
    #         Because our dataset contains many more men-labeled captions than women-labeled ones, we rely on 
    #         non-parametric, rank-based methods that are robust to both skewed distributions and sample-size imbalance.

    #         **Cliff’s delta** is an effect-size measure that tells us how large a difference is, independently of how many data points we have. 
    #         Unlike p-values, it is not inflated by large datasets and therefore helps distinguish *statistical significance* from 
    #         *practical relevance*.

    #         **How it works**

    #         Cliff’s delta measures the probability that a randomly chosen caption from one group (e.g., men-labeled) has a higher score 
    #         than a randomly chosen caption from the other group (e.g., women-labeled). It answers the question: 
    #         *If we randomly pick one caption from each gender, how often does one outperform the other?*

    #         It ranges from **–1 to +1**:
    #         - **0** → complete overlap between groups  
    #         - **Positive values** → higher scores tend to come from the first group  
    #         - **Negative values** → higher scores tend to come from the second group  

    #         **Interpretation guide**

    #         - |δ| < 0.147 → Negligible effect
    #         - 0.147 ≤ |δ| < 0.33 → Small effect 
    #         - 0.33 ≤ |δ| < 0.47 → Medium effect 
    #         - |δ| ≥ 0.47 → Large effect 
            
    #         """)

    st.write("""
        We test the following hypothesis:

        H₀ (null hypothesis):
        There is no difference in funny score distributions between men- and women-labeled captions.

        Here is what got from it:
        - Mann–Whitney U test: p-value ≈ 3.2 × 10⁻²⁶ → statistically significant
        - Cliff’s delta: δ ≈ –0.029 → negligible effect size
        -> include the hypothesis, the results and analyse them.
        
        This means that, in practice, the audience does not meaningfully prefer captions about one
        gender over the other. This apparent neutrality invites interpretation. One possibility is that the audience
        evaluates captions primarily on linguistic cleverness rather than subject matter.
        Another is that long-standing gender stereotypes have become so normalized that they no
        longer register as distinctive — they are simply part of the expected background of       humor.

        In this sense, the absence of audience preference does not imply the absence of bias.
        Instead, it may signal that these representations are culturally settled: familiar enough
        to amuse, unremarkable enough to go unquestioned.
        """)

    st.subheader("What about the top and worst captions?")

    st.write("""
        Since there is no statistical difference when looking at the whole set of captions, we dig deeper.
        Instead of looking at all captions, we focus on the edges of audience reaction:
        - the top 5% most upvoted captions
        - the bottom least liked captions
        
        We did this for both gender. Here is the resulting distributions. For these plots, it's the same as before,
        you can click on the legend to select the gender you want to see. 
        """)

    plot_html("_webappp/assets/graph/funny_score_distrib_5.html",height=450)

    st.write("""
        And the conclusion: even among the funniest and least funny captions, the distributions remain similar. 
        Still, we test this hypothesis formally, by applying the same tests as before.

        **Worst 5%**
        - p-value: 4.4 × 10⁻⁶⁶ → statistically significant
        - Cliff’s delta: –0.207 → small effect
        This means that among the worst-performing captions, women-labeled captions tend to score
        slightly lower than the men labeled ones. The difference is statistically clear, but the effect
        remains small. Not the dramatic result we were expecting...
                
        **Top 5%**
        - p-value: 0.094 → not statistically significant
        - Cliff’s delta: 0.020 → negligible effect
        Among the best-performing captions, there is no statistically significant difference.
        """)

    st.subheader("What does this tell us?")

    st.write("""
        Despite the clear difference in representation, audience response stays remarkably
        gender-neutral. This sets up a compelling tension for the data story:
        while stereotypes and archetypes persist in content, they do not translate into clear 
        rewards from the crowd.
        """)

    st.divider()






































with what_we_learned_4:

    st.header("4. So... What did we learn about gender?")

    st.markdown("""
    Gender in the New Yorker Caption Contest is highly visible, strongly patterned, but weakly
    consequential. Men and women are not depicted in the same ways — stereotypes persist,
    roles differ, archetypes dominate — yet these differences rarely translate into measurable
    differences in audience approval.

    The imbalance, then, is not enforced by the crowd but embedded in the stories themselves.
    Gender shapes who gets to act, who gets to be observed, and which lives feel rich enough
    to joke about — even when everyone laughs the same.
        """)
