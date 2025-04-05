import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QStackedWidget, QLineEdit, QHBoxLayout, QComboBox, QGridLayout
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
        }
        self.violine_variants = {
            "E": [("Varnish", 120, d) for d in range(54, 72, 2)] +
                  [("Venice Twist", 120, d) for d in range(54, 72, 2)] +
                  [("Natural", 120, d) for d in range(54, 72, 2)],
            "A": [("Varnish", 120, d) for d in range(72, 94, 2)] +
                  [("Venice Twist", 120, d) for d in range(72, 94, 2)] +
                  [("Natural", 120, d) for d in range(72, 94, 2)],
            "D": [(v, 120, d) for v in ["Varnish", "Venice Twist", "Natural"] for d in [102, 106, 110, 124]] +
                  [("SR", 60, d) for d in [58, 61, 64]],
            "G": [("Ram Sterling", 60, d) for d in [70, 74, 78]]
        }
        self.user_data = {}
        self.selected_instrument = None
        self.selected_string_type = None
        self.selected_string = None
        self.selected_variant = None
        self.init_ui()

    def init_ui(self):
        self.stacked = QStackedWidget(self)

        self.page_main = QWidget()
        main_layout = QVBoxLayout()
        label = QLabel("Was möchtest du zählen?")
        label.setFont(QFont("Segoe UI", 14))
        label.setAlignment(Qt.AlignCenter)

        self.toro_btn = QPushButton("Toro Strings")
        self.setup_button(self.toro_btn, "#ff5722", "#e64a19")
        self.toro_btn.clicked.connect(lambda: self.choose_instrument("Toro"))

        main_layout.addWidget(label)
        main_layout.addWidget(self.toro_btn)
        self.page_main.setLayout(main_layout)

        self.page_instruments = QWidget()
        inst_layout = QVBoxLayout()
        self.instrument_label = QLabel("Wähle ein Instrument:")
        self.instrument_label.setFont(QFont("Segoe UI", 13))
        self.instrument_label.setAlignment(Qt.AlignCenter)
        self.back_btn1 = self.make_back_button(self.page_main)

        inst_layout.addWidget(self.instrument_label)
        self.violin_btn = QPushButton("Violine")
        self.setup_button(self.violin_btn, "#3f51b5", "#303f9f")
        self.violin_btn.clicked.connect(lambda: self.choose_mode("Violine"))
        inst_layout.addWidget(self.violin_btn)
        inst_layout.addWidget(self.back_btn1)
        self.page_instruments.setLayout(inst_layout)

        self.page_mode = QWidget()
        mode_layout = QVBoxLayout()
        self.mode_label = QLabel("Modus wählen:")
        self.mode_label.setFont(QFont("Segoe UI", 14))
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.fill_btn = QPushButton("🔄 Fill in order")
        self.direct_btn = QPushButton("🎯 Direct select")
        self.setup_button(self.fill_btn, "#2196f3", "#1976d2")
        self.setup_button(self.direct_btn, "#ff9800", "#f57c00")
        self.fill_btn.clicked.connect(lambda: print("TODO: Fill mode"))
        self.direct_btn.clicked.connect(self.show_direct_string_select)
        self.back_btn2 = self.make_back_button(self.page_instruments)

        mode_layout.addWidget(self.mode_label)
        mode_layout.addWidget(self.fill_btn)
        mode_layout.addWidget(self.direct_btn)
        mode_layout.addWidget(self.back_btn2)
        self.page_mode.setLayout(mode_layout)

        self.page_direct_strings = QWidget()
        self.direct_grid = QGridLayout()
        self.direct_label = QLabel("Wähle eine Saite:")
        self.direct_label.setFont(QFont("Segoe UI", 14))
        self.direct_label.setAlignment(Qt.AlignCenter)
        self.direct_grid.addWidget(self.direct_label, 0, 0, 1, 2)
        row = 1
        col = 0
        for s in self.instrument_strings["Violine"]:
            btn = QPushButton(s)
            self.setup_button(btn, "#4caf50", "#388e3c")
            btn.clicked.connect(lambda checked, st=s: self.show_variants(st))
            self.direct_grid.addWidget(btn, row, col)
            col += 1
            if col > 1:
                row += 1
                col = 0
        self.back_btn3 = self.make_back_button(self.page_mode)
        self.direct_grid.addWidget(self.back_btn3, row + 1, 0, 1, 2)
        self.page_direct_strings.setLayout(self.direct_grid)

        self.page_variants = QWidget()
        self.variant_layout = QVBoxLayout()
        self.variant_label = QLabel("Variante wählen:")
        self.variant_label.setFont(QFont("Segoe UI", 14))
        self.variant_label.setAlignment(Qt.AlignCenter)
        self.variant_buttons_layout = QVBoxLayout()
        self.back_btn4 = self.make_back_button(self.page_direct_strings)
        self.variant_layout.addWidget(self.variant_label)
        self.variant_layout.addLayout(self.variant_buttons_layout)
        self.variant_layout.addWidget(self.back_btn4)
        self.page_variants.setLayout(self.variant_layout)

        self.page_quantity = QWidget()
        input_layout = QVBoxLayout()
        self.quantity_label = QLabel("Menge eingeben:")
        self.quantity_label.setFont(QFont("Segoe UI", 14))
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
        self.save_btn = QPushButton("✅ Speichern")
        self.setup_button(self.save_btn, "#4caf50", "#388e3c")
        self.save_btn.clicked.connect(self.save_quantity)
        self.back_btn5 = self.make_back_button(self.page_variants)
        input_layout.addWidget(self.quantity_label)
        input_layout.addWidget(self.quantity_input, alignment=Qt.AlignCenter)
        input_layout.addWidget(self.save_btn)
        input_layout.addWidget(self.back_btn5)
        self.page_quantity.setLayout(input_layout)

        self.stacked.addWidget(self.page_main)
        self.stacked.addWidget(self.page_instruments)
        self.stacked.addWidget(self.page_mode)
        self.stacked.addWidget(self.page_direct_strings)
        self.stacked.addWidget(self.page_variants)
        self.stacked.addWidget(self.page_quantity)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked)
        self.setLayout(layout)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#1e1e1e"))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

    def setup_button(self, button, color, hover):
        button.setFixedHeight(50)
        button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
        """)

    def make_back_button(self, target_page):
        btn = QPushButton("⬅️ Zurück")
        self.setup_button(btn, "#757575", "#616161")
        btn.clicked.connect(lambda: self.stacked.setCurrentWidget(target_page))
        return btn

    def choose_instrument(self, string_type):
        self.selected_string_type = string_type
        self.stacked.setCurrentWidget(self.page_instruments)

    def choose_mode(self, instrument):
        self.selected_instrument = instrument
        self.stacked.setCurrentWidget(self.page_mode)

    def show_direct_string_select(self):
        self.stacked.setCurrentWidget(self.page_direct_strings)

    def show_variants(self, string_name):
        self.selected_string = string_name
        for i in reversed(range(self.variant_buttons_layout.count())):
            self.variant_buttons_layout.itemAt(i).widget().setParent(None)
        for v in self.violine_variants[string_name]:
            version, length, diameter = v
            btn = QPushButton(f"{version} | L={length} | D={diameter}")
            self.setup_button(btn, "#673ab7", "#512da8")
            btn.clicked.connect(lambda checked, var=v: self.select_variant(var))
            self.variant_buttons_layout.addWidget(btn)
        self.stacked.setCurrentWidget(self.page_variants)

    def select_variant(self, variant):
        self.selected_variant = variant
        self.quantity_input.clear()
        self.stacked.setCurrentWidget(self.page_quantity)

    def save_quantity(self):
        qty = self.quantity_input.text()
        v = self.selected_variant
        print(f"SAVED {self.selected_string} - {v[0]} | L={v[1]} | D={v[2]} = {qty}")
        self.stacked.setCurrentWidget(self.page_direct_strings)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Besetellungen()
    window.show()
    sys.exit(app.exec_())
