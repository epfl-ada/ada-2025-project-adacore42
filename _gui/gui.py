import sys
import pandas as pd
import signal
import importlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QLabel, QTableWidget, QTableWidgetItem, QSplitter, QPushButton
)

signal.signal(signal.SIGINT, signal.SIG_DFL)

from plots_gui import PlotGUI



# ===============================================================
#  PANEL CLASSES
# ===============================================================

class MenuPanel(QWidget):
    """Top panel with a reload button."""
    def __init__(self, on_reload_callback):
        super().__init__()
        layout = QHBoxLayout(self)
        self.setLayout(layout)

        self.button = QPushButton("🔁 Reload Plots")
        self.button.clicked.connect(on_reload_callback)
        layout.addWidget(self.button)


# ---------------------------------------------------------------
class PlotListPanel(QListWidget):
    """Left panel containing the list of available plots."""
    def __init__(self, on_selection_callback, plots):
        super().__init__()
        self.on_selection_callback = on_selection_callback
        self.refresh(plots)
        self.currentTextChanged.connect(self._handle_selection)

    def _handle_selection(self, item_name: str):
        """Internal method triggered when selection changes."""
        self.on_selection_callback(item_name)

    def refresh(self, plots):
        """Repopulate the list from a new plots list."""
        self.clear()
        for plot in plots:
            self.addItem(plot.title)


# ---------------------------------------------------------------
class DisplayPanel(QWidget):
    """Right panel responsible for showing selected plot or table."""
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def clear(self):
        """Remove all widgets from the display area."""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_plot(self, plotData: PlotGUI):
        """Display a matplotlib FigureCanvas."""
        self.clear()
        self.layout.addWidget(QLabel(plotData.description), stretch=1)
        self.layout.addWidget(plotData.get_canvas(), stretch=10)


# ===============================================================
#  MAIN WINDOW
# ===============================================================
class MainWindow(QWidget):
    """Main GUI window assembling list + display panels."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data & Plot Viewer")
        self.resize(1000, 800)

        # Keep reference to module so we can reload it
        self.plots = PlotGUI.load_plots()

        # Layout
        main_layout = QVBoxLayout(self)
        self.menuPanel = MenuPanel(self.reload_plots)

        splitter = QSplitter(self)
        self.listPanel = PlotListPanel(self.display_item, self.plots)
        self.displayPanel = DisplayPanel()

        splitter.addWidget(self.listPanel)
        splitter.addWidget(self.displayPanel)
        splitter.setSizes([200, 800])

        main_layout.addWidget(self.menuPanel, stretch=1)
        main_layout.addWidget(splitter, stretch=10)

    # -----------------------------------------------------------
    def display_item(self, item_name: str):
        """Called whenever user selects a plot in the list."""
        found = next((p for p in self.plots if p.title == item_name), None)
        if found:
            self.displayPanel.show_plot(found)

    # -----------------------------------------------------------
    def reload_plots(self):
        """Reload plots_gui.py and update the plot list."""

        self.plots = PlotGUI.load_plots()
        self.listPanel.refresh(self.plots)
        print("✅ Plots reloaded from plots_gui.py")


# ===============================================================
#  ENTRY POINT
# ===============================================================
if __name__ == "__main__":

    app = QApplication(sys.argv)
    viewer = MainWindow()
    viewer.show()
    sys.exit(app.exec_())