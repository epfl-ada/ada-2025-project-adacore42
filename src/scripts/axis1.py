### Imports ###

# working librairies
import os
import pickle

# classic librairies
import numpy as np
import pandas as pd

# plotting librairies
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Statistics librairies
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.stats import chi2_contingency, fisher_exact, ttest_ind, mannwhitneyu

# Embeddings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans


from scipy.stats import ttest_ind
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# ============================
#   1.1. What is funny ? 
# ============================
def plot_boxplot_interactive(df, columns_category, features, save_fig = False, title=None):
    feature_labels = {
        'polarity': 'Sentiment Polarity',
        'subjectivity': 'Subjectivity',
        'num_words': 'Words number',
        'num_punct': 'Punctuations number',
        'num_repeats': 'Repetition'
    }
    groups = df[columns_category].unique()
    base_colors = ['green', 'orange']

    colors = {
        grp: base_colors[i] if i < len(base_colors) else 'gray'
        for i, grp in enumerate(groups)
    }
    #colors = {'best':'green',  'worst':'orange'}

    # Calculer les p-values et les stocker dans un dictionnaire
    p_values = {}
    for f in features:
        g1 = df[df[columns_category]==groups[0]][f]
        g2 = df[df[columns_category]==groups[1]][f]
        t_stat, p_val = ttest_ind(g1, g2, equal_var=False)
        p_values[f] = p_val

    # Créer le plot
    fig = make_subplots(rows=1, cols=len(features),subplot_titles=[feature_labels[f] for f in features])#,horizontal_spacing=0.05 

    
    for i, f in enumerate(features):
        for grp in df[columns_category].unique():
            
            df_sub = df[df[columns_category] == grp]

            fig.add_trace(
                go.Box(
                    y=df_sub[f],
                    name=grp,
                    marker_color=colors.get(grp, 'black'),
                    
                    customdata=df_sub[['caption_id', 'funny_score_scaled','source_id']],
                    hovertemplate=
                        "<b>Value:</b> %{y:.2f}<br>" +
                        "<b>Funny score:</b> %{customdata[1]:.2f}<br>" +
                        "<b>Caption ID:</b> %{customdata[0]}<br>" +
                        "<b>Contest ID:</b> %{customdata[2]}<br>" +
                        "<extra></extra>"
                ),
                row=1, col=i+1
            )

        
        # Ajouter l'annotation p-value **une seule fois par feature**
        y_max = df[f].max()
        text_annot = f"p = {p_values[f]:.3e}" + ("**" if p_values[f] < 0.05 else "")

        fig.add_annotation(
            x=0.5, y=y_max*1.05,
            text=text_annot,
            showarrow=False,
            font=dict(size=14, color="black"),
            xref=f"x{i+1}",
            yref=f"y{i+1}"
        )
    # Change this for other purpose than axe 1 - part 1   
    if columns_category == "caption_type":
        title_cat = "Comparison of best and worst captions in each contest"
    else:
        title_cat = "Comparison of best and worst captions overall contests"


    fig.update_layout(height=600, width=200*len(features), showlegend=False,
                      title = title_cat)
    
    if save_fig:
        fig.write_html(f"plot{title}.html")
    fig.show()




# ===========================================================
#   1.3. Topic detection with TF-IDF (A REVOIIIIR !!!!!!)
# ===========================================================

# 1)
def split_top_caption_vs_rest(df, score_col, top_percent=0.1):
    """
    Split top 10% vs bottom 90% (default)
    """
    threshold = df[score_col].quantile(1-top_percent)
    df_top = df[df[score_col] >= threshold].reset_index(drop=True)
    df_bottom = df[df[score_col] < threshold].reset_index(drop=True)

    return df_top, df_bottom
    
    
# 2)
def calc_chi2_score(vocab, freq_top, freq_bottom, df_top, df_bottom):
    chi2_scores = []

    for i, word in enumerate(vocab):
        a = freq_top[i]      # top occurrences
        b = freq_bottom[i]   # bottom occurrences
        c = len(df_top) - a
        d = len(df_bottom) - b

        contingency = np.array([[a, b], [c, d]])
        # Test χ²
        chi2, pval_chi2, _, _ = chi2_contingency(contingency)
        chi2_scores.append((word, chi2, pval_chi2))

    chi2_df = pd.DataFrame(chi2_scores, columns=["word", "chi2", "p"])
    chi2_df = chi2_df.sort_values("chi2", ascending=False)
        
    return chi2_df

def calc_log_odds(vocab, freq_top, freq_bottom, alpha = 0.01):
    """
    Calculate the log_odds of ......... ???
    Monroe et al. (2019) method, mainly used in NLP
    alpha = 0.01 means Dirichlet prior
    """
    N_top = freq_top.sum()
    N_bottom = freq_bottom.sum()
    log_odds = (np.log((freq_top + alpha)/(N_top + alpha*len(vocab))) -
                np.log((freq_bottom + alpha)/(N_bottom + alpha*len(vocab))))
    
    return log_odds

def bag_of_word_log_odds(df, df_top, df_bottom, text_col="cleaned_caption",
                         ngram_range=(1,1)):
    """
    Bag-of-Words + chi2 + log-odds, compatible n-grams.
    """
    vectorizer = CountVectorizer(ngram_range=ngram_range)
    X = vectorizer.fit_transform(df[text_col])
    vocab = np.array(vectorizer.get_feature_names_out())

    freq_top = np.asarray(vectorizer.transform(df_top[text_col]).sum(axis=0)).flatten()
    freq_bottom = np.asarray(vectorizer.transform(df_bottom[text_col]).sum(axis=0)).flatten()

    chi2_df = calc_chi2_score(vocab, freq_top, freq_bottom, df_top, df_bottom)
    log_odds = calc_log_odds(vocab, freq_top, freq_bottom, alpha=0.01)

    return vocab, chi2_df, log_odds


def plot_wordcloud(words, values, title):
    wc = WordCloud(width=900, height=500, background_color="white").generate_from_frequencies(dict(zip(words, np.abs(values))))
    plt.figure(figsize=(12,6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16)
    plt.show()


# 3)
def plot_tfidf(tfidf_means, features, tfidf_idx, subset='top'):
    plt.figure(figsize=(12,5))
    sns.barplot(x=tfidf_means[tfidf_idx], y=features[tfidf_idx])
    plt.title(f"Top 20 TF-IDF words (from {subset} captions)")
    plt.show()

def calc_tf_idf(df, text_col, nb_words=30, ngram_range=(1,1)):
    """
    TF-IDF compatible with n-grams.
    """
    tfidf_vectorizer = TfidfVectorizer(ngram_range=ngram_range)
    tfidf = tfidf_vectorizer.fit_transform(df[text_col])

    features = np.array(tfidf_vectorizer.get_feature_names_out())
    tfidf_means = np.asarray(tfidf.mean(axis=0)).flatten()

    tfidf_idx = tfidf_means.argsort()[-nb_words:]
    return tfidf, features, tfidf_means, tfidf_idx


# 4)
def plot_embeddings(sim_top, sim_bottom):
    plt.figure(figsize=(10,5))
    sns.kdeplot(sim_top, label="Top 10%", fill=True)
    sns.kdeplot(sim_bottom, label="Bottom 90%", fill=True)
    plt.title("Embeddings similarity to Top 10% centroid")
    plt.xlabel("Cosine similarity")
    plt.legend()
    plt.show()

def calc_embeddings(df_top, df_bottom, text_col="cleaned_caption"):
    """
    Calculate embedding of the captions with a SBERT model
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")

    emb_top = model.encode(df_top[text_col], show_progress_bar=True)
    emb_bottom = model.encode(df_bottom[text_col], show_progress_bar=True)

    centroid_top = emb_top.mean(axis=0, keepdims=True)

    # Similarity of each caption with the centroid of funny
    sim_top = cosine_similarity(emb_top, centroid_top).flatten()
    sim_bottom = cosine_similarity(emb_bottom, centroid_top).flatten()

    return sim_top, sim_bottom




def visualize_caption_analysis(df, score_col="mean", text_col="cleaned_caption", top_percent=0.1, ngram_range=(1,1)):
    """
    Analyse complète (Bag-of-Words, log-odds, TF-IDF, embeddings) avec n-grams.
    """

    # 1) Split
    df_top, df_bottom = split_top_caption_vs_rest(df, score_col, top_percent)
    print(f"Top {int(top_percent*100)}% captions: {len(df_top)}, Bottom: {len(df_bottom)}")

    # 2) Bag-of-Words + log-odds (ngram aware)
    vocab, chi2_df, log_odds = bag_of_word_log_odds(
        df, df_top, df_bottom, text_col=text_col, ngram_range=ngram_range
    )
    print(chi2_df)

    # Top / bottom words
    top_idx = np.argsort(log_odds)[-30:]
    bottom_idx = np.argsort(log_odds)[:30]

    plot_wordcloud(vocab[top_idx], log_odds[top_idx], f"Top words (log-odds) ngram={ngram_range}")
    plot_wordcloud(vocab[bottom_idx], log_odds[bottom_idx], f"Bottom words (log-odds) ngram={ngram_range}")

    # 3) TF-IDF n-grams
    tfidf_top, features, tfidf_means, tfidf_idx = calc_tf_idf(
        df_top, text_col=text_col, nb_words=30, ngram_range=ngram_range
    )
    plot_tfidf(tfidf_means, features, tfidf_idx, subset="top")

    # 4) Embeddings similarity
    sim_top, sim_bottom = calc_embeddings(df_top, df_bottom, text_col=text_col)
    print("Mean sim (top):", np.mean(sim_top))
    print("Mean sim (bottom):", np.mean(sim_bottom))

    ttest_sim, pval_sim = ttest_ind(sim_top, sim_bottom)
    print(f"T-test similarity: {ttest_sim}, p={pval_sim}")

    df_top["length"] = df_top[text_col].str.split().apply(len)
    df_bottom["length"] = df_bottom[text_col].str.split().apply(len)

    plot_embeddings(sim_top, sim_bottom)

    # 5) Statistical tests
    t_len, p_len = ttest_ind(df_top["length"], df_bottom["length"])
    mw_len, p_mw = mannwhitneyu(df_top["length"], df_bottom["length"])
    print(f"T-test length: {t_len}, p={p_len}")
    print(f"Mann-Whitney length: {mw_len}, p={p_mw}")

    return {
        "df_top": df_top,
        "df_bottom": df_bottom,
        "vocab": vocab,
        "log_odds": log_odds,
        "sim_top": sim_top,
        "sim_bottom": sim_bottom
    }



def cluster_funny_captions(df, text_col="cleaned_caption", score_col="mean", top_percent=0.1, n_clusters=5):
    """
    Cluster top funny captions and visualize representative examples.
    
    Parameters:
    - df : DataFrame with captions and scores
    - text_col : column with cleaned captions
    - score_col : funniness score
    - top_percent : top fraction to consider as funny
    - n_clusters : number of clusters
    """
    
    # Select top captions
    df_top, _ = split_top_caption_vs_rest(df, score_col, top_percent)
    print(f"Selected {len(df_top)} top captions for clustering.")
    
    # Encode captions
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(df_top[text_col], show_progress_bar=True)
    
    # Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    df_top['cluster'] = labels
    
    # Analyze each cluster
    cluster_summary = {}
    
    for c in range(n_clusters):
        cluster_idxs = np.where(labels == c)[0]
        cluster_emb = embeddings[cluster_idxs]
        cluster_texts = df_top.loc[cluster_idxs, text_col].tolist()
        
        # Centroid
        centroid = cluster_emb.mean(axis=0, keepdims=True)
        # Similarity to centroid
        sims = cosine_similarity(cluster_emb, centroid).flatten()
        top_idx = sims.argsort()[-5:][::-1]  # top 5 captions closest to centroid
        
        representative_texts = [cluster_texts[i] for i in top_idx]
        
        # WordCloud for cluster
        all_text = " ".join(cluster_texts)
        wc = WordCloud(width=800, height=400, background_color="white").generate(all_text)

        """# === 🔽 AJOUT POUR INTEGRATION GUI 🔽 ===
        plot = pg.WordCloudPlotGUI(
            cluster_id=c,
            wordcloud=wc,
            representative_texts=representative_texts
        )
        pg.PlotGUI.add_plots([plot])
        # === 🔼 AJOUT POUR INTEGRATION GUI 🔼 ==="""

        # Display (optional for debugging)
        plt.figure(figsize=(10,5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Cluster {c} (n={len(cluster_texts)}, cluster mean score={df_top.loc[cluster_idxs, score_col].mean():.2f})")
        plt.show()

     
        print(f"Cluster {c} top representative captions:")
        for t in representative_texts:
            print(" -", t)
        print("\n" + "="*50 + "\n")
        
        cluster_summary[c] = {
            "n_captions": len(cluster_texts),
            "representative": representative_texts
        }
    
    return df_top, cluster_summary



# Are the top really different from the mass ?
# est ce que on voit des métiers apparaitre ? bam transition vers la partie 2