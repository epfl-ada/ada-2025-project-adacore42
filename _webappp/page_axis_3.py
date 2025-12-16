import streamlit as st
import pandas as pd
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html

pageData = PagesData.AXIS_3.value 

pageData.page_firstBlock()

st.write(
    """
    In this part, we shift our focus to the representatio of gender in the contest. The idea is to investigate
    wether humor reveals a stereotipical view of gender (roles in society, character, ...) or if it follows the evolution
    of the norms.

    To structure this investigation, we defined the following research questions: 

    1. How are men and women depicted in cartoons and captions, and do these depictions reflect 
    traditional gender roles or stereotypes?

    2. How does audience response relate to gendered content — do captions about one gender 
    receive more positive attention than the other?
    """
)

st.image("data/newyorker_caption_contest_virgin/images/582.jpg", width=700)
st.markdown(
    "<h3 style='text-align: center;'>Yes, I see the train but I think we can beat it.</h3>",
    unsafe_allow_html=True)

st.divider()

st.subheader("1. Setting the Scene: Who Appears in the Contest?")

"**A simple method**"

st.write("""
    Before diving into our scientific analysis, it's important to define the method to find gender in the
    cartoon descriptions and captions. It is rather simple actually, we created two big dictionnaries; one for
    women labeled word and one for men. It contains common english names, occupations, pronouns...
    With these dictionnaries, we can do some simple gender detection: iterate through the image descriptions 
    and captions, and annotate it as 'men', 'women', 'both' or 'neutral' depending on the presence of 
    gendered words.
    """
    )

"**The results**"

st.write("""
    We applied this simple method and got these plots, and guess what? We already found something intersting!
    Almost 50% of the cartoons are related only to men. Also women are present alone only in 8% of the cartoons
    and we even see that they are more likely to appear with men. And, as expected, this is translated to the captions,
    where men clearly dominates.
    """)
# If possible, I would like to have a button were you can select which plot you see: either the one for the 
# cartoons or the one for the captions. I put the two plot next.
plot_html(r"_Other\amelie_analysis\saved plots\counts_cartoons.html")
# plot_html(r"_Other\amelie_analysis\saved plots\counts_captions.html")
st.divider()

# There is a big gap in the website here idk why

st.subheader("2. Behind the Scene: How Gender Is Depicted")

st.write("""
    Now that we have a better idea of the gender distribution, let's look at how gender is depicted.
    """)

"**Words Matter**"
st.write("""
    A way to see how each gender is depicted is to see which words are associated with them. To find these 
    words, we iterate through the contests and counted the occurence of verbs and adjectives in men and women
    labeled captions. This results in these beautiful wordcloud where we observe the top 50 most occuring words
    for each gender. For clarity, the size of the words indicates frequency while the color are just for esthetic
    purposes.
    """)
# # Insert wordclouds. Man and Women wordcloud next to each other with a 
# # button where you can choose if you want to see the verbs or adjectives
# # The image appears blurry, idk why
st.image(r"_Other\amelie_analysis\saved plots\wordclouds_verbs.png", width=700)
# st.image("_Other\amelie_analysis\saved plots\wordclouds_verbs.png", width=700)

st.write("""
    At first glance, the word clouds do not seem to raise any stereotype. Words related to men and women seem quite
    similar. They are both surrounded by the same words. But when we look in detail, we see
    a more intersting story.
         
    NOT FINISHED
    """)

"**Themes we keep coming back to**"

# st.write(
#     """
#     Topic modeling gives us a way to step back from individual jokes and look at patterns: not what one 
#     caption says, but what thousands of captions collectively suggest. By aggregating BERTopic outputs 
#     into broader themes, we can compare how men and women are framed across the New Yorker caption contest         
# """)

# ## Insert treemap for both gender.
# plot_html(r"_Other\amelie_analysis\saved plots\topic_male.html")

# plot_html(r"_Other\amelie_analysis\saved plots\topic_female.html")


# st.write(
#     """
#     Female-Centered Themes: Archetypes First, Context Second

#     The topic graph for women captions is striking for its concentration around archetypes. A large share of captions fall 
#     into themes centered on roles rather than situations: mothers, wives, brides, queens, witches, and other symbolic figures. 
#     These are not merely descriptive categories, they are culturally loaded shortcuts. A “mother” is not just a person; 
#     she comes with expectations. "Karen" is not just any name. It represents entitlement,complaint, and social policing condensed into a single name.
#     What stands out is how often women appear as types, rather than as actors in specific scenarios. Even when women are placed 
#     in professional or public settings, those roles are frequently filtered through gendered framing: appearance, age, marital status, or relational identity.
#     In short, female-centered humor tends to answer the question: what kind of woman is she? rather than what is she doing?

#     Male-Centered Themes: Situations Over Identities

#     The male topic graph tells a different story. While male archetypes do exist (the husband, the boss, the politician), they occupy a noticeably 
#     smaller share of the thematic space. Instead, men-labeled captions are more widely distributed across situational themes: workplaces, friendships, 
#     absurd scenarios, authority structures, and everyday inconveniences.
#     Men are more often framed as participants in events, not embodiments of roles. The humor comes from what happens to them, not from what they are 
#     supposed to represent.
#     This broader thematic spread suggests that masculinity in these captions functions as a kind of default setting: flexible, situational, and less 
#     likely to be reduced to a single defining trait.

#     Same Medium, Different Narrative Logic

#     Put side by side, the two graphs suggest that gender does not just change who appears in New Yorker captions, it changes how humor is constructed.
#     Women are more likely to be funny because they fit (or violate) a recognizable archetype.
#     Men are more likely to be funny because they are placed in a situation that goes wrong.
#     This does not mean that female captions are more stereotypical in an overt or malicious way. Rather, it shows that gendered humor often relies 
#     on different narrative shortcuts. For women, humor frequently leans on shared cultural assumptions about roles. For men, it leans on circumstance.

#     Representation Without Reinvention

#     Perhaps the most telling insight is not the presence of stereotypes, but their persistence. Despite spanning decades of submissions, the thematic 
#     structure of gendered captions suggests that many familiar patterns remain firmly in place. The New Yorker caption contest has evolved in format 
#     and audience, but its gendered humor often returns to the same conceptual wells.
#     Women appear, but often as symbols.
#     Men appear, but often as defaults.

#     And this difference sets the stage for the next question: if gendered themes are framed differently, does the audience respond differently too?

#     (Spoiler: not as much as one might expect.)
# """)
 
"**Same themes, different reactions?**"

st.subheader("3. Does Gender Win the Crowd?")
"**Are gendered captions funnier?**"

st.subheader("4. So What’s the Joke, Really?")
"**Conclusion**"
