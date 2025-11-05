import re
from typing import List, Set, Dict
import matplotlib.pyplot as plt
import seaborn as sns


class GenderAnalysis:
    """
    A class grouping utility functions for detecting and analyzing gendered language in text.
    """

    def __init__(self):
        # Word lists from Danielle Sucher's "Jailbreak the Patriarchy"
        self.male_terms = [
            'guy', 'spokesman', 'chairman', "men's", 'men', 'him', "he's", 'his', 'boy',
            'boyfriend', 'boyfriends', 'boys', 'brother', 'brothers', 'dad', 'dads',
            'dude', 'father', 'fathers', 'fiance', 'gentleman', 'gentlemen', 'god',
            'grandfather', 'grandpa', 'grandson', 'groom', 'he', 'himself', 'husband',
            'husbands', 'king', 'male', 'man', 'mr', 'nephew', 'nephews', 'priest',
            'prince', 'son', 'sons', 'uncle', 'uncles', 'waiter', 'widower', 'widowers'
        ]

        self.female_terms = [
            'heroine', 'spokeswoman', 'chairwoman', "women's", 'actress', 'women',
            "she's", 'her', 'aunt', 'aunts', 'bride', 'daughter', 'daughters', 'female',
            'fiancee', 'girl', 'girlfriend', 'girlfriends', 'girls', 'goddess',
            'granddaughter', 'grandma', 'grandmother', 'herself', 'ladies', 'lady',
            'mom', 'moms', 'mother', 'mothers', 'mrs', 'ms', 'niece', 'nieces',
            'priestess', 'princess', 'queens', 'she', 'sister', 'sisters', 'waitress',
            'widow', 'widows', 'wife', 'wives', 'woman'
        ]

        # Basic list of common English stopwords (can be expanded) [from Andras]
        # These are basic words that are used in a lot of sentences, I don't want to see them on my word clouds

        self.STOPWORDS = {
        # --- pronouns and determiners ---
        "i","me","my","myself","we","our","ours","ourselves","you","your","yours",
        "yourself","yourselves","he","him","his","himself","she","her","hers","herself",
        "it","its","itself","they","them","their","theirs","themselves","us",
        "what","which","who","whom","this","that","these","those",
        
        # --- auxiliary verbs & modals ---
        "am","is","are","was","were","be","been","being","have","has","had","having",
        "do","does","did","doing","can","could","will","would","shall","should","may",
        "might","must","ought",
        
        # --- articles, prepositions, conjunctions ---
        "a","an","the","and","but","if","or","because","as","until","while","of","at",
        "by","for","with","about","against","between","into","through","during","before",
        "after","above","below","to","from","up","down","in","out","on","off","over",
        "under","again","further","then","once","here","there","when","where","why",
        "how","all","any","both","each","few","more","most","other","some","such","no",
        "nor","not","only","own","same","so","than","too","very","s","t","now","just",
        
        # --- contractions & spoken forms ---
        "im","ive","id","youre","youve","youd","hes","shes","theyre","theyve","weve",
        "wed","dont","doesnt","didnt","cant","couldnt","wont","wouldnt","shouldnt",
        "isnt","arent","wasnt","werent","thats","theres","whats","whos","hows","lets",
        "re","don","ill","ll","d","ve","y","ma",
        
        # --- generic filler verbs & expressions ---
        "get","got","getting","go","goes","going","gone","see","saw","seen","say",
        "says","said","make","makes","made","know","knows","knew","think","thinks",
        "thought","need","needs","needed","want","wants","wanted","like","likes",
        "liked","use","used","using","try","trying","tried","work","works","worked",
        "take","takes","took","put","puts","doing","done","give","gives","gave",
        
        # --- discourse fillers ---
        "well","really","one","even","still","lot","thats","thing","things","way",
        "something","anything","everything","nothing","time","back","new","also",
        "ever","always","maybe"
        }

    # ---------------------------
    # PART 0 – GENDER DETECTION
    # ---------------------------

    def remove_nan(dataC):

        dataC0 = dataC.copy(deep=True)

        # find the where the NaN's are in the metadata
        no_NaN = dataC0[dataC0['image_descriptions'].notna()].index

        # Let's remove them
        dataC.dropna(subset=['image_descriptions'], inplace=True)        

        return no_NaN, dataC0

    def get_metadata(self, dataC):
        """
        Preps the metadata to be utilized in the analysis
        """

        dataC0 = dataC.copy(deep = True)

        # put it in lower case
        dataC0["image_descriptions"] = dataC0["image_descriptions"].apply(
            lambda x: [s.lower() for s in x] if isinstance(x, list) else str(x).lower()
        )
        # remove the []
        dataC0["image_descriptions"] = dataC0["image_descriptions"].apply(
            lambda x: " ".join(x) if isinstance(x, list) else str(x)
        )
        dataC0['gender_mention'] = dataC0['image_descriptions'].apply(self.detect_gender)

        return dataC0
    
    def get_Top10_captions(self, dataA, no_NaN):
        
        dataTop10 = []
        count = []

        # !! Since we don't have the metadata for some contest we need to use specfic .csv

        for idx in no_NaN:

            contest = dataA[idx]

            # Keep only the top 10
            df_top10 = contest[contest.index < 10].copy(deep = True)

            # put it in lower case
            df_top10["caption"] = df_top10["caption"].apply(
                lambda x: [s.lower() for s in x] if isinstance(x, list) else str(x).lower()
            )

            # for each of them apply the function to detect gender
            df_top10['gender_mention'] = df_top10['caption'].apply(self.detect_gender)

            dataTop10.append(df_top10)

            # Count mentions per contest
            gender_counts = (
                df_top10["gender_mention"]
                .value_counts()
                #.unstack(fill_value=0)
                .reset_index()
            )

            count.append(gender_counts)

        return count, dataTop10

    def detect_gender(self, text: str) -> str:
        """
        Detects whether a text mentions male, female, both, or neutral terms.
        Returns one of: "male", "female", "both", or "neutral".
        """

        male = any(re.search(rf"\b{word}\b", text, re.IGNORECASE) for word in self.male_terms)
        female = any(re.search(rf"\b{word}\b", text, re.IGNORECASE) for word in self.female_terms)

        if male and female:
            return "both"
        elif male:
            return "male"
        elif female:
            return "female"
        else:
            return "neutral"

    # ---------------------------
    # PART 1 – ANALYSIS HELPERS
    # ---------------------------

    @staticmethod
    def gender_the_sentence(sentence_words: Set[str],
                            male_words: Set[str],
                            female_words: Set[str]) -> str:
        """
        Returns the gender associated with a sentence based on overlap with gendered word lists.
        """

        mw_length = len(male_words.intersection(sentence_words))
        fw_length = len(female_words.intersection(sentence_words))

        if mw_length > 0 and fw_length == 0:
            return 'male'
        elif mw_length == 0 and fw_length > 0:
            return 'female'
        elif mw_length > 0 and fw_length > 0:
            return 'both'
        else:
            return 'none'

    @staticmethod
    def is_it_proper(word: str, proper_nouns: Dict[str, Dict[str, int]]) -> None:
        """
        Identifies proper nouns (capitalized words) and counts their occurrences
        in a dictionary structured as:
        {word_lower: {'upper': count, 'lower': count}}
        """

        case = 'upper' if word[0].isupper() else 'lower'
        word_lower = word.lower()

        if word_lower not in proper_nouns:
            proper_nouns[word_lower] = {case: 1}
        else:
            proper_nouns[word_lower][case] = proper_nouns[word_lower].get(case, 0) + 1

    @staticmethod
    def increment_gender(sentence_words: List[str],
                         gender: str,
                         sentence_counter: Dict[str, int],
                         word_counter: Dict[str, int],
                         word_freq: Dict[str, Dict[str, int]]) -> None:
        """
        Updates counters for sentences, words, and word frequencies by gender.
        """

        sentence_counter[gender] = sentence_counter.get(gender, 0) + 1
        word_counter[gender] = word_counter.get(gender, 0) + len(sentence_words)

        if gender not in word_freq:
            word_freq[gender] = {}

        for word in sentence_words:
            word_freq[gender][word] = word_freq[gender].get(word, 0) + 1

    def analyse_text(self, 
                     data, 
                     tokenizer, 
                     punctuation, 
                     sentence_counter, 
                     word_counter, 
                     word_freq, 
                     proper_nouns, 
                     C: bool = False) -> None:
        """
        Analyzes text data in a pandas DataFrame to detect gendered terms and 
        update sentence and word frequency counters.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame containing text columns ('caption' or 'image_descriptions').
        tokenizer : object
            A sentence tokenizer (e.g. nltk.data.load('tokenizers/punkt/english.pickle')).
        punctuation : str
            String of punctuation characters to strip (e.g. string.punctuation).
        sentence_counter : dict
            Dictionary tracking the number of sentences per gender.
        word_counter : dict
            Dictionary tracking the number of words per gender.
        word_freq : dict
            Dictionary tracking frequency of words per gender.
        proper_nouns : dict
            Dictionary tracking proper noun capitalization patterns.
        C : bool, optional
            If True, analyze 'image_descriptions'; otherwise, analyze 'caption'.
        """

        column = 'image_descriptions' if C else 'caption'
        list_text = data[column].values

        for idx in range(data.shape[0]):
            text = list_text[idx]

            # Split into sentences
            sentences = tokenizer.tokenize(text)

            for sentence in sentences:
                # Word tokenize and strip punctuation
                sentence_words = sentence.split()
                sentence_words = [
                    w.strip(punctuation) for w in sentence_words 
                    if len(w.strip(punctuation)) > 0
                ]

                # Track capitalization for proper nouns
                for word in sentence_words[1:]:
                    self.is_it_proper(word, proper_nouns)

                # Lowercase and deduplicate words
                sentence_words = set(w.lower() for w in sentence_words)

                # Determine gender of the sentence
                gender = self.gender_the_sentence(
                    sentence_words, 
                    set(self.male_terms), 
                    set(self.female_terms)
                )

                # Increment counters
                self.increment_gender(sentence_words, gender, sentence_counter, word_counter, word_freq)


    # ---------------------------
    # VISUALIZATION
    # ---------------------------

    @staticmethod
    def plot_overall_counts(
        overall_counts,
        title: str = "Overall Presence of Gender Mentions",
        xlabel: str = "Gender Mention Category",
        ylabel: str = "Number of Captions",
        colors: str = "skyblue",
        edgecolor: str = "black",
        neutral: bool = True
    ):
        """
        Plots a bar chart showing the overall presence of gender mentions.

        Parameters
        ----------
        overall_counts : pd.DataFrame or pd.Series
            Must contain columns or index for ['male', 'female', 'both'].
        title : str, optional
            Plot title.
        xlabel : str, optional
            X-axis label.
        ylabel : str, optional
            Y-axis label.
        colors : str or list, optional
            Color(s) for bars.
        edgecolor : str, optional
            Edge color for bars.
        """
        if neutral:
            plt.figure(figsize=(6, 4))
            overall_counts[["male", "female", "both", "neutral"]].plot(
                kind='bar', color=colors, edgecolor=edgecolor
            )
        else: 
            plt.figure(figsize=(6, 4))
            overall_counts[["male", "female", "both"]].plot(
                kind='bar', color=colors, edgecolor=edgecolor
            )

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_cumulative_mentions(
        cumulative,
        title: str = "Cumulative Gender Mentions per Contest",
        xlabel: str = "Contest Index (chronological)",
        ylabel: str = "Cumulative Count",
        legend_title: str = "Gender Mention",
        neutral: bool = True
    ):
        """
        Plots the cumulative count of gender mentions across contests.

        Parameters
        ----------
        cumulative : pd.DataFrame
            A dataframe where each column corresponds to a gender category,
            and the index represents contest order.
        title : str, optional
            Plot title.
        xlabel : str, optional
            X-axis label.
        ylabel : str, optional
            Y-axis label.
        legend_title : str, optional
            Title for the legend.
        """
        plt.figure(figsize=(10, 6))

        if neutral:
            for col in cumulative.columns:
                plt.plot(cumulative.index, cumulative[col], label=col, linewidth=2)
        else: 
            for col in cumulative.columns[:-1]:
                plt.plot(cumulative.index, cumulative[col], label=col, linewidth=2)
                
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(title=legend_title)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_gender_cooccurrence(
        cross,
        title: str = "Gender Co-occurrence: Image vs Caption",
        xlabel: str = "Caption Gender",
        ylabel: str = "Image Gender",
        cmap: str = "Blues"
    ):
        """
        Plots a heatmap of gender co-occurrence between image and caption.

        Parameters
        ----------
        cross : pd.DataFrame
            Cross-tabulation of gender categories for image vs caption.
        title : str, optional
            Plot title.
        xlabel : str, optional
            X-axis label.
        ylabel : str, optional
            Y-axis label.
        cmap : str, optional
            Color map for heatmap.
        """
        plt.figure(figsize=(6, 5))
        sns.heatmap(cross, annot=True, fmt="d", cmap=cmap, cbar=False)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_wordclouds(male_cloud, female_cloud):
        """
        Displays male and female word clouds side by side.

        Parameters
        ----------
        male_cloud : wordcloud.WordCloud
            Word cloud object for male-dominant words.
        female_cloud : wordcloud.WordCloud
            Word cloud object for female-dominant words.
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 7))

        axes[0].imshow(male_cloud, interpolation='bilinear')
        axes[0].set_title('Male-dominant words', fontsize=16)
        axes[0].axis('off')

        axes[1].imshow(female_cloud, interpolation='bilinear')
        axes[1].set_title('Female-dominant words', fontsize=16)
        axes[1].axis('off')

        plt.tight_layout()
        plt.show()

