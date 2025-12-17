# Humor as a Mirror: The New Yorker Captions as Reflections of Society, Politics, and Stereotypes 

## **Abstract**  
Humor is a universal yet complex form of expression. The more we think about it and the more complexes it becomes! An example of humor purposes could be in the way of dealing with more ‘serious’ matters [1] or easing social  tensions and establishing social bonds [2].

With this in mind, this project aim to investigate how jokes reflect societal traits and values. Our analysis will focus on three major themes: politics and gender. We will begin by examining what is generally perceived as “funny” and “unfunny,” and then explore how humor operates within each of these social domains. Finally, we will synthesize our findings to understand what humor reveals about the norms, power structures, and sensitivities of contemporary society.


## **Research Questions**  
The project is divided into **3 axes of research directions**:

### **Axis 1: What Is Considered Funny**  
- How do linguistic features (caption length, punctuation, lexical diversity, unexpected words, sentiment polarity) affect perceived funniness?
- What are the funniest themes?
- Which of the above attributes contribute most to making a caption funny?

### **Axis 2: Professions, Politics, and Power** 

- Which occupations appear most frequently, and how are they portrayed (ridiculed, admired)?” What stereotypes are recurrent (e.g., doctors are heroes, politicians are corrupt)?  
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

   The main purpose of these datasets is to construct a comprehensive list of occupations. Other data in said datasets is not used.

2. **Dictionary of gendered words**:

This dictionary was constructed based on Danielle Sucher's "Jailbreak the Patriarchy" 
(https://github.com/DanielleSucher/Jailbreak-the-Patriarchy)

## **Methods**

### **Axis 1: What Is Considered Funny**  

This part aims to understand which characteristics of a caption explain its perceived funniness.

Data preparation : Each caption is associated with:
- Its funniness score (target variable).
- A set of linguistic and semantic features, including: Length, Punctuation, Lexical diversity, Sentiment polarity (computed using TextBlob), Semantic alignment with the image.

To address the first research questions, we will use correlation and non-parametric tests such as Spearman’s ρ, Kruskal–Wallis test and Mann–Whitney U to assess how each feature individually relates to funniness. To minimize confounding effects, we will construct a caption similarity metric (based on text embeddings or length-normalized vectors) and compare groups of captions with similar distributions of other attributes when testing each factor.

Finally, to capture multivariate and non-linear relationships, we will train a Random Forest model using all features simultaneously. The features of importance would then be deduce as the higher nodes in the decision trees correspond to features with stronger predictive power.

### **Axis 2: Professions, Politics, and Power** 

First, we build a **comprehensive list of occupations**. This is done by merging aforementioned datasets. 

**Analysis**
The **jobs in each caption must be extracted**, allowing us to:  
- Track the **count of occupations**.
- Analyse **where and when** they occur.
- Identify **co-occurring words** to label **recurrent stereotypes, ridicule, and mockery** of jobs.

Similar approach taken for the **political research**:
- Create a **list of political words**.
- Treat **ambiguous words** with care (e.g., *left* and *right*).
- Analyse the **funniness score** of the captions and evolution of volume.

**Visualisations:**  
- **Bar charts**: frequency of occupations/political topics.
- **Bar charts**: average funniness scores per category.
- **Heatmaps**: cross-tabulating professions and sentiments.

### **Axis 3: Gender Roles**

This section investigates how men and women are depicted in cartoons and captions, the language patterns associated with each gender, and how audience responses relate to these depictions.

**Data Preparation**
- Gender annotation: Identify men, women, or gender-neutral characters in cartoons and captions using a gendered dictionary.
- Feature extraction: Capture lexical features (word frequency, co-occurrences, role categories), sentiment (polarity, subjectivity), and audience metrics (votes, winning captions).

**Analysis**
- Language Patterns: Analyze word usage and co-occurrences, generate word clouds, and track changes over time.
- Audience Response: Compare sentiment and success of captions mentioning men vs women, and assess whether stereotypical portrayals are rewarded.

**Visualizations**
- Bar charts for gender frequencies and mentions.
- Word clouds and co-occurrence heatmaps.
- Temporal plots for shifts in depictions and language.


### Website **
URL : MISSING LINK 

### Members contribution**

 - General Statistical necessities: Cyrielle
 - Axis 1: Katia & Cyrielle
 - Axis 2: Andras
 - Axis 3: Amelie
 - Data preprocessing & website: Dominic
 - Datastory : All members wrote the part of the website that corresponds to their analysis. 


## **Sources**

[1] Powell, C. (1988). *A Phenomenological Analysis of Humour in Society.* In: Powell, C., Paton, G.E.C. (eds) **Humour in Society.** Palgrave Macmillan, London. [https://doi.org/10.1007/978-1-349-19193-2_5](https://doi.org/10.1007/978-1-349-19193-2_5)

[2] Palagi, E., Caruana, F., & de Waal, F. B. M. (2022). *The naturalistic approach to laughter in humans and other animals: Towards a unified theory.* Philosophical Transactions of the Royal Society B: Biological Sciences, 377(1863), 20210175. [https://doi.org/10.1098/rstb.2021.0175](https://doi.org/10.1098/rstb.2021.0175)


