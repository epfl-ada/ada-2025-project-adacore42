from pathlib import Path

# ------------------------------------------------------------------------------
# Paths to initial data folders and files
# ------------------------------------------------------------------------------

# Virgin New Yorker Caption Contest data folder path
VNCC_MAIN_DIR_PATH = Path("data") / "newyorker_caption_contest_virgin"
VNCC_DATA_DIR_PATH = VNCC_MAIN_DIR_PATH / "data"
VNCC_IMAGES_DIR_PATH = VNCC_MAIN_DIR_PATH / "images"
VNCC_CONTESTS_JSON_PATH = VNCC_MAIN_DIR_PATH / "contests.json"

# ------------------------------------------------------------------------------
# Paths to stored data
# ------------------------------------------------------------------------------
DATAPREP_PKL_FILENAME = "dataPrepared.pkl"
PLOTSGUI_PKL_FILENAME = "plots_gui.pkl"



STORED_MAIN_DIR_PATH = Path("src") / "data"
STORED_DATAPREP_PKL_PATH = STORED_MAIN_DIR_PATH / DATAPREP_PKL_FILENAME
STORED_PLOTSGUI_PKL_PATH = STORED_MAIN_DIR_PATH / PLOTSGUI_PKL_FILENAME

