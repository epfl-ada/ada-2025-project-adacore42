# Create a TF-IDF matrix from the cleaned captions
import time
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.stats import ttest_ind
import pandas as pd
def extract_documents(dataA, text_column='cleaned_caption', metric='funny_score_scaled'):
    '''
    Extracts the corpus (cleaned captions) and corresponding funniness scores.
    '''

    if not isinstance(dataA, list):
        dataA = [dataA]

    documents = []
    targets = []
    contest_ids = []

    for contest_id, df in enumerate(dataA):
        texts = df[text_column]
        scores = df[metric]

        for text, score in zip(texts, scores):
            if isinstance(text, str):  # Ensure text is a string
                documents.append(text)
                targets.append(score)
                contest_ids.append(contest_id)
                
    return documents, targets, contest_ids

def create_tf_idf_matrix(documents, ngram_range = (1,2), print_time = False, **kwargs):
    '''
    This will create a TF-IDF matrix from whatever column is specified, using the specified n-gram range.
    '''
    start_time = time.time() # tracking execution time

    vectorizer = TfidfVectorizer(ngram_range=ngram_range, **kwargs)

    tf_idf_matrix = vectorizer.fit_transform(documents)
    end_time = time.time()

    if print_time:
        print(f"TF-IDF matrix created in {end_time - start_time:.2f} seconds.")
        print(f"Matrix shape: {tf_idf_matrix.shape}")
    return tf_idf_matrix, vectorizer

def extract_terms_counts(tf_idf_matrix, feature_names, terms):
    '''
    Extracts the counts of specified terms from the TF-IDF matrix.
    '''
    terms_lower = [term.lower() for term in terms]

    term_indices = np.where(np.isin(feature_names, terms_lower))[0]

    #Sum TF-IDF across documents for each term
    term_counts = tf_idf_matrix[:, term_indices].sum(axis=0)  # still sparse
    term_counts = np.array(term_counts).flatten()  # small, safe array

    return term_counts, term_indices



    
