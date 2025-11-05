# **Humor as a Mirror: Social Attitudes, Politics, and Biases in the The New Yorker Caption Contest**

## **Abstract**  
*A 150-word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?*

Humor is a universal yet complex form of expression. The more we think about it and the more complexes it becomes! An example of humor purposes could be in the way of dealing with more ‘serious’ matters [1] or easing social  tensions and establishing social bonds [2].

With this in mind, this project aim to investigate how jokes reflect societal traits and values. Our analysis will focus on three major themes: politics, gender, and taboos (or social biases). We will begin by examining what is generally perceived as “funny” and “unfunny,” and then explore how humor operates within each of these social domains. Finally, we will synthesize our findings to understand what humor reveals about the norms, power structures, and sensitivities of contemporary society.


## **Research Questions**  
The project is divided into **4 axes of research directions**:### **Axis 1: What Is Considered Funny** 

*FILL*

### **Axis 2: Professions, Politics, and Power** 

- “Which occupations appear most frequently, and how are they portrayed (ridiculed, admired)?” What stereotypes are recurrent (e.g., doctors are heroes, politicians are corrupt)?  
- Do captions reflect partisan leanings (Democrat vs. Republican) or mock political figures more broadly? Are the political jokes rated differently?

### **2. Axis: Humor in Time → Historical & Contextual Dimensions: *"When and why do jokes resonate?"*** 

*FILL*

### **Axis 3: Gender Roles**

*FILL*

## **Proposed Additional Datasets**  

1. **Five datasets are used to construct an exhaustive list of occupations**:  
   - [**O*NET**](https://www.onetonline.org/find/all)  
   - [**ESCO (ESCO dataset v1.2.0)**](https://esco.ec.europa.eu/en/use-esco/download)   
   - [**Kaggle Job Description Dataset**](https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset)  
   - [**US Labor Statistics (May 2024, all data)** ](https://www.bls.gov/oes/tables.htm)   
   - [**US Census Data (2018 Census Occupation Index)**](https://www.census.gov/topics/employment/industry-occupation/guidance/indexes.html)

   While these datasets contain their own methods of categorising jobs, the main concern for the project at this stage is **solely to construct a full list of occupations**, ranging from very specific titles to more general terms. In total, these datasets add up to **~33,000 distinct occupations**, once the data is cleaned and treated. The list could be further enriched by including **synonyms and colloquial terms** for each job.

*FILL*

## **Methods**

### **Axis 1: What Is Considered Funny**  

*FILL*

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

### **Axis 3: Gender Roles**

*FILL*

## **Proposed Timeline**
-12/11 : 
  - conduct analysis 
-19/11 : 
  - conduct analysis
	- present intermediate result to the group
- 26/11 : 
	- final result of each axis?
- 03/12 : 
	- start HTML writing and design the web page
	- discuss results that are the most important and should be uploaded on website 
- 10/12 : 
  - update all result on website

- 17/12 : HANDOUT P3 (schedule meeting tuesday before for last reading and modification and cheers with vin chaud)

### **Organization within the Team**  

**Main team meeting on Fridays 15pm-->**
 - General Statistical necessities: Cyrielle
 - Axis 1: Katia & Cyrielle
 - Axis 2: Andras
 - Axis 3: Amelie
 - Organisation of github & website: Dominic


### **Questions for TAs**  
- For axis 3, we are using the metadata of the images. The metadata is missing about half the data (compared to the captions data) so we will throw out missing data from this analysis. Is it scientifically okay that for axis 1 & 2 we use all the data, but for axis 3 we only use half the data? 
- [Question 2] 
*FILL*

## **Sources**

[1] Powell, C. (1988). *A Phenomenological Analysis of Humour in Society.* In: Powell, C., Paton, G.E.C. (eds) **Humour in Society.** Palgrave Macmillan, London. [https://doi.org/10.1007/978-1-349-19193-2_5](https://doi.org/10.1007/978-1-349-19193-2_5)

[2] Palagi, E., Caruana, F., & de Waal, F. B. M. (2022). *The naturalistic approach to laughter in humans and other animals: Towards a unified theory.* Philosophical Transactions of the Royal Society B: Biological Sciences, 377(1863), 20210175. [https://doi.org/10.1098/rstb.2021.0175](https://doi.org/10.1098/rstb.2021.0175)


