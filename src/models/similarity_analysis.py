import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import umap
from scipy.stats import spearmanr, pearsonr
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, SimilarityFunction
import plotly.express as px
from mpl_toolkits.mplot3d import Axes3D
from wordcloud import WordCloud



# ==================================================================================
# class SimilarityModel
# This class is used to evaluate the semantic and structural similarity
# between all pairs of captions for one contest
# ==================================================================================

class SimilarityModel:
    """
    Class to evaluate the semantic and structural similarity between all pairs of captions for one contest
    """

    def __init__(self, model_name='all-MiniLM-L6-v2', sample_size=None):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, similarity_fn_name=SimilarityFunction.COSINE)
        self.scaler = StandardScaler()
        self.sample_size = sample_size


    # Semantic similarity
    def compute_semantic_similarity(self, df, text_col='caption'):
        """
        Compute matrix of semantic similarity (cosinus) between all captions.
        """
        embeddings = self.model.encode(df[text_col].tolist(), convert_to_tensor=True)
        semantic_sim = self.model.similarity(embeddings, embeddings)
        return semantic_sim


    # Structure similarity
    #Note for myself : @staticmethod means that the function does not need a self argument.
    @staticmethod
    def extract_structure_features(text):
        """
        Structural features extraction from a text : number of chars, number of words, average word lenght, density of punctuation, ratio of upper case letters, ratio of digit.
        """
        text = str(text)
        words = re.findall(r"\b\w+\b", text)
        punct = re.findall(r"[^\w\s]", text)
        letters = re.findall(r"[A-Za-z]", text)
        digits = re.findall(r"\d", text)

        n_chars = len(text)
        n_words = len(words)
        avg_word_len = np.mean([len(w) for w in words]) if words else 0
        punct_density = len(punct) / n_chars if n_chars > 0 else 0
        upper_letters_ratio = sum(1 for c in text if c.isupper()) / len(letters) if letters else 0
        digit_ratio = len(digits) / n_chars if n_chars > 0 else 0

        return [n_chars, n_words, avg_word_len, punct_density, upper_letters_ratio, digit_ratio]


    def compute_structure_similarity(self, df, text_col='caption'):
        """
        Compute matrix of structural similarity (cosinus) between all captions.
        """
        features = np.array([self.extract_structure_features(t) for t in df[text_col]])
        features_scaled = self.scaler.fit_transform(features)
        structure_sim = cosine_similarity(features_scaled)
        return structure_sim



    # Combinaison of semantic and structural similarity
    @staticmethod
    def compute_combined_similarity(semantic_sim, structural_sim, semantic_weight=0.5, structural_weight=0.5):
        return semantic_weight * semantic_sim + structural_weight * structural_sim



    # Visualisation
    def plot_similarity_matrix(self, sim_matrix, caption_list):
        """
        Plot a heatmap of combined similarity matrix
        """
        df_sim = pd.DataFrame(sim_matrix, index=caption_list, columns=caption_list)

        plt.figure(figsize=(8, 6))
        if df_sim.shape[0] <= 10:
            sns.heatmap(df_sim, cmap="coolwarm", xticklabels=True, yticklabels=True, annot=True, fmt=".2f", linewidths=.5)
        elif 10 < df_sim.shape[0] <= 30:
            sns.heatmap(df_sim, cmap="coolwarm", xticklabels=True, yticklabels=True, annot=False, linewidths=.5)
        else:
            sns.heatmap(df_sim, cmap="coolwarm", xticklabels=False, yticklabels=False, annot=False, linewidths=.5)
        plt.title("Combined similarity matrix (Semantic + Structural)")
        plt.show()

        return None
    

    




# ======================================================
# class CaptionClustering
# Caption clustering by similarity metric, UMAP visualisation
# ======================================================

class CaptionClustering:
    """
    Perform KMeans clustering on SBERT embeddings, then visualize the clusters with UMAP.
    """

    def __init__(self, model_name='all-MiniLM-L6-v2', n_clusters=10, normalize=True):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.normalize = normalize
        self.scaler = StandardScaler()
        self.clustering_method = KMeans(n_clusters, random_state=42, n_init=10)
        self.n_clusters = n_clusters
        self.embeddings = None
        self.cluster_labels = None


    # Compute the clusterisation of the captions
    def cluster_captions(self, df, text_col='caption'):
        print(f"SBERT encoding with '{self.model_name}'")
        self.embeddings = self.model.encode(df[text_col].tolist(), convert_to_numpy=True, show_progress_bar=True)

        if self.normalize:
            self.embeddings = self.scaler.fit_transform(self.embeddings)

        print(f"KMeans clustering with {self.n_clusters} clusters")
        self.cluster_labels = self.clustering_method.fit_predict(self.embeddings)

        return self.cluster_labels, self.embeddings
    


    # Compute the centroid of a cluster
    def compute_centroid(self, cluster_id):
        idx = np.where(self.cluster_labels == cluster_id)[0]
        if len(idx) == 0:
            raise ValueError(f"No items found in cluster {cluster_id}.")
        centroid = self.embeddings[idx].mean(axis=0, keepdims=True)
        return centroid



    # Find the most representative caption of the cluster
    def find_representative_caption(self, df, cluster_id, text_col='caption'):
        idx = np.where(self.cluster_labels == cluster_id)[0]
        if len(idx) == 0:
            raise ValueError(f"No items found in cluster {cluster_id}.")

        centroid = self.compute_centroid(cluster_id)
        cluster_embeddings = self.embeddings[idx]
        sims = cosine_similarity(cluster_embeddings, centroid).flatten()
        best_idx = idx[np.argmax(sims)]  # global index in df

        return df.iloc[best_idx][text_col], float(np.max(sims))


    # Generate a WordCloud for a cluster
    def generate_wordcloud(self, df, cluster_id, text_col='caption', width=900, height=500):
        idx = np.where(self.cluster_labels == cluster_id)[0]
        if len(idx) == 0:
            raise ValueError(f"No items found in cluster {cluster_id}.")

        texts = df.iloc[idx][text_col].tolist()
        full_text = " ".join(texts)

        wc = WordCloud(width=width, height=height, background_color="white").generate(full_text)

        plt.figure(figsize=(12,6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"WordCloud – Cluster {cluster_id}")
        plt.show()

        return wc


    # Compute meaningful cluster stats
    def compute_cluster_stats(self, df, cluster_id, text_col='caption'):
        idx = np.where(self.cluster_labels == cluster_id)[0]
        if len(idx) == 0:
            raise ValueError(f"No items found in cluster {cluster_id}.")

        texts = df.iloc[idx][text_col].tolist()

        lengths = [len(t.split()) for t in texts]
        avg_len = float(np.mean(lengths))
        std_len = float(np.std(lengths))

        centroid = self.compute_centroid(cluster_id)
        sims = cosine_similarity(self.embeddings[idx], centroid).flatten()

        stats = {
            "cluster_id": cluster_id,
            "n_items": len(idx),
            "avg_caption_length": avg_len,
            "std_caption_length": std_len,
            "avg_similarity_to_centroid": float(np.mean(sims)),
            "min_similarity": float(np.min(sims)),
            "max_similarity": float(np.max(sims)),
        }

        return stats



    # Evaluate the intra cluster similarity with our class SimilarityModel
    def evaluate_intra_cluster_similarity(self, df, text_col='caption', semantic_weight=0.8, structural_weight=0.2, plot=True):
        """
        Evaluates intra-cluster similarity and displays heatmaps only for the requested clusters.

        If 'plot' is:
        - True : displays all clusters
        - False : displays no clusters
        - list : displays only the specified clusters (e.g., [0, 14, 40])
        """
        sim_model = SimilarityModel(self.model_name)
        df = df.copy()
        df['cluster'] = self.cluster_labels

        cluster_stats = []

        for c in sorted(df['cluster'].unique()):
            subset = df[df['cluster'] == c]
            if len(subset) < 3:
                continue  # avoids clusters that are too small

            semantic_sim_cluster = sim_model.compute_semantic_similarity(subset, text_col)
            structural_sim_cluster = sim_model.compute_structure_similarity(subset, text_col)
            combined_sim_cluster = sim_model.compute_combined_similarity(
                semantic_sim_cluster,
                structural_sim_cluster,
                semantic_weight=semantic_weight,
                structural_weight=structural_weight
            )

            # Intra-cluster mean (excluding diagonal)
            n = len(subset)
            mean_sim = (combined_sim_cluster.sum().sum() - n) / (n**2 - n)
            mean_sim = float(mean_sim)
            cluster_stats.append({'cluster': c, 'n': n, 'mean_comb_sim': mean_sim})

            should_plot = (
                (plot is True) or
                (isinstance(plot, (list, tuple)) and c in plot)
            )
            if should_plot:
                print(f"Cluster {c}: {n} captions — mean combined similarity = {mean_sim:.3f}")
                sim_model.plot_similarity_matrix(combined_sim_cluster, subset[text_col].tolist())


                # ADDED FOR MILESTONE 3
                centroid = self.compute_centroid(c)
                rpz_caption, sim2centroid = self.find_representative_caption(df, c, text_col='caption')
                wc = self.generate_wordcloud(df, c, text_col='caption', width=900, height=300)
                cluster_stats_from_centroid = self.compute_cluster_stats(df, c, text_col='caption')
                
                print(f"Representative caption: '{rpz_caption}',\n(cosinus only) similarity to centroid = {sim2centroid:.02f}")
                for key, value in cluster_stats_from_centroid.items():
                    if key in("cluster_id", "n_items"):
                        print(f"{key}: {value}")
                    else: print(f"{key}: {value:.02f}")
                #...



        # global stats
        cluster_df = pd.DataFrame(cluster_stats)
        sns.histplot(cluster_df['mean_comb_sim'], bins=20)
        plt.title("Distribution of intra-cluster similarities")
        plt.show()

        return cluster_df   
        



    # Perform a UMAP reduction for visualization
    def UMAP_reduction(self, df, umap_n_components=3, umap_n_neighbors=15, umap_min_dist=0.1, umap_metric='cosine'):
        reducer = umap.UMAP(
            n_components=umap_n_components,
            n_neighbors=umap_n_neighbors,
            min_dist=umap_min_dist,
            metric=umap_metric,
            random_state=42
        )

        umap_embeddings = reducer.fit_transform(self.embeddings)

        # Create a DataFrame of the clusters + UMAP coordinates
        df_clusters = df.copy()
        df_clusters['cluster'] = self.cluster_labels
        df_clusters['umap_x'] = umap_embeddings[:, 0]
        df_clusters['umap_y'] = umap_embeddings[:, 1]
        if umap_n_components == 3:
            df_clusters['umap_z'] = umap_embeddings[:, 2]
        

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(projection='3d')
        n_clusters = len(np.unique(self.cluster_labels))
        cmap = plt.cm.get_cmap('tab20', n_clusters)

        for i, cluster_id in enumerate(sorted(np.unique(self.cluster_labels))):
            subset = df_clusters[df_clusters['cluster'] == cluster_id]
            ax.scatter(
                subset['umap_x'], subset['umap_y'], subset['umap_z'],
                label=f'Cluster {cluster_id}',
                color=cmap(i),
                s=40, alpha=0.7
            )

        ax.set_title(f'UMAP projection of KMeans clusters (k={self.n_clusters})')
        ax.set_xlabel('UMAP-1')
        ax.set_ylabel('UMAP-2')
        ax.set_zlabel('UMAP-3')
        #ax.legend(title='Clusters', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.show()

        return df_clusters





# ==============================================================================================
# class HumorSimilarityAnalysis
# Analysis of the correlation between caption humour scores within a similarity cluster
# ==============================================================================================

class SimilarHumorAnalysis:
    """
    Class to analysis of the correlation between caption humour scores within a similarity cluster
    """

    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.sim_model = SimilarityModel(model_name)
        self.sims = []
        self.humor_diffs = []
        self.corr_spearman = 0.0
        self.corr_pearson = 0.0



    def scores_correlation(self, df, text_col='caption', humor_col='funny', semantic_weight=0.5, structural_weight=0.5, sample_size=None):
        self.sims, self.humor_diffs = [], []
        if sample_size and len(df) > sample_size:
            df = df.head(sample_size).reset_index(drop=True)

        semantic_sim = self.sim_model.compute_semantic_similarity(df, text_col)
        structural_sim = self.sim_model.compute_structure_similarity(df, text_col)
        sim_matrix = self.sim_model.compute_combined_similarity(semantic_sim, structural_sim, semantic_weight, structural_weight)

        scores = df[humor_col].to_numpy()
        n = len(scores)

        for i in range(n):
            for j in range(i + 1, n):
                self.sims.append(sim_matrix[i, j])
                self.humor_diffs.append(abs(scores[i] - scores[j]))

        self.sims, self.humor_diffs = np.array(self.sims), np.array(self.humor_diffs)
        self.corr_spearman, _ = spearmanr(self.sims, -self.humor_diffs)
        self.corr_pearson, _ = pearsonr(self.sims, -self.humor_diffs)

        return {"spearman": self.corr_spearman, "pearson": self.corr_pearson}
    

    def plot_scores_correlation(self):
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=self.sims, y=-self.humor_diffs, alpha=0.5)
        plt.xlabel("Combined similarities")
        plt.ylabel("Proximity of the humor score (inverse of the gap)")
        plt.title(f"Correlation between humor and similarity\nSpearman = {self.corr_spearman:.2f}, Pearson = {self.corr_pearson:.2f}")
        plt.show()

        return None


    def scores_correlation_by_cluster(self, df, cluster_col='cluster', text_col='caption', humor_col='funny',
                                  semantic_weight=0.7, structural_weight=0.3, min_size=3):
        """
        Calculates the humor/similarity correlation in each cluster separately (negative correlations = humor consistency).
        Returns a DataFrame with the correlations per cluster.
        """
        results = []
        for c in sorted(df[cluster_col].unique()):
            subset = df[df[cluster_col] == c]
            if len(subset) < min_size:
                continue

            corr = self.scores_correlation(
                subset,
                text_col=text_col,
                humor_col=humor_col,
                semantic_weight=semantic_weight,
                structural_weight=structural_weight
            )
            results.append({'cluster': c, 'n': len(subset), **corr})

        results_df = pd.DataFrame(results)
        sns.histplot(results_df['spearman'], bins=20)
        plt.title("Correlation humour scores/similarity (Spearman) by cluster")
        plt.show()
        return results_df