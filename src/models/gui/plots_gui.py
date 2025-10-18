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


    # ---------------------------------------------------------------------------------------------
    # Legacy directory reference – maintained for backward compatibility
    # Always points to the _gui/ folder (current directory)
    # ---------------------------------------------------------------------------------------------
    base_dir = os.path.dirname(os.path.abspath(__file__))     # Path – current folder (_gui)
    filePath = os.path.join(base_dir, "plots_gui.pkl")         # Path – local pickle file inside _gui/


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

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Example usage – instantiate a histogram plot and save to the pickle file
# Demonstrates persistence between runs
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Representative examples of ScatterPlotGUI instantiation
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

import numpy as np

plotsGUI = []

# 1. Simple linear relation
plotsGUI.append(
    ScatterPlotGUI(
        title="Simple Linear",
        description="Basic X–Y linear relation example.",
        xlabel="X values",
        ylabel="Y values",
        dataX=[1, 2, 3, 4, 5],
        dataY=[2, 4, 6, 8, 10],
    )
)

# 2. Random scatter
plotsGUI.append(
    ScatterPlotGUI(
        title="Random Distribution",
        description="Random points with transparency.",
        dataX=np.random.randn(100),
        dataY=np.random.randn(100),
        c="tomato",
        alpha=0.5,
        s=40,
    )
)

# 3. Parabolic curve
x = np.linspace(-3, 3, 60)
y = x**2
plotsGUI.append(
    ScatterPlotGUI(
        title="Parabola Shape",
        description="Y = X² curve with filled circles.",
        xlabel="X",
        ylabel="Y = X²",
        dataX=x,
        dataY=y,
        c="royalblue",
        s=70,
        marker="o",
        edgecolors="black",
    )
)

# 4. Color-mapped sine wave
x = np.linspace(0, 10, 100)
y = np.sin(x)
plotsGUI.append(
    ScatterPlotGUI(
        title="Color-mapped Sine Wave",
        description="Sine wave with color gradient by Y value.",
        dataX=x,
        dataY=y,
        c=y,
        cmap="viridis",
        s=80,
        alpha=0.8,
        marker="^",
    )
)

# 5. Two groups for comparison
plotsGUI.append(
    ScatterPlotGUI(
        title="Group A",
        description="First data cluster.",
        dataX=[1, 2, 3, 4],
        dataY=[1, 1.5, 1.8, 2.2],
        c="green",
        marker="o",
    )
)

plotsGUI.append(
    ScatterPlotGUI(
        title="Group B",
        description="Second data cluster overlaid.",
        dataX=[2, 3, 4, 5],
        dataY=[3, 2.7, 2.5, 2.2],
        c="orange",
        marker="x",
    )
)


PlotGUI.save_plots(plotsGUI)


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Optional demonstration block – explicitly showing plot save process
# Ensures output consistency and informs about skipped/added plots
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––