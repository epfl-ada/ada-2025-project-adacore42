import streamlit as st
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html, plot_html_version2
from _webappp.assets.app_design import *
from _webappp.assets.app_definitions import *
import pandas as pd
import numpy as np
from _webappp.assets.app_definitions import AppParams as AP



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


PagesData.AXIS_2.value.description = """
    Humour is something so hard to model, that it is often simpler to look for patterns surrounding certain topics rather than trying to directly model exactly what makes something funny. In this section of our story on humour in the New Yorker Caption Contest, we focus on occupational references in captions. Why? Our whole lives are oriented around our works and professions, thus it is no suprise that occupations have tunneled their way into our humour. Look at the figure below and decide which caption you find the funniest! 
    """

PagesData.AXIS_2.value.page_firstBlock()

ImageCaptionCenter_C(
    image_path="data/newyorker_caption_contest_virgin/images/595.jpg",
    caption=[
        "They didn't say who... they just said one of us won't be here in the spring...",
        "Surprise, surprise. The new manager is a fat white guy with no pants.",
        "I hear he had a meltdown after the holidays last year.",
    ],
)
st.write( """
    The captions above are among the funniest captions submitted for this cartoon. The winner was the second caption, which makes a reference to managers and plays on the stereotype of managers and corporate culture. You could reasonably shrug and say that this is only one cartoon, but occupational references are actually quite common in everyday humour. If you would like to see where occupational humour appears, how well it performs, and how it is distributed across the New Yorker Caption Contest, read on!
""")

st.subheader("A few words on Methodology")
st.write("""
        Identifying occupational references in captions is not straightforward. People can be explicit, like naming a job title, but they can also be indirect, by hinting at workplace routines, professional stereotypes, or role specific jargon. With a dataset this large, manual annotation is not feasible, so we take a simple approach: we restrict the analysis to direct mentions of job titles taken from a curated list of roughly 33,000 occupations. We then preprocess the captions to standardise the text and use string matching to detect job titles. This gives us a reliable baseline for studying where occupations appear and how they perform in humour, without introducing the extra assumptions and complexity of a model designed to infer indirect references. However, we acknowledge that this approach misses a large part of humour related to subtle references to occupations, which could be explored in future work.
""")
st.subheader("Where do occupations appear and how frequent are they?")

st.write("""
       If we split the captions into two simple groups, those that mention an occupation and those that do not, one thing becomes clear straight away. Only a small share of captions talk about jobs at all. Specifically, out of the total number of captions, only about 6.14% contain direct references to job titles from our list. That may sound low, but it is worth remembering what this number does and does not mean. We are only counting explicit job titles, so any occupational humour that works through hints or stereotypes without naming the role will not be captured here.
         
        Interestingly, a simple t-test reveals that captions with occupational references are on average rated less funny than those without (p-value < 0.05). While this might seem counterintuitive, it could be explained by the fact that occupational humour often relies on stereotypes or clichés that might not resonate with all audiences. Additionally, people might have different experiences and perceptions of certain occupations, which could influence their appreciation of jokes related to them. In any case, we shoul not lose hope in occupational humour just yet! There could be many confounding factors at play here and we should dig deeper and look at distributions patterns before drawing any firm conclusions.
         """)
# ImageCaptionCenter_C(
#     image_path="data/newyorker_caption_contest_virgin/images/661.jpg",
#     caption=[
#         "I am pleased to announce that Dopey will be leaving us to pursue a career as White House Chief of Staff.",
#         "Really? All of you are running for the Democratic presidential nomination?",
#         "Grouchy, you'll be Press Secretary, Dopey you'll be Attorney General...",
#     ],
# )

# st.divider()

st.write("""
        It might not be surprising that the term "clown" is found most commonly in humour about occupations, since humour is their job definition. That said, we should treat this result with caution:"clown" is also used as a casual insult.
         
        Still, the pattern is an inviting starting point. What other jobs occur most often in captions? Are the top occurences other jobs from the entertainment sector or do we make fun of people running our political systems, who keep us safe, or those who take care of our health?
         """)
plot_html_version2("_webappp/assets/graphs/occupation_dropdown_plot.html")

st.write(
    """
    This reveals that people like to joke about quite serious jobs, and perhaps jobs that everyone can relate to in their lives. The next question is whether they only appear because of the cartoon's context. The bar chart below focuses on the 20 most common occupations and shows that these jobs appear in roughly half of all contests, with some cropping up almost everywhere. For example, "president" and "cop" show up in nearly every contest in the dataset, while "chef" appears in fewer than half of them. This suggests that the most common occupations are not simply tied to a handful of scenes or themes, but are part of the contest vocabulary.
    """
)

plot_html_version2("_webappp/assets/graphs/term_num_contests_bar.html")
st.write("""
          Frequency tells us what is common, but not what actually works as a joke. To asess the performance of occupations we can check which occupations are actually the funniest, or the worst performers. This can be done by looking at the median funny scores, introduced in axis 1, of captions that reference each occupation above a certain threshold frequency. The results show us that it is indeed not the most frequent occupations that are present in the funniest captions: None of the top 20 most frequent make the cut! 
        
         In each of the charts, we see a very small gradual change along the occupations, showing that there are no occupations that are dramatically funnier or less funny than others. Furthermore, we see that the difference between the best and worst occupations is quite small, suggesting that while some jobs might be slightly funnier than others on average, the overall impact of occupation on humour is limited.
         """)
plot_html_version2("_webappp/assets/graphs/best_worst_occupations_by_median.html")

st.write("""
        We can now choose a certain set of occupation that we can track a bit more in depth! We handpick frequent jobs so that we can make proper statistical tests like doctors, nurses, presidents, lawyers, interns, ceos, cops and clowns a bit more closely. More importantly, we are interested in the distribution of their funny score across different contests, to deduce which jobs are in the funniest captions. On a more statistical note, it is best to look at distributions instead of simply comparing jobs based on their median funniness. The key question is not only which occupation has the highest median score, but how reliably each one contributes to a joke across different contests.

        What we find is striking in its consistency. All of these occupations have very similar funniness distributions, each with a median of roughly 23 points. The distributions also share the same overall shape: they are left skewed, with relatively few extremely low scoring captions, a dense cluster around the middle, and a longer tail of higher scoring outliers. In practical terms: occupational humour seems to produce a steady baseline of moderately funny captions, with the occasional standout line that rises well above the rest.
         """)
plot_html_version2("_webappp/assets/graphs/occupation_distribution_multiple.html")
st.write("""
        An even clearer way to compare these distributions is with a box plot as it shows well the outlier behaviour:
         """)
# plot_html_version2("_webappp/assets/graphs/occupation_box_plots.html")
# st.write("""
#         This plot confirms what we saw before. All of the occupations cluster around a median funniness score of roughly 23 points, with broadly similar spreads and a familiar pattern of outliers. In other words, the differences between these jobs are subtle rather than dramatic, and any apparent ranking is driven more by small shifts in distribution than by clear separation between occupations.
#          """)
# comparing the full funniness distributions for every pair of occupations rather than relying on a single summary statistic. 
st.write("""
        All of this leads to a natural question: among the occupations that appear most often, are any consistently funnier than the others. To test this, we run a set of pairwise Mann Whitney U tests, with results on the heatmaps below. Darker cells indicate stronger evidence that the two occupations differ in how funny their captions tend to be.
        """)
plot_html_version2("_webappp/assets/graphs/pairwise_occupation_heatmaps.html")
st.write("""
        The results are striking at first glance. Almost every occupation appears to be significantly different from almost every other one. CEOs stand out most clearly, showing significant differences against most occupations. Meanwhile, the nurse distribution is not significantly different from doctors, lawyers, presidents, or interns, and also overlaps with clowns and cops, which suggests that these roles tend to attract a similar style of caption, or at least a similar reception from voters. There are a few other similarities within the set too: somehow doctors and presidents seem to attract similar humour as interns. 
        
        To put these significance results into perspective, we should also consider Cliff’s delta which tells us about the size and direction of the difference. This shows us that, despite the many significant differences, the effect sizes are generally quite small. Most values tend to be near zero, which means that while occupations may differ in their funniness distributions, these differences are subtle rather than stark. The clearest separation appears when comparing CEOs to other occupations but even this remains quite small. For CEOs, the effect size is typically moderate, although it drops to small when CEOs are compared with clowns, suggesting that these two roles generate humour that is closer in reception than the p values suggets.     
         """)
#The take home message is simple: occupations do shape humour, but more by gently nudging the distribution than by creating dramatic winners and losers.
st.write("""
         While all this analysis shows us some nice introductory results about occupations in our humour, we should be careful not to jump to any conclusions too quickly. Instead of looking at individual occupations, it might better to look at broader groups, which is what we will do next.
         """)
#Treating these as entirely separate occupations can dilute the signal and make the interpretation feel more fragmented than the humour intends.
st.divider()
st.subheader("Are some categories of occupations funnier than others?")
st.write("""
         When making jokes about some occupations, we think of a general name like "lawyer" but in reality there are many sub categories of lawyers (e.g. attorneys, solicitors). For interpretative and statistical reasons, it makes sense to group occupations into broader categories as this way we can have a larger sample, but also track general occupations that we think of when making jokes. The grouping is done with the help of AI tools, and are designed to reflect familiar sectors of work and social roles. This will give us more interpretable lens for comparing how different kinds of occupations show up in humour. THe categories are:
        """)
st.markdown("""
            - Arts and Entertainment (e.g. actor, musician, artist)
            - Business, Management, and Finance (e.g. ceo, manager, accountant)
            - Law, Government and Politics (e.g. lawyer, president, judge)
            - Healthcare and Medicine (e.g. doctor, nurse, therapist)
            - Education and Academia (e.g. teacher, professor, researcher)
            - Science and Technology (e.g. engineer, scientist, programmer)
            - Trades, Crafts and Manufacturing (e.g. plumber, electrician, factory worker)
            - Service Industry and Hospitality (e.g. waiter, chef, hotel staff)
            - Transportation and Logistics (e.g. driver, pilot, delivery person)
            - Agriculture, Animals and Outdoors (e.g. farmer, veterinarian, park ranger)
            - Public Safety, Militar and Security (e.g. police officer, firefighter, soldier)
            - Sports and Fitness (e.g. athlete, coach, personal trainer)
            - Media and Communications (e.g. journalist, publicist, broadcaster)
            - Domestic and Personal Care (e.g. nanny, housekeeper, personal trainer)  
         """)

st.write("""
          Together, these categories capture a large share of the occupation references. We can move from individual job titles to a broader question: how is funniness distributed across these occupational categories.
         """)
plot_html_version2("_webappp/assets/graphs/occupation_category_boxplot.html")
st.write("""
            The box plot tells a story that feels familiar by now. Across all occupation categories, the typical caption lands at a global median funniness score of 23.12. Education and Academia comes out on top, while Public Safety, Military and Security sits at the bottom. Yet the bigger pattern is not the ranking, it is the shape. Every category leans left, meaning most captions that mention an occupation are rated on the unfunny side, with the occasional standout joke stretching the distribution upwards. In other words, occupational humour is usually ordinary, but it sometimes produces a real hit.

        This is a useful reminder for reading these plots in a data story. We are not simply asking which category is funniest on average. We are asking how our humour behaves. The boxes near the lower scores suggest that job titles alone rarely carry a joke. The higher outliers suggest that when an occupation based caption works, it tends to work because it adds something else, such as a recognisable stereotype, a surprising role reversal, or a sharp twist on workplace culture.
""")
#There is a practical implication too. These categories do not appear equally often in the dataset. Only five categories have more than 10,000 captions that mention them, so some boxes are built from much smaller evidence. This can explain the apparently less outliers in categories like Education and Academia or Domestic and Personal Care. With fewer data points, there are simply fewer chances for a caption to break out as a high scoring joke.

st.write("""
 Using a series of Mann Whitney U tests, described in the Methodology section, we can compare funniness distributions across occupational categories rather than relying on a single summary measure. The aim of such a pairwise comparison is to see if the distribution of funniness scores for captions mentioning occupations from one category is significantly different from that of another. In more practical terms, we want to know if mentioning jobs from certain categories tends to produce funnier captions than mentioning jobs from other categories.
""")
plot_html_version2("_webappp/assets/graphs/pairwise_occupation_category_heatmaps.html")
st.write("""
        The results are broadly what we might expect. Most category pairs have p values below 0.05, which suggests that their funniness distributions are detectably different in this dataset. At the same time, there are clusters of overlap where we do not see a statistically significant difference. Categories that sit close together in everyday thinking also tend to sit close together here like for example, Education and Academia with Science and Technology.
         
        The pattern supports a simple intuition. Categories that are similar in social function tend to produce humour with comparable funniness distributions. Still, it is important to remember that p values speak to detectability rather than magnitude, which is why we also examine effect sizes in the next step.
         
        Cliff’s delta provides a useful complement to the p values. Where p values are large, effect sizes are small, as we would expect from possibly overlapping distributions. More importantly, even where p values are small, the effect sizes remain modest. The largest contrast is between Arts and Entertainment and Law, Government and Politics, with an absolute delta of about 0.11, which still counts as a small effect by common benchmarks. Overall, this suggests that occupational categories shape humour in subtle ways, with categories clustering together and differences showing up as gentle shifts in distributions rather than sharp separations.
         """)
#A few categories stand out more sharply. Business, Management and Finance shows significant differences against almost every other category, with Transportation and Logistics as a notable exception. This suggests that business related humour has a distinctive profile in the dataset, perhaps because it draws on a particularly recognisable set of workplace dynamics and stereotypes.
st.write("""
        So what have we learnt so the identified professional fields? No professional field is consistently funnier than the others in any dramatic sense, yet the funniness distributions are statistically distinguishable for most category pairs. This suggests that while occupations do not strongly influence humour on their own, they do interact with other elements of a caption to produce different humour outcomes. 
         
        That naturally raises the next question. If the category alone is not doing the heavy lifting, what else is? Are there particular themes that tend to co occur with different occupational categories, and do those themes help explain why the distributions shift?
         """)

st.divider()

st.subheader("Themes Across Captions")

st.write("""
        A natural next step is to look beyond how occupations occur in captions and concern ourselves with what tends to appear alongside them. When a caption mentions doctors, are they framed as heroes, as exhausted workers, or as something else entirely?
         
         Before modelling, we remove the occupation terms themselves so that the model surfaces what co occurs with the jobs, rather than simply repeating the job titles. Then, topic detection is handled by BERTopic, a modern topic modelling approach summarised in the Methodology section. The following aggragated topics are found:
         """)
plot_html_version2("_webappp/assets/graphs/aggregated_topics_all_categories.html")

st.write("""
        The first thing to notice is that the number of topics varies quite a bit across categories. Some, like Arts and Entertainment, yield a rich set of themes, while others, like Domestic and Personal Care, produce only a few distinct topics. That shows up immediately in the topic results: themes are less stable, and in a few cases no topic appears more than 200 times. This is a limitation of both the dataset and our deliberately conservative method, but it is shows that some categories occur much less frequently than others.

        We can see some interesting patterns emerging from the different topics. For certain categories like Arts and Entertainment the share of each topic is quite evenly distributed, suggesting a wider range of comedic angles. Meanwhile, in others, certain topic overshadow the rest. For example, in the Law, Government and Politics category, topics related to elections and democracy as well as Courts and legal proceedings dominate the humour landscape. One thread runs through nearly every category: a taste for absurdism, satire, and metaphor. Captions frequently lean on exaggeration, not only to make the joke land, but also to highlight any social observations. Finally, we can see that most of the topics we find for each category make sense and we do not see surprising themes emergy.
         """)

st.write("""      
         Now that we have looked at the themes that cluster around different kinds of work, we can ask about about their nature: what is the tone of these jokes. Do some professions tend to be framed more warmly, while others attract more negative humour?
         """)

st.divider()

st.subheader("Do we appriciate the work of other people?")
st.write("""
        Joking about occupations is fun, and we all do it, but it raises a sharper question: do we consistently paint some jobs in a positive light and others in a negative one. Take Politicians: A familiar stereotype paints them as slippery or dishonest, but does that cynicism actually show up in the tone of the captions. Let's find out!
         
        To explore this, we assign each caption a sentiment score using VADER sentiment analysis approach described in the Methodology section. We will follow closely the categories that had a large number of mentions to provide us with some statistical footing. The histogram below summarises the sentiment distributions for some of the categories. Intuitively, sentiment scores range from -1 (very negative) to +1 (very positive), with 0 representing a neutral tone.
         """)
plot_html_version2("_webappp/assets/graphs/sentiment_distribution_occupation_categories.html")
st.write("""
        Unsurpringly, all occupational categories cluster around a neutral sentiment. This suggests that while captions do reference occupations, they do not consistently frame them in a certain light but rather rely on other elements to carry the humour. 
         We also see a slightly larger shift towards a positive sentiment for all occupations, with Law, Government and Politics being the most positive and Public Safety, Military and Security being the most negative. This could reflect a tendency to view professions related to governance and public service in a favourable light, while those associated with enforcement and security might attract more critical humour. Still, the differences are modest and the distributions overlap heavily.
        """)

st.write("""
        To provide some statistical backing, we can analyse the statistical descriptors of the distributions. The table below shows the mean, median, standard deviation as well as the fraction of positive, negaive and neutral captions for each occupational category. The polarity imbalance simply measures the difference between the fraction of positive and negative captions, giving us a sense of the overall sentiment tilt for each category.
         """)

data = [
    ["Arts and Entertainment", 15660, 0.053247, 0.0, 0.332061, 0.325479, 0.235888, 0.438633, 0.089591],
    ["Business, Management and Finance", 12721, 0.09743, 0.0, 0.317269, 0.351859, 0.161701, 0.48644, 0.190158],
    ["Law, Government and Politics", 16707, 0.077949, 0.0, 0.338742, 0.355001, 0.198959, 0.446041, 0.156042],
    ["Healthcare and Medicine", 8349, 0.07694, 0.0, 0.326821, 0.349144, 0.197628, 0.453228, 0.151515],
    ["Service Industry and Hospitality", 13505, 0.09202, 0.0, 0.313933, 0.360163, 0.16468, 0.475157, 0.195483],
    ["Public Safety, Military and Security", 10276, 0.052072, 0.0, 0.333473, 0.329895, 0.240658, 0.429447, 0.089237],
]
cols = [
    "Occupation Category", "num_sentences", "avg_sentiment", "median_sentiment", "std_sentiment",
    "pct_positive", "pct_negative", "pct_neutral", "polarity_imbalance"
]
df = pd.DataFrame(data, columns=cols)

st.markdown(
    "<h3 style='text-align: center; margin-bottom: 0.4rem;'>Sentiment summary by occupation category</h3>", unsafe_allow_html=True)
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Occupation Category": st.column_config.TextColumn(width="large"),
        "Number of Sentences": st.column_config.NumberColumn("Captions", format="%d"),
        "Average sentiment": st.column_config.NumberColumn("Mean sentiment", format="%.3f"),
        "Median sentiment": st.column_config.NumberColumn("Median sentiment", format="%.3f"),
        "Std sentiment": st.column_config.NumberColumn("Std dev", format="%.3f"),
        "Positive (%)": st.column_config.NumberColumn("% positive", format="%.1f%%"),
        "Negative (%)": st.column_config.NumberColumn("% negative", format="%.1f%%"),
        "Neutral (%)": st.column_config.NumberColumn("% neutral", format="%.1f%%"),
        "Polarity imbalance": st.column_config.NumberColumn("Polarity imbalance", format="%.3f"),
    },
)
st.write("""
        From the table, we can see that all occupational categories have a slightly positive average sentiment, with Business, Management and Finance having the highest average sentiment of 0.09743. Meanwhile, the median is 0.0 for all categories, indicating a slight positive skew in the sentiment distribution. Therefore, the typical caption is neutral and that the positive tilt is driven by a smaller set of more upbeat captions rather than a uniformly positive tone. Variation is also broadly comparable across categories. Standard deviations sit in a narrow band, from 0.313933 to 0.338742, which suggests that the spread of sentiment within each category is similar.
        
         All these statistical terms simply confirm our previous observations from the histograms: while there are slight differences in sentiment across occupational categories, the overall sentiment distributions are relatively similar, with a slight positive tilt. This suggests that while occupations do influence the tone of humour to some extent, they do not strongly dictate whether captions are perceived as positive or negative. This indicates a balanced approach to humour, where occupations are not consistently framed in a positive or negative light.
         """)
#Here
st.write("""
        To push the sentiment story a little further, we compared how the tone of captions shifts across occupational categories. The main picture is simple. Pairwise Mann Whitney U tests reveal that most categories have significantly different sentiment distributions from each other, with a few exceptions like Healthcare with Government and Politics and Business and Finance with Service Industry. However, when we look at Cliff's delta to understand the effect sizes of these differences, we find that they are generally small (less than 0.147) across the board. This suggests that while the sentiment distributions are statistically different, the practical significance of these differences is limited.
         
         We can try and think of why certain occupation categories might have similar sentiment distributions. Business, Management and Finance and Service Industry and Hospitality might both be associated with customer service and workplace dynamics, resulting in comparable sentiment patterns. Similarly, Healthcare and Medicine and Law, Government and Politics might both involve high-stakes decision-making and ethical considerations, leading to similar sentiment distributions.
         """)

st.write("""
        To summarise, our sentiment analysis of occupational categories in captions indicates that while there are variations in sentiment across different professions, the overall tone remains relatively balanced and neutral. This suggests that humour related to occupations does not consistently lean towards positivity or negativity, but rather reflects a diverse range of perspectives and attitudes towards different professions. Furthermore, the statistical tests reveal that while most occupational categories have significantly different sentiment distributions, the effect sizes of these differences are small, indicating limited practical significance.
         """)
         
        
st.divider()
st.subheader("What have we learned?")
st.write("""
        In this axis, we traced how occupations show up in New Yorker captions, from simple frequency to performance, themes, and tone. Common jobs such as "clown" and "president" appear often, but they do not consistently produce high funniness scores. Instead, occupation based captions cluster around a low to mid range median, with occasional outliers, suggesting that job titles set the scene but rarely carry the joke on their own. Grouping occupations into broader categories revealed detectable differences in funniness distributions, but the gaps are generally modest. This lead us to look at the themes that occur with different occupational categories. Topic modelling showed what sits around these occupations, from workplace culture to wider social roles, while sentiment remains mostly neutral with a slight positive tilt, suggesting a balanced approach to occupational humour. Overall, occupations provide a familiar backdrop for humour, but the real comedic value comes from how they are framed and the context in which they appear.
         
        Enjoy this final cartoon from contest #726 that features occupational humour!
         """)
ImageCaptionCenter_C(
    image_path="data/newyorker_caption_contest_virgin/images/726.jpg",
    caption=[
        "The President says that we should ignore them they will just go away.",
        "Relax! The president says they're harmless.",
        "Should I call the SWAT team?",
    ],
)
#

#SHort summary: The analysis of occupations revealed that while certain jobs appear frequently in humour, they do not consistently lead to funnier captions. Instead, occupational references tend to cluster around low to mid-range funniness scores, with occasional outliers that are percieved as very funny. Grouping occupations into broader categories showed some detectable differences in humour about different types of work, but these differences were generally modest and with small statistical effect sizes. Topic modelling revealed common themes that co-occur with occupational references, highlighting the context in which these jobs are framed in humour. These were often related to workplace culture, social roles, and stereotypes associated with different professions. Sentiment analysis showed that comments with occupations are generally neutral, but with a slight positive tilt, suggesting a balanced approach to occupational humour. 