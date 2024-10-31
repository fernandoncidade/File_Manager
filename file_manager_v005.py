import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableWidget, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon, QFont
from directory_utils_v005 import init_db, select_directory, scan_directory, analyze_directory, detect_renamed_directories, detect_renamed_files, detect_added_items, detect_deleted_items, detect_modified_items, save_to_db, load_db_content, export_to_excel, export_to_csv, export_to_txt, clear_data, format_time


class DirectoryAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_directory = ""
        self.previous_state = {}

    def initUI(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")
        self.setWindowTitle('Analisador de Diretórios')
        icon_title_path = os.path.join(icon_path, "manager_files1.ico")
        self.setWindowIcon(QIcon(icon_title_path))
        self.setGeometry(100, 100, 1000, 500)

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()
        layout_1.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout_h_1 = QHBoxLayout()

        self.label_selecione = QLabel('Selecionar Diretório:', self)
        layout_h_1.addWidget(self.label_selecione)

        select_button = self.create_button(self)
        elecione_icon_path = os.path.join(icon_path, "selecione.ico")
        select_button.setIcon(QIcon(elecione_icon_path))
        select_button.clicked.connect(self.select_directory)
        layout_h_1.addWidget(select_button)
        layout_1.addLayout(layout_h_1)

        layout_h_2 = QHBoxLayout()

        self.label_analyze = QLabel('Analisar Diretório:', self)
        layout_h_2.addWidget(self.label_analyze)
         
        analyze_button = self.create_button(self)
        analyze_icon_path = os.path.join(icon_path, "analyze.ico")
        analyze_button.setIcon(QIcon(analyze_icon_path))
        analyze_button.clicked.connect(self.analyze_directory)
        layout_h_2.addWidget(analyze_button)
        layout_1.addLayout(layout_h_2)

        layout_h_3 = QHBoxLayout()

        self.label_export_excel = QLabel('Exportar para Excel:', self)
        layout_h_3.addWidget(self.label_export_excel)

        export_excel_button = self.create_button(self)
        xlsx_icon_path = os.path.join(icon_path, "xlsx.ico")
        export_excel_button.setIcon(QIcon(xlsx_icon_path))
        export_excel_button.clicked.connect(self.export_to_excel)
        layout_h_3.addWidget(export_excel_button)
        layout_1.addLayout(layout_h_3)

        layout_h_4 = QHBoxLayout()

        self.label_export_csv = QLabel('Exportar para CSV:', self)
        layout_h_4.addWidget(self.label_export_csv)

        export_csv_button = self.create_button(self)
        csv_icon_path = os.path.join(icon_path, "csv.ico")
        export_csv_button.setIcon(QIcon(csv_icon_path))
        export_csv_button.clicked.connect(self.export_to_csv)
        layout_h_4.addWidget(export_csv_button)
        layout_1.addLayout(layout_h_4)

        layout_h_5 = QHBoxLayout()

        self.label_export_txt = QLabel('Exportar para TXT:', self)
        layout_h_5.addWidget(self.label_export_txt)

        export_txt_button = self.create_button(self)
        txt_icon_path = os.path.join(icon_path, "txt.ico")
        export_txt_button.setIcon(QIcon(txt_icon_path))
        export_txt_button.clicked.connect(self.export_to_txt)
        layout_h_5.addWidget(export_txt_button)
        layout_1.addLayout(layout_h_5)

        layout_h_6 = QHBoxLayout()

        self.label_clear = QLabel('Limpar Dados:', self)
        layout_h_6.addWidget(self.label_clear)

        clear_button = self.create_button(self)
        clear_icon_path = os.path.join(icon_path, "clear.ico")
        clear_button.setIcon(QIcon(clear_icon_path))
        clear_button.clicked.connect(self.clear_data)
        layout_h_6.addWidget(clear_button)
        layout_1.addLayout(layout_h_6)

        layout_2 = QVBoxLayout()
        
        self.directory_label = QLabel('Nenhum diretório selecionado:', self)
        layout_2.addWidget(self.directory_label)

        self.db_content = QTableWidget(self)
        layout_2.addWidget(self.db_content)

        layout.addLayout(layout_1)
        layout.addLayout(layout_2)

        self.setLayout(layout)
        self.init_db()

    def create_button(self, text):
        button = QPushButton(text)
        button.setMinimumWidth(3 * button.fontMetrics().horizontalAdvance('m'))
        button.setMaximumWidth(3 * button.fontMetrics().horizontalAdvance('m'))
        button.setFont(QFont('Arial', 9))
        return button

    # Métodos importados
    init_db = init_db
    select_directory = select_directory
    scan_directory = scan_directory
    analyze_directory = analyze_directory
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
