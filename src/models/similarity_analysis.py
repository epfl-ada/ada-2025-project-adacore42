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



# ==================================================================================
# class SimilarityModel
# This class is used to evaluate the semantic and structural similarity
# between all pairs of captions for one contest
# ==================================================================================

class SimilarityModel:
    """
    Class to evaluate the semantic and structural similarity between all pairs of captions for one contest
    """

    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, similarity_fn_name=SimilarityFunction.COSINE)
        self.scaler = StandardScaler()


    # Semantic similarity
    def compute_semantic_similarity(self, df, text_col='caption'):
        """
        Compute matrix of semantic similarity (cosinus) between all captions.
        """
        embeddings = self.model.encode(df[text_col].tolist(), convert_to_tensor=True)
        semantic_sim = self.model.similarity(embeddings, embeddings)
        return semantic_sim


    # Structure similarity
    #@staticmethod means that the function does not need a self argument.
    @staticmethod
    def extract_structure_features(text):
        """
        Structural features extraction from a text.
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
    def plot_similarity_matrix(self, df, text_col='caption', semantic_weight=0.5, structural_weight=0.5, sample_size=None):
        """
        Plot a heatmap of combined similarity matrix
        """
        if sample_size and len(df) > sample_size:
            df = df.sample(sample_size, random_state=42).reset_index(drop=True)

        captions = df[text_col].tolist()

        semantic_sim = self.compute_semantic_similarity(df, text_col)
        structural_sim = self.compute_structure_similarity(df, text_col)
        sim_matrix = self.compute_combined_similarity(semantic_sim, structural_sim, semantic_weight, structural_weight)

        df_sim = pd.DataFrame(sim_matrix, index=captions, columns=captions)

        plt.figure(figsize=(10, 8))
        sns.heatmap(df_sim, cmap="coolwarm", xticklabels=True, yticklabels=True, annot=True, fmt=".2f", linewidths=.5)
        plt.title("Matrice de similarité combinée (Sémantique + Structurelle)")
        plt.show()

        return df_sim
    




# ======================================================
# class CaptionClustering
# Caption clustering by similarity metric, UMAP visualisation
# ======================================================

class CaptionClustering:
    """
    Perform KMeans clustering on SBERT embeddings, then visualize the clusters with UMAP.
    """

    def __init__(self, model_name='all-MiniLM-L6-v2', normalize=True):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.normalize = normalize
        self.scaler = StandardScaler()
        self.kmeans = None
        self.embeddings = None
        self.cluster_labels = None



    def cluster_captions(self, df, text_col='caption', n_clusters=5, random_state=42):
        print(f"SBERT encoding with '{self.model_name}'")
        self.embeddings = self.model.encode(df[text_col].tolist(), convert_to_numpy=True, show_progress_bar=True)

        if self.normalize:
            self.embeddings = self.scaler.fit_transform(self.embeddings)

        print(f"KMeans clustering with {n_clusters} clusters")
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self.cluster_labels = self.kmeans.fit_predict(self.embeddings)

        return self.cluster_labels, self.embeddings


    def UMAP_reduction(self, df, n_clusters=5, random_state=42, umap_n_neighbors=15, umap_min_dist=0.1, umap_metric='cosine'):
        print("UMAP dimensional reduction")
        reducer = umap.UMAP(n_neighbors=umap_n_neighbors, min_dist=umap_min_dist, metric=umap_metric, random_state=random_state)
        
        umap_embeddings = reducer.fit_transform(self.embeddings)

        df_clusters = df.copy()
        df_clusters['cluster'] = self.cluster_labels
        df_clusters['umap_x'] = umap_embeddings[:, 0]
        df_clusters['umap_y'] = umap_embeddings[:, 1]

        plt.figure(figsize=(10, 8))
        sns.scatterplot(data=df_clusters, x='umap_x', y='umap_y', hue='cluster', palette='tab10', s=70, alpha=0.8, edgecolor='white')
        plt.title(f"Clusters SBERT (KMeans, k={n_clusters})")
        plt.tight_layout()
        plt.show()

        return df_clusters, self.embeddings




# ==============================================================================================
# class HumorSimilarityAnalysis
# Analysis of the correlation between caption humour scores within a similarity cluster
# ==============================================================================================

class SimilarHumorAnalysis:
    """
    Classe pour analyser la corrélation entre similarité sémantique et score d’humour.
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