import sys
import pandas as pd
import signal
import importlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QLabel, QTableWidget, QTableWidgetItem, QSplitter, QPushButton
)

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Allow safe interrupt (Ctrl+C) when running PyQt in terminal
# Prevents GUI freeze on interrupt
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Import base PlotGUI class from module
from plots_gui import PlotGUI


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Define main window size (width, height)
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
WINDOW_SIZE = (1000, 600)





# ===============================================================
#  PANEL CLASSES – individual GUI components
# ===============================================================

class MenuPanel(QWidget):
    """Top panel with a reload button."""
    def __init__(self, on_reload_callback):
        super().__init__()
        layout = QHBoxLayout(self)                  # Layout – horizontal arrangement
        self.setLayout(layout)

        # Create a reload button
        self.button = QPushButton("🔁 Reload Plots")
        self.button.clicked.connect(on_reload_callback)  # Connect button to reload callback
        layout.addWidget(self.button)


# ---------------------------------------------------------------
class PlotListPanel(QListWidget):
    """Left panel containing the list of available plots."""
    def __init__(self, on_selection_callback, plots):
        super().__init__()
        self.on_selection_callback = on_selection_callback   # Callback when plot is selected
        self.refresh(plots)                                  # Populate list
        self.currentTextChanged.connect(self._handle_selection)

    def _handle_selection(self, item_name: str):
        """Internal method triggered when selection changes."""
        self.on_selection_callback(item_name)

    def refresh(self, plots):
        """Repopulate the list from a new plots list."""
        self.clear()                                         # Remove previous entries
        for plot in plots:
            self.addItem(plot.title)                         # Add each plot title


# ---------------------------------------------------------------
class DisplayPanel(QWidget):
    """Right panel responsible for showing selected plot or table."""
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)                      # Layout – vertical arrangement
        self.setLayout(self.layout)

    def clear(self):
        """Remove all widgets from the display area."""
        while self.layout.count():                           # Remove child widgets one by one
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_plot(self, plotData: PlotGUI):
        """Display a matplotlib FigureCanvas."""
        self.clear()                                         # Reset display area
        desctription = QLabel(plotData.description)          # Add description label
        desctription.setWordWrap(True)                       # Allow multiline wrapping

        self.layout.addWidget(desctription, stretch=1)       # Add label to layout
        self.layout.addWidget(plotData.get_canvas(), stretch=10)  # Add plot canvas


# ===============================================================
#  MAIN WINDOW – orchestrates all GUI components
# ===============================================================
class MainWindow(QWidget):
    """Main GUI window assembling list + display panels."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data & Plot Viewer")             # Set window title
        self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])           # Apply default window size

        # Keep reference to module so we can reload it later
        self.plots = PlotGUI.load_plots()                     # Load plots from pickle

        # ------------------------------------------------------
        # Layout setup (top-down)
        # ------------------------------------------------------
        main_layout = QVBoxLayout(self)
        self.menuPanel = MenuPanel(self.reload_plots)         # Create top reload bar

        # Create splitter dividing list and display panels
        splitter = QSplitter(self)
        self.listPanel = PlotListPanel(self.display_item, self.plots)
        self.displayPanel = DisplayPanel()

        splitter.addWidget(self.listPanel)                    # Left – plot list
        splitter.addWidget(self.displayPanel)                 # Right – plot viewer
        splitter.setSizes([200, 800])                         # Default splitter sizes (px)

        # Add elements to main layout
        main_layout.addWidget(self.menuPanel, stretch=1)
        main_layout.addWidget(splitter, stretch=10)

    # -----------------------------------------------------------
    def display_item(self, item_name: str):
        """Called whenever user selects a plot in the list."""
        found = next((p for p in self.plots if p.title == item_name), None)
        if found:
            self.displayPanel.show_plot(found)                # Display the selected plot

    # -----------------------------------------------------------
    def reload_plots(self):
        """Reload plots_gui.py and update the plot list."""
        self.plots = PlotGUI.load_plots()                     # Reload from file
        self.listPanel.refresh(self.plots)                    # Refresh list
        print("✅ Plots reloaded from plots_gui.py")           # Console confirmation


# ===============================================================
#  ENTRY POINT – application launcher
# ===============================================================
if __name__ == "__main__":

    app = QApplication(sys.argv)                              # Create QApplication instance
    viewer = MainWindow()                                     # Initialize main window
    viewer.show()                                             # Display GUI
    sys.exit(app.exec_())                                     # Start event loop (block until exit)