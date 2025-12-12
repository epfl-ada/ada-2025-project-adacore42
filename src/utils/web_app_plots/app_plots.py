import pickle
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import plotly.graph_objects as go
import numpy as np
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Default plot class adapted for GUI
# This file defines a generic plot interface used by graphical components
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

#Plots Web App (basicly same as in plots_gui.py, but only necessary)
class PWA(ABC):


    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # Default plot class adapted for GUI
    # Handles loading data, defining figure logic, and saving plot states to disk
    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    root = None
    filePath = None#root / STORED_PLOTSGUI_PKL_PATH              # Path – location of stored GUI plots (.pkl)
    data_path = None#root / STORED_DATAPREP_PKL_PATH              # Path – location of pre-processed data (.pkl)

    # ---------------------------------------------------------------------------------------------
    # Class constructor – initializes title, labels, and data reference
    # ---------------------------------------------------------------------------------------------
    def __init__(self, 
                 title: str = "No Title", 
                 description: str = "No Description", 
                 X_label: str = "X-axis", 
                 Y_label: str = "Y-axis", 
                 X_data = None, 
                 Y_data = None, 
                 plotParams = None):
        
        self.title = title                     # Title – plot title text
        self.description = description         # Description – optional long text
        
        self.X_label = X_label                   # X-axis label
        self.Y_label = Y_label                   # Y-axis label
        
        self.X_data = np.array(X_data)
        self.Y_data = np.array(Y_data)
        
        self.plotParams = plotParams         # Plot parameters – dictionary for custom settings

        self.set_root_path()
    
    @classmethod
    def set_root_path(cls):
        import sys
        from pathlib import Path

        root = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
        
        while root.parent != root:
            if ((root / ".git").exists() and 
                (root / "README.md").exists() and 
                (root / "results.ipynb").exists()):
                break
            root = root.parent

        if str(root) not in sys.path:
            sys.path.insert(0, str(root))

        # Import project-level paths AFTER sys.path modification
        from src.utils.paths import STORED_DATAPREP_PKL_PATH, STORED_PLOTSGUI_PKL_PATH

        cls.root = root
        cls.filePath = root / STORED_PLOTSGUI_PKL_PATH
        cls.data_path = root / STORED_DATAPREP_PKL_PATH
    
    def set_data_default(self):
        # Load the default dataset ONCE, at class level
        # Default dataset – shared across all instances of PWA and its subclasses
        with open(os.path.normpath(PWA.data_path), "rb") as f:
            return pickle.load(f)

    # ---------------------------------------------------------------------------------------------
    # Static method – loads all saved plots from the pickle file (plots_gui.pkl)
    # Returns an empty list if the file does not exist
    # ---------------------------------------------------------------------------------------------

    @staticmethod
    def load_plots():
        """Static method — Load plots list from file."""
        if not os.path.exists(PWA.filePath):
            print("⚠️ No existing plots file found. Returning empty list.")
            return [] 
            
        with open(PWA.filePath, "rb") as f:
            data = pickle.load(f)
            plots = data.get("plots", [])

        print(f"✅ Loaded {len(plots)} plots from {PWA.filePath}")
        return plots
    

    # ---------------------------------------------------------------------------------------------
    # Static method – saves all plot objects to pickle file, avoiding duplicate titles
    # ---------------------------------------------------------------------------------------------
    
    @staticmethod
    def add_plots(plots):
        """Static method — add plots list to file, ignoring duplicates by title."""
        if not plots:
            print("⚠️ No plots to save.")
            return 

        # Load existing plots (if file exists)
        existing = []
        if os.path.exists(PWA.filePath):
            try:
                with open(PWA.filePath, "rb") as f:
                    existing = pickle.load(f).get("plots", [])
            except (EOFError, pickle.UnpicklingError):
                print(f"⚠️ File {PWA.filePath} was empty or corrupted — starting fresh.")
                existing = []

        # Build a dictionary keyed by title to ensure uniqueness
        unique_plots = {p.title: p for p in existing}

        # Add new plots, skipping duplicates
        added = 0
        for p in plots:
            if p.title not in unique_plots:
                unique_plots[p.title] = p
                added += 1

        # Save back to file (serialized as dictionary)
        with open(PWA.filePath, "wb") as f:
            pickle.dump({"plots": list(unique_plots.values())}, f)

        print(f"💾 Saved {len(unique_plots)} total plots to {PWA.filePath}")
        if added:
            print(f"✅ Added {added} new plots.")
        else:
            print("ℹ️ No new plots were added (all already present).")



    # ---------------------------------------------------------------------------------------------
    # Static method – replace plot (by title)
    # ---------------------------------------------------------------------------------------------
    
    @staticmethod
    def replace_plots(plots):
        """Static method — Replace all plots in the pickle file with the provided list."""
        if not plots:
            print("⚠️ No plots provided. Nothing to save.")
            return

        # Overwrite the file directly with new plots
        with open(PWA.filePath, "wb") as f:
            pickle.dump({"plots": plots}, f)

        print(f"💾 Replaced all plots in {PWA.filePath}")
        print(f"✅ Saved {len(plots)} new plots.")


    @staticmethod
    def replace_plot(new_plot):
        """Static method — Replace an existing plot (matched by title) with a new one."""
        if not os.path.exists(PWA.filePath):
            print("⚠️ No existing plots file found. Abort.")
            return

        with open(PWA.filePath, "rb") as f:
            data = pickle.load(f)
            plots = data.get("plots", [])

        replaced = False
        for i, p in enumerate(plots):
            if p.title == new_plot.title:
                plots[i] = new_plot
                replaced = True
                break

        if not replaced:
            plots.append(new_plot)
            print(f"⚠️ No existing plot titled '{new_plot.title}' — added as new.")
        else:
            print(f"🔁 Replaced existing plot titled '{new_plot.title}'.")

        with open(PWA.filePath, "wb") as f:
            pickle.dump({"plots": plots}, f)

        print(f"💾 Saved {len(plots)} total plots to {PWA.filePath}")

    @staticmethod
    def delete_plot_by_title(title: str):
        """Static method — Delete a specific plot (by title) from the stored plots file."""
        if not os.path.exists(PWA.filePath):
            print("⚠️ No existing plots file found.")
            return

        with open(PWA.filePath, "rb") as f:
            data = pickle.load(f)
            plots = data.get("plots", [])

        # Filter out the plot with matching title
        new_plots = [p for p in plots if p.title != title]

        if len(new_plots) == len(plots):
            print(f"⚠️ No plot found with title '{title}'.")
            return

        # Save updated list
        with open(PWA.filePath, "wb") as f:
            pickle.dump({"plots": new_plots}, f)

        print(f"🗑️ Deleted plot '{title}' from {PWA.filePath}")
        print(f"💾 Remaining plots: {len(new_plots)}")

