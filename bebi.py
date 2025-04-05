import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QStackedWidget, QLineEdit, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class Besetellungen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Besetellungen \U0001F9EE")
        self.setFixedSize(600, 600)
        self.instrument_strings = {
            "Violine": ["E", "A", "D", "G"],
            "Viola": ["A", "D", "G", "C"],
            "Cello": ["C", "G", "D", "A"],
            "Bassgambe": ["D", "G", "C", "e", "a", "d'"],
            "Diskantgambe": ["d''", "a'", "e'", "c'", "g", "d"]
        }
        self.violine_variants = {
            "E": {"type": "RAM", "length": 120, "diameters": list(range(54, 72, 2)), "versions": ["Varnish", "Venice Twist", "Natural"]},
            "A": {"type": "RAM", "length": 120, "diameters": list(range(72, 94, 2)), "versions": ["Varnish", "Venice Twist", "Natural"]},
            "D": [
                {"type": "RAM", "length": 120, "diameters": [102, 106, 110, 124], "versions": ["Varnish", "Venice Twist", "Natural"]},
                {"type": "SR", "length": 60, "diameters": [58, 61, 64], "versions": ["Standard"]}
            ],
            "G": [
                {"type": "SR", "length": 60, "diameters": [70, 74, 78], "versions": ["Ram Sterling"]}
            ]
        }
        self.current_strings = []
        self.current_string_index = 0
        self.selected_instrument = None
        self.current_variant_index = 0
        self.current_diameter_index = 0
        self.current_alt_variant_index = 0
        self.init_ui()

    def init_ui(self):
        self.stacked = QStackedWidget(self)

        self.page_main = QWidget()
        main_layout = QVBoxLayout()

        self.label = QLabel("Was möchtest du bestellen?")
        self.label.setFont(QFont("Segoe UI", 14))
        self.label.setStyleSheet("color: #61dafb;")
        self.label.setAlignment(Qt.AlignCenter)

        self.tor_button = QPushButton("Toro Strings \U0001F3BB")
        self.tonica_button = QPushButton("Tonica Strings \U0001F3BB")
        self.col_button = QPushButton("Colophony \U0001F9F4")

        self.setup_button(self.tor_button, "#ff5722", "#e64a19")
        self.setup_button(self.tonica_button, "#9c27b0", "#7b1fa2")
        self.setup_button(self.col_button, "#4caf50", "#388e3c")

        self.tor_button.clicked.connect(lambda: self.show_instruments("Toro"))
        self.tonica_button.clicked.connect(lambda: self.show_instruments("Tonica"))
        self.col_button.clicked.connect(self.colophony_clicked)

        main_layout.addWidget(self.label)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.tor_button)
        main_layout.addWidget(self.tonica_button)
        main_layout.addWidget(self.col_button)
        self.page_main.setLayout(main_layout)

        self.page_instruments = QWidget()
        instrument_layout = QVBoxLayout()

        self.instrument_label = QLabel("Wähle ein Instrument:")
        self.instrument_label.setFont(QFont("Segoe UI", 13))
        self.instrument_label.setStyleSheet("color: #fcd34d;")
        self.instrument_label.setAlignment(Qt.AlignCenter)
        instrument_layout.addWidget(self.instrument_label)

        for instrument in self.instrument_strings:
            btn = QPushButton(instrument)
            self.setup_button(btn, "#3f51b5", "#303f9f")
            btn.clicked.connect(lambda checked, inst=instrument: self.start_string_entry(inst))
            instrument_layout.addWidget(btn)

        self.page_instruments.setLayout(instrument_layout)

        self.page_string_input = QWidget()
        self.string_layout = QVBoxLayout()
        self.string_label = QLabel("String:")
        self.string_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.string_label.setAlignment(Qt.AlignCenter)

        self.variant_label = QLabel("")
        self.variant_label.setFont(QFont("Segoe UI", 14))
        self.variant_label.setAlignment(Qt.AlignCenter)
        self.variant_label.setStyleSheet("color: #61dafb;")

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Anzahl")
        self.quantity_input.setAlignment(Qt.AlignCenter)
        self.quantity_input.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.quantity_input.setFixedSize(200, 60)
        self.quantity_input.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                color: #ffffff;
                border: 2px solid #61dafb;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        self.next_button = QPushButton("Next")
        self.setup_button(self.next_button, "#007acc", "#005f99")
        self.next_button.clicked.connect(self.next_string)

        self.string_layout.addWidget(self.string_label)
        self.string_layout.addWidget(self.variant_label)
        self.string_layout.addWidget(self.quantity_input, alignment=Qt.AlignCenter)
        self.string_layout.addWidget(self.next_button)
        self.page_string_input.setLayout(self.string_layout)

        self.stacked.addWidget(self.page_main)
        self.stacked.addWidget(self.page_instruments)
        self.stacked.addWidget(self.page_string_input)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked)
        self.setLayout(layout)

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

    def show_instruments(self, string_type):
        self.selected_string_type = string_type
        self.stacked.setCurrentWidget(self.page_instruments)

    def start_string_entry(self, instrument):
        self.selected_instrument = instrument
        self.current_strings = self.instrument_strings[instrument]
        self.current_string_index = 0
        self.current_variant_index = 0
        self.current_diameter_index = 0
        self.current_alt_variant_index = 0
        self.show_next_string()

    def show_next_string(self):
        if self.selected_instrument == "Violine":
            if self.current_string_index >= len(self.current_strings):
                self.stacked.setCurrentWidget(self.page_main)
                return

            string_name = self.current_strings[self.current_string_index]
            string_data = self.violine_variants[string_name]

            if isinstance(string_data, dict):
                versions = string_data["versions"]
                diameters = string_data["diameters"]
                length = string_data["length"]
                if self.current_variant_index >= len(versions):
                    self.current_variant_index = 0
                    self.current_diameter_index = 0
                    self.current_string_index += 1
                    self.show_next_string()
                    return

                if self.current_diameter_index >= len(diameters):
                    self.current_diameter_index = 0
                    self.current_variant_index += 1
                    self.show_next_string()
                    return

                current_version = versions[self.current_variant_index]
                current_diameter = diameters[self.current_diameter_index]

                self.string_label.setText(f"{self.selected_instrument}: Saite {string_name}")
                self.variant_label.setText(f"{current_version} | L={length} | D={current_diameter}")
                self.quantity_input.clear()
                self.stacked.setCurrentWidget(self.page_string_input)
            elif isinstance(string_data, list):
                if self.current_alt_variant_index >= len(string_data):
                    self.current_alt_variant_index = 0
                    self.current_string_index += 1
                    self.show_next_string()
                    return

                variant = string_data[self.current_alt_variant_index]
                versions = variant["versions"]
                diameters = variant["diameters"]
                length = variant["length"]

                if self.current_variant_index >= len(versions):
                    self.current_variant_index = 0
                    self.current_diameter_index = 0
                    self.current_alt_variant_index += 1
                    self.show_next_string()
                    return

                if self.current_diameter_index >= len(diameters):
                    self.current_diameter_index = 0
                    self.current_variant_index += 1
                    self.show_next_string()
                    return

                current_version = versions[self.current_variant_index]
                current_diameter = diameters[self.current_diameter_index]

                self.string_label.setText(f"{self.selected_instrument}: Saite {string_name}")
                self.variant_label.setText(f"{current_version} | L={length} | D={current_diameter}")
                self.quantity_input.clear()
                self.stacked.setCurrentWidget(self.page_string_input)

        else:
            self.stacked.setCurrentWidget(self.page_main)

    def next_string(self):
        qty = self.quantity_input.text()
        if self.selected_instrument == "Violine":
            string_name = self.current_strings[self.current_string_index]
            string_data = self.violine_variants[string_name]
            if isinstance(string_data, dict):
                current_version = string_data["versions"][self.current_variant_index]
                current_diameter = string_data["diameters"][self.current_diameter_index]
                length = string_data["length"]
                print(f"{self.selected_instrument} - {string_name} ({current_version}) L={length} D={current_diameter}: {qty}")
                self.current_diameter_index += 1
            elif isinstance(string_data, list):
                variant = string_data[self.current_alt_variant_index]
                current_version = variant["versions"][self.current_variant_index]
                current_diameter = variant["diameters"][self.current_diameter_index]
                length = variant["length"]
                print(f"{self.selected_instrument} - {string_name} ({current_version}) L={length} D={current_diameter}: {qty}")
                self.current_diameter_index += 1
            self.show_next_string()

    def colophony_clicked(self):
        print("Colophony clicked — no UI yet")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Besetellungen()
    window.show()
    sys.exit(app.exec_())
