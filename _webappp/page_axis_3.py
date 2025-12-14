import streamlit as st
import pandas as pd
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html

pageData = PagesData.AXIS_3.value 

pageData.page_firstBlock()

st.write(
    """
    A caption is never just a caption.

    Behind a few carefully chosen words lies a set of assumptions: who gets to speak, 
    who is being laughed at, and what the audience is expected to recognize as “normal.” 
    Cartoons may look lighthearted and timeless, but the ideas they rely on often are not.

    What, then, hides behind captions that appear harmlessly funny?
    """
)

### Insert intersting cartoon

st.divider()

st.write(
    """
    In a cultural moment where conversations about gender are more visible, more contested, 
    and more nuanced than ever, humor can be a revealing place to look. Jokes compress social 
    norms into a single line, sometimes reinforcing them, sometimes quietly updating them, 
    and sometimes pretending nothing has changed at all. The apparent innocence of a caption 
    can make these patterns easy to miss.

    In this data story, we look beneath the surface of New Yorker cartoons and captions to 
    examine how gender is represented and how those representations are received.
    """
)

st.divider()

st.write(
    """
    We investigate two core questions:

    1. How are men and women depicted in cartoons and captions, and do these depictions reflect 
    traditional gender roles or stereotypes?

    2. How does audience response relate to gendered content — do captions about one gender 
    receive more positive attention than the other?
    """
)

st.write(
    """
    By tracing patterns across themes, sentiment, and audience reactions, we ask whether 
    gender still functions as a punchline or whether its role in humor has become so familiar 
    that it no longer stands out at all.
    """
)
st.divider()

st.subheader("1. Setting the Scene: Who Appears in the Joke?")

"**Who gets mentionned?**"
# Insert barplots. Button to choose to see for captions or cartoons

"**Has the cast changed over time?**"
# Insert plots. Button to choose to see for captions or cartoons

st.subheader("2. Behind the Scene: How Gender Is Depicted")
"**Words Matter**"
# Insert wordclouds. Man and Women wordcloud next to each other with a 
# button where you can choose if you want to see the verbs or adjectives

"**Themes we keep coming back to**"

st.write(
    """
    Topic modeling gives us a way to step back from individual jokes and look at patterns: not what one 
    caption says, but what thousands of captions collectively suggest. By aggregating BERTopic outputs 
    into broader themes, we can compare how men and women are framed across the New Yorker caption contest         
""")

## Insert treemap for both gender.

st.write(
    """
    Female-Centered Themes: Archetypes First, Context Second

    The topic graph for women captions is striking for its concentration around archetypes. A large share of captions fall 
    into themes centered on roles rather than situations: mothers, wives, brides, queens, witches, and other symbolic figures. 
    These are not merely descriptive categories, they are culturally loaded shortcuts. A “mother” is not just a person; 
    she comes with expectations. "Karen" is not just any name. It represents entitlement,complaint, and social policing condensed into a single name.
    What stands out is how often women appear as types, rather than as actors in specific scenarios. Even when women are placed 
    in professional or public settings, those roles are frequently filtered through gendered framing: appearance, age, marital status, or relational identity.
    In short, female-centered humor tends to answer the question: what kind of woman is she? rather than what is she doing?

    Male-Centered Themes: Situations Over Identities

    The male topic graph tells a different story. While male archetypes do exist (the husband, the boss, the politician), they occupy a noticeably 
    smaller share of the thematic space. Instead, men-labeled captions are more widely distributed across situational themes: workplaces, friendships, 
    absurd scenarios, authority structures, and everyday inconveniences.
    Men are more often framed as participants in events, not embodiments of roles. The humor comes from what happens to them, not from what they are 
    supposed to represent.
    This broader thematic spread suggests that masculinity in these captions functions as a kind of default setting: flexible, situational, and less 
    likely to be reduced to a single defining trait.

    Same Medium, Different Narrative Logic

    Put side by side, the two graphs suggest that gender does not just change who appears in New Yorker captions, it changes how humor is constructed.
    Women are more likely to be funny because they fit (or violate) a recognizable archetype.
    Men are more likely to be funny because they are placed in a situation that goes wrong.
    This does not mean that female captions are more stereotypical in an overt or malicious way. Rather, it shows that gendered humor often relies 
    on different narrative shortcuts. For women, humor frequently leans on shared cultural assumptions about roles. For men, it leans on circumstance.

    Representation Without Reinvention

    Perhaps the most telling insight is not the presence of stereotypes, but their persistence. Despite spanning decades of submissions, the thematic 
    structure of gendered captions suggests that many familiar patterns remain firmly in place. The New Yorker caption contest has evolved in format 
    and audience, but its gendered humor often returns to the same conceptual wells.
    Women appear, but often as symbols.
    Men appear, but often as defaults.

    And this difference sets the stage for the next question: if gendered themes are framed differently, does the audience respond differently too?

    (Spoiler: not as much as one might expect.)
""")
 
"**Same themes, different reactions?**"

st.subheader("3. Does Gender Win the Crowd?")
"**Are gendered captions funnier?**"

st.subheader("4. So What’s the Joke, Really?")
"**Conclusion**"
 
plot_html(r"_Other\amelie_analysis\saved plots\topic_male.html")

plot_html(r"_Other\amelie_analysis\saved plots\topic_female.html")
