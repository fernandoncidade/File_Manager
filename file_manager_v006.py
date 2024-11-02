import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableWidget, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon, QFont
from directory_utils_v006 import (init_db, select_directory, scan_directory, start_observer, stop_observer, process_events,
                                  toggle_analyze_directory, analyze_directory, detect_and_save_moves, detect_and_save_renames,
                                  detect_and_save_additions, detect_and_save_deletions, detect_and_save_modifications,
                                  detect_moved_items, detect_renamed_directories, detect_renamed_files, detect_added_items,
                                  detect_deleted_items, detect_modified_items, save_to_db, load_db_content, export_to_excel,
                                  export_to_csv, export_to_txt, clear_data, format_time)


class DirectoryAnalyzer(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_analyzing = False
        self.current_directory = ""
        self.previous_state = {}
        self.current_state = {}

        self.initUI()
        self.init_db()

    def initUI(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")
        self.setWindowTitle('Analisador de Diretórios')
        self.setWindowIcon(QIcon(os.path.join(icon_path, "manager_files1.ico")))
        self.setGeometry(100, 100, 1000, 500)

        layout = QHBoxLayout()
        layout_1 = QVBoxLayout()
        layout_1.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.add_button_with_label(layout_1, 'Selecionar Diretório:', 'selecione.ico', self.select_directory, icon_path)
        self.add_button_with_label(layout_1, 'Analisar/Parar Diretório:', 'analyze.ico', self.toggle_analyze_directory, icon_path)
        self.add_button_with_label(layout_1, 'Exportar para Excel:', 'xlsx.ico', self.export_to_excel, icon_path)
        self.add_button_with_label(layout_1, 'Exportar para CSV:', 'csv.ico', self.export_to_csv, icon_path)
        self.add_button_with_label(layout_1, 'Exportar para TXT:', 'txt.ico', self.export_to_txt, icon_path)
        self.add_button_with_label(layout_1, 'Limpar Dados:', 'clear.ico', self.clear_data, icon_path)

        layout_2 = QVBoxLayout()
        self.result_label = QLabel('Selecione um diretório para começar')
        self.directory_label = QLabel('Nenhum diretório selecionado:', self)
        self.db_content = QTableWidget(self)
        layout_2.addWidget(self.directory_label)
        layout_2.addWidget(self.result_label)
        layout_2.addWidget(self.db_content)

        layout.addLayout(layout_1)
        layout.addLayout(layout_2)
        self.setLayout(layout)

    def add_button_with_label(self, layout, label_text, icon_name, callback, icon_path):
        layout_h = QHBoxLayout()
        label = QLabel(label_text, self)
        layout_h.addWidget(label)
        button = self.create_button()
        button.setIcon(QIcon(os.path.join(icon_path, icon_name)))
        button.clicked.connect(callback)
        layout_h.addWidget(button)
        layout.addLayout(layout_h)
        return button

    def create_button(self):
        button = QPushButton()
        button.setMinimumWidth(3 * button.fontMetrics().horizontalAdvance('m'))
        button.setMaximumWidth(3 * button.fontMetrics().horizontalAdvance('m'))
        button.setFont(QFont('Arial', 9))
        return button

    # Métodos importados
    init_db = init_db
    select_directory = select_directory
    scan_directory = scan_directory
    start_observer = start_observer
    stop_observer = stop_observer
    process_events = process_events
    toggle_analyze_directory = toggle_analyze_directory
    analyze_directory = analyze_directory
    detect_and_save_moves = detect_and_save_moves
    detect_and_save_renames = detect_and_save_renames
    detect_and_save_additions = detect_and_save_additions
    detect_and_save_deletions = detect_and_save_deletions
    detect_and_save_modifications = detect_and_save_modifications
    detect_moved_items = detect_moved_items
    detect_renamed_directories = detect_renamed_directories
    detect_renamed_files = detect_renamed_files
    detect_added_items = detect_added_items
    detect_deleted_items = detect_deleted_items
    detect_modified_items = detect_modified_items
    save_to_db = save_to_db
    load_db_content = load_db_content
    export_to_excel = export_to_excel
    export_to_csv = export_to_csv
    export_to_txt = export_to_txt
    clear_data = clear_data
    format_time = format_time


if __name__ == '__main__':
    app = QApplication(sys.argv)
    analyzer = DirectoryAnalyzer()
    analyzer.show()
    sys.exit(app.exec())
