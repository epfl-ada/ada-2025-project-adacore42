import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import re
from collections import Counter
from src.utils.general_utils import *

# ===============================
# 1. Plot Votes vs Mean score
# ===============================
def plot_votes_vs_score(dataA, cartoon_ids=(108, 150, 260, 370)):
    """Displays scatter plots of Votes vs Average Score for several cartoons."""
    plt.figure(figsize=(8, 6))
    for cartoon_id in cartoon_ids:
        df = dataA[cartoon_id]
        plt.scatter(df["votes"], df["mean"], alpha=0.4, s=8, label=f"Contest {cartoon_id}")
    


    plt.xlabel("Votes")
    plt.ylabel("Mean score")
    plt.title("Votes vs. Average Score for Several Cartoons")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()


# ====================================
# 2. HISTOGRAM + KS test : normal distribution ?
# ====================================
def plot_mean_histograms(dataA, cartoon_ids=(108, 150, 260, 370)):
    """
    Histograms of average scores for several cartoons
    Results of the normality test (KS)
    Comparative box plot + descriptive statistics
    """
    # histogram
    plt.figure(figsize=(8, 6))
    means_data = {}

    for cartoon_id in cartoon_ids:
        df = dataA[cartoon_id]
        means = df["mean"].dropna().values
        means_data[cartoon_id] = means

        plt.hist(means, bins=20, alpha=0.5, label=f"Cartoon {cartoon_id}")

        # KS test (normal distribution)
        ks_stat, p_value = stats.kstest(means, 'norm', args=(np.mean(means), np.std(means, ddof=1)))
        print(f"[Cartoon {cartoon_id}] KS-stat={ks_stat:.4f}, p-value={p_value:.6f}")

    plt.title("Distribution of average scores (per cartoon)")
    plt.xlabel("Mean score")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

    # Descriptive statistics
    stats_summary = []
    for cartoon_id, values in means_data.items():
        stats_summary.append({
            "Cartoon ID": cartoon_id,
            "N": len(values),
            "Mean": np.mean(values),
            "Median": np.median(values),
            "Std": np.std(values, ddof=1),
            "Q1": np.percentile(values, 25),
            "Q3": np.percentile(values, 75),
            "Min": np.min(values),
            "Max": np.max(values),
        })

    df_stats = pd.DataFrame(stats_summary)

    # Box plot
    plt.figure(figsize=(10, 6))
    plt.boxplot(means_data.values(), labels=[f"{cid}" for cid in means_data.keys()],
                patch_artist=True, medianprops=dict(color="black"))
    plt.title("Comparison of average score distributions")
    plt.xlabel("Cartoon ID")
    plt.ylabel("Mean score")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

    return df_stats

# ==========================================
# 3. Histrograms of 'funny' vote ratios
# ==========================================

def plot_funny_ratios(dataA, cartoon_ids=(108, 150, 260, 370)):
    """
    Display on a single figure (4 subplots side by side)
    the distribution of the ratios of 'funny', 'somewhat_funny' and 'not_funny' votes
    for several cartoons.
    """
    cols = ['not_funny', 'somewhat_funny', 'funny']
    n = len(cartoon_ids)
    
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 5), sharey=True)
    
    if n == 1:
        axes = [axes]
    
    for ax, cartoon_id in zip(axes, cartoon_ids):
        df = dataA[cartoon_id].copy()
        df[cols] = df[cols].div(df['votes'], axis=0)

        for col in cols:
            ax.hist(df[col], label=col, bins=100, alpha=0.6)
        
        ax.set_xlabel("Vote ratio")
        ax.set_title(f"Cartoon {cartoon_id}")
        ax.grid(True, linestyle='--', alpha=0.6)
        if ax == axes[0]:
            ax.set_ylabel("Number of captions")
    
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=3)
    
    fig.suptitle("Distribution of funniness votes (4 cartoons)", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()



# ======================================================
# Statistics on captions and votes
# ======================================================
def plot_captions_and_votes(df_meta, n=30, threshold_id=contest_index2absolute_index(530)):
    """
    Displays the distribution of the number of captions and votes for each cartoon (index as identifier),
    and marks the 30 best/worst cases.
    """
    ids = df_meta.index
    df_meta = df_meta.copy()
    df_meta['contest_id'] = ids

    # Sorting to find the extremes
    top_captions = df_meta.sort_values(by="num_captions", ascending=False).head(n)
    bot_captions = df_meta.sort_values(by="num_captions", ascending=True).head(n)
    top_votes = df_meta.sort_values(by="num_votes", ascending=False).head(n)
    bot_votes = df_meta.sort_values(by="num_votes", ascending=True).head(n)

    # Subplot: captions
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for cid in top_captions["contest_id"]:
        axes[0].axvline(x=cid, color='green', linestyle='-', alpha=0.3)
    for cid in bot_captions["contest_id"]:
        axes[0].axvline(x=cid, color='red', linestyle='-', alpha=0.3)


    axes[0].plot(df_meta["contest_id"], df_meta["num_captions"], color='tab:blue')
    axes[0].set_title("Distribution of the number of captions suggested per contest")
    axes[0].axvline(x=threshold_id, color='black', linestyle='--', alpha=1,
                    label='Start of the online crowdsourcing voting system')

    axes[0].set_xlabel("Contest ID")
    axes[0].set_ylabel("NUmber of submitted captions")
    axes[0].legend(loc="upper left")
    axes[0].grid(True, linestyle='--', alpha=0.5)
    

    # Subplot : votes
    for cid in top_votes["contest_id"]:
        axes[1].axvline(x=cid, color='green', linestyle='-', alpha=0.3)
    for cid in bot_votes["contest_id"]:
        axes[1].axvline(x=cid, color='red', linestyle='-', alpha=0.3)

    axes[1].plot(df_meta["contest_id"], df_meta["num_votes"], color='tab:purple')
    axes[1].set_title("Distribution of the number of votes per contest")
    axes[1].axvline(x=threshold_id, color='black', linestyle='--', alpha=1,
                    label='Start of the online crowdsourcing voting system')

    axes[1].set_xlabel("Cartoon ID")
    axes[1].set_ylabel("Nombre de votes")
    axes[1].legend(loc="upper left")
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Distribution of captions and votes by cartoon", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()



# ======================================================
#  Top locations in cartoons
# ======================================================
def plot_top_locations(df_meta, top_n=50):
    """
    Cleans and counts the locations present in the metadata,
    then displays the top-N most frequent locations.
    """
    def normalize_location(loc):
        loc = loc.lower().strip()
        loc = re.sub(r"^(the |a |an |in |at |on |inside |outside |into )", "", loc)
        loc = re.sub(r"[^\w\s]", "", loc)
        return loc

    # Standardization of places
    all_locations = [
        normalize_location(loc)
        for sublist in df_meta["image_locations"].dropna()
        for loc in sublist
    ]

    # Manual corrections
    manual_corrections = {
        "living roo": "living room",
        "heavan": "heaven",
        "front hard": "front yard",
        "ktichen": "kitchen",
    }
    normalized_locations = [manual_corrections.get(loc, loc) for loc in all_locations]

    # Counting
    loc_counts = Counter(normalized_locations)
    top_locations = loc_counts.most_common(top_n)
    df_top = pd.DataFrame(top_locations, columns=["Lieu", "Fréquence"])

    # Visualization
    plt.figure(figsize=(15, 4))
    plt.bar(*zip(*top_locations))
    plt.xticks(rotation=90)
    plt.title(f"Top {top_n} Top 10 locations represented among all contests")
    plt.grid(True, linestyle='--', alpha=0.6, axis="y")
    plt.show()

    return df_top


# ======================================================
#  Analysis of question types (W-words)
# ======================================================
def plot_question_types(all_questions, top_n=10):
    """
    Determines the question type (W-word) for each caption/question and displays the most frequent ones.
    """
    def get_question_type(question):
        question = question.lower().strip()
        match = re.match(r"(why|what|how|who|where|when|is|are|does|do|can|could|would|should)", question)
        return match.group(0) if match else "other"

    question_types = [get_question_type(q) for q in all_questions]
    type_counts = Counter(question_types)

    df_types = pd.DataFrame(type_counts.most_common(), columns=["Question type", "Frequency"])

    # Visualization
    plt.figure(figsize=(8, 4))
    plt.bar(*zip(*type_counts.most_common(top_n)))
    plt.title("Most aked question type among all contests")
    plt.xlabel("W-word")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle='--', alpha=0.6, axis="y")
    plt.show()

    return df_types
