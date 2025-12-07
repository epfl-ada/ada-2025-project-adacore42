import pickle
import os
import sys
import numpy as np
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


class PlotGUI(ABC):


    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # Default plot class adapted for GUI
    # Handles loading data, defining figure logic, and saving plot states to disk
    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

    filePath = root / STORED_PLOTSGUI_PKL_PATH              # Path – location of stored GUI plots (.pkl)
    data_path = root / STORED_DATAPREP_PKL_PATH              # Path – location of pre-processed data (.pkl)

    # ---------------------------------------------------------------------------------------------
    # Class constructor – initializes title, labels, and data reference
    # ---------------------------------------------------------------------------------------------
    def __init__(self, title: str = "No Title", description: str = "No Description", xlabel: str = "X-axis", ylabel: str = "Y-axis", mode=0, plotParams = None):
        self.title = title                     # Title – plot title text
        self.description = description         # Description – optional long text
        self.xlabel = xlabel                   # X-axis label
        self.ylabel = ylabel                   # Y-axis label
        self.plotParams = plotParams         # Plot parameters – dictionary for custom settings
        self.mode = mode

    def set_data_default(self):
        # Load the default dataset ONCE, at class level
        # Default dataset – shared across all instances of PlotGUI and its subclasses
        with open(os.path.normpath(PlotGUI.data_path), "rb") as f:
            return pickle.load(f)

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
    def add_plots(plotsGUI):
        """Static method — add plotsGUI list to file, ignoring duplicates by title."""
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

    @staticmethod
    def replace_plots(plotsGUI):
        """Static method — Replace all plots in the pickle file with the provided list."""
        if not plotsGUI:
            print("⚠️ No plots provided. Nothing to save.")
            return

        # Overwrite the file directly with new plots
        with open(PlotGUI.filePath, "wb") as f:
            pickle.dump({"plotsGUI": plotsGUI}, f)

        print(f"💾 Replaced all plots in {PlotGUI.filePath}")
        print(f"✅ Saved {len(plotsGUI)} new plots.")


    @staticmethod
    def replace_plot(new_plot):
        """Static method — Replace an existing plot (matched by title) with a new one."""
        if not os.path.exists(PlotGUI.filePath):
            print("⚠️ No existing plots file found. Abort.")
            return

        with open(PlotGUI.filePath, "rb") as f:
            data = pickle.load(f)
            plotsGUI = data.get("plotsGUI", [])

        replaced = False
        for i, p in enumerate(plotsGUI):
            if p.title == new_plot.title:
                plotsGUI[i] = new_plot
                replaced = True
                break

        if not replaced:
            plotsGUI.append(new_plot)
            print(f"⚠️ No existing plot titled '{new_plot.title}' — added as new.")
        else:
            print(f"🔁 Replaced existing plot titled '{new_plot.title}'.")

        with open(PlotGUI.filePath, "wb") as f:
            pickle.dump({"plotsGUI": plotsGUI}, f)

        print(f"💾 Saved {len(plotsGUI)} total plots to {PlotGUI.filePath}")

    @staticmethod
    def delete_plot_by_title(title: str):
        """Static method — Delete a specific plot (by title) from the stored plots file."""
        if not os.path.exists(PlotGUI.filePath):
            print("⚠️ No existing plots file found.")
            return

        with open(PlotGUI.filePath, "rb") as f:
            data = pickle.load(f)
            plotsGUI = data.get("plotsGUI", [])

        # Filter out the plot with matching title
        new_plots = [p for p in plotsGUI if p.title != title]

        if len(new_plots) == len(plotsGUI):
            print(f"⚠️ No plot found with title '{title}'.")
            return

        # Save updated list
        with open(PlotGUI.filePath, "wb") as f:
            pickle.dump({"plotsGUI": new_plots}, f)

        print(f"🗑️ Deleted plot '{title}' from {PlotGUI.filePath}")
        print(f"💾 Remaining plots: {len(new_plots)}")


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Example subclass – Histogram plot
# Implements its own version of define_plot()
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

class HistPlotGUI(PlotGUI): #ça devrait pas marcher
 
    def define_plot(self, ax: plt.Axes) -> plt.Axes:
        ax.hist(self.data['dataA'][0]["mean"], bins=30, color='skyblue', edgecolor='black')
        return ax


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Example subclass – Scatter plot
# Each subclass defines its own plotting logic while reusing PlotGUI infrastructure
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Generic scatter plot class for GUI
class ScatterPlotGUI(PlotGUI):
    def __init__(
        self,
        title: str = "Scatter Plot",
        description: str = "Default scatter plot description.",
        xlabel: str = "X-axis",
        ylabel: str = "Y-axis",

        dataX=None,
        dataY=None,
        mode=0,
        s=20,                    # Marker area in points² (controls size)
        c="skyblue",             # Marker face color (can be single or array)
        marker="o",              # Marker shape ('o', 'x', '^', etc.)
        cmap=None,               # Colormap (used if 'color' is numeric)
        norm=None,               # Normalization object for colormap scaling
        vmin=None,               # Lower bound for colormap normalization
        vmax=None,               # Upper bound for colormap normalization
        alpha=0.7,               # Marker transparency (0.0–1.0)
        linewidths=None,         # Edge line width of markers
        edgecolors="black",      # Marker edge color
        plotnonfinite=False):     # Whether to plot NaN or inf points

        super().__init__(title, description, xlabel, ylabel , mode)

        self.plotParams = dict( s=s,
                                c=c,
                                marker=marker,
                                cmap=cmap,
                                norm=norm,
                                vmin=vmin,
                                vmax=vmax,
                                alpha=alpha,
                                linewidths=linewidths,
                                edgecolors=edgecolors,
                                plotnonfinite=plotnonfinite,)
        
        self.dataX = dataX
        self.dataY = dataY

    #Le changement d'affichage se fait soir par choix de mode.
    def define_plot(self, ax: plt.Axes) -> plt.Axes:
        match self.mode:
            case 1:
                return self.plot_1(ax)
            case _:                     # default / else
                return self.plot_0(ax)
        
    #Par exemple un plot normal
    def plot_0(self, ax: plt.Axes) -> plt.Axes:
        ax.scatter(self.dataX, self.dataY, **self.plotParams)                     
        return ax
    
    #Et ici un plot en log. 
    def plot_1(self, ax: plt.Axes) -> plt.Axes:
        ax.scatter(self.dataX, self.dataY, **self.plotParams)                     # Scatter plot with custom attributes
        return ax





# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# WordCloud Plot display
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

class WordCloudPlotGUI(PlotGUI):

    def __init__(self, cluster_id, wordcloud, representative_texts=None):
        super().__init__(
            title=f"Cluster {cluster_id} WordCloud",
            description="WordCloud of clustered captions",
            xlabel="",
            ylabel=""
        )

        self.cluster_id = cluster_id
        self.wordcloud = wordcloud
        self.representative_texts = representative_texts or []


    def plot_wordcloud_clusters(self, ax: plt.Axes) -> plt.Axes:
        """Draw the wordcloud directly on the axis."""
        ax.imshow(self.wordcloud, interpolation="bilinear")
        ax.axis("off")
        return ax
    


class ClusterScoresPlotGUI(PlotGUI):
    """Plot distribution of funniness scores for each cluster."""

    def __init__(self, df_top, score_col="mean"):
        super().__init__(
            title="Score distribution by cluster",
            description="Histogram/KDE of funniness scores per cluster",
            xlabel="Score",
            ylabel="Density"
        )
        self.df_top = df_top
        self.score_col = score_col

    def get_fig(self) -> Figure:
        clusters = sorted(self.df_top["cluster"].unique())
        n = len(clusters)

        cols = int(np.ceil(np.sqrt(n)))
        rows = int(np.ceil(n / cols))

        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
        axes = np.array(axes).reshape(rows, cols)

        for idx, c in enumerate(clusters):
            r, col = idx // cols, idx % cols
            ax = axes[r, col]

            scores = self.df_top[self.df_top.cluster == c][self.score_col]

            ax.hist(scores, bins=20, density=True, alpha=0.6)
            ax.set_title(f"Cluster {c} (n={len(scores)})")

        for idx in range(len(clusters), rows*cols):
            axes[idx//cols, idx%cols].axis("off")

        fig.tight_layout()
        return fig

