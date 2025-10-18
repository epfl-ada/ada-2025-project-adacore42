import pickle
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Project root auto-detection
# Dynamically climbs upward until repository markers are found (.git / README.txt / results.ipynb)
# This ensures imports work correctly regardless of where the script is executed
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
root = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
while root.parent != root:
    if ((root / ".git").exists() and 
        (root / "README.txt").exists() and 
        (root / "results.ipynb").exists()):
        break
    root = root.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

# Import standardized project-level paths (defined in src/utils/paths.py)
from src.utils.paths import STORED_DATAPREP_PKL_PATH, STORED_PLOTSGUI_PKL_PATH


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Default plot class adapted for GUI
# This file defines a generic plot interface used by graphical components
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

plotsGUI = []   # Global list storing all instantiated GUI plot objects


class PlotGUI(ABC):


    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # Default plot class adapted for GUI
    # Handles loading data, defining figure logic, and saving plot states to disk
    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

    filePath = root / STORED_PLOTSGUI_PKL_PATH              # Path – location of stored GUI plots (.pkl)
    data_path = root / STORED_DATAPREP_PKL_PATH              # Path – location of pre-processed data (.pkl)



    # Load the default dataset ONCE, at class level
    # Default dataset – shared across all instances of PlotGUI and its subclasses
    with open(os.path.normpath(data_path), "rb") as f:
        default_data = pickle.load(f)

    # ---------------------------------------------------------------------------------------------
    # Legacy directory reference – maintained for backward compatibility
    # Always points to the _gui/ folder (current directory)
    # ---------------------------------------------------------------------------------------------
    base_dir = os.path.dirname(os.path.abspath(__file__))     # Path – current folder (_gui)
    filePath = os.path.join(base_dir, "plots_gui.pkl")         # Path – local pickle file inside _gui/


    # ---------------------------------------------------------------------------------------------
    # Class constructor – initializes title, labels, and data reference
    # ---------------------------------------------------------------------------------------------
    def __init__(self, title: str = "No Title", description: str = "No Description", xlabel: str = "X-axis", ylabel: str = "Y-axis", data=None):
        self.title = title                     # Title – plot title text
        self.description = description         # Description – optional long text
        self.xlabel = xlabel                   # X-axis label
        self.ylabel = ylabel                   # Y-axis label
        self.data = data if data is not None else PlotGUI.default_data   # Data – default if not provided

    # ---------------------------------------------------------------------------------------------
    # Base plot definition placeholder – overridden by subclasses
    # ---------------------------------------------------------------------------------------------
    def define_plot(ax: plt.Axes) -> plt.Axes:
        return ax

    # ---------------------------------------------------------------------------------------------
    # Creates and returns a matplotlib Figure object ready for display
    # ---------------------------------------------------------------------------------------------
    def get_fig(self) -> Figure:
        fig, ax = plt.subplots()        # Create figure and axis
        self.set_ax(ax)                 # Apply titles and labels
        self.define_plot(ax)            # Apply subclass-specific drawing
        return fig


    # ---------------------------------------------------------------------------------------------
    # Returns the Figure wrapped as a Qt canvas (for GUI embedding)
    # ---------------------------------------------------------------------------------------------
    def get_canvas(self) -> FigureCanvas:
        return FigureCanvas(self.get_fig())

    # ---------------------------------------------------------------------------------------------
    # Common axis formatting (applied to all plot types)
    # ---------------------------------------------------------------------------------------------
    def set_ax(self, ax: plt.Axes):
        """Set common properties for a matplotlib Axes."""
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)

    # ---------------------------------------------------------------------------------------------
    # Dynamically reassigns the plot definition method (useful for runtime customization)
    # ---------------------------------------------------------------------------------------------
    def set_define_plot(self, func):
        """Set the define_plot method to a new function."""
        self.define_plot = func  # Bind the method to the instance

    # ---------------------------------------------------------------------------------------------
    # Displays the generated plot in a standalone matplotlib window
    # ---------------------------------------------------------------------------------------------
    def show(self):
        """Display the plot in a matplotlib window."""
        fig = self.get_fig()
        fig.show()


    # ---------------------------------------------------------------------------------------------
    # Static method – loads all saved plots from the pickle file (plots_gui.pkl)
    # Returns an empty list if the file does not exist
    # ---------------------------------------------------------------------------------------------
    @staticmethod
    def load_plots():
        """Static method — Load plotsGUI list from file."""
        if not os.path.exists(PlotGUI.filePath):
            print("⚠️ No existing plots file found. Returning empty list.")
            return [] 
            
        with open(PlotGUI.filePath, "rb") as f:
            data = pickle.load(f)
            plotsGUI = data.get("plotsGUI", [])

        print(f"✅ Loaded {len(plotsGUI)} plots from {PlotGUI.filePath}")
        return plotsGUI
    


    # ---------------------------------------------------------------------------------------------
    # Static method – saves all plot objects to pickle file, avoiding duplicate titles
    # Ensures continuity between GUI sessions
    # ---------------------------------------------------------------------------------------------
    @staticmethod
    def save_plots(plotsGUI):
        """Static method — Save plotsGUI list to file, ignoring duplicates by title."""
        if not plotsGUI:
            print("⚠️ No plots to save.")
            return 

        # Load existing plots (if file exists)
        existing = []
        if os.path.exists(PlotGUI.filePath):
            try:
                with open(PlotGUI.filePath, "rb") as f:
                    existing = pickle.load(f).get("plotsGUI", [])
            except (EOFError, pickle.UnpicklingError):
                print(f"⚠️ File {PlotGUI.filePath} was empty or corrupted — starting fresh.")
                existing = []

        # Build a dictionary keyed by title to ensure uniqueness
        unique_plots = {p.title: p for p in existing}

        # Add new plots, skipping duplicates
        added = 0
        for p in plotsGUI:
            if p.title not in unique_plots:
                unique_plots[p.title] = p
                added += 1

        # Save back to file (serialized as dictionary)
        with open(PlotGUI.filePath, "wb") as f:
            pickle.dump({"plotsGUI": list(unique_plots.values())}, f)

        print(f"💾 Saved {len(unique_plots)} total plots to {PlotGUI.filePath}")
        if added:
            print(f"✅ Added {added} new plots.")
        else:
            print("ℹ️ No new plots were added (all already present).")


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Example subclass – Histogram plot
# Implements its own version of define_plot()
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

class HistPlotGUI(PlotGUI):
 
    def define_plot(self, ax: plt.Axes) -> plt.Axes:
        ax.hist(self.data['dataA'][0]["mean"], bins=30, color='skyblue', edgecolor='black')
        return ax


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Example subclass – Scatter plot
# Each subclass defines its own plotting logic while reusing PlotGUI infrastructure
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

class ScatterPlotGUI(PlotGUI):
    def define_plot(self, ax: plt.Axes) -> plt.Axes:
        dataA = self.data['dataA']                           # List – DataFrames for each contest
        x = [len(df) for df in dataA]                        # X – number of captions per contest
        y = [df["votes"].sum() for df in dataA]              # Y – total votes per contest
        ax.scatter(x, y, alpha=0.7, color='skyblue', edgecolor='black')
        return ax



# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Example usage – instantiate a histogram plot and save to the pickle file
# Demonstrates persistence between runs
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

plotsGUI.append(
    HistPlotGUI( 
        title="ExempleTitele", 
        description="ExempleDescription ExempleDescription ExempleDescription ExempleDescription ExempleDescription ExempleDescription", 
        xlabel="ExempleXlabel", 
        ylabel="ExempleYlabel"))  

# Save plots (duplicates are ignored by title)
PlotGUI.save_plots(plotsGUI)  # Save the plots list to file (ignoring duplicates by title)



# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Optional demonstration block – explicitly showing plot save process
# Ensures output consistency and informs about skipped/added plots
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––