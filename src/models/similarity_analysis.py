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



    def cluster_captions(self, df, text_col='caption'):
        print(f"SBERT encoding with '{self.model_name}'")
        self.embeddings = self.model.encode(df[text_col].tolist(), convert_to_numpy=True, show_progress_bar=True)

        if self.normalize:
            self.embeddings = self.scaler.fit_transform(self.embeddings)

        print(f"KMeans clustering with {self.n_clusters} clusters")
        self.cluster_labels = self.clustering_method.fit_predict(self.embeddings)

        return self.cluster_labels, self.embeddings
    



    def evaluate_intra_cluster_similarity(self, df, text_col='caption', semantic_weight=0.8, structural_weight=0.2, plot=True):
        """
        Évalue la similarité moyenne (intra-cluster) et affiche une heatmap pour inspection.
        Retourne un DataFrame récapitulatif.
        Une distribution des similarités moyennes intra-cluster
        
        Corrélation négative ⇒ plus deux captions sont similaires, plus leur score d’humour est proche → cohérence humoristique.
        Corrélation proche de 0 ⇒ pas de lien entre similarité textuelle et perception humoristique.
        Corrélation positive (rare) ⇒ clusters mal formés ou humour hétérogène malgré similarité sémantique.
        """
        sim_model = SimilarityModel(self.model_name)
        df = df.copy()
        df['cluster'] = self.cluster_labels

        cluster_stats = []
        for c in sorted(df['cluster'].unique()):
            subset = df[df['cluster'] == c]
            if len(subset) < 3:
                continue  # éviter les clusters trop petits

            semantic_sim_cluster = sim_model.compute_semantic_similarity(subset, text_col)
            structural_sim_cluster = sim_model.compute_structure_similarity(subset, text_col)
            combined_sim_cluster = sim_model.compute_combined_similarity(semantic_sim_cluster, structural_sim_cluster, semantic_weight=semantic_weight, structural_weight=structural_weight)
            
            # Moyenne intra-cluster (hors diagonale)
            n = len(subset)
            mean_sim = (combined_sim_cluster.sum().sum() - n) / (n**2 - n)
            mean_sim = float(mean_sim)
            cluster_stats.append({'cluster': c, 'n': n, 'mean_comb_sim': mean_sim})

            if plot:
                print(f"Cluster {c}: {n} captions — mean combined similarity = {mean_sim:.3f}")
                sim_model.plot_similarity_matrix(combined_sim_cluster, subset[text_col].tolist())

        cluster_df = pd.DataFrame(cluster_stats)
        sns.histplot(cluster_df['mean_comb_sim'], bins=20)
        plt.title("Distribution of intra-cluster similarities")
        plt.show()
        return cluster_df



    # ajouter couleur par score d’humour ?
    def UMAP_reduction(self, df, umap_n_components=3, umap_n_neighbors=15, umap_min_dist=0.1, umap_metric='cosine'):
        print("UMAP dimensional reduction")
        reducer = umap.UMAP(n_components=umap_n_components, n_neighbors=umap_n_neighbors, min_dist=umap_min_dist, metric=umap_metric, random_state=42)
        
        umap_embeddings = reducer.fit_transform(self.embeddings)

        df_clusters = df.copy()
        df_clusters['cluster'] = self.cluster_labels
        df_clusters['umap_x'] = umap_embeddings[:, 0]
        df_clusters['umap_y'] = umap_embeddings[:, 1]
        df_clusters['umap_z'] = umap_embeddings[:, 2]

        fig = px.scatter_3d(df_clusters, x='umap_x', y='umap_y', z='umap_z', color='cluster', color_discrete_sequence=px.colors.qualitative.Set1, title=f"Clusters SBERT (KMeans, k={self.n_clusters})", width=800, height=600)
        fig.show()

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
        plt.xlabel("Similarité combinée")
        plt.ylabel("Proximité du score d’humour (inverse de l’écart)")
        plt.title(f"Corrélation humour/similarité\nSpearman = {self.corr_spearman:.2f}, Pearson = {self.corr_pearson:.2f}")
        plt.show()

        return None


    def scores_correlation_by_cluster(self, df, cluster_col='cluster', text_col='caption', humor_col='funny',
                                  semantic_weight=0.7, structural_weight=0.3, min_size=3):
        """
        Calcule la corrélation humour/similarité dans chaque cluster séparément (corrélations négatives = cohérence humoristique).
        Retourne un DataFrame avec les corrélations par cluster.
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
        plt.title("Distribution des corrélations humour/similarité (Spearman) par cluster")
        plt.show()
        return results_df