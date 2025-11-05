import pandas as pd
import numpy as n
import pickle
import re
from pathlib import Path
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

"""
root = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
while root.parent != root:
    if ((root / ".git").exists() and 
        (root / "README.txt").exists() and 
        (root / "results.ipynb").exists()): break
    root = root.parent
if str(root) not in sys.path: sys.path.insert(0, str(root))

print("Root folder at: ", root)"""

# Detect root starting from this file or from notebook’s cwd
try:
    start_path = Path(__file__).resolve()
except NameError:
    start_path = Path.cwd()

root = start_path
while root != root.parent:
    # Check for any known project markers
    if any((root / marker).exists() for marker in [".git", "README.md", "results.ipynb", "README.txt"]):
        break
    root = root.parent

# Sanity check — fallback if nothing found
if not any((root / marker).exists() for marker in [".git", "README.md", "results.ipynb", "README.txt"]):
    print("⚠️ Project root not found — defaulting to current working directory")
    root = Path.cwd()

print(f"✅ Root folder detected at: {root}")

# Add project root to sys.path if not already
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from src.utils.paths import *
from src.utils.general_utils import *
from src.utils.function_axis_1 import compute_funny_ranking  


stored_dataprep_pkl_path = root / STORED_DATAPREP_PKL_PATH
with open(stored_dataprep_pkl_path, "rb") as f:
    data = pickle.load(f)

### Data import and merging ### 

dataA = data['dataA']

for i, df in enumerate(dataA):
    df['source_df'] = i  # i correspond à la position dans la liste dataA

#dataTEST_merged = pd.concat(dataA, ignore_index=True)
dataA_merged = pd.concat(dataA, ignore_index=True)


### Need of funny metric ###

vote_cols = ['not_funny', 'somewhat_funny', 'funny']

# Somme cumulée de toutes les captions
total_votes = dataA_merged[vote_cols].sum()

print("Total votes:", total_votes)

# Barplot global
plt.figure()
total_votes.plot(kind='bar', color=['red','orange','green'])
plt.ylabel("Total number of votes")
plt.xticks(rotation=0)
plt.title("Global distribution of votes across all captions")
plt.show()

