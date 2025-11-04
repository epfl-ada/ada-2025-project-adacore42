#Loading packages (hopefully installed, all is correct version and whatnot)

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import spacy
import textblob as TextBlob
import contractions
import string


nltk.download('punkt')       # Tokeniser
nltk.download('stopwords')   # Stopwords list
nltk.download('wordnet')     # Lemmatiser
nlp = spacy.load('en_core_web_sm')

stop_words = set(stopwords.words('english')) # Initialise stopwords
lemmatizer = WordNetLemmatizer() # Initialise lemmatiser

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