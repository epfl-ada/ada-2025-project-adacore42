# ** Humor as a Mirror: The New Yorker Captions as Reflections of Society, Politics, and Stereotypes **

## **Abstract**  
Humor is a universal yet complex form of expression. The more we think about it and the more complexes it becomes! An example of humor purposes could be in the way of dealing with more ‘serious’ matters [1] or easing social  tensions and establishing social bonds [2].

With this in mind, this project aim to investigate how jokes reflect societal traits and values. Our analysis will focus on three major themes: politics, gender, and taboos (or social biases). We will begin by examining what is generally perceived as “funny” and “unfunny,” and then explore how humor operates within each of these social domains. Finally, we will synthesize our findings to understand what humor reveals about the norms, power structures, and sensitivities of contemporary society.


## **Research Questions**  
The project is divided into **3 axes of research directions**:

### **Axis 1: What Is Considered Funny**  
- Are shorter captions rated as funnier?
- Does the use of punctuation (e.g., ?, !, …) increase perceived humor?
- Does lexical diversity or the presence of unexpected words correlate with funniness?
- Do sentiment polarity and emotional tone (positive vs. negative) influence humor ratings?
- Are captions that are semantically less aligned with their paired image (i.e., more surprising) perceived as funnier?
- what are the funniest themes? 
- Which of the above attiributes contribute most to makes a caption funny?

### **Axis 2: Professions, Politics, and Power** 

- “Which occupations appear most frequently, and how are they portrayed (ridiculed, admired)?” What stereotypes are recurrent (e.g., doctors are heroes, politicians are corrupt)?  
- Do captions reflect partisan leanings (Democrat vs. Republican) or mock political figures more broadly? Are the political jokes rated differently?


### **Axis 3: Gender Roles**  

- How are men and women depicted in New Yorker cartoons and captions, and do these depictions reflect traditional gender roles or stereotypes?

- How does audience response (e.g., votes or winning captions) relate to gendered content—do captions about one gender receive more positive attention, and does this reinforce or challenge stereotypes?

## **Proposed Additional Datasets**  

1. **Five datasets are used to construct an exhaustive list of occupations**:  
   - [**O*NET**](https://www.onetonline.org/find/all)  
   - [**ESCO (ESCO dataset v1.2.0)**](https://esco.ec.europa.eu/en/use-esco/download)   
   - [**Kaggle Job Description Dataset**](https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset)  
   - [**US Labor Statistics (May 2024, all data)** ](https://www.bls.gov/oes/tables.htm)   
   - [**US Census Data (2018 Census Occupation Index)**](https://www.census.gov/topics/employment/industry-occupation/guidance/indexes.html)

   While these datasets contain their own methods of categorising jobs, the main concern for the project at this stage is **solely to construct a full list of occupations**, ranging from very specific titles to more general terms. In total, these datasets add up to **~33,000 distinct occupations**, once the data is cleaned and treated. The list could be further enriched by including **synonyms and colloquial terms** for each job.

2. **Dictionary of gendered words**:

This dictionary was constructed based on Danielle Sucher's "Jailbreak the Patriarchy" 
(https://github.com/DanielleSucher/Jailbreak-the-Patriarchy)

## **Methods**

### **Axis 1: What Is Considered Funny**  

This part aims to understand which characteristics of a caption explain its perceived funniness.

Data preparation : Each caption is associated with:
- Its funniness score (target variable).
- A set of linguistic and semantic features, including: Length, Punctuation, Lexical diversity, Sentiment polarity (computed using tools such as VADER or TextBlob), Semantic alignment with the image.

To address the first research questions, we will use correlation and non-parametric tests such as Spearman’s ρ, Kruskal–Wallis test and Mann–Whitney U to assess how each feature individually relates to funniness. To minimize confounding effects, we will construct a caption similarity metric (based on text embeddings or length-normalized vectors) and compare groups of captions with similar distributions of other attributes when testing each factor.

Finally, to capture multivariate and non-linear relationships, we will train a Random Forest model using all features simultaneously. The features of importance would then be deduce as the higher nodes in the decision trees correspond to features with stronger predictive power.

### **Axis 2: Professions, Politics, and Power** 

The first step is to construct a **comprehensive list of occupations**, which can be **specific** (e.g., *electromagnetic engineer*) or **general** (e.g., *physicist, nurse, doctor*). This was done by cleaning and merging the aforementioned occupation datasets.  

After this, the **jobs in each caption must be extracted and saved**, allowing us to:  
- Track the **count of occupations**  
- Analyze **where and when** they occur  
- Identify **co-occurring words** to label **recurrent stereotypes, ridicule, and mockery** of jobs  

A similar approach is taken for the **political research** of this axis:  
- Create a **list of political words**  
- Treat **ambiguous words** with care (e.g., *left* and *right* may or may not be political)  
- Once political words are located, analyse the **funniness score** of the caption  

**Visualisations produced by this axis include:**  
- **Bar charts** and **word clouds** for frequency of occupations/political topics  
- **Histograms** for frequency of professions/politics over time  
- **Bar charts** for average funniness scores per category  
- Possibly **heatmaps** cross-tabulating professions and sentiments  

For the website presentation, it could be interesting to include **annotated cartoons** to display jobs being ridiculed.

### **Axis 3: Gender Roles**

This section investigates how men and women are depicted in cartoons and captions, the language patterns associated with each gender, and how audience responses relate to these depictions.

**Data Preparation**
- Gender annotation: Identify men, women, or gender-neutral characters in cartoons and captions using a gendered dictionary.
- Feature extraction: Capture lexical features (word frequency, co-occurrences, role categories), sentiment (polarity, subjectivity), and audience metrics (votes, winning captions).

**Analysis**
- Language Patterns: Analyze word usage and co-occurrences, generate word clouds, and track changes over time.
- Audience Response: Compare sentiment and success of captions mentioning men vs women, and assess whether stereotypical portrayals are rewarded.

**Visualizations**
- Bar charts for gender frequencies and mentions
- Word clouds and co-occurrence heatmaps
- Temporal plots for shifts in depictions and language

## **Proposed Timeline**
-12/11 : 
  - conduct analysis :
    - axis 1 : get all attributes wanted + similarity metric
    - axis 2 : 
    - axis 3 : get a wider gender dictionnary + work on language patterns over time
-19/11 : 
  - conduct analysis : 
    - axis 1 : perform statistical test + start random forest
    - axis 2 : 
    - axis 3 : audience response
	- present intermediate result to the group
- 26/11 : 
	- conduct analysis : 
    - axis 1 : finish random forest
    - axis 2 : 
    - axis 3 : polish plots and structure of the analysis
- 03/12 : 
	- start HTML writing and design the web page
	- discuss results that are the most important and should be uploaded on website 
- 10/12 : 
  - update all result on website

- 17/12 : HANDOUT P3 (last reading and modification. Cheers with vin chaud :) )

### **Organization within the Team**  

**Main team meeting on Fridays 15pm-->**
 - General Statistical necessities: Cyrielle
 - Axis 1: Katia & Cyrielle
 - Axis 2: Andras
 - Axis 3: Amelie
 - Organisation of github & website: Dominic


### **Questions for TAs**  
- 1)  For axis 3, we are using the metadata of the images. The metadata is missing about half the data (compared to the captions data) so we will throw out missing data from this analysis. Is it scientifically okay that for axis 1 & 2 we use all the data, but for axis 3 we only use half the data? 
- 2) Concerning the part 'Building a similarity metric'. We have done : _[**1.** SBERT embeddings for the captions. **2.** K-Means clusters based on those embeddings - intended to group semantically similar captions. **3.** A custom similarity metric (e.g., cosine similarity on semantic and structural similarities) to quantify how close two captions are.]_ The idea behing those implementations was we suspected that unbalanced text content could bias your further comparisons (wherever it would be).
So we want to use this clustering to balance the dataset - e.g., by pairing or grouping captions that are “semantically equivalent” but differ in another variable (like treatment/control, date of publication, elements presents in the cartoon, etc.), so that comparisons (hypothesis tests) are meaningful. But the questions are : when this approach is appropriate (for which type of problems) and how to implement it in practice ? Secondly, this metric is not perfect (as explained in results.ipynb, because of noises in classification, and only focus on semantic similarity) could it create misleading “similar” pairs and affect our analysis ?

## **Sources**

[1] Powell, C. (1988). *A Phenomenological Analysis of Humour in Society.* In: Powell, C., Paton, G.E.C. (eds) **Humour in Society.** Palgrave Macmillan, London. [https://doi.org/10.1007/978-1-349-19193-2_5](https://doi.org/10.1007/978-1-349-19193-2_5)

[2] Palagi, E., Caruana, F., & de Waal, F. B. M. (2022). *The naturalistic approach to laughter in humans and other animals: Towards a unified theory.* Philosophical Transactions of the Royal Society B: Biological Sciences, 377(1863), 20210175. [https://doi.org/10.1098/rstb.2021.0175](https://doi.org/10.1098/rstb.2021.0175)


