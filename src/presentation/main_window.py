#src/presentation/main_window.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM Merge Studio")
        self.setGeometry(100,100,  800, 600)
        
        # Central widget still have to get used on the name Widget, for me it is synonym for useless garbage to adorn something with
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Initial setup
        self._setup_ui()
        
    def _setup_ui(self):
        """Initialize the UI components"""
        pass  # We'll add components as needed