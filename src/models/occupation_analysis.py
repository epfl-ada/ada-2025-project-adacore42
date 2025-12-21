#It must be disclosed that this code was generated with the assistance of AI tools, either whole blocks or certain functionalities.
#The AI used: ChatGPT-5 by OpenAI and GitHub Copilot.
#plotting was overall done by ChatGPT, epecially to convert matplotlib to plotly
#Code was primarily written in a different file (see _Other/andras_analysis/axis2_complete.ipynb) and then ported here.

import numpy as np
from scipy.stats import ttest_ind
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import re
import spacy
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from itertools import combinations



class OccupationAnalysis:
    """
    A class for performing all analysis related to occupations in text data.
    """
#--------------------------------------------------------#
#Initialization
    def __init__(self, tf_idf_matrix, feature_names, term_indices, term_counts, documents, scores, contest_ids,occupations_mapping, occupation_to_category = None, occupation_df_path = None, category_caption_df_path =None, force_rebuild = False):
        self.tf_idf_matrix = tf_idf_matrix
        self.feature_names = np.array(feature_names)
        self.term_indices = np.array(term_indices)
        self.term_counts = np.array(term_counts)
        self.documents = documents
        self.contest_ids = np.array(contest_ids)
        self.scores = np.array(scores)
        self.syn_to_occ = occupations_mapping
        self.occupation_df_path = occupation_df_path
        self.category_caption_df_path = category_caption_df_path
        self.force_recompute = force_rebuild

        occupation_categories = {
        "Arts and Entertainment": [
            "clown","magician","artist","pianist","film","performer","art critic","actor","comedian","model",
            "singer","dancer","musician","musical conductor","circus performer","writer","poet","cartoonist",
            "illustrator","dj","screenwriter","playwright","story writer","story reader","fiction writer",
            "concert pianist","trumpeter","soloist","harpist","band leader","vocalist","photographer",
            "camera operator","cinematographer","news anchor","radio announcer","radio commentator","showman",
            "ventriloquist","stagehand","stage manager","puppeteer","master chef","fashion model",
            "fashion stylist","fashion designer","fashion director","fashion coordinator","dresser",
            "costume designer","opera singer","art model","artists model","art director","artistic director",
            "conceptual artist","music teacher","piano player","piano mover","animator","yoga instructor"
        ],
        "Business, Management and Finance": [
            "boss","ceo","owner","executive","chief","manager","assistant","administrator","supervisor",
            "branch manager","department head","project manager","operations manager","investment banker",
            "banker","financier","financial advisor","financial analyst","financial planner","accountant",
            "tax accountant","auditor","internal auditor","consultant","business consultant",
            "marketing consultant","marketing director","sales manager","sales associate","sales representative",
            "sales assistant","store manager","business manager","business analyst","entrepreneur","broker",
            "insurance agent","insurance broker","insurance underwriter","cpa","account executive","asset manager",
            "portfolio manager","investment advisor","vendor","purchaser","buyer","seller"
        ],
        "Law, Government and Politics": [
            "lawyer","attorney","attorney general","judge","justice","prosecutor","public defender",
            "district attorney","trial lawyer","patent attorney","corporate lawyer","criminal lawyer",
            "probate lawyer","legal counsel","legal advisor","legal aide","paralegal","litigator",
            "litigation attorney","politician","senator","us senator","congressman","congressperson",
            "state representative","representative","president","vice president","governor","mayor",
            "commissioner","ambassador","diplomat","legislator","councilman","official","city official",
            "precinct captain","police commissioner"
        ],
        "Healthcare and Medicine": [
            "doctor","dentist","surgeon","chiropractor","physician","physician assistant","cardiologist",
            "pediatrician","nurse","rn","nurse practitioner","medical doctor","medical officer",
            "medical resident","medical writer","medical illustrator","medical consultant",
            "medical technologist","orthodontist","ophthalmologist","optometrist","optician","psychiatrist",
            "psychologist","clinical","mental health","therapist","massage therapist","physical therapist",
            "occupational therapy","emt","paramedic","dietitian","nutritionist","radiologist","virologist",
            "epidemiologist","urologist","proctologist","pathologist","hematologist","dermatologist",
            "anesthesiologist","neurosurgeon","oncologist","veterinarian","podiatrist","speech therapist",
            "speech pathologist"
        ],
        "Education and Academia": [
            "professor","teacher","kindergarten teacher","music teacher","math teacher","school nurse",
            "school counselor","school principal","assistant principal","educator","lecturer","tutor",
            "academic researcher","research scientist","scientist","student nurse","research analyst","mentor",
            "instructor","piano professor"
        ],
        "Science and Engineering": [
            "scientist","biologist","chemist","physicist","astronaut","engineer","software engineer",
            "civil engineer","mechanical engineer","electrical engineer","aerospace engineer",
            "environmental scientist","epidemiologist","geologist","hydrologist","astronomer","astrophysicist",
            "anthropologist","archaeologist","ichthyologist","ornithologist","zoologist","herpetologist",
            "entomologist","economist","statistician","data scientist","data analyst","programmer",
            "network engineer","cloud engineer","cybersecurity","technician","technologist"
        ],
        "Trades, Crafts and Manufacturing": [
            "carpenter","mason","plumber","electrician","welder","mechanic","machinist","builder","contractor",
            "construction worker","ironworker","stonemason","bricklayer","roofer","house painter","glass cutter",
            "glass blower","blacksmith","farrier","tool maker","metalworker","engraver","seamstres","tailor",
            "dressmaker","cobbler","upholsterer","woodworker","boat builder","ship carpenter","steamfitter",
            "pipe fitter","painter","sculptor"
        ],
        "Service Industry and Hospitality": [
            "chef","cook","sous chef","barista","bartender","waiter","waitress","server","valet",
            "hotel concierge","housekeeper","maid","janitor","laundry","baker","pastry chef","line cook",
            "butler","doorman","caterer","bar manager","food handler","food processor","delivery driver",
            "tour guide","travel agent","host","hostess","customer service","hairdresser","stylist","manicurist"
        ],
        "Transportation and Logistics": [
            "driver","uber driver","taxi driver","delivery driver","truck driver","bus driver","pilot","co pilot",
            "airline pilot","ship captain","sailor","fisherman","train driver","train conductor",
            "forklift operator","baggage handler","loader","mover","courier","dispatcher","navigator","porter",
            "mail carrier","mailman","postal worker"
        ],
        "Agriculture, Animals and Outdoors": [
            "farmer","rancher","gardener","shepherd","beekeeper","fisher","fisherman","hunter","cowboy",
            "lumberjack","park ranger","forester","tree surgeon","tree trimmer","zookeeper","animal trainer",
            "dog walker","dog trainer","agricultural worker","crop duster","game warden"
        ],
        "Public Safety, Military and Security": [
            "cop","police officer","security guard","guard","prison guard","firefighter","fire chief","marshal",
            "constable","deputy","soldier","military","lifeguard","paramedic","border patrol","parole officer",
            "detective","homicide detective","inspector","first responder","sheriff","policewoman",
            "transit police","state trooper"
        ],
        "Sports and Fitness": [
            "athlete","football player","baseball player","basketball player","skier","swimmer","diver","golfer",
            "tennis player","yoga teacher","fitness instructor","trainer","personal trainer","coach",
            "boxing coach","boxing instructor","umpire","referee","jockey","skateboarder","runner","pitcher",
            "catcher","drummer"
        ],
        "Media and Communications": [
            "journalist","reporter","columnist","news writer","editor","copyeditor","fact checker","publicist",
            "press secretary","communication officer","commentator","blogger","vlogger","publisher","copywriter",
            "speech writer","screen writer","court stenographer","captioner"
        ],
        "Domestic and Personal Care": [
            "babysitter","nanny","caregiver","housekeeper","house sitter","homemaker","child care","home health aide",
            "personal shopper","personal assistant","personal stylist","life coach","doula"
        ]
        }

        # category: list of canonical occupations
        self.occupation_categories = occupation_categories

        

        if occupation_to_category is None:
            # building reverse mapping: occupation to category
            occupation_to_category = {}
            for category, occupations in occupation_categories.items():
                for occ in occupations:
                    occupation_to_category[occ] = category
            self.occupation_to_category = occupation_to_category
        
        else:
            self.occupation_to_category = occupation_to_category

        # Load or build occupation dataframe
        self._occupation_df = self._load_or_build_occupation_dataframe()
        self._category_caption_df = self._load_or_build_category_caption_dataframe()


    #--------------------------------------------------------#
    # Load or build dataframes
    #--------------------------------------------------------#
    def _load_or_build_occupation_dataframe(self):
        if (self.occupation_df_path is not None and not self.force_recompute and os.path.exists(self.occupation_df_path)):
            print("Loading cached occupation dataframe...")
            return pd.read_pickle(self.occupation_df_path)
        print("Building occupation dataframe...")
        df = self.build_occupation_dataframe()
        
        if self.occupation_df_path is not None:
            df.to_pickle(self.occupation_df_path)

        return df

    def _load_or_build_category_caption_dataframe(self):
        
        if (self.category_caption_df_path is not None and not self.force_recompute and os.path.exists(self.category_caption_df_path)):
            print("Loading cached category-caption dataframe...")
            return pd.read_pickle(self.category_caption_df_path)
        
        print("Building category-caption dataframe...")
        df = self.build_category_dataframe()

        if self.category_caption_df_path is not None:
            df.to_pickle(self.category_caption_df_path)

        return df 
    #--------------------------------------------------------#
    # all getters
    #--------------------------------------------------------#
    def get_tf_idf_matrix(self):
        '''
        Getter for the TF-IDF matrix
        '''
        return self.tf_idf_matrix
    
    def get_feature_names(self):
        '''
        Getter for the feature names
        '''
        return self.feature_names
    def get_term_indices(self):
        '''
        Getter for the term indices
        '''
        return self.term_indices
    def get_term_counts(self):
        '''
        Getter for the term counts
        '''
        return self.term_counts
    def get_documents(self):
        '''
        Getter for the documents
        '''
        return self.documents
    def get_scores(self):
        '''
        Getter for the funniness scores
        '''
        return self.scores
    
    def get_contest_ids(self):
        '''
        Getter for the contest IDs
        '''
        return self.contest_ids
    
    def get_occupations_mapping(self):
        '''
        Getter for the occupation synonyms to canonical occupation mapping
        '''
        return self.syn_to_occ
    
    def get_occupation_to_category(self):
        '''
        Getter for the occupation to category mapping
        '''
        return self.occupation_to_category
    
    #getter for occupation dataframe
    def get_occupation_dataframe(self):
        '''
        Getter for the occupation-level dataframe
        '''
        if self._occupation_df is None:
            self._occupation_df = self.build_occupation_dataframe()
        return self._occupation_df
    
    #getter for category-caption dataframe
    def get_category_caption_dataframe(self):
        '''
        Getter for the caption-category level dataframe
        '''
        if self._category_caption_df is None:
            self._category_caption_df = self.build_category_dataframe()
        return self._category_caption_df
    
    def get_occupation_categories(self):
        '''
        Getter for the occupation categories mapping
        '''
        return self.occupation_categories
    
    # Get occupation synonyms by category
    def get_occupation_category(self, category_name):
        """
        Prints the occupation synonyms for a given category.
        """
        if category_name not in self.occupation_categories:
            raise ValueError(f"Category '{category_name}' not found.")
        
        return self.occupation_categories[category_name]
    
    #---------------------------------------------------------#
    # Remove words from occupation analysis
    # --------------------------------------------------------# 
    def remove_terms_from_analysis(self, terms_to_remove):
        """
        Removes specified terms from occupation analysis.
        """
        terms_to_remove = set(term.lower() for term in terms_to_remove)

        #fix occupation dataframe
        if self._occupation_df is not None:
            self._occupation_df = self._occupation_df[~self._occupation_df['term'].str.lower().isin(terms_to_remove)].reset_index(drop=True)

        #fix category-caption dataframe
        if self._category_caption_df is not None:
            self._category_caption_df = self._category_caption_df[~self._category_caption_df['category'].str.lower().isin(terms_to_remove)].reset_index(drop=True)
        
        #fixing the syn_to_occ mapping
        self.syn_to_occ = {syn: occ for syn, occ in self.syn_to_occ.items() if occ.lower() not in terms_to_remove}

        #fix occupation categories
        for category, occupations in self.occupation_categories.items():
            self.occupation_categories[category] = [occ for occ in occupations if occ.lower() not in terms_to_remove]

    #---------------------------------------------------------#
    # Exploratory analysis functions
    # --------------------------------------------------------#   
    def exploratory_occupation_analysis(self, alpha=0.05, print_results=True):
        """
        Some exploratory statistics on occupations in the TF-IDF matrix.
        """
        mask_docs_with_term = np.array(self.tf_idf_matrix[:, self.term_indices].sum(axis=1) > 0).flatten()

        num_with_term = mask_docs_with_term.sum()
        total_docs = self.tf_idf_matrix.shape[0]

        if print_results:
            print(f"Number of documents with at least one occupation term: {num_with_term} out of {total_docs} total documents ({num_with_term / total_docs * 100:.2f}%)")

        # T-test for funniness scores
        scores_with_term = self.scores[mask_docs_with_term]
        scores_without_term = self.scores[~mask_docs_with_term]
        
        t_stat, p_value = ttest_ind(scores_with_term, scores_without_term, equal_var=False)

        if print_results:
            print(f"T-test results: t-statistic = {t_stat:.4f}, p-value = {p_value:.4f}")

            if p_value < alpha:
                print(f"The difference in funniness scores is statistically significant (alpha = {alpha}).")
            else:
                print(f"The difference in funniness scores is not statistically significant (alpha = {alpha}).")

        #average and std of funniness scores
        avg_funniness_per_term = []
        std_funniness_per_term = []

        for idx in self.term_indices:
            mask_term = np.array(self.tf_idf_matrix[:, idx].toarray().flatten() > 0)
            
            if mask_term.any():
                avg_funniness_per_term.append(self.scores[mask_term].mean())
                std_funniness_per_term.append(self.scores[mask_term].std())
            else:
                avg_funniness_per_term.append(0.0)
                std_funniness_per_term.append(0.0)
        
        term_analysis_df = pd.DataFrame({
            'term': self.feature_names[self.term_indices],
            'term_count': self.term_counts,
            'avg_funniness': avg_funniness_per_term,
            'std_funniness': std_funniness_per_term
        }).sort_values(by='term_count', ascending=False).reset_index(drop=True)

        results = {
            'num_docs_with_term': int(num_with_term),
            'total_docs': int(total_docs),
            't_statistic': t_stat,
            'p_value': p_value
        }
        return term_analysis_df, results

    # building a detailed occupation dataframe for further analyses
    def build_occupation_dataframe(self):
        """
        Builds and caches a DataFrame mapping each canonical occupation
        to statistics using funny_score_scaled.
        """

        occupations = sorted(set(self.syn_to_occ.values()))

        occupation_contests = {occ: set() for occ in occupations}
        occupation_funniness = {occ: [] for occ in occupations}
        occupation_temporal = {occ: {} for occ in occupations}
        occupation_term_counts = {occ: 0 for occ in occupations}

        for idx, doc in enumerate(self.documents):
            doc_lower = doc.lower()
            contest_id = self.contest_ids[idx]
            score = self.scores[idx]

            for syn, occ in self.syn_to_occ.items():
                if syn in doc_lower:
                    occupation_term_counts[occ] += 1
                    occupation_contests[occ].add(contest_id)
                    occupation_funniness[occ].append(score)
                    occupation_temporal[occ][contest_id] = (
                        occupation_temporal[occ].get(contest_id, 0) + 1
                    )

        #this can be greatly simplified by not looping through all occupations so many times
        occupation_analysis_df = pd.DataFrame({
            "term": occupations,
            "category": [self.occupation_to_category.get(occ, "Miscellaneous") for occ in occupations],
            "term_count": [occupation_term_counts[occ] for occ in occupations],
            "funniness_scores": [occupation_funniness[occ] for occ in occupations],
            "avg_funniness": [np.mean(occupation_funniness[occ]) if occupation_funniness[occ] else 0.0 for occ in occupations],
            "median_funniness": [np.median(occupation_funniness[occ]) if occupation_funniness[occ] else 0.0 for occ in occupations],
            "std_funniness": [np.std(occupation_funniness[occ]) if occupation_funniness[occ] else 0.0 for occ in occupations],
            "contests": [occupation_contests[occ] for occ in occupations],
            "temporal_distribution": [occupation_temporal[occ] for occ in occupations],
        })

        occupation_analysis_df["num_contests"] = occupation_analysis_df["contests"].apply(len)

        occupation_analysis_df = occupation_analysis_df.sort_values(by="term_count", ascending=False).reset_index(drop=True)

        return occupation_analysis_df


    #building a caption-category dataframe for category-level analysis
    def build_category_dataframe(self):
        '''
        This builds a caption-level dataframe with each row being a (caption, category) pair
        '''
        rows = []

        for idx, doc in enumerate(self.documents):
            doc_lower = doc.lower()
            score = self.scores[idx]
            contest_id = self.contest_ids[idx]

            categories_found = set()

            for syn, occ in self.syn_to_occ.items():
                if syn in doc_lower:
                    category = self.occupation_to_category.get(occ)
                    if category is not None:
                        categories_found.add(category)
            
            for category in categories_found:
                rows.append({
                    'caption_index': idx,
                    'category': category,
                    'funniness_score': score,
                    'contest_id': contest_id
                })

        return pd.DataFrame(rows)
    
    #--------------------------------------------------------#
    # adding a scores column to the occupation dataframe, without rebuilding everything
    def add_scores_to_occupation_dataframe(self, overwrite=True):
        '''
        Adds a funniness scores column to the occupation dataframe.
        '''
        funniness_by_occ = {occ: [] for occ in self._occupation_df['term']}

        #get the scores
        for idx, doc in enumerate(self.documents):
            if (idx+1) % 1000 == 0:
                print(f"Processing document {idx+1}/{len(self.documents)}")
            
            doc_lower = doc.lower()
            score = self.scores[idx]

            for syn, occ in self.syn_to_occ.items():
                if syn in doc_lower and occ in funniness_by_occ:
                    funniness_by_occ[occ].append(score)

        self._occupation_df['funniness_scores'] = self._occupation_df['term'].map(funniness_by_occ)

        #save
        if overwrite and self.occupation_df_path is not None:
            self._occupation_df.to_pickle(self.occupation_df_path)

        return self._occupation_df
    
    #--------------------------------------------------------#
    #Plotting functions in html format for initial exploration
    #--------------------------------------------------------#

    #plotting top occupations by count
    def plot_top_occupations_by_count(self, start = 0, end = 20, save_path=None, plot_method = 'plotly', color = 'blugrn'):
        """
        Plots the top N occupation terms by frequency count.
        """
        df_plot = self._occupation_df.sort_values(by='term_count', ascending=False).iloc[start:end].copy()
        if plot_method == 'plotly':
            hover_data = {
                'num_contests': True,
                'std_funniness': ':.2f',
                'avg_funniness': ':.2f',
                'num_contests': True,
                'term': False
            }
            fig = px.bar(df_plot, x = 'term', y='term_count', hover_data = hover_data,
                        title=f'Top Occupation Terms by Frequency Count (Ranks {start+1} to {end})')
            
            fig.update_traces(marker = dict(color = df_plot['avg_funniness'], colorscale = color, line = dict(color = "rgba(0,0,0,0.7)", width = 1) ))
            fig.update_layout(xaxis_title='Occupation Term', yaxis_title='Frequency Count', template = 'plotly_white', xaxis_tickangle = -45, height = 600, hovermode = 'closest', showlegend = False, title = dict(x = 0.5, xanchor = 'center', text = f"Top Occupations by Frequency Count (Ranks {start+1} to {end})<br><sub>Hover to see number of contests and funniness stats</sub>"))
            if save_path:
                fig.write_html(save_path)
            fig.show()
        elif plot_method == 'plt':
            terms = df_plot["term"].values
            counts = df_plot["term_count"].values

            fig, ax = plt.subplots(figsize=(max(10, len(terms) * 0.4), 6))

            ax.bar(terms,counts,color=color,edgecolor="black",linewidth=1)

            ax.set_xlabel("Occupation Term")
            ax.set_ylabel("Frequency Count")

            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

            ax.set_title(f"Top Occupations by Frequency Count (Ranks {start+1} to {end})",fontsize=12)

            ax.grid(axis="y", linestyle="--", alpha=0.4)

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")

            plt.show()


    # plotting with dropdown menu
    def plot_occupation_dropdown(self, page_size=10, save_path=None, color = 'blugrn'):
        """
        Plots an interactive dropdown to explore occupation statistics.
        """
        occupation_df_sorted = self._occupation_df.sort_values(by='term_count', ascending=False).reset_index(drop=True)
        
        n_pages = (len(occupation_df_sorted) + page_size - 1) // page_size

        fig = go.Figure()

        for page in range(n_pages):
            start_idx = page * page_size
            end = start_idx + page_size
            df_page = occupation_df_sorted.iloc[start_idx:end]

            fig.add_trace(go.Bar(
                x=df_page['term'],
                y=df_page['term_count'],
                visible = (page == 0),
                marker=dict(color=df_page["term_count"], colorscale = color, line=dict(color="rgba(0,0,0,0.7)", width=1)),
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Caption count: %{y}<br>"
                    "Avg funniness: %{customdata[0]:.2f}<br>"
                    "Std funniness: %{customdata[1]:.2f}<br>"
                    "Num contests: %{customdata[2]}<extra></extra>"
                ),
                customdata=np.stack((
                    df_page['avg_funniness'],
                    df_page['std_funniness'],
                    df_page['num_contests']
                ), axis=-1)
            ))
        buttons = [dict(
            label = f"{i*page_size + 1} - {min((i+1)*page_size, len(occupation_df_sorted))}",
            method = "update",
            args = [{"visible": [j == i for j in range(n_pages)]},
                    {"title": f"Occupation Terms {i*page_size + 1} to {min((i+1)*page_size, len(occupation_df_sorted))} by Frequency Count"}]) for i in range(n_pages)]
        

        fig.update_layout(
            updatemenus = [dict(buttons = buttons, direction = "down")],
            title = "Occupations by Caption Count",
            xaxis_title = "Occupation",
            yaxis_title = "Caption Count",
            template = 'plotly_white',
            xaxis_tickangle = -45,
            height = 650,
        )
        if save_path:
            fig.write_html(save_path)
        fig.show()

    #plotting top occupations by average or median funniness
    def plot_top_occupations_by_funniness(self, top_n=20, threshold = 50, save_path=None, measure='avg', ascending=False, plot_method = 'plotly', color = 'blugrn'):
        """
        Plots the top N occupation terms by average funniness score.
        """
        df_plot = self._occupation_df[self._occupation_df['term_count'] >= threshold].sort_values(by=f'{measure}_funniness', ascending=ascending).head(top_n).copy()
        if plot_method == 'plotly':
            hover_data = {
                'term_count': True,
                'std_funniness': ':.2f',
                'avg_funniness': ':.2f',
                'median_funniness': ':.2f',
                'term': False
            }
            ascending_string = 'Bottom' if ascending else 'Top'
            title = 'Average' if measure == 'avg' else 'Median'
            title_string=  f'{ascending_string} {top_n} Occupation Terms by {title} Funniness Score'
            fig = px.bar(df_plot, x = 'term', y=f'{measure}_funniness', hover_data = hover_data,
                        title=title_string)
            
            fig.update_traces(marker = dict(color = df_plot['term_count'], colorscale = color, line = dict(color = "rgba(0,0,0,0.7)", width = 1)))
            fig.update_layout(xaxis_title='Occupation Term', yaxis_title=f'{title} Funniness Score', template = 'plotly_white', xaxis_tickangle = -45, height = 600, hovermode = 'closest', showlegend = False, title = dict(x = 0.5, xanchor = 'center', text = f"Top {top_n} Occupations by {title} Funniness<br><sub>Hover to see frequency and score variability</sub>"))
            if save_path:
                fig.write_html(save_path)
            fig.show()
        elif plot_method == 'plt':
            terms = df_plot["term"].values
            scores = df_plot[f"{measure}_funniness"].values
            title = "Average" if measure == "avg" else "Median"

            fig, ax = plt.subplots(figsize=(max(10, len(terms) * 0.4), 6))

            ax.bar(
                terms,
                scores,
                color= color,   # Plotly default blue
                edgecolor="black",
                linewidth=1
            )

            ax.set_xlabel("Occupation Term")
            ax.set_ylabel(f"{title} Funniness Score")

            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

            ax.set_title(
                f"Top {top_n} Occupation Terms by {title} Funniness Score",
                fontsize=12
            )

            ax.grid(axis="y", linestyle="--", alpha=0.4)

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")

            plt.show()
            


    def plot_best_worst_occupations_by_median(
        self,
        top_n=20,
        threshold=50,
        color="blugrn",
        height=600,
        save_path=None,
    ):
        df = self._occupation_df[self._occupation_df["term_count"] >= threshold].copy()

        # Best (highest median)
        df_best = (
            df.sort_values(by="median_funniness", ascending=False)
            .head(top_n)
            .copy()
        )

        # Worst (lowest median)
        df_worst = (
            df.sort_values(by="median_funniness", ascending=True)
            .head(top_n)
            .copy()
        )

        hover_data = {
            "term_count": True,
            "std_funniness": ":.2f",
            "avg_funniness": ":.2f",
            "median_funniness": ":.2f",
            "term": False,
        }

        fig_best = px.bar(
            df_best,
            x="term",
            y="median_funniness",
            hover_data=hover_data,
        )

        fig_worst = px.bar(
            df_worst,
            x="term",
            y="median_funniness",
            hover_data=hover_data,
        )

        fig = go.Figure(data=fig_best.data + fig_worst.data)

        # Initial visibility
        fig.data[0].visible = True
        fig.data[1].visible = False

        # Coloring
        fig.data[0].update(
            marker=dict(
                color=df_best["term_count"],
                colorscale=color,
                line=dict(color="rgba(0,0,0,0.7)", width=1),
            )
        )
        fig.data[1].update(
            marker=dict(
                color=df_worst["term_count"],
                colorscale=color,
                line=dict(color="rgba(0,0,0,0.7)", width=1),
            )
        )

        fig.update_layout(
            title=dict(
                text=f"Top {top_n} Occupations by Median Funniness",
                x=0.5,
                xanchor="center",
            ),
            xaxis_title="Occupation Term",
            yaxis_title="Median Funniness Score",
            template="plotly_white",
            xaxis_tickangle=-45,
            height=height,
            hovermode="closest",
            showlegend=False,
            margin=dict(t=120),
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    x=0.5,
                    y=1.08,
                    xanchor="center",
                    yanchor="top",
                    buttons=[
                        dict(
                            label="Best (Highest Median)",
                            method="update",
                            args=[
                                {"visible": [True, False]},
                                {
                                    "title.text": f"Top {top_n} Occupations by Median Funniness"
                                },
                            ],
                        ),
                        dict(
                            label="Worst (Lowest Median)",
                            method="update",
                            args=[
                                {"visible": [False, True]},
                                {
                                    "title.text": f"Bottom {top_n} Occupations by Median Funniness"
                                },
                            ],
                        ),
                    ],
                )
            ],
        )

        if save_path:
            fig.write_html(save_path)

        fig.show()


    #plotting the distribution of a chosen occupation term
    def plot_occupation_distribution(self, occupation_term, nbins = 30, save_path=None, plot_method = 'plotly', color = 'cornflowerblue'):
        """
        Plots the distribution of funniness scores for a given occupation term.
        """
        df_plot = self.get_occupation_dataframe()

        row = df_plot[df_plot['term'].str.lower() == occupation_term.lower()]
        if row.empty:
            raise ValueError(f"Occupation term '{occupation_term}' not found in the occupation dataframe.")
        
        scores = row.iloc[0]['funniness_scores']
        if not scores:
            raise ValueError(f"No funniness scores found for occupation term '{occupation_term}'.")
        
        df_plot = pd.DataFrame({'funniness_score': scores})

        if plot_method == 'plotly':
            fig = px.histogram(df_plot, x='funniness_score', nbins=nbins, marginal = "box",
                            title=f'Distribution of Funniness Scores for "{occupation_term}"',
                            hover_data = {'funniness_score': ':.2f'})
            fig.update_traces(marker=dict(color=color, line=dict(color="rgba(0,0,0,0.7)", width=1)))            
            fig.update_layout(xaxis_title='Funniness Score', yaxis_title='Count', template = 'plotly_white', height = 500, hovermode = 'closest', title = dict(x = 0.5, xanchor = 'center', text = f'Distribution of Funniness Scores for "{occupation_term}"'))
            if save_path:
                fig.write_html(save_path)
            fig.show()

        elif plot_method == 'plt':
            scores = df_plot["funniness_score"].values

            # Layout with boxplot on top and histogram below
            fig = plt.figure(figsize=(8, 6))
            gs = fig.add_gridspec(2, 1, height_ratios=[1, 4], hspace=0.05)

            ax_box = fig.add_subplot(gs[0])
            ax_hist = fig.add_subplot(gs[1], sharex=ax_box)

            # Boxplot (marginal)
            ax_box.boxplot(scores,vert=False,patch_artist=True,showfliers=True)

            ax_box.set_yticks([])
            ax_box.set_ylabel("")
            ax_box.grid(False)

            # Color box (Plotly default blue)
            for patch in ax_box.artists:
                patch.set_facecolor(color)
                patch.set_alpha(0.8)

            # Histogram
            ax_hist.hist(
                scores,
                bins=nbins,
                color= color,
                alpha=0.8,
                edgecolor="black"
            )

            ax_hist.set_xlabel("Funniness Score")
            ax_hist.set_ylabel("Count")

            # Clean up layout to mimic plotly_white
            ax_hist.grid(axis="y", linestyle="--", alpha=0.4)

            # Remove x labels from boxplot
            plt.setp(ax_box.get_xticklabels(), visible=False)

            # Centered title
            fig.suptitle(
                f'Distribution of Funniness Scores for "{occupation_term}"',fontsize=12,y=0.97)

            plt.tight_layout(rect=[0, 0, 1, 0.95])

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")

            plt.show()

        return df_plot
    
    def plot_occupation_distribution_multiple(self, occupation_terms, nbins = 30, save_path=None, color = 'cornflowerblue'):
        """
        This is the same as above, but with a button to change occupation terms.
        """
        df = self.get_occupation_dataframe()
        occupation_terms_lower = [term.lower() for term in occupation_terms]
        sub_df = df[df['term'].str.lower().isin(occupation_terms_lower)]
        if sub_df.empty:
            raise ValueError("None of the specified occupation terms were found in the occupation dataframe.")
        
        fig = go.Figure()
        terms = sub_df['term'].tolist()
        for i, (_,row) in enumerate(sub_df.iterrows()):
            scores = row['funniness_scores']
            hist = go.Histogram(
                x=scores,
                nbinsx=nbins,
                name=row['term'],
                visible=(i == 0),
                marker=dict(color=color, line=dict(color="rgba(0,0,0,0.7)", width=1)),
                hovertemplate='Funniness Score: %{x:.2f}<br>Count: %{y}<extra></extra>'
            )
            fig.add_trace(hist)
        buttons = []
        for i, term in enumerate(terms):
            visibility = [False] * len(terms)
            visibility[i] = True
            buttons.append(dict(
                label=term,
                method="update",
                args=[{"visible": visibility},
                    {"title": f'Distribution of Funniness Scores for "{term}"'}]
            ))
        fig.update_layout(
            updatemenus = [dict(active=0, buttons=buttons, x = 0.5, xanchor = 'center', y = 1.15, yanchor = 'top')],
            xaxis_title='Funniness Score',
            yaxis_title='Count',
            template = 'plotly_white',
            height = 500,
            title = f"Distribution of Funniness Scores for \"{terms[0]}\""
        )
        
        if save_path:
            fig.write_html(save_path)
        fig.show()


    def plot_occupation_box_plot(self, occupation_terms, save_path = None, plot_method = 'plotly', color = 'cornflowerblue'):
        """
        Plotting the box plot of the funniness score of multiple occupations on the same plot close to each other. 
        """
        df_plot = self.get_occupation_dataframe()
        occupation_terms_lower = [term.lower() for term in occupation_terms]

        df_reduced = df_plot[df_plot['term'].str.lower().isin(occupation_terms_lower)]

        if df_reduced.empty:
            raise ValueError("None of the specified occupation terms were found in the occupation dataframe.")
        
        #explode the funniness scores
        df_plot = df_reduced[['term', 'funniness_scores']].explode('funniness_scores')

        if plot_method == 'plotly':
        
            fig = px.box(df_plot,x="term",y="funniness_scores",points="outliers", title="Funniness score distribution by occupation", hover_data = {'funniness_scores': ':.2f', 'term': False})

            fig.update_layout(xaxis_title="Occupation", yaxis_title="Funniness score", template="plotly_white", height=600, xaxis_tickangle=-45, hovermode="closest", title=dict(x=0.5, xanchor="center"))

            fig.update_traces(marker=dict(color=color, line=dict(color="rgba(0,0,0,0.7)", width=1)), selector =dict(type="box"), )

            if save_path:
                fig.write_html(save_path)

            fig.show()
        elif plot_method == 'plt':
            terms = df_plot["term"].unique()

            data = [
                df_plot.loc[df_plot["term"] == term, "funniness_scores"].values
                for term in terms]

            fig, ax = plt.subplots(figsize=(max(8, len(terms) * 0.5), 6))

            bp = ax.boxplot(
                data,
                labels=terms,
                patch_artist=True,
                showfliers=True
            )

            # Match Plotly default blue
            for box in bp["boxes"]:
                box.set_facecolor(color)
                box.set_alpha(0.8)

            # Axis labels
            ax.set_xlabel("Occupation")
            ax.set_ylabel("Funniness score")

            # Rotate x-axis labels
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

            # Centered title
            ax.set_title(
                "Funniness score distribution by occupation",
                loc="center",
                fontsize=12
            )

            # Light grid like plotly_white
            ax.grid(axis="y", linestyle="--", alpha=0.4)

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")

            plt.show()
                    



    #--------------------------------------------------------#
    # Tests to compare specific occupations
    #--------------------------------------------------------#
    def compare_set_of_occupations(self, occupation_list, interpret = False, alpha = 0.05):
        '''
        Compares funniness score distributions among a set of occupation terms using Kruskal-Wallis H-test.
        '''
        df = self.get_occupation_dataframe()
        occupation_list_lower = [occ.lower() for occ in occupation_list]

        sub_df = df[df['term'].isin(occupation_list)]
        if sub_df.shape[0] < 2:
            raise ValueError("At least two of the specified occupation terms must be found in the occupation dataframe.")
        
        score_groups = [scores for scores in sub_df['funniness_scores'] if len(scores) > 0]
        if len(score_groups) < 2:
            raise ValueError("At least two occupation terms must have associated funniness scores.")
        
        stat, p_value = stats.kruskal(*score_groups)

        if interpret:
            if p_value < alpha:
                print(f"Kruskal-Wallis test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The differences in funniness scores among the occupations are statistically significant (alpha = {alpha}).")
            else:
                print(f"Kruskal-Wallis test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The differences in funniness scores among the occupations are not statistically significant (alpha = {alpha}).")
        return stat, p_value


    def compare_occupations(self, occupation1, occupation2, interpret = False, alpha = 0.05, alternative = 'two-sided'):
        '''
        Compares funniness score distributions between two occupation terms using Mann-Whitney U test.
        '''
        df = self.get_occupation_dataframe()
        occupation_1_lower = occupation1.lower()
        occupation_2_lower = occupation2.lower()

        sub_df = df[df['term'].str.lower().isin([occupation_1_lower, occupation_2_lower])]
        if sub_df.shape[0] < 2:
            raise ValueError("Both specified occupation terms must be found in the occupation dataframe.")
        
        Scores_occ1 = sub_df[sub_df['term'].str.lower() == occupation_1_lower]['funniness_scores'].iloc[0]
        Scores_occ2 = sub_df[sub_df['term'].str.lower() == occupation_2_lower]['funniness_scores'].iloc[0]
        
        if len(Scores_occ1) == 0 or len(Scores_occ2) == 0:
            raise ValueError("One or both occupation terms have no associated funniness scores.")
        
        stat, p_value = stats.mannwhitneyu(Scores_occ1, Scores_occ2, alternative=alternative)
        if interpret:
            if p_value < alpha:
                print(f"Mann-Whitney U test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The difference in funniness scores between '{occupation1}' and '{occupation2}' is statistically significant (alpha = {alpha}).")
            else:
                print(f"Mann-Whitney U test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The difference in funniness scores between '{occupation1}' and '{occupation2}' is not statistically significant (alpha = {alpha}).")
        return stat, p_value
    
    def cliffs_delta_occupations(self, occupation1, occupation2, interpret = False, alpha = 0.05):
        '''
        Computes Cliff's Delta effect size between two occupation terms.
        '''
        df = self.get_occupation_dataframe()
        occupation_1_lower = occupation1.lower()
        occupation_2_lower = occupation2.lower()

        sub_df = df[df['term'].str.lower().isin([occupation_1_lower, occupation_2_lower])]
        if sub_df.shape[0] < 2:
            raise ValueError("Both specified occupation terms must be found in the occupation dataframe.")
        
        rows_occ1 = sub_df[sub_df['term'].str.lower() == occupation_1_lower]['funniness_scores'].iloc[0]
        rows_occ2 = sub_df[sub_df['term'].str.lower() == occupation_2_lower]['funniness_scores'].iloc[0]
        if len(rows_occ1) == 0 or len(rows_occ2) == 0:
            raise ValueError("One or both occupation terms have no associated funniness scores.")
        rows_occ1 = np.array(rows_occ1)
        rows_occ2 = np.array(rows_occ2)

        n1 = len(rows_occ1)
        n2 = len(rows_occ2)
        greater = sum(1 for x in rows_occ1 for y in rows_occ2 if x > y)
        lesser = sum(1 for x in rows_occ1 for y in rows_occ2 if x < y)

        delta = (greater - lesser) / (n1 * n2)

        if interpret:
            abs_delta = abs(delta)
            if abs_delta < 0.147:
                size = "negligible"
            elif abs_delta < 0.33:
                size = "small"
            elif abs_delta < 0.474:
                size = "medium"
            else:
                size = "large"
            print(f"Cliff's Delta: {delta:.4f} ({size} effect size)")
        
        return delta


    def pairwise_occupation_testing(self, occupation_list, alpha = 0.05):
        pval_matrix = pd.DataFrame(np.ones((len(occupation_list), len(occupation_list))), index=occupation_list, columns=occupation_list)
        delta_matrix = pd.DataFrame(np.zeros((len(occupation_list), len(occupation_list))), index=occupation_list, columns=occupation_list)

        for occ_1, occ_2 in combinations(occupation_list,2):
            _, p_value = self.compare_occupations(occ_1, occ_2, interpret = False)
            delta = self.cliffs_delta_occupations(occ_1, occ_2, interpret = False)

            pval_matrix.loc[occ_1, occ_2] = p_value
            delta_matrix.loc[occ_1, occ_2] = delta
            pval_matrix.loc[occ_2, occ_1] = p_value
            delta_matrix.loc[occ_2, occ_1] = -delta # anti-symmetric

        return pval_matrix, delta_matrix
    #--------------------------------------------------------#
    # Categorical analysis functions
    #--------------------------------------------------------#
    
    #plotting boxplot for category-level funniness scores
    def plot_category_boxplot(self, order_by="median", save_path=None, color = 'cornflowerblue', plot_method = 'plotly'):
        '''
        Creates an interactive Plotly boxplot of funniness score distributions
        grouped by occupation category.
        order_by : {"median", "mean", "count", "std"}.
        '''

        # Use cached caption-category dataframe
        df = self.get_category_caption_dataframe().copy()

        # Compute category-level statistics
        stats = (
            df.groupby("category")["funniness_score"]
            .agg(["median", "mean", "count", "std"])
            .reset_index()
        )

        valid_orders = {"median", "mean", "count", "std"}
        if order_by not in valid_orders:
            raise ValueError(f"order_by must be one of {valid_orders}")

        ordered_categories = (
            stats.sort_values(by=order_by, ascending=False)["category"].tolist()
        )

        if plot_method == 'plotly':
            # Create boxplot
            fig = px.box(
                df,
                x="category",
                y="funniness_score",
                category_orders={"category": ordered_categories},
                title=f"Funniness score distribution by occupation category (ordered by {order_by})"
            )

            # Add sample size annotations
            annotations = []
            y_max = df["funniness_score"].max()
            y_range = y_max - df["funniness_score"].min()

            for _, row in stats.iterrows():
                annotations.append(
                    dict(
                        x=row["category"],
                        y=y_max + 0.05 * y_range,
                        text=f"n={int(row['count'])}",
                        showarrow=False,
                        font=dict(size=10),
                        xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="rgba(0,0,0,0.2)",
                        borderwidth=1
                    )
                )
            # Final layout
            fig.update_layout(
                xaxis_title="Occupation category",
                yaxis_title="Funny score scaled",
                template="plotly_white",
                height=650,
                xaxis_tickangle=-45,
                annotations=annotations,
                showlegend=False,
                hovermode="closest",
                title=dict(
                    x=0.5,
                    xanchor="center",
                    text=(
                        f"Funniness score distribution by occupation category<br>"
                        f"<sub>{len(ordered_categories)} categories • "
                        f"{len(df)} caption-category matches • "
                        f"Global median: {df['funniness_score'].median():.2f}</sub>"
                    )
                )
            )
            fig.update_traces(marker=dict(color=color, line=dict(color="rgba(0,0,0,0.7)", width=1)), selector=dict(type="box"))
            if save_path:
                fig.write_html(save_path)

            fig.show()
        elif plot_method == 'plt':

            # Reorder dataframe by category order
            df["category"] = pd.Categorical(df["category"],categories=ordered_categories,ordered=True)
            df = df.sort_values("category")

            # Prepare data for boxplot
            data = [df.loc[df["category"] == cat, "funniness_score"].values for cat in ordered_categories]

            fig, ax = plt.subplots(figsize=(max(20, len(ordered_categories) * 0.35), 12))

            boxprops = dict(linewidth=1.2)
            medianprops = dict(color="black", linewidth=1.5)
            whiskerprops = dict(linewidth=1.2)
            capprops = dict(linewidth=1.2)

            bp = ax.boxplot(
                data,
                patch_artist=True,
                labels=ordered_categories,
                boxprops=boxprops,
                medianprops=medianprops,
                whiskerprops=whiskerprops,
                capprops=capprops,
                showfliers=True
            )

            # Color boxes (single color similar to Plotly default)
            for box in bp["boxes"]:
                box.set_facecolor(color)
                box.set_alpha(0.8)

            # Axis labels
            ax.set_xlabel("Occupation category")
            ax.set_ylabel("Funny score scaled")

            # Rotate x labels
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

            # Add sample size annotations
            y_min = df["funniness_score"].min()
            y_max = df["funniness_score"].max()
            y_range = y_max - y_min

            for i, row in stats.iterrows():
                ax.text(
                    x=ordered_categories.index(row["category"]) + 1,
                    y=y_max + 0.05 * y_range,
                    s=f"n={int(row['count'])}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    bbox=dict(
                        facecolor="white",
                        edgecolor="black",
                        boxstyle="round,pad=0.25",
                        linewidth=0.5,
                        alpha=0.8
                    )
                )

            # Title + subtitle
            ax.set_title(
                "Funniness score distribution by occupation category\n"
                f"{len(ordered_categories)} categories • "
                f"{len(df)} caption-category matches • "
                f"Global median: {df['funniness_score'].median():.2f}",
                fontsize=15,
                pad = 30
            )

            # Improve layout
            ax.grid(axis="y", linestyle="--", alpha=0.4)
            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")

            plt.show()
                    

    #statistical testing between categories
    def kruskal_wallis_test(self, interpret = False, alpha =    0.05):
        '''
        Performs Kruskal-Wallis H-test to determine if there are statistically significant differences
        in funniness scores across occupation categories.
        '''

        df = self.get_category_caption_dataframe()

        category_groups = [group['funniness_score'].values for name, group in df.groupby('category')]

        stat, p_value = stats.kruskal(*category_groups)
        if interpret:
            if p_value < alpha:
                print(f"Kruskal-Wallis test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The differences in funniness scores across categories are statistically significant (alpha = {alpha}).")
            else:
                print(f"Kruskal-Wallis test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The differences in funniness scores across categories are not statistically significant (alpha = {alpha}).")
        return stat, p_value
    
    def targeted_category_test(self, category1, category2, interpret = False, alpha = 0.05, alternative = 'two-sided'):
        df = self.get_category_caption_dataframe()
        scores_cat1 = df[df['category'] == category1]['funniness_score'].values
        scores_cat2 = df[df['category'] == category2]['funniness_score'].values

        if len(scores_cat1) == 0 or len(scores_cat2) == 0:
            raise ValueError("One or both categories have no associated funniness scores.")
        
        stat, p_value = stats.mannwhitneyu(scores_cat1, scores_cat2, alternative= alternative)

        if interpret:
            if p_value < alpha:
                print(f"Mann-Whitney U test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The difference in funniness scores between '{category1}' and '{category2}' is statistically significant (alpha = {alpha}).")
            else:
                print(f"Mann-Whitney U test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The difference in funniness scores between '{category1}' and '{category2}' is not statistically significant (alpha = {alpha}).")
        return stat, p_value

    def cliffs_delta(self, category1, category2, interpret = False, alpha = 0.05):
        '''
        Computes Cliff's Delta effect size between two occupation categories.
        '''
        df = self.get_category_caption_dataframe()
        scores_cat1 = df[df['category'] == category1]['funniness_score'].values
        scores_cat2 = df[df['category'] == category2]['funniness_score'].values

        if len(scores_cat1) == 0 or len(scores_cat2) == 0:
            raise ValueError("One or both categories have no associated funniness scores.")
        
        x = np.asarray(scores_cat1)
        y = np.asarray(scores_cat2)

        nx = len(x)
        ny = len(y)
        greater = np.sum(x[:, None] > y)
        lesser = np.sum(x[:, None] < y)
        delta = (greater - lesser) / (nx * ny)
        if interpret:
            
            abs_delta = abs(delta)
            if abs_delta < 0.147:
                size = "negligible"
            elif abs_delta < 0.33:
                size = "small"
            elif abs_delta < 0.474:
                size = "medium"
            else:
                size = "large"
            print(f"Cliff's Delta: {delta:.4f} (effect size: {size})")

        return delta

    def pairwise_category_testing(self, category_list, alpha = 0.05):
        pval_matrix = pd.DataFrame(np.ones((len(category_list), len(category_list))), index=category_list, columns=category_list)
        delta_matrix = pd.DataFrame(np.zeros((len(category_list), len(category_list))), index=category_list, columns=category_list)

        for cat_1, cat_2 in combinations(category_list,2):
            _, p_value = self.targeted_category_test(cat_1, cat_2, interpret = False)
            delta = self.cliffs_delta(cat_1, cat_2, interpret = False)

            pval_matrix.loc[cat_1, cat_2] = p_value
            delta_matrix.loc[cat_1, cat_2] = delta
            pval_matrix.loc[cat_2, cat_1] = p_value
            delta_matrix.loc[cat_2, cat_1] = -delta # anti-symmetric

        return pval_matrix, delta_matrix
    
    #--------------------------------------------------------#
    # Temporal analyses functions
    #--------------------------------------------------------#
    def temporal_counting(self, occupations):
        '''
        temporal counting for a list of occupations/a single occupation provided as a single-element list
        returns a dictionary mapping contest_id to counts
        '''

        occ_df = self.get_occupation_dataframe()

        counts_per_contest = {}

        for occ in occupations:
            row = occ_df[occ_df['term'] == occ]
            if row.empty:
                continue
            
            temporal = row.iloc[0]['temporal_distribution']

            for contest_id, count in temporal.items():
                counts_per_contest[contest_id] = counts_per_contest.get(contest_id, 0) + count
        
        return counts_per_contest

    def plot_temporal_trends(self, occupations, title = None, cumulative = False, save_path=None, color='crimson', plot_method='plotly'):
        '''
        Plots temporal trends for a list of occupations.
        '''

        counts_per_contest = self.temporal_counting(occupations)

        if not counts_per_contest:
            raise ValueError("No data found for the specified occupations.")
        
        if cumulative:
            y = counts_per_contest.cumsum()
        else:
            y = counts_per_contest
        
        if plot_method == 'plotly':
            fig = px.line(x = list(y.keys()), y = list(y.values()), markers = True, labels = {'x':'Contest ID', 'y':'Cumulative Count' if cumulative else 'Count'},
                        title = title or f'Temporal Trend for Occupations: {", ".join(occupations)}')
            fig.update_traces(line=dict(color=color))
            
            fig.update_layout(template = 'plotly_white', height = 500, hovermode = 'closest', title = dict(x = 0.5, xanchor = 'center', text = title or f'Temporal Trend for Selected Occupations'),
                            xaxis_title = 'Contest ID',
                            yaxis_title = 'Cumulative Count' if cumulative else 'Count')

            if save_path:
                fig.write_html(save_path)
            fig.show()
        elif plot_method == 'plt':
            plt.figure(figsize=(10,6))
            plt.plot(list(y.keys()), list(y.values()), marker='o', color=color)
            plt.title(title or f'Temporal Trend for Selected Occupations')
            plt.xlabel('Contest ID')
            plt.ylabel('Cumulative Count' if cumulative else 'Count')
            plt.grid(axis='y', linestyle='--', alpha=0.4)
            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")

            plt.show()


    def plot_group_temporal_trends(self, group_dict, cumulative = False, min_total = 5, save_path=None, plot_method='plotly'):
        '''
        Plots temporal trends for multiple occupation groups.
        group_dict : dict mapping group names to lists of occupations
        '''
        if plot_method == 'plotly':
            fig = px.line()

            for group_name, occupations in group_dict.items():
                series = self.temporal_counting(occupations)

                if sum(series.values()) < min_total:
                    continue

                if cumulative:
                    y = pd.Series(series).sort_index().cumsum()
                else:
                    y = pd.Series(series).sort_index()

                fig.add_scatter(x = y.index, y = y.values, mode = 'lines+markers', name = group_name)

            fig.update_layout(template = 'plotly_white', height = 600, hovermode = 'closest',
                            title = dict(x = 0.5, xanchor = 'center', text = 'Temporal Trends for Occupation Groups ({cumulative} counts)'.format(cumulative = 'Cumulative' if cumulative else 'Non-cumulative')),
                            xaxis_title = 'Contest ID',
                            yaxis_title = 'Cumulative Count' if cumulative else 'Count')

            if save_path:
                fig.write_html(save_path)
            fig.show() 
        elif plot_method == 'plt':
            plt.figure(figsize=(10,6))

            for group_name, occupations in group_dict.items():
                series = self.temporal_counting(occupations)

                if sum(series.values()) < min_total:
                    continue

                if cumulative:
                    y = pd.Series(series).sort_index().cumsum()
                else:
                    y = pd.Series(series).sort_index()

                plt.plot(y.index, y.values, marker='o', label=group_name)

            plt.title('Temporal Trends for Occupation Groups ({cumulative} counts)'.format(cumulative = 'Cumulative' if cumulative else 'Non-cumulative'))
            plt.xlabel('Contest ID')
            plt.ylabel('Cumulative Count' if cumulative else 'Count')
            plt.legend()
            plt.grid(axis='y', linestyle='--', alpha=0.4)
            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")

            plt.show()

    #--------------------------------------------------------#
    # Topic modelling
    #--------------------------------------------------------#
    def topic_model_category(self, category_name, min_topics = 15, ngram_size = (1,2), min_tokens = 2, model_name = "all-MiniLM-L6-v2"):
        '''
        Topic modelling with BERTopic for a given occupation category.
        '''
        if category_name not in self.occupation_categories:
            raise ValueError(f"Category '{category_name}' not found.")
        
        df_category = self.get_category_caption_dataframe()
        df_category = df_category[df_category['category'] == category_name].copy()

        if df_category.empty:
            raise ValueError(f"No captions found for category '{category_name}'.")
        
        df_category["caption"] = df_category["caption_index"].apply(lambda idx: self.documents[idx])

        category_terms = set()
        for occ in self.occupation_categories[category_name]:
            for token in occ.lower().split():
                category_terms.add(token)

        #remove occupation terms from captions
        def clean_caption(text):
            text_lower = text.lower()
            tokens = re.findall(r'\b\w+\b', text_lower)
            tokens_cleaned = [tok for tok in tokens if tok not in category_terms]
            return ' '.join(tokens_cleaned)
        df_category['cleaned_caption'] = df_category['caption'].apply(clean_caption)

        #filter captions with min tokens
        df_category = df_category[df_category['cleaned_caption'].str.split().apply(len) >= min_tokens]
        
        captions = df_category['cleaned_caption'].tolist()

        if not captions:
            raise ValueError(f"No captions meet the minimum token requirement for category '{category_name}'.")
        
        # Initialize BERTopic model
        sentence_model = SentenceTransformer(model_name)
        embeddings = sentence_model.encode(captions, show_progress_bar=True)
        vectorizer_model = CountVectorizer(stop_words='english')

        topic_model = BERTopic(
            vectorizer_model = vectorizer_model,
            min_topic_size = min_topics,
            n_gram_range = ngram_size,
            embedding_model = sentence_model,
            verbose = True
        )

        topics, probs = topic_model.fit_transform(captions, embeddings)

        output = df_category.reset_index(drop=True).copy()
        output['topic'] = topics
        output['topic_probability'] = probs
        return topic_model, output

    def map_aggragate_topics_external(self, topic_info, aggregation_dict, label_dict):
        '''
        Maps and aggregates topics based on a provided aggregation dictionary.
        topic info: Datafram with Count and Name columns
        aggregation_dict : dictionary mapping the Names to new aggregated topics
        label_dict: human readable format of aggregation_dict
        '''
        topic_to_group = {}
        for group, topics in aggregation_dict.items():
            for topic in topics:
                topic_to_group[topic] = group
        
        topic_to_label = {}
        for group, labels in label_dict.items():
            for label in labels:
                topic_to_label[label] = group
        df = topic_info.copy()
        df['aggregated_topic'] = df['Name'].map(topic_to_group)
        df = df.dropna(subset=['aggregated_topic'])

        grouping = df.groupby('aggregated_topic').agg(total_count = ('Count', 'sum'), topics = ('Name', list), n_topics = ('Name', 'count')).reset_index()
        
        grouping["topic_labels"] = grouping["topics"].apply(lambda topics: [topic_to_label.get(t, t) for t in topics])
        return grouping

    def plot_aggregated_topics_treemap_external(self,aggregated_topic_df,min_mentions=200,save_path=None,color="Pastel",max_topics=20,title=None,):

        df = aggregated_topic_df[aggregated_topic_df["total_count"] >= min_mentions].copy()

        if df.empty:
            print("No aggregated topics meet the minimum mentions threshold.")
            return

        total = df["total_count"].sum()
        df["percentage"] = df["total_count"] / total * 100

        circle_data = []

        for _, row in df.iterrows():
            group = row["aggregated_topic"]
            count = row["total_count"]
            percentage = row["percentage"]
            topics = row["topic_labels"][:max_topics]

            # Group node
            circle_data.append(dict(id=group,label=group,parent="",value=count,type="group",percent=percentage,))

            # Child nodes (kept, but will be hidden visually)
            child_value = max(count / max(len(topics), 1), 1)

            for topic in topics:
                circle_data.append(dict(id=f"{group}::{topic}",label=topic,parent=group,value=child_value,type="topic",percent=None,))

        df_circle = pd.DataFrame(circle_data)

        # Colors
        palette = (getattr(px.colors.qualitative, color) if isinstance(color, str) else color)

        group_colors = {g: palette[i % len(palette)] for i, g in enumerate(df["aggregated_topic"])}

        df_circle["color"] = df_circle.apply(lambda r: group_colors[r["id"]] if r["type"] == "group" else group_colors[r["parent"]], axis=1,)

        color_map = dict(zip(df_circle["id"], df_circle["color"]))

        # Hover text (groups only)
        df_circle["hover_text"] = df_circle.apply(
            lambda r: (
                f"<b>{r['label']}</b><br>"
                f"Total mentions: {r['value']}<br>"
                f"Share: {r['percent']:.2f}%"
            )
            if r["type"] == "group"
            else f"<b>{r['label']}</b><br>Group: {r['parent']}",
            axis=1,
        )

        # Treemap
        fig = px.treemap(
            df_circle,
            ids="id",
            names="label",
            parents="parent",
            values="value",
            color="id",
            color_discrete_map=color_map,
            custom_data=["hover_text"],
            title=title or f"Aggregated Topics (min mentions: {min_mentions})",
        )

        # hiding sub groups(could not fix to look better)
        fig.update_traces(
            maxdepth=1,
            root_color="lightgrey",
            hovertemplate="%{customdata[0]}<extra></extra>",
            textinfo="label",  # only group titles
        )

        fig.update_layout(width=1200, height=500)

        if save_path:
            fig.write_html(save_path)

        fig.show()


    #--------------------------------------------------------#
    # Sentiment analysis
    #--------------------------------------------------------#
    def get_captions_for_category(self, category_name):
        '''
        Retrieves a list of captions associated with a given occupation category.
        '''
        if category_name not in self.occupation_categories:
            raise ValueError(f"Category '{category_name}' not found.")
        
        df_category = self.get_category_caption_dataframe()

        caption_indices = df_category.loc[df_category['category'] == category_name, 'caption_index'].unique()

        return [self.documents[idx] for idx in caption_indices]
    

    def compute_sentiment_for_category(self, category_name):
        '''
        Computes sentiment scores for captions in a given occupation category using VADER.
        '''
        if category_name not in self.occupation_categories:
            raise ValueError(f"Category '{category_name}' not found.")
        
        nlp = spacy.load("en_core_web_sm")
        analyser = SentimentIntensityAnalyzer()

        captions = self.get_captions_for_category(category_name)

        if len(captions) == 0:
            raise ValueError(f"No captions found for category '{category_name}'.")
        
        rows = []


        for idx, doc in enumerate(nlp.pipe(captions)):
            for sent in doc.sents:
                sentiment = analyser.polarity_scores(sent.text)
                rows.append({
                    'category': category_name,
                    'caption_index': idx,
                    'sentence': sent.text,
                    'neg': sentiment['neg'],
                    'neu': sentiment['neu'],
                    'pos': sentiment['pos'],
                    'compound': sentiment['compound']
                })

        return pd.DataFrame(rows)
            

    def sentiment_summary_by_category(self, sentiment_df, type_of_sentiment='compound', level = 0.05):
        '''
        Provides a summary of sentiment scores for a given occupation category, need to pass the compound scores dataframe.
        '''
        if sentiment_df.empty:
            raise ValueError("Sentiment dataframe is empty.")

        series = sentiment_df[type_of_sentiment].values

        summary = {
            'category': sentiment_df['category'].iloc[0],
            'num_sentences': len(series),
            'avg_sentiment': np.mean(series),
            'median_sentiment': np.median(series),
            'std_sentiment': np.std(series),
            'pct_positive': float((series >= level).mean()),
            'pct_negative': float((series <= -level).mean()),
            'pct_neutral': float(((series > -level) & (series < level)).mean()),
            'polarity_imbalance': float((series >= level).mean()) - float((series <= -level).mean())
        }
        return summary
    
    def plot_sentiment_distribution_external(self, sentiment_dfs, type_of_sentiment='compound', save_path=None, colors=['mediumseagreen'], plot_method='plotly'):
        '''
        Plots a kde distribution of sentiment scores for multiple occupation categories.
        sentiment_dfs : list of sentiment dataframes for different categories
        '''
        if plot_method == 'plotly':
            fig = go.Figure()
            for i, df in enumerate(sentiment_dfs):
                category = df['category'].iloc[0]
                
                fig.add_histogram(
                x=df[type_of_sentiment],
                histnorm="probability", # density
                nbinsx=100,
                name=category,
                opacity=0.5,
                marker=dict(color=colors[i % len(colors)],line=dict(color="rgba(0,0,0,0.5)", width=1),),)

            fig.update_layout(
                barmode="overlay",
                template="plotly_white",
                height=500,
                xaxis_title="Sentiment Score",
                yaxis_title="Density",
                title=dict(
                    text=f"Sentiment Score Distribution ({type_of_sentiment})",
                    x=0.5,
                    xanchor="center",
                ),
                legend_title_text="Category",
            )

            if save_path:
                fig.write_html(save_path)

            fig.show()

        elif plot_method == 'plt':
            plt.figure(figsize=(10,6))
            for i, sentiment_df in enumerate(sentiment_dfs):
                sns.kdeplot(sentiment_df[type_of_sentiment], fill=True, alpha=0.5, label=sentiment_df['category'].iloc[0], color=colors[i])
            #plt.title(f"Sentiment Score Distribution ({type_of_sentiment}) for Occupation Categories")
            plt.xlabel("Sentiment Score")
            plt.ylabel("Density")
            plt.grid(axis='y', linestyle='--', alpha=0.4)
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.show()

        
    
    # this could have been made easier if sentiments was part of the class, but was done rushed
    def sentiment_kruskal_wallis_test_external(self, sentiment_dfs, interpret = False, alpha = 0.05, type_of_sentiment='compound'):
        '''
        Performs Kruskal-Wallis H-test to determine if there are statistically significant differences
        in sentiment scores across occupation categories.
        sentiment_dfs : list of sentiment dataframes for different categories
        '''

        category_groups = [df[type_of_sentiment].values for df in sentiment_dfs]

        stat, p_value = stats.kruskal(*category_groups)
        if interpret:
            if p_value < alpha:
                print(f"Kruskal-Wallis test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The differences in sentiment scores across categories are statistically significant (alpha = {alpha}).")
            else:
                print(f"Kruskal-Wallis test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The differences in sentiment scores across categories are not statistically significant (alpha = {alpha}).")
        return stat, p_value
    
    # this could have been made easier if sentimentdf1 and sentimentdf2 were part of the class, but for flexibility we keep them as arguments
    def sentiment_cliffs_delta_external(self, sentiment_df1, sentiment_df2, interpret = False, type_of_sentiment='compound'):
        '''
        Computes Cliff's Delta effect size between two occupation categories based on sentiment scores.
        sentiment_df1, sentiment_df2 : sentiment dataframes for the two categories
        '''
        scores_cat1 = sentiment_df1[type_of_sentiment].values
        scores_cat2 = sentiment_df2[type_of_sentiment].values

        if len(scores_cat1) == 0 or len(scores_cat2) == 0:
            raise ValueError("One or both categories have no associated sentiment scores.")
        
        x = np.asarray(scores_cat1)
        y = np.asarray(scores_cat2)

        nx = len(x)
        ny = len(y)
        greater = np.sum(x[:, None] > y)
        lesser = np.sum(x[:, None] < y)
        delta = (greater - lesser) / (nx * ny)
        if interpret:
            
            abs_delta = abs(delta)
            if abs_delta < 0.147:
                size = "negligible"
            elif abs_delta < 0.33:
                size = "small"
            elif abs_delta < 0.474:
                size = "medium"
            else:
                size = "large"
            print(f"Cliff's Delta: {delta:.4f} (effect size: {size})")

        return delta
    
    #again, external keyword means the dataframes are passed as arguments, not part of the class
    def sentiment_mann_whitney_external(self, sentiment_df1, sentiment_df2, interpret = False, alpha = 0.05, alternative = 'two-sided', type_of_sentiment='compound'):
        scores_cat1 = sentiment_df1[type_of_sentiment].values
        scores_cat2 = sentiment_df2[type_of_sentiment].values

        if len(scores_cat1) == 0 or len(scores_cat2) == 0:
            raise ValueError("One or both categories have no associated sentiment scores.")
        
        stat, p_value = stats.mannwhitneyu(scores_cat1, scores_cat2, alternative= alternative)

        if interpret:
            if p_value < alpha:
                print(f"Mann-Whitney U test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The difference in sentiment scores between the two categories is statistically significant (alpha = {alpha}).")
            else:
                print(f"Mann-Whitney U test statistic: {stat:.4f}, p-value: {p_value:.4f}")
                print(f"The difference in sentiment scores between the two categories is not statistically significant (alpha = {alpha}).")
        return stat, p_value

            
        