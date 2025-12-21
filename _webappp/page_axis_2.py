import streamlit as st
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html, plot_html_version2
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
        It might not be surprising that the term "clown" is found most commonly in humour about occupations, since humour is their job definition. That said, we should treat this result with a little caution. In everyday language, "clown" is also used as a casual insult for someone acting foolishly, so not every mention is necessarily a literal reference to the profession. 
         
        Still, the pattern is an inviting starting point. What other jobs occur most often in captions? Are the top occurences other jobs from the entertainment sector or do we make fun of people running our political systems, who keep us safe, or those who take care of our health? Well, See the bar chart below for the most frequently occuring occupations. Are there any surprises?
         """)
plot_html_version2("_webappp/assets/graphs/occupation_dropdown_plot.html")

st.write(
    """
    Well, it seems like people like to joke about quite serious jobs, and perhaps jobs that everyone can relate to in their lives. Now that we know which occupations are mentioned most often, the next question is whether they only appear because of a few cartoons with the right setting. One way to check is to see how widely each occupation is spread across the contests.  The bar chart below focuses on the 20 most common occupations and shows that these jobs appear in roughly half of all contests, with some cropping up almost everywhere. For example, "president" and "cop" show up in nearly every contest in the dataset, as there are 383 contests in total. By contrast, "chef" appears in fewer than half of them. This suggests that the most common occupations are not simply tied to a handful of scenes or themes, but are part of the contest vocabulary more generally, even if the jokes themselves vary widely in how funny they are.
    """
)

plot_html_version2("_webappp/assets/graphs/term_num_contests_bar.html")
st.write("""
          Frequency tells us what is common, but not what actually works as a joke. To asess the performance of occupations we can check which occupations are actually the funniest, or the worst performers. This can be done by looking at the median funny scores, introduced in axis 1, of captions that reference each occupation above a certain threshold frequency to avoid noise. The results show us that it is indeed not the most frequent occupations that are present in the funniest captions: None of the top 20 most frequnt make the cut for best or worst occupations. In each of the charts, we see a very small gradual change along the x-axis, indicating that there are no occupations that are dramatically funnier or less funny than others. Furthermore, we see that the difference between the best and worst occupations is quite small, suggesting that while some jobs might be slightly funnier than others on average, the overall impact of occupation on humour is limited.
         """)
plot_html_version2("_webappp/assets/graphs/best_worst_occupations_by_median.html")

st.write("""
         Now that we have an idea of the most frequent, the best performers in terms of humour, and those that fell flat, we can choose a certain set of occupation that we can track a bit more in depth! We handpick frequent jobs so that we can make proper statistical tests. We choose to follow doctors, nurses, presidents, lawyers, interns, ceos, cops and clowns a bit more closely. More importantly, we are interested in the distribution of their funny score across different contests, to deduce which jobs from this list do we find to contribute to a joke the not. On a more statistical note, it is best to look at distributions instead of simply comparing jobs based on their median funniness. The key question is not only which occupation has the highest average score, but how reliably each one contributes to a joke across different contests. That is why we focus on distributions rather than relying on a single mean or median.

        What we find is striking in its consistency. All of these occupations have very similar funniness distributions, each with a median of roughly 23 points. The distributions also share the same overall shape: they are left skewed, with relatively few extremely low scoring captions, a dense cluster around the middle, and a longer tail of higher scoring outliers. In practical terms, occupational humour seems to produce a steady baseline of moderately funny captions, with the occasional standout line that rises well above the rest.
         """)
plot_html_version2("_webappp/assets/graphs/occupation_distribution_multiple.html")
st.write("""
        An even clearer way to compare these distributions is with a box plot. It lets us see the median, the spread, and the outliers for each occupation at a glance. The figure below shows the box plots for the occupations we highlighted above.
         """)
plot_html_version2("_webappp/assets/graphs/occupation_box_plots.html")
st.write("""
        This plot confirms what we saw before. All of the occupations cluster around a median funniness score of roughly 23 points, with broadly similar spreads and a familiar pattern of outliers. In other words, the differences between these jobs are subtle rather than dramatic, and any apparent ranking is driven more by small shifts in distribution than by clear separation between occupations.
         """)

st.write("""
        All of this leads to a natural question: among the occupations that appear most often, are any consistently funnier than the others. To test this, we run a set of pairwise Mann Whitney U tests, comparing the full funniness distributions for every pair of occupations rather than relying on a single summary statistic. The heatmap below summarises the results. Darker cells indicate stronger evidence that the two occupations differ in how funny their captions tend to be.
        """)
plot_html_version2("_webappp/assets/graphs/pairwise_occupation_heatmaps.html")
st.write("""
        The results are striking at first glance. Almost every occupation appears to be significantly different from almost every other one. CEOs stand out most clearly, showing significant differences against nearly all other occupations. Meanwhile, nurses sit in a cluster of closer neighbours. Their distribution is not significantly different from doctors, lawyers, presidents, or interns, and also overlaps with clowns and cops,which suggests that these roles tend to attract a similar style of caption, or at least a similar reception from voters. There are a few other similarities within the set too: somehow doctors and presidents seem to attract similar humour as interns. 
        
        To put these significance results into perspective, we should also  consider an effect size measure because, while the Mann Whitney U test tells us whether two distributions are detectably different, it does not tell us how large that difference is. For that, we use Cliff’s delta, which compares two groups by estimating how often a randomly chosen caption from one occupation scores higher than a randomly chosen caption from the other. Values near zero indicate very similar distributions, while values further from zero indicate a clearer separation, and the sign shows which occupation tends to score higher.
        What we see here is that, despite the many significant differences, the effect sizes are generally quite small. MOst values tend to be near zero, which means that while occupations may differ in their funniness distributions, these differences are subtle rather than stark. The clearest separation appears when comparing CEOs to other occupations. For CEOs, the effect size is typically moderate, although it drops to small when CEOs are compared with clowns, suggesting that these two roles generate humour that is closer in reception than the p values alone might imply. The take home message is simple: occupations do shape humour, but more by gently nudging the distribution than by creating dramatic winners and losers.
         """)
st.write("""
         While all this analysis shows us some nice introductory results about occupations in our humour, we should be careful not to jump to any conclusions too quickly. When making jokes about some occupations, we think of a general name like "lawyer" but in reality there are many sub categories of lawyers (e.g. attorneys, solicitors). Treating these as entirely separate occupations can dilute the signal and make the interpretation feel more fragmented than the humour intends. For interpretative and statistical reasons, it makes sense to group occupations into broader categories as this way we can have a larger sample, but also track general occupations that we think of when making jokes. This leads us to see if certain categories of occupations are funnier than others.
         """)

st.divider()
st.subheader("Are some categories of occupations funnier than others?")
st.write("""
        From the roughly 3,000 distinct occupation terms found in the captions, we created 14 broader categories, with some assistance from an AI tool. Any occupations that did not fit cleanly into these groupings were left uncategorised, so that ambiguous cases did not add noise to the analysis. The categories themselves are designed to reflect familiar sectors of work and social roles, giving us a more interpretable lens for comparing how different kinds of occupations show up in humour. This leads us to the following set of categories:
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
          Together, these categories capture a large share of the occupation references in the captions and give us a framework for the rest of the analysis. With this structure in place, we can move from individual job titles to a broader question: how is funniness distributed across these occupational categories.
         """)
plot_html_version2("_webappp/assets/graphs/occupation_category_boxplot.html")
st.write("""
            The box plot tells a story that feels familiar by now, but still worth pausing on. Across all occupation categories, the typical caption lands at a global median funniness score of 23.12. Education and Academia comes out on top, while Public Safety, Military and Security sits at the bottom. Yet the bigger pattern is not the ranking, it is the shape. Every category leans left, meaning most captions that mention an occupation are rated on the unfunny side, with the occasional standout joke stretching the distribution upwards. In other words, occupational humour is usually ordinary, but it sometimes produces a real hit.

        This is a useful reminder for reading these plots in a data story. We are not simply asking which category is funniest on average. We are asking how our humour behaves. The boxes near the lower scores suggest that job titles alone rarely carry a joke. The higher outliers suggest that when an occupation based caption works, it tends to work because it adds something else, such as a recognisable stereotype, a surprising role reversal, or a sharp twist on workplace culture.

        There is a practical implication too. These categories do not appear equally often in the dataset. Only five categories have more than 10,000 captions that mention them, so some boxes are built from much smaller evidence. This can explain the apparently less outliers in categories like Education and Academia or Domestic and Personal Care. With fewer data points, there are simply fewer chances for a caption to break out as a high scoring joke.
""")

st.write("""
 Using a series of Mann Whitney U tests, described in the Methodology section, we can compare funniness distributions across occupational categories rather than relying on a single summary measure. As before, the heatmap is one way to visualise the results. The aim of such a pairwie comparison is to see if the distribution of funniness scores for captions mentioning occupations from one category is significantly different from that of another category. In more practical terms, we want to know if mentioning jobs from certain categories tends to produce funnier captions than mentioning jobs from other categories.
""")
plot_html_version2("_webappp/assets/graphs/pairwise_occupation_category_heatmaps.html")
st.write("""
        The results are broadly what we might expect. Most category pairs have p values below 0.05, which suggests that their funniness distributions are detectably different in this dataset. At the same time, there are clusters of overlap where we do not see a statistically significant difference. Categories that sit close together in everyday thinking also tend to sit close together here. For example, Education and Academia is not clearly separable from Science and Technology or Politics, and Healthcare and Medicine shows overlap with Sports and Fitness.

        A few categories stand out more sharply. Business, Management and Finance shows significant differences against almost every other category, with Transportation and Logistics as a notable exception. This suggests that business related humour has a distinctive profile in the dataset, perhaps because it draws on a particularly recognisable set of workplace dynamics and stereotypes.

        The pattern supports a simple intuition. Categories that are similar in social function tend to produce humour with comparable funniness distributions. Still, it is important to remember that p values speak to detectability rather than magnitude, which is why we also examine effect sizes in the next step.

        Cliff's delta offers a directly complementary view of the results. WHen the p-values were large, the effect sizes are always small, which is what we would expect because non significant results suggest similar distributions. However, even when the p-values are small, the effect sizes do not tend to be much larger, with largest value occuring for Arts and Entertainment compared to Law, Government and Politics. The value is 0.11 in magnitude, which is still considered a small effect size according to common benchmarks. This reinforces the idea that while occupational categories do shape humour, they do so in subtle ways rather than creating stark differences in funniness. Overall, the analysis suggests that occupational humour is nuanced, jokes about different kinds of work tend to cluster together, but the differences between categories are more about gentle shifts in distribution than dramatic separations.
         """)
st.write("""
        So what have we learnt so the identified professional fields? No professional field is consistently funnier than the others in any dramatic sense, yet the funniness distributions are statistically distinguishable for most category pairs. This suggests that while occupations do not strongly influence humour on their own, they do interact with other elements of a caption to produce different humour outcomes. 
         
        That naturally raises the next question. If the category alone is not doing the heavy lifting, what else is. Are there particular themes that tend to co occur with different occupational categories, and do those themes help explain why the distributions shift. Let us find out.
         """)

st.divider()

st.subheader("Themes Across Captions")

st.write("""
        A natural next step is to look beyond how occupations occur in captions and concern ourselves with what tends to appear alongside them. When a caption mentions doctors, are they framed as heroes, as exhausted workers, or as something else entirely? When they mention law and government, do we see power, bureaucracy, or everyday frustration?
         
         Before modelling, we remove the occupation terms themselves so that the model surfaces what co occurs with the jobs, rather than simply repeating the job titles. Then, topic detection is handled by BERTopic, a modern topic modelling approach summarised in the Methodology section. We run the model separately for each occupational category to capture the unique themes that arise in different contexts. The results are summarised below.
         """)
plot_html_version2("_webappp/assets/graphs/aggregated_topics_all_categories.html")

st.write("""
        The first thing to notice is that the number of topics varies quite a bit across categories. Some, like Arts and Entertainment, yield a rich set of themes, while others, like Domestic and Personal Care, produce only a few distinct topics. That shows up immediately in the topic results: themes are less stable, and in a few cases no topic appears more than 200 times. This is a limitation of both the dataset and our deliberately conservative method, but it is also informative in its own right. Some kinds of work simply show up less often in caption humour, at least when we restrict ourselves to direct mentions of job titles.

        Beyond This, we can see some interesting patterns emerging from the different topics. For certain categories like Arts and Entertainment the share of each topic is quite evenly distributed, suggesting a wider range of comedic angles people take. Meanwhile, in others, certain topic overshadow the rest. For example, in the Law, Government and Politics category, topics related to elections and democracy as well as Courts and legal proceedings dominate the humour landscape, while in Business, Management and Finance, topics related to corporate culture and office life are most prominent. 
         
        One thread runs through nearly every category: a taste for absurdism, satire, and metaphor. Captions frequently lean on exaggeration, not only to make the joke land, but also to highlight any social observations. Finally, we can see that most of the topics we find for each category make sense given the nature of the occupations involved and we do not see any particularly surprising themes emerging.
         """)

st.write("""      
         Now that we have looked at the themes that cluster around different kinds of work, we can ask about about their nature: what is the tone of these jokes. Do some professions tend to be framed more warmly, while others attract more negative humour. For instance, do captions that mention healthcare workers lean more positive than captions that mention politicians.
         """)

st.divider()

st.subheader("Do we appriciate the work of other people?")
st.write("""
        Joking about occupations is fun, and we all do it, but it raises a sharper question: do we consistently paint some jobs in a positive light and others in a negative one. For example, doctors and nurses are heroes who help us when we get sick, but they are also somewhat related to death and so people might be afraid of them? or take Politicians: A familiar stereotype paints them as slippery or dishonest, but does that cynicism actually show up in the tone of the captions. Let's find out!
         
        To explore this, we assign each caption a sentiment score using a standard sentiment analysis approach described in the Methodology section. We will follow closely the categories that had a large number of mentions to provide us with some statistical footing. The histogram below summarises the sentiment distributions for a few of the caegories discussed before. A negative sentiment score indicates a more negative tone, while a positive score indicates a more positive tone.
         """)
plot_html_version2("_webappp/assets/graphs/sentiment_distribution_occupation_categories.html")
st.write("""
        Unsurpringly, all occupational categories cluster around a neutral sentiment. This suggests that while captions do reference occupations, they do not consistently frame them in a positive or negative light but rather rely on other elements to carry the humour. However, we also see a slightly larger shift towards a positive sentiment for all occupations, with Law, Government and Politics being the most positive and Public Safety, Military and Security being the most negative. This could reflect a tendency to view professions related to governance and public service in a favourable light, while those associated with enforcement and security might attract more critical or cautious humour. Still, the differences are modest and the distributions overlap heavily. The broader takeaway is that occupational references alone do not strongly determine the emotional tone of the humour.
                """)

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
        From the table, we can see that all occupational categories have a slightly positive average sentiment, with Business, Management and Finance having the highest average sentiment of 0.09743, while Public Safety, Military and Security has the lowest average sentiment of 0.052072. This of course only tells us that the data is slightly skewed towards positive sentiment, but not by much, because the median sentiment for all categories is 0.0. This tells us that the typical caption is neutral and that the positive tilt is driven by a smaller set of more upbeat captions rather than a uniformly positive tone. The standard deviation of sentiment scores is relatively similar across categories, ranging from 0.313933 to 0.338742, suggesting a comparable level of sentiment variability within each category.
        
         Variation is also broadly comparable across categories. Standard deviations sit in a narrow band, from 0.313933 to 0.338742, which suggests that the spread of sentiment within each category is similar. In plain terms, some captions are warm, some are biting, and most sit somewhere in the middle, regardless of the occupational field being referenced.
        
         All these statistical terms simply confirm our previous observations from the histograms: while there are slight differences in sentiment across occupational categories, the overall sentiment distributions are relatively similar, with a slight positive tilt. This suggests that while occupations do influence the tone of humour to some extent, they do not strongly dictate whether captions are perceived as positive or negative. Furthermore, in captions, people tend to make approximately the same number of positive as negative jokes about occupations, as the median sentiment is 0.0 for all categories. This indicates a balanced approach to humour, where occupations are not consistently framed in a positive or negative light.
         """)

st.write("""
        To further the sentiment analysis, we can again conduct a series of statistical tests to compare the sentiment distributions across occupation categories. Pairwise Mann Whitney U tests reveal that most categories have significantly different sentiment distributions from each other, with a few exceptions. In fact, we find that the null hypothesis of equal distributions cannot be rejected for the following pairs: Arts and Entertainment vs Public Safety, Military and Security, then Business, Management and Finance vs Service Industry and Hospitality, and finally Healthcare and Medicine vs Law, Government and Politics. This suggests that for these pairs of categories, the sentiment distributions are similar enough that we cannot confidently say they differ significantly.
         
        To interpret these results, we can try and think of why certain occupation categories might have similar sentiment distributions. For example, both Arts and Entertainment and Public Safety, Military and Security might bring a mix of admiration and criticism, leading to a balanced sentiment distribution. Similarly, Business, Management and Finance and Service Industry and Hospitality might both be associated with customer service and workplace dynamics, resulting in comparable sentiment patterns. Finally, Healthcare and Medicine and Law, Government and Politics might both involve high-stakes decision-making and ethical considerations, leading to similar sentiment distributions. While these are some possible interpretation, they serve to influence the reader to think about the underlying reasons for the observed statistical similarities. 
         
         Once again, conducting a U-test is not enough to draw conclusions, we should also inspect Cliff's delta values to understand the effect sizes of these differences. We infact find that every pair of occupation categories has a small effect size (|d| < 0.147), indicating that while the sentiment distributions are statistically different, the practical significance of these differences is limited. This further shows the need to improve our methodology to capture more nuanced sentiment differences across occupational categories. Nevertheless, these results provide us with some insights into how sentiment varies across different professions in humour contexts.
         """)

st.write("""
        To summarise, our sentiment analysis of occupational categories in captions indicates that while there are slight variations in sentiment across different professions, the overall tone remains relatively balanced and neutral. This suggests that humour related to occupations does not consistently lean towards positivity or negativity, but rather reflects a diverse range of perspectives and attitudes towards different professions. Furthermore, the statistical tests reveal that while most occupational categories have significantly different sentiment distributions, the effect sizes of these differences are small, indicating limited practical significance.
         """)

st.divider()
st.subheader("What have we learned?")
st.write("""
        In this axis, we traced how occupations show up in New Yorker captions, from simple frequency to performance, themes, and tone. Common jobs such as "clown" and "president" appear often, but they do not consistently produce higher funniness scores. Instead, occupation based captions cluster around a low to mid range median, with occasional outliers, suggesting that job titles set the scene but rarely carry the joke on their own. Grouping occupations into broader categories reveals statistically detectable differences in funniness distributions, but the gaps are generally modest. This lead us to look at the themes that occur with different occupational categories. Topic modelling showed what sits around these occupations, from workplace culture to wider social roles, while sentiment remains mostly neutral with a slight positive tilt, which suggests a balanced approach to occupational humour. Overall, occupations provide a familiar backdrop for humour, but the real comedic value comes from how they are framed and the context in which they appear.
         
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
