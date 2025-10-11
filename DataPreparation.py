#!/usr/bin/env python
# coding: utf-8

# In[43]:


def warning1(text):
    print("WARNING!!! ", text)


# # Initialisation –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# In[44]:


import pandas as pd
import numpy as np
import re

pathToData = "newyorker_caption_contest_virgin"


# Further we will use fillowing naming: 
# 
# - dataAx - for data from csv
# - dataCx - for data from contests
# 
# 
# - dataAx/dataCx means it's itteration in the cleaning process.
# - dataA0 - stands for the virgin data directly from the provided files. 
# - dataA/dataC with no x means the final, cleaned data ready to be exported from this file. 
# 

# For further improvement of the initial data please use the following format in case you modify the data in the cell: 
# 
# - n - last iteration of modifyed dataAx
# - m - m = n + 1
# 
# ```python
# 
# dataAm = dataAn.copy() #(1)
# 
# # The code that modifies dataAm
# 
# dataA = dataAm.copy() #(2)
# 
# # The code that prints out something
# ```
# 
# - (1) - So the data from previous cells rests intact. This way we are sure that for each execution of the improvement cell the variables take their "initial stae". No need to rerun the previous ones. 
# - (2) - So the file output final variable dataA or dataC is actualised. 

# # CSV –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# In[45]:


dataA_exceptions = [525, 540]
dataA_startID = 510
dataA_endID = 895

dataA0 = []
dataA = []

for i in range(dataA_startID, dataA_endID+1):
    if i in dataA_exceptions: continue
    dataA0.append(pd.read_csv(f"{pathToData}/data/{i}.csv"))


dataA1 = dataA0.copy()
dataA = dataA1.copy()

dataA1[1].head(5)


# ## Other

# ### Remove redundant columns (index and rank)

# We could import directly with rank index:
# ```python
# pd.read_csv(f"../newyorker_caption_contest_virgin/data/{i}.csv", index_col=['rank'])
# ```
# but since not all files have column rank it makes sense to import as it is and later remove the redundant column. 

# ```python
# data.reset_index(drop=True)
# ```
# **reset_index** 
# - reindex the rows by making a new index column
# - make the previous index column a normal one label column "index"
# 
# **drop=True** 
# - removes the previous index column. 
# 
# ```python
# data.set_index('rank')
# ```
# **set_index('rank')**
# - set the column 'rank' as index column
# - only of column rank realy exists
# 
# 
# 

# In[46]:


dataA2 = []

for i, data in enumerate(dataA1):

    if 'rank' in data.columns: 
        if (data.index == data['rank']).all(): 
            data = data.reset_index(drop=True)
            data = data.set_index('rank')
            dataA2.append(data)
        else: 
            print("WHF???")

    else:
        data = data.sort_values('mean', ascending=False)
        data = data.reset_index(drop=True)
        data.index.name = 'rank'
        dataA2.append(data)

# Test if no dataFrame was lost
#if (len(dataA2) == len(dataA1)): print("Success")

dataA = dataA2.copy()
dataA2[300]


# ### Consistency verification 

# Test if there are any NaN

# In[47]:


def dataA_verifcation(dataA):

    isAnyNull = False
    for data in dataA: 
        isAnyNull = data.isnull().values.any()

    if isAnyNull == True: warning1("There are still some Nulls")




# Since data not contain some values, we are searching the NaN and replacing. 
# 
# ```python
# data.isnull().values.any(): 
# ```
# - return true if there is any value that is null from data 
# 
# 
# ```python
# dataA3[i].fillna('CAPTION_NOT_FOUND', inplace = True):
# ```
# - For dataframe i fill ALL na values with 'text'

# In[48]:


dataA3 = dataA2.copy()

for i, data in enumerate(dataA2):
    if data.isnull().values.any(): 
        #print(data.isnull().values.any(), i)
        dataA3[i].fillna('CAPTION_NOT_FOUND', inplace = True)

# Verify if there are realy no more NaN

dataA = dataA3.copy()
dataA_verifcation(dataA3)


# # JSON ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# In[49]:


dataC_lastGoodID = 251

dataC0= pd.read_json(f'{pathToData}/contests.json') 

dataC1 = dataC0.copy()
dataC = dataC1.copy()

dataC1.head()


# In[50]:


dataC2 = dataC1.copy()

dataC2_metadata = pd.json_normalize(dataC1.metadata)
dataC2 = dataC1.drop(columns=['metadata'])
dataC2 = pd.concat([dataC2, dataC2_metadata], axis=1)

dataC = dataC2.copy()

print(dataC2.iloc[100])
print("–––––––––––––––––––––––––––––––––")
print(dataC2.iloc[300])


# ## Other

# ### Identifying problems

# 1. Verify is contests.json size match the quantity of .CSVs.
# 2.  Search for missing rows. By comparing the expected index (i + dataA_offset, ti get the starting contest_id value) and the actual index (row["contest_id"]) we can verify if any row is missing. We will deal with their filling a bit later. 
# 3. Verify if for each row contest_id, images and data have always the same number. 
# 4. Verify if the order of the datas are the same as indexes (ex: (id: 13) == (contest_id - dataA_offset))
# 
# Use ```python .str.extract()``` for whole columns, 
# 
# but use ```python re.search()``` for single cell (string) values.

# In[51]:


dataC3 = dataC2.copy()
dataC_missingRows = []

def dataC_verifcation(dataC, missingRows):
    dataC_lenght = dataC.shape[0]
    dataA_lenght = len(dataA0)
    if dataC_lenght != dataA_lenght: 
        print(f"WARNING: Different size: JSON ({dataC_lenght}) vs CSV ({dataA_lenght})")

    for i, row in dataC.iterrows():
        i += len(missingRows)
        if row['contest_id'] != i + dataA_startID:
            print("WARNING: Missing row at: ", i+dataA_startID)
            missingRows.append(i + dataA_startID)
            continue

        match_contest_id = row["contest_id"]
        match_image = int(re.search(r"\d+", row["image"]).group())
        match_data  = int(re.search(r"\d+", row["data"]).group())

        if (match_contest_id == match_data == match_image) == False: 
            print("WARNING: Unconsistent data at: ", i+dataA_startID)

        if row['contest_id'] - dataA_startID != i: 
            print("WARNING: ID do not math contest_id")

dataC = dataC3.copy()
dataC_verifcation(dataC3, dataC_missingRows)


# It is okay, since the 525.csv and 540.csv are also missing. 

# ### Remove redundant columns 

# Since we know the starting id dataA_startID, we can substract dataA_startID from all rows and get the "normalised" indexes. 
# Also dataA is already normalised exluding missing rows, so we have to normalise without missing rows to be consistent with .csv.
# From the previous tests (like id vs contest_id) we know that data is sorted by contest_id and hence by id itself.
# 
# 
# So here we remove contest_id columns contest_id, image and data.

# In[52]:


dataC4 = dataC3.copy()

dataC4 = dataC3.drop(columns=["contest_id", "image", "data"])


dataC = dataC4.copy()

dataC4.head(5)


# # Conclusion –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# So here you can test and see the final form of CSVs and JSONs:

# In[53]:


def print_initialData():

    print("Initial contest index: dataA_startID = ", dataA_startID)
    print("Last contest index: dataA_endID = ", dataA_endID)
    print("Last good value in dataC: dataC_lastGoodId = ", dataC_lastGoodID)

    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    print("dataA[0]––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    display(dataA[0])

    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    print("dataC–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    display(dataC)


    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    print("dataC.iloc[dataC_lastGoodId-1]––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    display(dataC.iloc[dataC_lastGoodID])



    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    print("dataC.iloc[dataC_lastGoodId]––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    display(dataC.iloc[dataC_lastGoodID+1])


# In[54]:


# ======================================================
# Export global variables 
# ======================================================

__all__ = [
    "dataA",
    "dataC",
    "dataA_startID",
    "dataA_endID",
    "dataC_lastGoodID",
    "print_initialData"
]

print("DataPreparation variables exported successfully.")

