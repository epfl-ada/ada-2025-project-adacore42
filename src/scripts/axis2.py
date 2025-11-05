# =========================
# 2. Professions, Politics, and Power
# =========================

# -------------------------
# Context and Research Questions
# -------------------------
# Professions in Humor: Which jobs are depicted most often? Which are ridiculed vs. admired? 
# What stereotypes recur (e.g., lawyers as tricksters, doctors as saviors)?
# Politics in Humor: Do captions reflect partisan leanings (Democrat vs. Republican) 
# or mock political figures more broadly? Are political jokes rated differently?

# =========================
# Package Imports
# =========================

#Loading packages (install any missing ones first, fix any version issues)
import os

# Data manipulation
import pandas as pd
import pickle
import ast
import numpy as np


# Language processing
from collections import Counter

# Plotting
import seaborn as sns
import matplotlib.pyplot as plt


# =========================
# Data Loading Functions
# =========================

# Load caption contest data
def load_newyorker_data(filepath = '../../data/cleaned_data_nouns.pkl'):
    if os.path.exists(filepath) == False:
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "rb") as f:
        data = pickle.load(f)

    dataA1 = data["dataA_nouns"]
    dataC1 = data["dataC_nouns"]
    dataA_startID1 = data["dataA_startID"]
    dataA_endID1 = data["dataA_endID"]
    dataC_lastGoodID1 = data["dataC_lastGoodID"]
    print("Data loaded successfully.")
    return dataA1, dataC1, dataA_startID1, dataA_endID1, dataC_lastGoodID1

# Load occupations dataset
def load_occupations(filepath='../../data/final_combined_occupations.csv'):
    if os.path.exists(filepath) == False:
        raise FileNotFoundError(f"File not found: {filepath}")
    
    occupations_df = pd.read_csv(filepath)
    occupations_df['Synonyms'] = occupations_df['Synonyms'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    return occupations_df

# =========================
# Occupation Processing Functions
# =========================


# Count occurrences of occupations in text
def count_occupations(text, syn_to_occ):
    '''
    Count occurrences of occupations in the given text.
    sync_to_occ: dictionary mapping synonyms to occupation names
    '''
    if isinstance(text, str):
        tokens = text.split()
    else:
        tokens = text
    occ_list = [syn_to_occ.get(tok.lower()) for tok in tokens if tok.lower() in syn_to_occ]
    return Counter(occ_list)

# Extract occupations from captions
def extract_occupations_captions(dataA, syn_to_occ, colname='occupation_counts', col_origin='cleaned_caption'):
    '''
    dataA: list of dataframe objects containing captions or a single dataframe
    colname: name of the new column to store occupation counts
    col_origin: name of the column containing the captions
    Adds a new column to each dataframe with counts of occupations in the captions
    '''
    if isinstance(dataA, list): 
        for i, df in enumerate(dataA):
            df[colname] = df[col_origin].apply(lambda text: count_occupations(text, syn_to_occ))
            dataA[i] = df

    elif isinstance(dataA, pd.DataFrame):
        dataA[colname] = dataA[col_origin].apply(lambda text: count_occupations(text, syn_to_occ))

    else:
        raise TypeError("dataA must be a list of DataFrames or a single DataFrame")


# Count total occurrences of occupations across captions
def count_occupation_occurrences_captions(dataA, col='occupation_counts'):
    '''
    dataA: list of dataframe objects containing captions with occupation counts
    returns total counts of occupations across all captions
    '''
    occupation_totals = Counter()
    for i in range(len(dataA)):
        df = dataA[i]
        for counts in df[col]:
            occupation_totals.update(counts)

    return occupation_totals


# -------------------------
# Temporal Analysis of Occupation Mentions
# -------------------------

# Occupation counts per contest
def occupation_counts_per_contest(dataA, col='occupation_counts'):
    """
    dataA: list of DataFrame objects containing captions with occupation counts
    returns: list of total occupation counts per contest
    """
    occupation_counts_list = []

    for df in dataA:
        total_occupations = 0
        for counts in df[col]:
            if isinstance(counts, dict):
                total_occupations += sum(counts.values())
        occupation_counts_list.append(total_occupations)

    return occupation_counts_list


# Check if a dictionary contains occupation data
def has_occupation(d):
    '''
    Check if the dictionary contains occupation data
    '''
    return isinstance(d, dict) and len(d) > 0

# =========================
# Plotting Functions
# =========================

# Bar chart function
def barchart(x,y, xlabel, ylabel, title, color):
    plt.figure(figsize=(9,6))
    sns.barplot(x=x, y=y, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Scatterplot function
def scatterplot(x,y, xlabel, ylabel, title, color):
    plt.figure(figsize=(9,6))
    sns.scatterplot(x=x, y=y, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.show()


