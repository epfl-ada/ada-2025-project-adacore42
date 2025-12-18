import ast
import pandas as pd
def load_occupation_mapping(csv_path):
    """
    Load occupation synonyms and return a mapping from synonym to occupation.
    """
    df = pd.read_csv(csv_path)

    df["Synonyms"] = df["Synonyms"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    syn_to_occ = {
        synonym.lower(): occ
        for occ, synonyms in zip(df["Occupation"], df["Synonyms"])
        for synonym in synonyms
    }

    return syn_to_occ