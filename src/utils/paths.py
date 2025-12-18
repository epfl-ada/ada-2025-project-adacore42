from pathlib import Path

# ------------------------------------------------------------------------------
# Files naming
# ------------------------------------------------------------------------------

DATAPREP_PKL_FILENAME = "data_prepared.pkl"
PLOTSGUI_PKL_FILENAME = "plots_web_app.pkl"
CONSTESTS_JSON_FILENAME = "contests.json"
DATA_PREPARATION_PY_FILENAME = "DataPreparation.py"
DATAPREPNOUNS_PKL_FILENAME = "data_prepared_occ.pkl"
DATAPREPTOKENS_PKL_FILENAME = "cleaned_data_prepared.pkl"
OCCUPATIONS_CSV_FILENAME = "final_combined_occupations.csv"
TFIDF_MATRIX_NPZ_FILENAME = "tf_idf_matrix.npz"
TF_IDF_MATRIX_METADATA_NPZ_FILENAME = "tf_idf_matrix_metadata.npz"
TFIDF_MATRIX_JOBLIB_PATH = "tf_idf_vectorizer.joblib"
OCCUPATIONS_ANALYSIS_PKL_FILENAME = "occupations_analysis.pkl"
OCCUPATIONS_CATEGORY_ANALYSIS_PKL_FILENAME = "occupations_category_analysis.pkl"

# ------------------------------------------------------------------------------
# Paths to initial data folders and files
# ------------------------------------------------------------------------------
STORED_MAIN_DIR_PATH = Path("data") 

# Virgin New Yorker Caption Contest data folder path
VNCC_MAIN_DIR_PATH = STORED_MAIN_DIR_PATH / "newyorker_caption_contest_virgin"
VNCC_DATA_DIR_PATH = VNCC_MAIN_DIR_PATH / "data"
VNCC_IMAGES_DIR_PATH = VNCC_MAIN_DIR_PATH / "images"
VNCC_CONTESTS_JSON_PATH = VNCC_MAIN_DIR_PATH / CONSTESTS_JSON_FILENAME

# ------------------------------------------------------------------------------
# Paths to stored data
# ------------------------------------------------------------------------------

STORED_DATAPREP_PKL_PATH = STORED_MAIN_DIR_PATH / DATAPREP_PKL_FILENAME
STORED_PLOTSGUI_PKL_PATH = STORED_MAIN_DIR_PATH / PLOTSGUI_PKL_FILENAME
STORED_DATAPREPNOUNS_PKL_PATH = STORED_MAIN_DIR_PATH / DATAPREPNOUNS_PKL_FILENAME
STORED_DATAPREPTOKENS_PKL_PATH = STORED_MAIN_DIR_PATH / DATAPREPTOKENS_PKL_FILENAME
OCCUPATIONS_CSV_PATH = STORED_MAIN_DIR_PATH / OCCUPATIONS_CSV_FILENAME
TFIDF_MATRIX_NPZ_PATH = STORED_MAIN_DIR_PATH / TFIDF_MATRIX_NPZ_FILENAME
TF_IDF_MATRIX_METADATA_NPZ_PATH = STORED_MAIN_DIR_PATH / TF_IDF_MATRIX_METADATA_NPZ_FILENAME
TFIDF_MATRIX_JOBLIB_PATH = STORED_MAIN_DIR_PATH / TFIDF_MATRIX_JOBLIB_PATH
OCCUPATIONS_ANALYSIS_PKL_PATH = STORED_MAIN_DIR_PATH / OCCUPATIONS_ANALYSIS_PKL_FILENAME
OCCUPATIONS_CATEGORY_ANALYSIS_PKL_PATH = STORED_MAIN_DIR_PATH / OCCUPATIONS_CATEGORY_ANALYSIS_PKL_FILENAME

# ----------------------------------------------------------------
# Paths to Python scripts
# ----------------------------------------------------------------

SRC_MAIN_DIR_PATH = Path("src")

DATA_DIR_PATH = SRC_MAIN_DIR_PATH / "data"
DATA_PREPARATION_PY_PATH = DATA_DIR_PATH / DATA_PREPARATION_PY_FILENAME