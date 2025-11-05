import spacy

nlp = spacy.load('en_core_web_sm')


def extract_nouns(text):
    # Ensure the input is a string, not a list
    if not isinstance(text, str):
        text = " ".join(text)
    doc = nlp(text.lower())
    return [token.text for token in doc if token.pos_ in ("NOUN", "PROPN")]