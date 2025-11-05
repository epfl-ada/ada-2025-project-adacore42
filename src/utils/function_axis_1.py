# --- Imports ---
from scipy.stats import zscore
import numpy as n
import matplotlib.pyplot as plt

# --- Fonctions ---

def compute_funny_ranking(data, by_image=False):
    """
    Compute humor ranking metrics for caption data.
    
    Parameters
    ----------
    data : pd.DataFrame or list[pd.DataFrame]
        Either a single merged dataframe or a list of dataframes per image.
    by_image : bool, optional (default=False)
        If True, compute rankings within each image dataframe in the list.
        If False, compute one global ranking on the merged dataframe.
        
    Returns
    -------
    pd.DataFrame or list[pd.DataFrame]
        DataFrame(s) with additional columns:
        ['funny_score', 'rank_funny']
    """
 
    def _compute(df):
        df = df.copy()

        # Proportions
        df['funny_over_total'] = df['funny'] / df['votes']
        df['unfunny_over_total'] = df['not_funny'] / df['votes']

        # Weighted z-scores
        df['funny_z'] = zscore(df['funny_over_total'] * n.log1p(df['votes']))
        df['not_funny_z'] = zscore(df['unfunny_over_total'] * n.log1p(df['votes']))

        # Combined metric and rank
        df['funny_score'] = df['funny_z'] - df['not_funny_z']
        df[f'rank_funny_{level}'] = df['funny_score'].rank(ascending=False, method='max') #'method="max"' assigns tied scores the highest (max) rank among the ties,
                                                                                             # ensuring integer ranks (no fractional values).
        # Remove columns not longer usefull
        df = df.drop(columns=['funny_over_total', 'unfunny_over_total','funny_z','not_funny_z'])
        return df

    # If working with multiple images
    if by_image:
        level = 'image'
        return [_compute(df) for df in data]
    else:
        level = 'overall'
        return _compute(data)


def plot_global_vote_distribution(dataA_merged):
    """
    Plots the global distribution of votes across all captions.

    Parameters
    ----------
    dataA_merged : pd.DataFrame
        DataFrame containing columns 'not_funny', 'somewhat_funny', 'funny'.
    """
    vote_cols = ['not_funny', 'somewhat_funny', 'funny']

    # Sum all votes
    total_votes = dataA_merged[vote_cols].sum()
    print("Total votes:", total_votes)

    # Plot bar chart
    plt.figure(figsize=(6,4))
    total_votes.plot(kind='bar', color=['red','orange','green'])
    plt.ylabel("Total number of votes")
    plt.xticks(rotation=0)
    plt.title("Global distribution of votes across all captions")
    plt.show()