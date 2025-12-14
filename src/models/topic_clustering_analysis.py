import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
from scipy import stats
from itertools import combinations
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from sklearn.metrics import silhouette_score

from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots



class CaptionTopicClusterer:
    """
    Topic modeling sur des captions avec BERTopic,
    mapping vers des topics agrégés et analyse des scores.
    """

    def __init__(self, embedding_model_name="all-MiniLM-L6-v2", fun_metric="mean", contest_idx=[], min_topic_size=10, n_gram_range=(1, 2), verbose=True):
        
        self.embedding_model = SentenceTransformer(embedding_model_name)

        self.min_topic_size = min_topic_size
        
        self.topic_model = BERTopic(
            embedding_model=self.embedding_model,
            min_topic_size=min_topic_size,
            n_gram_range=n_gram_range,
            verbose=verbose)
        
        self.agg_topic_289 = {"checkmate_win_lose": [-1,0,1,5,7,10,11,16,18,19,20,24,32,37,41,45,49,53,60],
                              "chess_mechanics_pieces": [2,3,4,7,18,20,27,30,31,35,41,46,59,66,79],
                              "death_grim_reaper_afterlife": [10,11,14,19,24,31,36,39,40,47,51,57,63,69],
                              "time_endgame_clock": [8,14,17,20,60,64],
                              "pop_culture": [21,23,25,33,38,43,55,56,61,70,71,75,78,77],
                              "bureaucracy_taxes_insurance": [6,52,80],
                              "deals_bets_rematches": [15,22,48,50,62,74],
                              "body_parts": [12,42,72],
                              "emotional_reactions": [7,29,37,65,58],
                              "family_domestic": [68,9,34],
                              "color_choice_white_black": [28],
                              "misc": [26,54,73,76,77]}
        
        self.fun_metric = fun_metric

        self.contest_idx = contest_idx

    # ---------------------------------------------------------
    # Topic modeling
    # ---------------------------------------------------------

    def fit_transform(self, captions):
        """
        Entraîne BERTopic et retourne uniquement les résultats du clustering.
        """
        embeddings = self.embedding_model.encode(captions, show_progress_bar=True)

        topics, probs = self.topic_model.fit_transform(captions, embeddings)

        df_topic_info = self.topic_model.get_topic_info()

        return {
            "captions": captions,
            "embeddings": embeddings,
            "topics": topics,
            "probs": probs,
            "df_topic_info": df_topic_info
        }

    # ---------------------------------------------------------
    # EVALUATION (sans refit)
    # ---------------------------------------------------------
    def evaluate_fit_transform(self, fit_results):

        captions = fit_results["captions"]
        embeddings = fit_results["embeddings"]
        topics = fit_results["topics"]

        # --- texts compatibles bigrams ---
        texts = [
            c.lower().replace(" ", "_").split("_")
            for c in captions
        ]
        dictionary = Dictionary(texts)

        # --- topic words ---
        topics_dict = self.topic_model.get_topics()
        topic_words = []

        for t in topics_dict:
            if t == -1 or topics_dict[t] is None:
                continue

            words = [
                w for w, _ in topics_dict[t][:10]
                if w in dictionary.token2id
            ]

            if len(words) >= 2:
                topic_words.append(words)

        # --- Coherence ---
        coherence_model = CoherenceModel(
            topics=topic_words,
            texts=texts,
            dictionary=dictionary,
            coherence="c_v"
        )
        coherence = coherence_model.get_coherence()

        # --- Diversity ---
        all_words = [w for topic in topic_words for w in topic]
        diversity = len(set(all_words)) / len(all_words) if all_words else np.nan

        # --- Silhouette ---
        valid_idx = [i for i, t in enumerate(topics) if t != -1]
        if len(set(np.array(topics)[valid_idx])) > 1:
            silhouette = silhouette_score(
                embeddings[valid_idx],
                np.array(topics)[valid_idx]
            )
        else:
            silhouette = np.nan

        outlier_rate = np.mean(np.array(topics) == -1)

        return {
            "min_topic_size": self.min_topic_size,
            "coherence": coherence,
            "diversity": diversity,
            "silhouette": silhouette,
            "outlier_rate": outlier_rate,
            "n_topics": len(topic_words)
        }



    # ---------------------------------------------------------
    # Mapping topics toward topics agregatted
    # ---------------------------------------------------------

    @staticmethod
    def map_topic_to_aggregated(topic_id, agg_mapping):
        """Retourne le nom du topic agrégé auquel appartient topic_id."""
        for agg_name, topic_list in agg_mapping.items():
            if topic_id in topic_list:
                return agg_name
        return "unmapped"

    def compute_aggregated_topic_info(self, df_topic_info, agg_topic):
        """
        Ajoute les topics agrégés et calcule les stats (Count, Name, Representative_Docs).
        """
        df = df_topic_info.copy()

        df["aggregated_topic"] = df["Topic"].apply(lambda x: self.map_topic_to_aggregated(x, agg_topic))

        agg_topics = (df.groupby("aggregated_topic")
                        .agg({
                            "Count": "sum",
                            "Name": "first",
                            "Representative_Docs": lambda x: list(x.iloc[:3]),
                        })
                        .reset_index()
                        .sort_values("Count", ascending=False))
        
        return agg_topics

    # ---------------------------------------------------------
    # Scores par topic agrégé
    # ---------------------------------------------------------

    def compute_topic_scores(self, df_data, agg_topic):
        """
        Merge topics + scores puis calcule les moyennes par topic agrégé.
        """

        df_data["aggregated_topic"] = df_data["topic_nb"].apply(lambda x: self.map_topic_to_aggregated(x, agg_topic))

        df_scores = (df_data.groupby("aggregated_topic")
                   .agg({self.fun_metric: "mean", "caption": "count"})
                   .reset_index()
                   .rename(columns={"caption": "Count"})
                   .sort_values(self.fun_metric, ascending=False))

        return df_scores
    

    # -------------------------------
    # Variance and outlier analysis
    # -------------------------------
    def compute_variance_stats(self, df_data):
        """
        Compute variance, IQR, and number of extreme outliers per aggregated topic.
        """
        groups = df_data.groupby("aggregated_topic")
        rows = []
        for name, g in groups:
            vals = g[self.fun_metric].dropna().values
            if len(vals)==0:
                continue
            q1, q3 = np.percentile(vals, [25,75])
            iqr = q3 - q1
            lower = q1 - 1.5*iqr
            upper = q3 + 1.5*iqr
            n_outliers = ((vals < lower) | (vals > upper)).sum()
            rows.append({
                        "aggregated_topic": name,
                        "count": len(vals),
                        "mean": np.mean(vals),
                        "median": np.median(vals),
                        "std": np.std(vals, ddof=1),
                        "var": np.var(vals, ddof=1),
                        "iqr": iqr,
                        "n_outliers": int(n_outliers)})
        return pd.DataFrame(rows).sort_values("mean", ascending=False)


    # -------------------------------
    # Stratification by percentiles and enrichment
    # -------------------------------
    def stratify_percentiles_and_compare(self, df_data, top_pct=10, middle_pct=(40,60)):
        """
        Returns dataframes for top N% and middle percentile and computes
        counts per aggregated topic + simple enrichment ratios (top proportion / overall proportion).
        """
        df = df_data.copy()
        df = df.dropna(subset=[self.fun_metric])
        n = len(df)
        top_k = int(math.ceil(n * top_pct / 100.0))
        # get top by metric
        df_sorted = df.sort_values(self.fun_metric, ascending=False).reset_index(drop=True)
        df_top = df_sorted.iloc[:top_k]
        # middle pct
        lo = int(math.floor(n * (middle_pct[0]/100.0)))
        hi = int(math.ceil(n * (middle_pct[1]/100.0)))
        df_middle = df_sorted.iloc[lo:hi]
        # counts per topic
        top_counts = df_top["aggregated_topic"].value_counts().rename("top_count").reset_index().rename(columns={"index":"aggregated_topic"})
        mid_counts = df_middle["aggregated_topic"].value_counts().rename("mid_count").reset_index().rename(columns={"index":"aggregated_topic"})
        overall = df["aggregated_topic"].value_counts().rename("overall_count").reset_index().rename(columns={"index":"aggregated_topic"})
        merged = overall.merge(top_counts, on="aggregated_topic", how="left").merge(mid_counts, on="aggregated_topic", how="left").fillna(0)
        merged["top_prop"] = merged["top_count"]/merged["overall_count"]
        merged["mid_prop"] = merged["mid_count"]/merged["overall_count"]
        merged["enrichment_top_vs_overall"] = (merged["top_count"] / top_k) / (merged["overall_count"] / n)
        merged = merged.sort_values("enrichment_top_vs_overall", ascending=False)
        
        # df_top → les meilleures lignes (top X %)
        # df_middle → la tranche centrale
        # merged → tableau comparatif par topic avec enrichissement
        return df_top, df_middle, merged



    # -------------------------------
    # Statistical tests
    # -------------------------------
    def kruskal_test(self, df_data):
        """
        Kruskal-Wallis test across aggregated topics (non-parametric ANOVA).
        Returns H-stat and p-value and group medians.
        """
        groups = [g[self.fun_metric].dropna().values for n,g in df_data.groupby("aggregated_topic")]
        names = [n for n,_ in df_data.groupby("aggregated_topic")]
        # only keep groups with at least 5 values
        filtered = [(names[i], groups[i]) for i in range(len(groups)) if len(groups[i])>=5]
        if len(filtered) < 2:
            return None
        arrays = [arr for n,arr in filtered]
        H, p = stats.kruskal(*arrays)
        medians = {n: np.median(arr) for n,arr in filtered}
        return {"H": H, "p": p, "medians": medians}


    def pairwise_mannwhitney(self, df_data, alpha=0.05):
        """
        Pairwise Mann-Whitney U tests with Bonferroni correction.
        Returns a dataframe of pairs and adjusted p-values.
        """
        groups = {name: g[self.fun_metric].dropna().values for name,g in df_data.groupby("aggregated_topic") if len(g[self.fun_metric].dropna())>=5}
        pairs = []
        names = list(groups.keys())
        m = len(names)
        for i,j in combinations(range(m),2):
            a = groups[names[i]]
            b = groups[names[j]]
            stat, p = stats.mannwhitneyu(a,b, alternative='two-sided')
            pairs.append({"group1": names[i], "group2": names[j], "U": stat, "p_raw": p})
        # Bonferroni
        for row in pairs:
            row["p_adj_bonf"] = min(row["p_raw"] * len(pairs), 1.0)
        df_pairs = pd.DataFrame(pairs).sort_values("p_adj_bonf")
        return df_pairs



    # ---------------------------------------------------------
    # Visualisations
    # ---------------------------------------------------------

    def plot_topic_scores(self, df_data, df_scores):
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_data.sort_values(by=self.fun_metric, ascending=False), x="aggregated_topic", y=self.fun_metric)
        plt.title(f"Distribution {self.fun_metric} par topic agrégé")
        plt.xticks(rotation=90)
        plt.xlabel("Topic agrégé")
        plt.ylabel(self.fun_metric)
        plt.tight_layout()
        plt.show()
    

    def plot_topic_scores2(self, df_data, order_by="median"):
        """
        Boxplot interactif Plotly de la distribution du score par topic agrégé.

        Parameters
        ----------
        df_data : pd.DataFrame
            Doit contenir aggregated_topic et self.fun_metric
        order_by : str
            "median" ou "mean" pour trier les topics
        show : bool
            Affiche ou retourne la figure
        """

        df = df_data.dropna(subset=[self.fun_metric]).copy()

        # --- calcul stats pour l'ordre ---
        stats = (
            df.groupby("aggregated_topic")[self.fun_metric]
            .agg(["median", "mean", "count"])
            .reset_index()
        )

        if order_by not in {"median", "mean"}:
            raise ValueError("order_by must be 'median' or 'mean'")

        ordered_topics = (
            stats.sort_values(order_by, ascending=False)["aggregated_topic"]
            .tolist()
        )

        # --- boxplot ---
        fig = px.box(
            df,
            x="aggregated_topic",
            y=self.fun_metric,
            category_orders={"aggregated_topic": ordered_topics},
            points="outliers",   # montre les outliers
            hover_data=df.columns,
            title=f"Distribution de {self.fun_metric} par topic agrégé"
        )

        # --- annotations N ---
        annotations = []
        for _, row in stats.iterrows():
            annotations.append(
                dict(
                    x=row["aggregated_topic"],
                    y=df[self.fun_metric].max(),
                    text=f"n={row['count']}",
                    showarrow=False,
                    yshift=20,
                    font=dict(size=10)
                )
            )

        fig.update_layout(
            xaxis_title="Topic agrégé",
            yaxis_title=self.fun_metric,
            template="plotly_white",
            height=500,
            xaxis_tickangle=-45,
            annotations=annotations
        )
        fig.show()
        return fig



    def plot_proportion_above_threshold(self, df_data, threshold=1.5, figsize=(10, 5)):
        """
        Barplot interactif de la proportion de captions au-dessus d'un seuil par topic.
        Inclut un subplot avec les counts absolus.
        """
        df = df_data.copy()
        df["above"] = (df[self.fun_metric] >= threshold).astype(int)
        
        prop = df.groupby("aggregated_topic")["above"].agg(["mean", "sum", "count"]).reset_index()
        prop.columns = ["aggregated_topic", "prop_above", "n_above", "total"]
        prop = prop.sort_values("prop_above", ascending=False)
        
        # Créer des subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(
                f"Proportion >= {threshold}",
                f"Nombre absolu >= {threshold}"
            ),
            horizontal_spacing=0.12
        )
        
        # Couleurs dégradées basées sur la proportion
        colors = [f'rgba({int(220-p*150)}, {int(100+p*100)}, {int(150-p*50)}, 0.8)' 
                for p in prop["prop_above"]]
        
        # Subplot 1: Proportions
        fig.add_trace(
            go.Bar(
                x=prop["aggregated_topic"],
                y=prop["prop_above"],
                marker_color=colors,
                text=[f'{p:.1%}' for p in prop["prop_above"]],
                textposition='outside',
                hovertemplate=(
                    '<b>%{x}</b><br>' +
                    'Proportion: %{y:.2%}<br>' +
                    'Nombre: %{customdata[0]}<br>' +
                    'Total: %{customdata[1]}<br>' +
                    '<extra></extra>'
                ),
                customdata=prop[["n_above", "total"]].values,
                name="Proportion"
            ),
            row=1, col=1
        )
        
        # Subplot 2: Counts absolus
        fig.add_trace(
            go.Bar(
                x=prop["aggregated_topic"],
                y=prop["n_above"],
                marker_color=colors,
                text=prop["n_above"],
                textposition='outside',
                hovertemplate=(
                    '<b>%{x}</b><br>' +
                    'Nombre >= threshold: %{y}<br>' +
                    'Total: %{customdata}<br>' +
                    'Proportion: %{text:.1%}<br>' +
                    '<extra></extra>'
                ),
                customdata=prop["total"].values,
                texttemplate=[f'{p:.1%}' for p in prop["prop_above"]],
                name="Count"
            ),
            row=1, col=2
        )
        
        # Mise en forme
        fig.update_xaxes(tickangle=-45, row=1, col=1)
        fig.update_xaxes(tickangle=-45, row=1, col=2)
        fig.update_yaxes(title_text="Proportion", row=1, col=1)
        fig.update_yaxes(title_text="Nombre de captions", row=1, col=2)
        
        fig.update_layout(
            title=dict(
                text=f"Analyse des captions avec {self.fun_metric} >= {threshold}<br>" +
                    f"<sub>{len(df)} captions totales • {df['above'].sum()} au-dessus du seuil ({df['above'].mean():.1%})</sub>",
                x=0.5,
                xanchor='center'
            ),
            height=500,
            showlegend=False,
            template='plotly_white'
        )
        
        fig.show()
        return prop, fig
    

    def plot_enrichment_bar(self, merged, top_n=20):
        """
        Bar chart des topics les plus enrichis dans le top percentile
        """
        df_plot = merged.head(top_n)

        fig = px.bar(
            df_plot,
            x="enrichment_top_vs_overall",
            y="aggregated_topic",
            orientation="h",
            title=f"Enrichissement des topics dans le top (Top {top_n})",
            labels={
                "enrichment_top_vs_overall": "Enrichissement (top vs overall)",
                "aggregated_topic": "Topic agrégé"
            }
        )

        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            template="plotly_white",
            height=500
        )
        fig.show()
        return fig



    def plot_top_vs_overall_props(self, merged, top_n=15):
        df_plot = merged.head(top_n).copy()

        total = merged["overall_count"].sum()
        df_plot["overall_prop"] = df_plot["overall_count"] / total

        fig = go.Figure()

        fig.add_bar(
            x=df_plot["aggregated_topic"],
            y=df_plot["top_prop"],
            name="Proportion dans le top"
        )

        fig.add_bar(
            x=df_plot["aggregated_topic"],
            y=df_plot["overall_prop"],
            name="Proportion globale"
        )

        fig.update_layout(
            barmode="group",
            title="Proportion des topics : Top vs Global",
            xaxis_title="Topic agrégé",
            yaxis_title="Proportion",
            template="plotly_white",
            height=450
        )
        
        fig.show()
        return fig


    def plot_bubble_enrichment(self, merged, top_n=30):
        df_plot = merged.head(top_n)

        fig = px.scatter(
            df_plot,
            x="overall_count",
            y="enrichment_top_vs_overall",
            size="top_count",
            color="aggregated_topic",
            hover_name="aggregated_topic",
            title="Enrichissement vs volume global des topics",
            labels={
                "overall_count": "Volume global",
                "enrichment_top_vs_overall": "Enrichissement top vs overall",
                "top_count": "Occurrences dans le top"
            }
        )

        fig.update_layout(
            template="plotly_white",
            height=500
        )

        fig.show()
        return fig



    # ---------------------------------------------------------
    # Sauvegarde and load
    # ---------------------------------------------------------

    @staticmethod
    def save_results(data_topics, data_topic_info, filepath):
        """Sauvegarde les résultats dans un pickle."""
        with open(filepath, "wb") as f:
            pickle.dump({"data_topics": data_topics, "data_topic_info": data_topic_info}, f)

    
    @staticmethod
    def load_results(data_topics, data_topic_info, filepath):
        """Load les résultats depuis un pickle."""
        with open(filepath, "rb") as f:
            data = pickle.load(f)
        
        df_topics_list = data['data_topics']
        df_topic_info_list = data['data_topic_info']
        
        return df_topics_list, df_topic_info_list

