import streamlit as st
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html
from _webappp.assets.app_design import *
from _webappp.assets.app_definitions import *
import pandas as pd
import numpy as np
from _webappp.assets.app_definitions import AppParams as AP

PagesData.AXIS_2.value.description = """
    Humour is something so hard to model, that it is often simpler to look for patterns surrounding certain topics rather than trying to directly model exactly what makes something funny. In this section of our story on humour in  the New Yorker Caption Contest, we focus on occupational references in captions. Why? Our whole lives are oriented around our works and professions, thus it is no suprise that occupations have tunneled their way into our humour. Look at the figure below and decide which caption you find the funniest! 
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
    The captions above are among the funniest captions submitted for this cartoon. The winner was the second caption, which makes a reference to managers and plays on the stereotype of managers and corporate culture. You could reasonably shrug and say that this is only one cartoon, but occupational references are actually quite common in everyday humour. If you would like to see where occupational humour appears, how well it tends to perform, and how it is distributed across the New Yorker Caption Contest, read on.
""")

st.subheader("A few words about our methodology")
st.write("""
        Identifying occupational references in captions is not straightforward. People can be explicit, by naming a job title, but they can also be indirect, by hinting at workplace routines, professional stereotypes, or role specific jargon. With a dataset this large, manual annotation is not feasible, so we take a deliberately simple approach: we restrict the analysis to direct mentions of job titles taken from a curated list of roughly 33,000 occupations. We then preprocess the captions to standardise the text by lowercasing and removing punctuation, and use string matching to detect job titles, including plural forms. This gives us a reliable baseline for studying where occupations appear and how they perform in humour, without introducing the extra assumptions and complexity of a model designed to infer indirect references. However, we acknowledge that this approach misses a large part of humour related to subtle or indirect references to occupations, which could be explored in future work.
""")
st.subheader("Where do occupations appear and how frequent are they?")

st.write("""
       If we split the captions into two simple groups, those that mention an occupation and those that do not, one thing becomes clear straight away. Only a small share of captions talk about jobs at all. Specifically, out of the total number of captions, only about 6.14% contain direct references to job titles from our curated list. That may sound low, but it is worth remembering what this number does and does not mean. We are only counting explicit job titles, so any occupational humour that works through hints or stereotypes without naming the role will not be captured here.
         
        Interestingly, a simple t-test reveals that captions with occupational references are on average rated less funny than those without (p-value < 0.05). While this might seem counterintuitive at first, it could be explained by the fact that occupational humour often relies on stereotypes or clichés that might not resonate with all audiences. Additionally, people might have different experiences and perceptions of certain occupations, which could influence their appreciation of jokes related to them. In any case, we shoul not lose hope in occupational humour just yet! There could be many confounding factors at play here and the sheer difference in group sizes (6.04% vs 93.96%) makes it hard to draw definitive conclusions. We should dig deeper and look at distributions, patterns, and other factors before making any strong claims about the role of occupations in humour.
         
        After all this text, I am sure you will enjoy a cartoon break! Here is a cartoon from contest #661 that features some occupational humour!   
         """
)
ImageCaptionCenter_C(
    image_path="data/newyorker_caption_contest_virgin/images/661.jpg",
    caption=[
        "I am pleased to announce that Dopey will be leaving us to pursue a career as White House Chief of Staff.",
        "Really? All of you are running for the Democratic presidential nomination?",
        "Grouchy, you'll be Press Secretary, Dopey you'll be Attorney General...",
    ],
)

st.divider()

st.write("""
        It might not be surprising that the term "clown" is found most commonly in humour about occupations, since basically humour is their job definition. As a sidenote, clown is often used to mean someone silly, so its mentions as most frequent occupation should be taken with a little suspicion. But if clowns are by definition funny, what other jobs occur most often in captions? Are the top occurences other jobs from the entertainment sector or do we make fun of people running our political systems, who keep us safe, or those who take care of our health? Well, See the bar chart below for the most frequently occuring occupations. Are there any surprises?
         """)
plot_html("_webappp/assets/graphs/occupation_dropdown_plot.html")
st.write(
    """
    Well, it seems like people like to joke about quite serious jobs, and perhaps jobs that everyone can relate to in some ways. So now that we know the most frequently occuring occupations, it makes sense to see in how many contests thy each appear in, becuase, what if their appearance is only due to the given setting? Well, the bar graph below for the 20 most common occupations tells us that all of the most frequent occupations are mentioned in around half the captions, with some being virtually everywhere. For instance, we see that some occupations like "president" and "cop" appear in nearly all contests (there are in total 383 contests in our dataset), while only "chef" appears in less than half of the contests. This suggests that all of these occupations are quite common and do not depend much on the specific cartoon content, however, there are some occupations which occur much more frequently than others, indicating that some jobs are more likely to be referenced in humour than others, no matter if the joke is actually funny or not.
    """
)
plot_html("_webappp/assets/graphs/term_num_contests_bar.html")
st.write("""
          Beyond simple frequency counts, we can check which occupations are actually the funniest, or the worst performers. This can be done by looking at the average or median funny scores, introduced in axis 1, of captions that reference each occupation above a certain threshold frequency to avoid noise. The results show us that it is indeed not the most frequent occupations that are present in the funniest captions: only "rabbi" made both cuts while the term "leader" were also among the worst performers. Notice however that the difference between the funniest and least funny occupations is only around 5 points, which is not a very large margin considering the funny score scale from 0 to 100. This suggests that while some occupations might be slightly funnier than others on "average", the overall difference in humour related to occupations is relatively small.
         """)
plot_html("_webappp/assets/graphs/best_worst_occupations_by_median.html")
st.write("""
         Now that we have an idea of the most frequent, the best performers in terms of humour, and those that fell flat, we can choose a certain set of occupation that we can track a bit more in depth! We handpick frequent jobs so that we can make proper statistical tests. We choose to follow doctors, nurses, presidents, lawyers, interns, ceos, cops and clowns a bit more closely. More importantly, we are interested in the distribution of their funny score across different contests, to deduce which jobs from this list do we find to contribute to a joke the not. On a more statistical note, it is best to look at distributions instead of simply comparing jobs based on their averages or median funniness. 
         """)
plot_html("_webappp/assets/graphs/occupation_distribution_multiple.html")
st.write("""
            Or, an even better way to visualise is through a box plot! See below the box plot for the previously highlighted occupations
         """)
plot_html("_webappp/assets/graphs/occupation_box_plots.html")
st.write("""
        We see that the median funniness for all occupations is quite similar, around 23 points, MISSING
         """)

st.write("""
         This all leads us to the question: from the most frequent occupations, which are funnier than others? To compare these occupations, we can conduct a series of statistical tests (Whitney-Mann U tests) between each pair of occupations to see if there are significant differences in their funniness distributions. The heatmap below summarises the results of these tests, where a darker color indicates a more significant difference in funniness between the two occupations being compared. 
         """)
plot_html("_webappp/assets/graphs/pairwise_occupation_heatmaps.html")
st.write("""
         While all this analysis shows us some nice introductory results about occupations in our humour, we should be careful not to jump to any conclusions too quickly. When making jokes about some occupations, we think of a general name like "lawyer" but in reality there are many sub categories of lawyers (e.g. attorneys), which should be grouped together for a more accurate analysis. For purely interpretative purposes, but also for statistical ones, it makes sense to group occupations into categories as this way we can have a larger sample, but also track general occupations that we think of when making jokes. This leads us to see if certain categories of occupations are funnier than others. Creating our grouping manually (with the help of some AI assistance) we can conduct an analysis on these categories rather than individual occupations.
         """)

st.divider()
st.subheader("Are some categories of occupations funnier than others?")
st.write("""
        From the approximately 3000 or so occupations that were found in the captions, we have created 14 categories to group them into, and discarded any occupations that did not fit into these categories, or were too hard to categorise correctly. We created the following categories:
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
          These categories cover a large portion of the general occupations found in captions, and provide a good basis for following them for the rest of the analysis. So now we can ask how funniness is distributed across these categories? 
         """)
plot_html("_webappp/assets/graphs/occupation_category_boxplot.html")
st.write("""
        The box plot tells a story that feels familiar by now, but still worth pausing on. Across all occupation categories, the typical caption lands at a global median funniness score of 23.12. Education and Academia comes out on top, while Public Safety, Military and Security sits at the bottom. Yet the bigger pattern is not the ranking, it is the shape. Every category leans left, meaning most captions that mention an occupation are rated on the unfunny side, with the occasional standout joke stretching the distribution upwards. In other words, occupational humour is usually ordinary, but it sometimes produces a real hit.

This is a useful reminder for reading these plots in a data story. We are not simply asking which category is funniest on average. We are asking how humour behaves. The clusters near the lower scores suggest that job titles alone rarely carry a joke. The higher outliers suggest that when an occupation based caption works, it tends to work because it adds something else, such as a recognisable stereotype, a surprising role reversal, or a sharp twist on workplace culture.

There is a practical implication too. These categories do not appear equally often in the dataset. Only five categories have more than 10,000 captions that mention them, so some boxes are built from much smaller evidence. That imbalance matters for interpretation, and it is why the distributional view is so helpful: it lets us separate broad patterns from a handful of unusually strong captions.
         
""")

st.write("""
Using a series of Mann Whitney U tests (see Methodology), we can compare the funniness distributions across occupation groups rather than relying on a single measure. As before, the heatmap is astonishingly clear. Almost every category is significantly different from almost every other category. The only exceptions are MISSING
""")
plot_html("_webappp/assets/graphs/pairwise_occupation_category_heatmaps.html")
st.write("""
        This MISSING
         """)
st.write("""
        So what have we learnt so the identified professional fields? Well, we can see that no occupational field is particularly funnier than others, but we can see that there are significant differences in funniness distributions between almost all categories. This suggests that while occupations do not strongly influence humour on their own, they do interact with other elements of a caption to produce different humour outcomes. This leads us to wonder what other elements might be at play here? Are there certain themes or topics that co occur with these occupational categories that might influence their funniness? Let's find out!
         """)
st.divider()

st.subheader("Themes Across Captions")

"""
A natural next step is to look beyond how often occupations appear, and ask what tends to appear alongside them. When captions mention doctors, are they framed as heroes, as exhausted workers, or as something else entirely. When they mention law and government, do we see power, bureaucracy, or everyday frustration.

 Before modelling, we remove the occupation terms themselves so that the model surfaces what co occurs with the jobs, rather than simply repeating the job titles. The interactive figures below summarise the most prominent themes within each category, giving us a clearer picture of the ideas, stereotypes, and situations that cluster around different kinds of work. Do any of these themes surprise you.
"""
st.write("""
        A natural next step is to look beyond how occupations occur in captions and concern ourselves with what tends to appear alongside them. When a caption mentions doctors, are they framed as heroes, as exhausted workers, or as something else entirely? When they mention law and government, do we see power, bureaucracy, or everyday frustration?
         
        To explore this, we group together all captions that reference each occupational category and run a topic model using BERTopic. You can find out more about BERTopic in the Methodology section. The interactive figures below summarise the most prominent themes within each category, giving us a clearer picture of the co-occuring themes with the different kinds of work. Do any of these themes surprise you?
         """
        )
plot_html("_webappp/assets/graphs/aggregated_topics_all_categories.html")

st.write("""
        That shows up immediately in the topic results: themes are less stable, and in a few cases no topic appears more than 200 times. This is a limitation of both the dataset and our deliberately conservative method, but it is also informative in its own right. Some kinds of work simply show up less often in caption humour, at least when we restrict ourselves to direct mentions of job titles.

        Beyond that, we can see some interesting patterns emerging from the different topics. For certain categories like Arts and Entertainment the share of each topic is quite evenly distributed, suggesting a wider range of comedic angles people take. Meanwhile, in others, certain topic overshadow the rest. For example, in the Law, Government and Politics category, topics related to elections and democracy as well as Courts and legal proceedings dominate the humour landscape, while in Business, Management and Finance, topics related to corporate culture and office life are most prominent. 
         
        One thread runs through nearly every category: a taste for absurdism, satire, and metaphor. Captions frequently lean on exaggeration and improbable scenarios, not only to make a joke land, but also to sharpen whatever social observation sits behind it challenges of different professions. Finally, we can see that most of the topics we find for each category make sense given the nature of the occupations involved and we do not see any particularly surprising themes emerging.
         """)

st.write("""
        As we have now looked at the themes that occur alongside occupations, we can wonder how the sentiment related to these occupations varies. Do we tend to joke positively about certain professions while being more negative towards others? For example, do we see more positive sentiment towards healthcare workers compared to politicians? 
         """)

st.divider()

st.subheader("Do we appriciate the work of other people?")
st.write("""
        Joking about occupations is fun, and we all do it, but it raises a sharper question: do we consistently paint some jobs in a positive light and others in a negative one. For example, doctors and nurses are heroes who help us when we get sick, but they are also somewhat related to death and so people might be afraid of them? or take Politicians: A familiar stereotype paints them as slippery or dishonest, but does that cynicism actually show up in the tone of the captions. Let's find out!
         
        To explore this, we assign each caption a sentiment score using a standard sentiment analysis approach described in the Methodology section. We will follow closely the categories that had a large number of mentions to provide us with some statistical footing. The hitogram below summarises the sentiment distributions for each occupational category. A negative sentiment score indicates a more negative tone, while a positive score indicates a more positive tone.
         """)

st.write("""
        Unsurpringly, most occupational categories cluster around a neutral sentiment. This suggests that while captions do reference occupations, they do not consistently frame them in a positive or negative light but rather rely on other elements to carry the humour. However, we also see a slightly larger shift towards a positive sentiment for all occupations, with Law, Government and Politics being the most positive and Public Safety, Military and Security being the most negative. This could reflect a tendency to view professions related to governance and public service in a favourable light, while occupations in the arts might be associated with more critical or satirical humour. Nevertheless, the overall sentiment distributions are relatively similar across categories, indicating that occupational references alone do not strongly influence the tone of the humour.
                """)
plot_html("_webappp/assets/graphs/occupation_sentiment_distribution.html")

st.write("""
        To provide some statistical backing to these observations, we can conduct analyse the statistical descriptors of the distributions. The table below shows the mean, median, standard deviation as well as the fraction of positive, negaive and neutral captions for each occupational category. The polarity imbalance simply measures the difference between the fraction of positive and negative captions, giving us a sense of the overall sentiment tilt for each category.
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

st.subheader("Sentiment summary by occupation category")

# Nice interactive table
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
        From the table, we can see that all occupational categories have a slightly positive average sentiment, with Business, Management and Finance having the highest average sentiment of 0.09743, while Public Safety, Military and Security has the lowest average sentiment of 0.052072. The median sentiment for all categories is 0.0, indicating that the tone linked to a category cannot be easily classified as positive or negative. The standard deviation of sentiment scores is relatively similar across categories, ranging from 0.313933 to 0.338742, suggesting a comparable level of sentiment variability within each category.
        
         All these statistical terms simply confirm our previous observations from the histograms: while there are slight differences in sentiment across occupational categories, the overall sentiment distributions are relatively similar, with a slight positive tilt. This suggests that while occupations do influence the tone of humour to some extent, they do not strongly dictate whether captions are perceived as positive or negative. Furthermore, in captions, people tend to make approximately the same number of positive as negative jokes about occupations, as the median sentiment is 0.0 for all categories. This indicates a balanced approach to humour, where occupations are not consistently framed in a positive or negative light.
         """)

st.write("""
        To further the sentiment analysis, we can again conduct a series of statistical tests to compare the sentiment distributions across occupation categories. Pairwise Mann Whitney U tests reveal that most categories have significantly different sentiment distributions from each other, with a few exceptions. In fact, we find that the null hypothesis of equal distributions cannot be rejected for the following pairs: Arts and Entertainment vs Public Safety, Military and Security, then Business, Management and Finance vs Service Industry and Hospitality, and finally Healthcare and Medicine vs Law, Government and Politics. This suggests that for these pairs of categories, the sentiment distributions are similar enough that we cannot confidently say they differ significantly.
         
        To interpret these results, we can try and think of why certain occupation categories might have similar sentiment distributions. For example, both Arts and Entertainment and Public Safety, Military and Security might evoke a mix of admiration and criticism, leading to a balanced sentiment distribution. Similarly, Business, Management and Finance and Service Industry and Hospitality might both be associated with customer service and workplace dynamics, resulting in comparable sentiment patterns. Finally, Healthcare and Medicine and Law, Government and Politics might both involve high-stakes decision-making and ethical considerations, leading to similar sentiment distributions. While these are some possible interpretation, they serve to influence the reader to think about the underlying reasons for the observed statistical similarities. 
         
         Once again, conducting a U-test is not enough to draw conclusions, we should also inspect Cliff's delta values to understand the effect sizes of these differences. We infact find that every pair of occupation categories has a small effect size (|d| < 0.147), indicating that while the sentiment distributions are statistically different, the practical significance of these differences is limited. This further shows the need to improve our methodology to capture more nuanced sentiment differences across occupational categories. Nevertheless, these results provide us with some insights into how sentiment varies across different professions in humour contexts.
         """)

st.write("""
        To summarise, our sentiment analysis of occupational categories in captions indicates that while there are slight variations in sentiment across different professions, the overall tone remains relatively balanced and neutral. This suggests that humour related to occupations does not consistently lean towards positivity or negativity, but rather reflects a diverse range of perspectives and attitudes towards different professions. Furthermore, the statistical tests reveal that while most occupational categories have significantly different sentiment distributions, the effect sizes of these differences are small, indicating limited practical significance. This highlights the complexity of humour and the need for more nuanced approaches to capture the subtleties of sentiment in occupational humour.
         """)

st.divider()
st.subheader("What have we learned?")
st.write("""
        This axis of our research into humour in the New Yorker Caption Contest has taken us on a journey through occupations, revealing intriguing patterns about how different professions are portrayed in comedic contexts. We began by identifying the most frequently mentioned occupations in captions, discovering that while some jobs like "clown" and "president" appear often, they do not necessarily correlate with higher funniness scores. Instead, we found that the funniness of captions mentioning occupations tends to cluster around a neutral median score, with occasional outliers that stand out as particularly funny. This suggests that while occupations can provide a backdrop for humour, they rarely carry the joke on their own. 

        We then grouped occupations into broader categories, such as Healthcare, Law, and Arts, to explore whether certain fields were funnier than others. Our analysis revealed significant differences in funniness distributions across these categories, indicating that the context and stereotypes associated with different professions play a crucial role in shaping humour. For instance, captions referencing Education and Academia tended to be funnier on average compared to those about Public Safety and Security.
         
        Delving deeper, we employed topic modelling to uncover the themes that co-occur with occupational references in captions. This approach highlighted the diverse angles from which different professions are joked about, ranging from workplace culture to societal roles. Finally, our sentiment analysis revealed that while there are slight variations in sentiment across occupational categories, the overall tone remains relatively balanced and neutral. This suggests that humour related to occupations does not consistently lean towards positivity or negativity, but rather reflects a diverse range of perspectives and attitudes towards different professions.
         
        As a final reflection, our exploration of occupations in humour has underscored the complexity of comedic expression. Occupations provide a rich tapestry of themes and stereotypes that comedians can draw upon, but the success of a joke often hinges on more than just the job title itself. Instead, it is the interplay of context, societal attitudes, and individual creativity that ultimately determines what makes us laugh.
         
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
