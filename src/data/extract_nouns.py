import spacy
import pickle
import os
nlp = spacy.load('en_core_web_sm')

def load_data(filepath ='../../data/cleaned_data_prepared.pkl'):
    if os.path.exists(filepath) == False:
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, "rb") as f:
        data = pickle.load(f)
    return data["dataA"], data["dataC"], data["dataA_startID"], data["dataA_endID"], data["dataC_lastGoodID"]

def extract_nouns(text):
    # Ensure the input is a string, not a list
    if not isinstance(text, str):
        text = " ".join(text)
    doc = nlp(text.lower())
    return [token.text for token in doc if token.pos_ in ("NOUN", "PROPN")]

def apply_noun_extraction(dataA):
    #create copy of dataA to store noun-extracted captions
    dataA_cleaned0 = dataA.copy()
    for i, df in enumerate(dataA_cleaned0):
        df['captions_nouns'] = df['cleaned_caption'].apply(extract_nouns)
        dataA_cleaned0[i] = df
        print(f"Extracting nouns .......... {(i+1)/len(dataA_cleaned0):.2%} complete.")
    return dataA_cleaned0

# saving into pickle file
def save_noun_data(dataA_cleaned0, dataC_cleaned0, dataA_startID, dataA_endID, dataC_lastGoodID, filepath='../../data/cleaned_data_nouns_copy.pkl'):
    with open(filepath, "wb") as f:
        pickle.dump({
            "dataA_nouns": dataA_cleaned0,
            "dataC_nouns": dataC_cleaned0,
            "dataA_startID": dataA_startID,
            "dataA_endID": dataA_endID,
            "dataC_lastGoodID": dataC_lastGoodID
        }, f)
    print("Noun-extracted data saved successfully.")

if __name__ == "__main__":
    dataA, dataC, dataA_startID, dataA_endID, dataC_lastGoodID = load_data(filepath='../../data/cleaned_data_prepared.pkl')
    dataA_cleaned0 = apply_noun_extraction(dataA)
    dataC_cleaned0 = dataC  # Assuming no changes to dataC
    save_noun_data(dataA_cleaned0, dataC_cleaned0, dataA_startID, dataA_endID, dataC_lastGoodID, filepath='../../data/cleaned_data_nouns_copy.pkl')