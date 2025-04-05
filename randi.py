import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QStackedWidget
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class Besetellungen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Besetellungen 🧮")
        self.setFixedSize(600, 600)
        self.init_ui()

    def init_ui(self):
        self.stacked = QStackedWidget(self)

        # 🟦 Page 1 - Main menu
        self.page_main = QWidget()
        main_layout = QVBoxLayout()

        self.label = QLabel("Was möchtest du bestellen?")
        self.label.setFont(QFont("Segoe UI", 14))
        self.label.setStyleSheet("color: #61dafb;")
        self.label.setAlignment(Qt.AlignCenter)

        # Toro Button
        self.tor_button = QPushButton("Toro Strings 🎻")
        self.setup_button(self.tor_button, "#ff5722", "#e64a19")
        self.tor_button.clicked.connect(self.show_instrument_selection)

        # Tonica Button
        self.tonica_button = QPushButton("Tonica Strings 🎻")
        self.setup_button(self.tonica_button, "#9c27b0", "#7b1fa2")
        self.tonica_button.clicked.connect(self.tonica_clicked)

        # Colophony Button
        self.col_button = QPushButton("Colophony 🧴")
        self.setup_button(self.col_button, "#4caf50", "#388e3c")
        self.col_button.clicked.connect(self.colophony_clicked)

        main_layout.addWidget(self.label)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.tor_button)
        main_layout.addWidget(self.tonica_button)
        main_layout.addWidget(self.col_button)
        self.page_main.setLayout(main_layout)

        # 🟪 Page 2 - Instrument selection for strings
        self.page_instruments = QWidget()
        instrument_layout = QVBoxLayout()
        self.instrument_label = QLabel("Wähle ein Instrument:")
        self.instrument_label.setFont(QFont("Segoe UI", 13))
        self.instrument_label.setStyleSheet("color: #fcd34d;")
        self.instrument_label.setAlignment(Qt.AlignCenter)

        self.violin_btn = QPushButton("Violine 🎻")
        self.setup_button(self.violin_btn, "#673ab7", "#512da8")
        self.violin_btn.clicked.connect(self.show_violin_strings)

        instrument_layout.addWidget(self.instrument_label)
        instrument_layout.addSpacing(10)
        instrument_layout.addWidget(self.violin_btn)
        self.page_instruments.setLayout(instrument_layout)

        # Add pages to stack
        self.stacked.addWidget(self.page_main)
        self.stacked.addWidget(self.page_instruments)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked)
        self.setLayout(layout)

        # Global dark theme palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#1e1e1e"))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

    def setup_button(self, button, color, hover_color):
        button.setFixedHeight(50)
        button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)

    def show_instrument_selection(self):
        self.stacked.setCurrentWidget(self.page_instruments)

    def show_violin_strings(self):
        print("🎻 Show E, A, D, G strings for violin — coming next!")

    def tonica_clicked(self):
        print("🎵 Tonica flow clicked — placeholder")

    def colophony_clicked(self):
        print("🧴 Colophony clicked — placeholder")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Besetellungen()
    window.show()
    sys.exit(app.exec_())
