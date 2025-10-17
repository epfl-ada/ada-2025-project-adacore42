import pickle
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

root = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
while root.parent != root:
    if ((root / ".git").exists() and 
        (root / "README.txt").exists() and 
        (root / "results.ipynb").exists()):
        break
    root = root.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

# ---------------------------------------------------------------------------------------------
# Import reusable project paths
# ---------------------------------------------------------------------------------------------
from src.utils.paths import STORED_DATAPREP_PKL_PATH, STORED_PLOTSGUI_PKL_PATH


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Default plot class adapted for GUI
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

plotsGUI = []


class PlotGUI(ABC):



    filePath = root / STORED_PLOTSGUI_PKL_PATH
    data_path = root /  STORED_DATAPREP_PKL_PATH



    # Load the default dataset ONCE, at class level
    with open(os.path.normpath(data_path), "rb") as f:
        default_data = pickle.load(f)

    # ---------------------------------------------------------------------------------------------
    

    base_dir = os.path.dirname(os.path.abspath(__file__))     # current folder (_gui)
    filePath = os.path.join(base_dir, "plots_gui.pkl")         # always inside _gui/


    # ---------------------------------------------------------------------------------------------

    def __init__(self, title: str = "No Title", description: str = "No Description", xlabel: str = "X-axis", ylabel: str = "Y-axis", data=None):
        self.title = title
        self.description = description
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.data = data if data is not None else PlotGUI.default_data

    # ---------------------------------------------------------------------------------------------

    def define_plot(ax: plt.Axes) -> plt.Axes:
        return ax

    def get_fig(self) -> Figure:
        fig, ax = plt.subplots()

        self.set_ax(ax)
        self.define_plot(ax)

        return fig


    def get_canvas(self) -> FigureCanvas:
        return FigureCanvas(self.get_fig())

    def set_ax(self, ax: plt.Axes):
        """Set common properties for a matplotlib Axes."""
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)

    def set_define_plot(self, func):
        """Set the define_plot method to a new function."""
        self.define_plot = func  # Bind the method to the instance

    def show(self):
        """Display the plot in a matplotlib window."""
        fig = self.get_fig()
        fig.show()


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
    


    # -----------------------------------------------------------
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

        # Save back to file
        with open(PlotGUI.filePath, "wb") as f:
            pickle.dump({"plotsGUI": list(unique_plots.values())}, f)

        print(f"💾 Saved {len(unique_plots)} total plots to {PlotGUI.filePath}")
        if added:
            print(f"✅ Added {added} new plots.")
        else:
            print("ℹ️ No new plots were added (all already present).")


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Plot initiation example
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

class HistPlotGUI(PlotGUI):
 
    def define_plot(self, ax: plt.Axes) -> plt.Axes:
        ax.hist(self.data['dataA'][0]["mean"], bins=30, color='skyblue', edgecolor='black')
        return ax

class ScatterPlotGUI(PlotGUI):
    def define_plot(self, ax: plt.Axes) -> plt.Axes:
        dataA = self.data['dataA']          # list of DataFrames
        x = [len(df) for df in dataA]       # number of captions per contest
        y = [df["votes"].sum() for df in dataA]  # total votes per contest
        ax.scatter(x, y, alpha=0.7, color='skyblue', edgecolor='black')
        return ax



plotsGUI.append(
    HistPlotGUI( 
        title="ExempleTitele", 
        description="ExempleDescription ExempleDescription ExempleDescription ExempleDescription ExempleDescription ExempleDescription", 
        xlabel="ExempleXlabel", 
        ylabel="ExempleYlabel"))  

PlotGUI.save_plots(plotsGUI)  # Save the plots list to file (ignoring duplicates by title)





# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Plots save example
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


