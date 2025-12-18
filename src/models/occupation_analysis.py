#It must be disclosed that this code was generated with the assistance of AI tools.
#The AI used was: ChatGPT-5 by OpenAI and GitHub Copilot.

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
        ],
        "Miscellaneous": []
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

        occupation_analysis_df = pd.DataFrame({
            "term": occupations,
            "category": [
                self.occupation_to_category.get(occ, "Miscellaneous")
                for occ in occupations
            ],
            "term_count": [occupation_term_counts[occ] for occ in occupations],
            "avg_funniness": [
                np.mean(occupation_funniness[occ]) if occupation_funniness[occ] else 0.0
                for occ in occupations
            ],
            "median_funniness": [
                np.median(occupation_funniness[occ]) if occupation_funniness[occ] else 0.0
                for occ in occupations
            ],
            "std_funniness": [
                np.std(occupation_funniness[occ]) if occupation_funniness[occ] else 0.0
                for occ in occupations
            ],
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
    #Plotting functions in html format for initial exploration
    #--------------------------------------------------------#

    #plotting top occupations by count
    def plot_top_occupations_by_count(self, start = 0, end = 20, save_path=None):
        """
        Plots the top N occupation terms by frequency count.
        """
        df_plot = self._occupation_df.sort_values(by='term_count', ascending=False).iloc[start:end].copy()
        hover_data = {
            'num_contests': True,
            'std_funniness': ':.2f',
            'avg_funniness': ':.2f',
            'num_contests': True,
            'term': False
        }
        fig = px.bar(df_plot, x = 'term', y='term_count', hover_data = hover_data,
                     title=f'Top Occupation Terms by Frequency Count (Ranks {start+1} to {end})')
        
        fig.update_traces(marker = dict(color = df_plot['avg_funniness'], colorscale = 'Viridis', line = dict(color = "rgba(0,0,0,0.7)"), width = 1))
        fig.update_layout(xaxis_title='Occupation Term', yaxis_title='Frequency Count', template = 'plotly_white', xaxis_tickangle = -45, height = 600, hovermode = 'closest', showlegend = False, title = dict(x = 0.5, xanchor = 'center', text = f"Top Occupations by Frequency Count (Ranks {start+1} to {end})<br><sub>Hover to see number of contests and funniness stats</sub>"))
        if save_path:
            fig.write_html(save_path)
        fig.show()

    # plotting with dropdown menu
    def plot_occupation_dropdown(occupation_df, page_size=10, save_path=None):
        """
        Plots an interactive dropdown to explore occupation statistics.
        """
        occupation_df_sorted = occupation_df.sort_values(by='term_count', ascending=False).reset_index(drop=True)
        
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
                marker=dict(color=df_page["term_count"], colorscale = 'Greens'),
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
    def plot_top_occupations_by_funniness(self, top_n=20, save_path=None, measure='avg', ascending=False):
        """
        Plots the top N occupation terms by average funniness score.
        """
        df_plot = self._occupation_df.sort_values(by=f'{measure}_funniness', ascending=ascending).head(top_n).copy()
        hover_data = {
            'count': True,
            'std_funniness': ':.2f',
            'avg_funniness': ':.2f',
            'median_funniness': ':.2f',
            'term': False
        }

        fig = px.bar(df_plot, x = 'term', y='avg_funniness', hover_data = hover_data,
                     title=f'Top {top_n} Occupation Terms by Average Funniness Score')
        
        fig.update_traces(marker = dict(color = df_plot['term_count'], colorscale = 'Blues', line = dict(color = "rgba(0,0,0,0.7)"), width = 1))
        fig.update_layout(xaxis_title='Occupation Term', yaxis_title='Average Funniness Score', template = 'plotly_white', xaxis_tickangle = -45, height = 600, hovermode = 'closest', showlegend = False, title = dict(x = 0.5, xanchor = 'center', text = f"Top {top_n} Occupations by Average Funniness<br><sub>Hover to see frequency and score variability</sub>"))
        if save_path:
            fig.write_html(save_path)
        fig.show()

    #plotting the distribution of a chosen occupation term
    def plot_occupation_distribution(self, occupation_term, nbins = 30, save_path=None):
        """
        Plots the distribution of funniness scores for a given occupation term.
        """
        canonical_term = self.syn_to_occ.get(occupation_term.lower())

        rows = []

        for idx, doc in enumerate(self.documents):
            doc_lower = doc.lower()
            score = self.scores[idx]

            for syn, occ in self.syn_to_occ.items():
                if syn == occupation_term.lower() and syn in doc_lower:
                    rows.append(score)
        if not rows:
            print(f"No occurrences found for occupation term: {occupation_term}")
            return

        df_plot = pd.DataFrame({'funniness_score': rows})

        fig = px.histogram(df_plot, x='funniness_score', nbins=nbins, marginal = "box",
                         title=f'Distribution of Funniness Scores for "{canonical_term}"',
                         hover_data = {'funniness_score': ':.2f'})
        
        fig.update_layout(xaxis_title='Funniness Score', yaxis_title='Count', template = 'plotly_white', height = 500, hovermode = 'closest', title = dict(x = 0.5, xanchor = 'center', text = f'Distribution of Funniness Scores for "{canonical_term}"'))
        if save_path:
            fig.write_html(save_path)
        fig.show()

    def plot_occupation_box_plot(self, occupation_terms, save_path = None):
        """
        Plotting the box plot of the funniness score of multiple occupations on the same plot close to each other. 
        """
        rows = []

        occupation_terms = [occ.lower() for occ in occupation_terms]

        for idx, doc in enumerate(self.documents):
            doc_lower = doc.lower()
            score = self.scores[idx]
            matched_occupations = set()

            for syn, occ in self.syn_to_occ.items():
                if syn in doc_lower and occ in occupation_terms:
                    matched_occupations.add(occ)
            
            for occ in matched_occupations:
                rows.append({
                    'occupation': occ,
                    'funniness_score': score
                })
        if not rows:
            print(f"No occurrences found for occupation terms: {occupation_terms}")
            return
        
        df_plot = pd.DataFrame(rows)
        fig = px.box(df_plot,x="occupation",y="funniness_score",points="outliers", title="Funniness score distribution by occupation")

        fig.update_layout(xaxis_title="Occupation", yaxis_title="Funniness score", template="plotly_white", height=600, xaxis_tickangle=-45, hovermode="closest", title=dict(x=0.5, xanchor="center"))

        if save_path:
            fig.write_html(save_path)

        fig.show()




    #--------------------------------------------------------#
    # Tests to compare specific occupations
    #--------------------------------------------------------#
    def compare_set_of_occupations(self, occupation_list, interpret = False, alpha = 0.05):
        '''
        Compares funniness score distributions among a set of occupation terms using Kruskal-Wallis H-test.
        '''
        if self.syn_to_occ is None:
            raise ValueError("Occupation mapping not provided.")
        
        occupation_groups = {occ: [] for occ in occupation_list}

        for idx, doc in enumerate(self.documents):
            doc_lower = doc.lower()
            score = self.scores[idx]

            for syn, occ in self.syn_to_occ.items():
                if occ in occupation_groups and syn in doc_lower:
                    occupation_groups[occ].append(score)
        
        # Remove empty groups
        occupation_groups = {occ: scores for occ, scores in occupation_groups.items() if scores}

        if len(occupation_groups) < 2:
            raise ValueError("At least two occupation terms must have associated funniness scores for comparison.")
        
        stat, p_value = stats.kruskal(*occupation_groups.values())

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
        if self.syn_to_occ is None:
            raise ValueError("Occupation mapping not provided.")
        
        rows_occ1 = []
        rows_occ2 = []

        for idx, doc in enumerate(self.documents):
            doc_lower = doc.lower()
            score = self.scores[idx]

            has_occ1 = False
            has_occ2 = False

            for syn, occ in self.syn_to_occ.items():
                if syn in doc_lower:
                    if occ == occupation1:
                        has_occ1 = True
                    elif occ == occupation2:
                        has_occ2 = True

            # keep only captions that mention exactly one occupation
            if has_occ1 and not has_occ2:
                rows_occ1.append(score)
            elif has_occ2 and not has_occ1:
                rows_occ2.append(score)

        
        if len(rows_occ1) == 0 or len(rows_occ2) == 0:
            raise ValueError("One or both occupation terms have no associated funniness scores.")
        
        stat, p_value = stats.mannwhitneyu(rows_occ1, rows_occ2, alternative= alternative)

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
        if self.syn_to_occ is None:
            raise ValueError("Occupation mapping not provided.")
        
        rows_occ1 = []
        rows_occ2 = []

        for idx, doc in enumerate(self.documents):
            doc_lower = doc.lower()
            score = self.scores[idx]

            has_occ1 = False
            has_occ2 = False

            for syn, occ in self.syn_to_occ.items():
                if syn in doc_lower:
                    if occ == occupation1:
                        has_occ1 = True
                    elif occ == occupation2:
                        has_occ2 = True

            # keep only captions that mention exactly one occupation
            if has_occ1 and not has_occ2:
                rows_occ1.append(score)
            elif has_occ2 and not has_occ1:
                rows_occ2.append(score)
        
        if len(rows_occ1) == 0 or len(rows_occ2) == 0:
            raise ValueError("One or both occupation terms have no associated funniness scores.")
        
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

    #--------------------------------------------------------#
    # Categorical analysis functions
    #--------------------------------------------------------#
    
    #plotting boxplot for category-level funniness scores
    def plot_category_boxplot(self, order_by="median", save_path=None):
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
        if save_path:
            fig.write_html(save_path)

        fig.show()

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
    #--------------------------------------------------------#
    # Temporal analyses functions
    #--------------------------------------------------------#
    def temporal_counting(self, occupations):
        '''
        Aggregate temporal counting for a list of occupations/
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

    def plot_temporal_trends(self, occupations, title = None, cumulative = False, save_path=None):
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
        
        fig = px.line(x = list(y.keys()), y = list(y.values()), markers = True, labels = {'x':'Contest ID', 'y':'Cumulative Count' if cumulative else 'Count'},
                      title = title or f'Temporal Trend for Occupations: {", ".join(occupations)}')
        
        fig.update_layout(template = 'plotly_white', height = 500, hovermode = 'closest', title = dict(x = 0.5, xanchor = 'center', text = title or f'Temporal Trend for Occupations: {", ".join(occupations)}'))

        if save_path:
            fig.write_html(save_path)
        fig.show()


    def plot_group_temporal_trends(self, group_dict, cumulative = False, min_total = 5, save_path=None):
        '''
        Plots temporal trends for multiple occupation groups.
        group_dict : dict mapping group names to lists of occupations
        '''

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
                          title = dict(x = 0.5, xanchor = 'center', text = 'Temporal Trends for Occupation Groups'),
                          xaxis_title = 'Contest ID',
                          yaxis_title = 'Cumulative Count' if cumulative else 'Count')

        if save_path:
            fig.write_html(save_path)
        fig.show() 


    #--------------------------------------------------------#
    # Topic modelling
    #--------------------------------------------------------#
    def topic_model_category(self, category_name, min_topics = 15, ngram_size = (1,2), min_tokens = 2, model_name = "all-MiniLM-L6-v2", random_state = 42):
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
            random_state = random_state,
            verbose = True
        )

        topics, probs = topic_model.fit_transform(captions, embeddings)

        output = df_category.reset_index(drop=True).copy()
        output['topic'] = topics
        output['topic_probability'] = probs
        return topic_model, output


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
    
    # this could have been made easier if sentiments was part of the class, but was done rushed
    def sentiment_kruskal_wallis_test_external(self, sentiment_dfs, interpret = False, alpha = 0.05):
        '''
        Performs Kruskal-Wallis H-test to determine if there are statistically significant differences
        in sentiment scores across occupation categories.
        sentiment_dfs : list of sentiment dataframes for different categories
        '''

        category_groups = [df['compound'].values for df in sentiment_dfs]

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
    def sentiment_cliffs_delta_external(self, sentiment_df1, sentiment_df2, interpret = False):
        '''
        Computes Cliff's Delta effect size between two occupation categories based on sentiment scores.
        sentiment_df1, sentiment_df2 : sentiment dataframes for the two categories
        '''
        scores_cat1 = sentiment_df1['compound'].values
        scores_cat2 = sentiment_df2['compound'].values

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
    def sentiment_mann_whitney_external(self, sentiment_df1, sentiment_df2, interpret = False, alpha = 0.05, alternative = 'two-sided'):
        scores_cat1 = sentiment_df1['compound'].values
        scores_cat2 = sentiment_df2['compound'].values

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

            
        