#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
# # Data Preparation 

# %%
def warning1(text): print("WARNING!!! ", text)
ACTIVATE_PRINTS = False

# %% [markdown]
# # Initialisation 

# %%
import pandas as pd
import numpy as np
import pickle
import re
from pathlib import Path
import sys
import matplotlib.pyplot as plt
from scipy.stats import zscore

# %%
# Get correct root path
try:
    root = Path(__file__).resolve().parent
except NameError:
    root = Path.cwd()  # fallback for Jupyter notebooks

while root.parent != root:
    if all((root / marker).exists() for marker in [".git", "README.md", "results.ipynb"]):
        break
    root = root.parent

# Fallback in case nothing found
if not any((root / marker).exists() for marker in [".git", "README.md", "results.ipynb"]):
    print("Could not locate project root — defaulting to current working directory")
    root = Path.cwd()

if ACTIVATE_PRINTS: print(f"Root folder detected at: {root}")

# Ensure importability of the project
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

# %%
# Get the paths to data and files
from src.utils.paths import VNCC_DATA_DIR_PATH, VNCC_CONTESTS_JSON_PATH, STORED_DATAPREP_PKL_PATH

# %% [markdown]
# ### Further we will use fillowing naming: 
#
# - dataAx - for data from csv
# - dataCx - for data from contests
#
#
# - dataAx/dataCx means it's itteration in the cleaning process.
# - dataA0 - stands for the virgin data directly from the provided files. 
# - dataA/dataC with no x means the final, cleaned data ready to be exported from this file. 
#
#
# ### For further improvement of the initial data please use the following format in case you modify the data in the cell: 
#
# - n - last iteration of modifyed dataAx
# - m - m = n + 1
#
# ```python
# dataAm = dataAn.copy() #(1) 
# #The code that modifies dataAm
# dataA = dataAm.copy() #(2) 
# ```
#
# - (1) - So the data from previous cells rests intact. This way we are sure that for each execution of the improvement cell the variables take their "initial stae". No need to rerun the previous ones. 
# - (2) - So the file output final variable dataA or dataC is actualised. 

# %% [markdown]
# # CSV 

# %%
dataA_exceptions = [525, 540]
dataA_startID = 510
dataA_endID = 895

dataA0 = []
dataA = []

for i in range(dataA_startID, dataA_endID+1):
    if i in dataA_exceptions: continue
    dataA0.append(pd.read_csv(root / VNCC_DATA_DIR_PATH / f"{i}.csv"))


dataA1 = dataA0.copy()
dataA = dataA1.copy()

if ACTIVATE_PRINTS: display(dataA[1].head(5))

# %% [markdown]
# ## Remove redundant columns (index and rank)
#
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

# %%
dataA2 = []

for i, data in enumerate(dataA1):

    if 'rank' in data.columns: 
        if (data.index == data['rank']).all(): 
            data = data.reset_index(drop=True)
            data = data.set_index('rank')
            dataA2.append(data)
        else: 
            if ACTIVATE_PRINTS: print("WHF???")

    else:
        data = data.sort_values('mean', ascending=False)
        data = data.reset_index(drop=True)
        data.index.name = 'rank'
        dataA2.append(data)

# Test if no dataFrame was lost
if (len(dataA2) == len(dataA1)): 
    if ACTIVATE_PRINTS:  print("Success")

dataA = dataA2.copy()

if ACTIVATE_PRINTS: display(dataA[300])


# %% [markdown]
# ### Consistency verification 

# %%
# Test if there are any NaN
def dataA_verifcation(dataA):

    isAnyNull = False
    for data in dataA: 
        isAnyNull = data.isnull().values.any()

    if isAnyNull == True: 
        if ACTIVATE_PRINTS: warning1("There are still some Nulls")


# %% [markdown]
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

# %%
dataA3 = dataA2.copy()

for i, data in enumerate(dataA3):
    if data.isnull().values.any(): 
        #print(data.isnull().values.any(), i)
        dataA3[i].fillna('CAPTION_NOT_FOUND', inplace = True)

# Verify if there are realy no more NaN
dataA = dataA3.copy()
dataA_verifcation(dataA3)

# %% [markdown]
# # JSON 

# %%
dataC_lastGoodID = 251

dataC0= pd.read_json(root / VNCC_CONTESTS_JSON_PATH) 

dataC1 = dataC0.copy()
dataC = dataC1.copy()

if ACTIVATE_PRINTS: display(dataC1.head())


# %%
dataC2 = dataC1.copy()

dataC2_metadata = pd.json_normalize(dataC1.metadata)
dataC2 = dataC1.drop(columns=['metadata'])
dataC2 = pd.concat([dataC2, dataC2_metadata], axis=1)

dataC = dataC2.copy()

if ACTIVATE_PRINTS: 
    print(dataC.iloc[100])
    print("–––––––––––––––––––––––––––––––––")
    print(dataC.iloc[300])

# %% [markdown]
#
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

# %%
dataC3 = dataC2.copy()
dataC_missingRows = []

def dataC_verifcation(dataC, missingRows):
    dataC_lenght = dataC.shape[0]
    dataA_lenght = len(dataA0)
    if dataC_lenght != dataA_lenght: 
        if ACTIVATE_PRINTS: print(f"WARNING: Different size: JSON ({dataC_lenght}) vs CSV ({dataA_lenght})")

    for i, row in dataC.iterrows():
        i += len(missingRows)
        if row['contest_id'] != i + dataA_startID:
            if ACTIVATE_PRINTS: print("WARNING: Missing row at: ", i+dataA_startID)
            missingRows.append(i + dataA_startID)
            continue

        match_contest_id = row["contest_id"]
        match_image = int(re.search(r"\d+", row["image"]).group())
        match_data  = int(re.search(r"\d+", row["data"]).group())

        if (match_contest_id == match_data == match_image) == False: 
            if ACTIVATE_PRINTS: print("WARNING: Unconsistent data at: ", i+dataA_startID)

        if row['contest_id'] - dataA_startID != i: 
            if ACTIVATE_PRINTS: print("WARNING: ID do not math contest_id")

dataC = dataC3.copy()
dataC_verifcation(dataC3, dataC_missingRows)

# %% [markdown]
# It is okay, since the 525.csv and 540.csv are also missing. 
# ### Remove redundant columns 
# Since we know the starting id dataA_startID, we can substract dataA_startID from all rows and get the "normalised" indexes. 
# Also dataA is already normalised exluding missing rows, so we have to normalise without missing rows to be consistent with .csv.
# From the previous tests (like id vs contest_id) we know that data is sorted by contest_id and hence by id itself.
#
#
# So here we remove contest_id columns contest_id, image and data.

# %%
dataC4 = dataC3.copy()

dataC4 = dataC3.drop(columns=["contest_id", "image", "data"])

dataC = dataC4.copy()

if ACTIVATE_PRINTS: display(dataC4.head(5))

# %% [markdown]
# # Improving datasets

# %% [markdown]
#
# ## Adding Temporal data (dataC) 
#
# The following webpage has dates of some of the contests. I will add it to the dataC table, as a new column:
# "https://nextml.github.io/caption-contest-data/"
#
# I fill follow the next steps, all in the same block of code so it can be re-run without issue. It looks a bit dense but it really doesn't do much.
# 1. I read the webpage, and get a "contest_id" for each image: Initially, the name of each contest is only given as "### Dashboard", and i remove the "Dashboard" from the name. To fit with the previous format of dataC, I reset the index. We need to watch out, 540 exists in the new table. I will need to remove it.
#
# 2. Additionally, the date here is the day the finalist was announced, not the date the cartoon came out... something to keep in mind.
#
# 3. I will clean the format of the dates. Sometimes there is an "estimated" keyword, sometimes there is two dates, and sometimes, the year is missing. When there are two dates, I only keep the last date. When a year is missing from a date, I look at the previous entry and take the year from there.
#
# 4. We can convert the 'date' column of the dates_table dataframe to a correct date format by using pd.to_datetime.
#
# 5. The dates are prepared now and can be merged with our dataset. 

# %%
url = "https://nextml.github.io/caption-contest-data/"
tables = pd.read_html(url)
dates_table = tables[0].copy()

# Get contest_id
dates_table['contest_id'] = dates_table['Contest Dashboard'].str.extract(r'(\d+)\s*Dashboard').astype(int)

# Keeping only relevant columns
dates_table = dates_table.rename(columns={"Finalists Announced (date of issue)": "date"})
dates_table = dates_table[['contest_id', 'date']]

#Removing row with contest_id 540
dates_table = dates_table[dates_table['contest_id'] != 540]
dates_table = dates_table.reset_index(drop=True)

# Remove "Estimated"
dates_table['date'] = dates_table['date'].str.replace(r'\s*\(estimated\)\s*$', '', regex=True, flags=re.IGNORECASE)

# Month-day & Month-day -> keep second "Month day[, Year]"
dates_table['date'] = dates_table['date'].str.replace(
    r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\s*&\s*'
    r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(,\s*\d{4})?$',
    r'\2 \3\4',
    regex=True,
    flags=re.IGNORECASE,
)

# Month-day & day[, Year]  -> keep "Month day2[, Year]"
dates_table['date'] = dates_table['date'].str.replace(
    r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\s*&\s*(\d{1,2})(,\s*\d{4})?$',
    r'\1 \2\3',
    regex=True,
    flags=re.IGNORECASE,
)

# day & day Month[, Year]  -> keep "Month day2[, Year]"
dates_table['date'] = dates_table['date'].str.replace(
    r'^(\d{1,2})\s*&\s*(\d{1,2})\s+'
    r'(January|February|March|April|May|June|July|August|September|October|November|December)(,\s*\d{4})?$',
    r'\3 \2\4',
    regex=True,
    flags=re.IGNORECASE,
)

# Ensure sorted by contest_id
dates_table = dates_table.sort_values('contest_id').reset_index(drop=True)

# Detect whether a row already has a 4-digit year
has_year = dates_table['date'].str.contains(r'\b(?:19|20)\d{2}\b', na=False)

# The previous row's year (immediate previous entry only)
prev_year = dates_table['date'].str.extract(r'\b((?:19|20)\d{2})\b', expand=False).shift(1)

# Rows needing a year AND where the previous row had a year
mask = (~has_year) & prev_year.notna()

# Append ", YYYY" from the previous entry's year
dates_table.loc[mask, 'date'] = (
    dates_table.loc[mask, 'date']
      .str.replace(r',\s*$', '', regex=True)   # remove any trailing comma
      + ', ' + prev_year[mask]
)

# Converting to datetime
dt = pd.to_datetime(dates_table['date'].str.strip().str.replace(r'\s+', ' ', regex=True),
                    errors='coerce')

# In case some dates are still NaT (not a time), try the explicit 'Month D, YYYY' pattern
mask = dt.isna()
if mask.any():
    dt.loc[mask] = pd.to_datetime(dates_table.loc[mask, 'date'],
                                  format='%B %d, %Y', errors='coerce')

# Reset the date column to the parsed dates
dates_table['date'] = dt

# Drop the contest_id
dates_table = dates_table.drop(columns=['contest_id'])



dataC5 = dataC4.copy()
dataC5 = pd.merge(dataC5, dates_table, left_index=True, right_index=True)

dataC = dataC5.copy()

if ACTIVATE_PRINTS: display(dataC.head())



# %% [markdown]
# ## Adding funnyness Score (dataA)

# %%
dataA4 = [data.copy() for data in dataA3]

for data in dataA4:

    dataFunny = pd.DataFrame()

    # funny = +2 / somewhat_funny = +1 / not_funny = -1

    dataFunny['weighted_funny_raw'] = ( 
        1 * data['funny'] 
        + 0.5 * data['somewhat_funny'] 
        - 1 * data['not_funny']
        )

    dataFunny['weighted_funny_percent'] = dataFunny['weighted_funny_raw'] / data['votes']

    dataFunny['weighted_funny_z'] = zscore( 
        dataFunny['weighted_funny_percent'] * np.log1p(data['votes'])
    )

    data['funny_score'] = np.round(dataFunny['weighted_funny_z'], 2)


    # data.sort_values(by='funny_score', ascending=False, inplace=True)
    # data.reset_index(drop=False, inplace=True)
    

dataA = dataA4.copy()

if ACTIVATE_PRINTS: display(dataA4[0].head(30))



# %% [markdown]
# # Conclusion 
#
# So here you can test and see the final form of CSVs and JSONs:

# %%
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

# print_initialData()


# %% [markdown]
# ### Convert this .ipynb to .py
# To simplify the execution of this file well convert it in a .py format

# %%
# !jupytext --to py DataPreparation.ipynb

# %% [markdown]
# ## Store data

# %%
with open(root / STORED_DATAPREP_PKL_PATH, "wb") as f:
    pickle.dump({"dataA_startID": dataA_startID, "dataA_endID": dataA_endID, "dataC_lastGoodID": dataC_lastGoodID, "dataA": dataA, "dataC": dataC}, f)

