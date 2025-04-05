from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QStackedWidget
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import sys

class Besetellungen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Besetellungen 🧮")
        self.setFixedSize(600, 600)
        self.init_ui()

    def init_ui(self):
        self.stacked = QStackedWidget(self)

        # Page 1 - Main selection
        self.page_main = QWidget()
        main_layout = QVBoxLayout()

        self.label = QLabel("Was möchtest du bestellen?")
        self.label.setFont(QFont("Segoe UI", 14))
        self.label.setStyleSheet("color: #61dafb;")
        self.label.setAlignment(Qt.AlignCenter)

        self.tor_button = QPushButton("Toro Strings 🎻")
        self.tor_button.setFixedHeight(50)
        self.tor_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.tor_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5722;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e64a19;
            }
        """)
        self.tor_button.clicked.connect(self.show_instrument_selection)

        main_layout.addWidget(self.label)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.tor_button)
        self.page_main.setLayout(main_layout)

        # Page 2 - Instrument selection
        self.page_instruments = QWidget()
        instrument_layout = QVBoxLayout()
        self.instrument_label = QLabel("Wähle ein Instrument:")
        self.instrument_label.setFont(QFont("Segoe UI", 13))
        self.instrument_label.setStyleSheet("color: #fcd34d;")
        self.instrument_label.setAlignment(Qt.AlignCenter)

        self.violin_btn = QPushButton("Violine 🎻")
        self.violin_btn.setFixedHeight(50)
        self.violin_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.violin_btn.setStyleSheet("""
            QPushButton {
                background-color: #673ab7;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #512da8;
            }
        """)
        self.violin_btn.clicked.connect(self.show_violin_strings)

        instrument_layout.addWidget(self.instrument_label)
        instrument_layout.addSpacing(10)
        instrument_layout.addWidget(self.violin_btn)
        self.page_instruments.setLayout(instrument_layout)

        # Add both pages to stacked widget
        self.stacked.addWidget(self.page_main)
        self.stacked.addWidget(self.page_instruments)

        # Set stacked as the main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stacked)
        self.setLayout(layout)

    def show_instrument_selection(self):
        self.stacked.setCurrentWidget(self.page_instruments)

    def show_violin_strings(self):
        print("Show E, A, D, G with variant options — coming next!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Besetellungen()
    window.show()
    sys.exit(app.exec_())
