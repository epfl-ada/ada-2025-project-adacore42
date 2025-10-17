import pickle
import os
import pandas as pd

# Saving and loading data utilies
##################


def save_object_pickle(obj, path):
    """
    Sauvegarde un objet Python (DataFrame, Series, liste, float, dict, etc.)
    dans un fichier .pkl.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if isinstance(obj, (pd.DataFrame, pd.Series)):
        obj.to_pickle(path)
    else:
        with open(path, "wb") as f:
            pickle.dump(obj, f)


def load_object_pickle(path):
    """
    Charge un objet Python depuis un fichier .pkl.
    Si c'est un DataFrame/Series, pandas le lira correctement.
    Sinon pickle sera utilisé.
    """
    try:
        return pd.read_pickle(path)  # fonctionne pour DataFrame/Series
    except Exception:
        with open(path, "rb") as f:
            return pickle.load(f)