import streamlit as st
from _webappp.assets.app_content import PagesData
from src.utils.general_utils import plot_html
from _webappp.assets.app_design import *
from _webappp.assets.app_definitions import *

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
st.write( 
    """
    The captions listed above are some of the funniest captions submitted for the given cartoon in caption contest. The winner was the second caption, which makes a reference to managers and plays on the stereotype of managers and corporate culture. You might say, okay, this is just one cartoon, but occupational references are actually quite common in our everyday humour. If the reader is interested in exploring how occupational humour is present, performs, and is distributed across the New Yorker Caption Contest dataset, then we encourage them to read on!
    """
)

st.subheader("A few words about our methodology")
st.write(
    """
    Identifying occupation references in captions is no easy feat: people make all kinds of references, from direct mentions of job titles to more subtle allusions to work-related activities or stereotypes. At the same time, we have a huge dataset of captions to analyse, so manual annotation is out of the question. To tackle the challenge, we have limited the research to looking for direct mentions of job titles from a curated list of about 33,000 occupations. We then preprocessed the captions to standardise the text (lowercasing, removing punctuation, etc.) and used string matching to identify occurences of job titles in the captions (plural forms were also considered). This method provides a solid foundation for seeing how we directly make fun of occupations, wihtout the complexity of trying to devise a more sophisticated NLP model to capture indirect references. However, we acknowledge that this approach misses a large part of humour related to subtle or indirect references to occupations, which could be explored in future work.
"""
)
st.subheader("Where do occupations appear and how frequent are they?")

st.write("""
        When we split all the captions in the New York Caption Contest dataset into two groups, those that reference occupations and those that do not, we can see that only a small fraction of captions actually talk about occupations. Specifically, out of the total number of captions, only about 6.14% contain direct references to job titles from our curated list. While this seems like a small value, it must be kept in mind that we are looking at direct references only, so all occupational humour might go up to a much larger percentage.

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
plot_html("_webappp/assets/graphs/occupation_frequency_plot.html")
st.write("""
          Beyond simple frequency counts, we can check which occupations are actually the funniest, or the worst performers. This can be done by looking at the average or median funny scores, introduced in axis 1, of captions that reference each occupation above a certain threshold frequency to avoid noise. The results show us that it is indeed not the most frequent occupations that are present in the funniest captions: only "rabbi" made both cuts while the term "leader" were also among the worst performers. Notice however that the difference between the funniest and least funny occupations (in terms of both average and median funny score) is only around 5 points, which is not a very large margin considering the funny score scale from 0 to 100. This suggests that while some occupations might be slightly funnier than others on average, the overall difference in humour related to occupations is relatively small.
         """)
#insert bar charts with funniest and least funny occupations
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
        From the 3000 or so occupations that were found in the captions, we have created 14 categories to group them into, and discarded any occupations that did not fit into these categories, or were too hard to categorise correctly. We created the following categories:
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
          We believe these categories cover a large portion of the common occupations found in captions, and provide a good basis for following them for the rest of the analysis. So, how is funniness distributed across these categories? 
         """)
plot_html("_webappp/assets/graphs/occupation_category_boxplot.html")
st.write("""
        From the box plot above, we can see that ...
         """)

st.write("""
        Through a Whitney-Mann U test (see methodology) we can show that the jobs in the group ... perform funnier than all other groups, followed by ... and .... The least funny occupation according to their performance compared to the others is ... While this statistic proves our intuition and shows us that indeed people in our society tend to laugh about ... more than about ..., A Cliffs delta test actually shows that due to the limited size of ech of these datasets, we cannot deduce conclusively that a group is certainly bigger than the other. 
         
        """)
st.divider()

st.subheader("Themes Across Captions")
st.write("""
        A natural next step in the analysis of how occupations occur in captions concern what are the general topics that occur with each of the categories examined before. Are doctors seen as heroes who save our lives? What do we really associate with people in the legal ang fovernemnt field?
         
        BERTopic is an amazing tool for finding patterns and topcis within sentences. Therefore, by grouping together all captions that mention a given category, we can fin what are the topics that occur in these captions (after removing the occupation itself). This can help us visualise what comes with the occupations in the sentence, and whether there are any recurring terms. The interactiv figures shown below highlight the most pertinent groupings found within each occupational category? Are there Any surprises?
         """
        )
# interactive plot to change categorical grouping like Amelie did
st.write("""
        Let us highlight the most unexpected topics found for the groups. ...
         """)

st.write("""
        So what have we learnt so far? 
         """)

st.divider()

st.subheader("Do we appriciate the work of other people?")
st.write("""
        It is all fun and interesting to joke about occupations, we all do it, but do we paint certain occupations always negatively or positively? For example, doctors and nurses are heroes who help us when we get sick, but they are also somewhat related to death and so people might be afraid of them? or for example, a common stereotype linked to politicians is that they always lie... but is this reflected in the sentiment felt towards these jobs? Well let's find out. 
         """)

st.write("""
        Vader's Sentiment is the perfect tool to look at the sentiment related to our categories of jobs. It provides a positive, negative and compound measure of the sentiment. We evaluate the sentiment towards the 5 groups identified in the previous section, and continue evaluating the sentiment related to them. The plots clearly show that there is no difference in sentimental ditribution: most of the comments show a neutral related to each group....
         """)



