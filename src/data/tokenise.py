#Loading packages (hopefully installed, all is correct version and whatnot)

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import spacy
import textblob as TextBlob
import contractions
import string
import os
import pickle


nltk.download('punkt')       # Tokeniser
nltk.download('stopwords')   # Stopwords list
nltk.download('wordnet')     # Lemmatiser
nlp = spacy.load('en_core_web_sm')

stop_words = set(stopwords.words('english')) # Initialise stopwords
lemmatizer = WordNetLemmatizer() # Initialise lemmatiser

def load_data(filepath = '../../data/data_prepared.pkl'):
    if os.path.exists(filepath) == False:
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, "rb") as f:
        data = pickle.load(f)
    return data["dataA"], data["dataC"], data["dataA_startID"], data["dataA_endID"], data["dataC_lastGoodID"]


def preprocess_text_list(entry, min_len=2):
    """
    Preprocess text by:
    - Lowercasing
    - Removing punctuation
    - Expanding contractions
    - Optional typo correction
    - Removing stopwords
    - Removing short tokens
    - Lemmatisation
    """

    if isinstance(entry, list):
        text = " ".join(entry)
    elif isinstance(entry, str):
        text = entry
    else:
        return ""

    # Lowercase
    text = text.lower()

    # Expand contractions
    text = contractions.fix(text)

    # Typo correction
    text = str(TextBlob(text).correct())

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenise
    tokens = word_tokenize(text)

    # Remove stopwords and short tokens
    tokens = [word for word in tokens if word not in stop_words and len(word) >= min_len]

    # Lemmatise
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return ' '.join(tokens)


# apply preprocessing to captions in dataA
def apply_preprocessing(dataA, dataC):
    size = len(dataA)
    
    #create copy of dataA to store cleaned captions
    dataA1, dataC1 = dataA.copy(), dataC.copy()

    for i, df in enumerate(dataA1):
        df['cleaned_caption'] = df['caption'].apply(preprocess_text_list)
        print(f"done with {(i+1)/size*100:.2f}%")
    
    # apply preprocessing to image_locations, questions, image_uncanny_descriptions, image_descriptions
    dataC1['cleaned_image_locations'] = dataC1['image_locations'].apply(preprocess_text_list)
    print("done with image_locations")
    dataC1['cleaned_questions'] = dataC1['questions'].apply(preprocess_text_list)
    print("done with questions")
    dataC1['cleaned_image_uncanny_descriptions'] = dataC1['image_uncanny_descriptions'].apply(preprocess_text_list)
    print("done with image_uncanny_descriptions")
    dataC1['cleaned_image_descriptions'] = dataC1['image_descriptions'].apply(preprocess_text_list)
    print("done with image_descriptions")
    return dataA1, dataC1

def save_data(dataA, dataC, dataA_startID, dataA_endID, dataC_lastGoodID, filepath='../../data/cleaned_data_prepared_copy.pkl'):
    with open(filepath, "wb") as f:
        pickle.dump({
            "dataA_startID": dataA_startID,
            "dataA_endID": dataA_endID,
            "dataC_lastGoodID": dataC_lastGoodID,
            "dataA": dataA,
            "dataC": dataC
        }, f)
    print(f"Cleaned data saved to {filepath}")

#if __name__ == "__main__":
#    dataA, dataC, dataA_startID, dataA_endID, dataC_lastGoodID = load_data(filepath='../../data/data_prepared.pkl') # Load data
#    dataA1, dataC1 = apply_preprocessing(dataA, dataC) # Tokenise and clean data
#    save_data(dataA1, dataC1, dataA_startID, dataA_endID, dataC_lastGoodID, filepath='../../data/cleaned_data_prepared_copy.pkl')