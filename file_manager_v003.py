import sys
import os
import pandas as pd
import sqlite3
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon


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
        self.setGeometry(100, 100, 600, 600)

        layout = QHBoxLayout()

        layout_1 = QVBoxLayout()
        layout_1.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.select_button = QPushButton('Selecionar Diretório', self)
        elecione_icon_path = os.path.join(icon_path, "selecione.ico")
        self.select_button.setIcon(QIcon(elecione_icon_path))
        self.select_button.clicked.connect(self.select_directory)
        layout_1.addWidget(self.select_button)
 
        self.analyze_button = QPushButton('Analisar Diretório', self)
        analyze_icon_path = os.path.join(icon_path, "analyze.ico")
        self.analyze_button.setIcon(QIcon(analyze_icon_path))
        self.analyze_button.clicked.connect(self.analyze_directory)
        layout_1.addWidget(self.analyze_button)

        self.export_excel_button = QPushButton('Exportar para Excel', self)
        xlsx_icon_path = os.path.join(icon_path, "xlsx.ico")
        self.export_excel_button.setIcon(QIcon(xlsx_icon_path))
        self.export_excel_button.clicked.connect(self.export_to_excel)
        layout_1.addWidget(self.export_excel_button)

        self.export_csv_button = QPushButton('Exportar para CSV', self)
        csv_icon_path = os.path.join(icon_path, "csv.ico")
        self.export_csv_button.setIcon(QIcon(csv_icon_path))
        self.export_csv_button.clicked.connect(self.export_to_csv)
        layout_1.addWidget(self.export_csv_button)

        self.export_txt_button = QPushButton('Exportar para TXT', self)
        txt_icon_path = os.path.join(icon_path, "txt.ico")
        self.export_txt_button.setIcon(QIcon(txt_icon_path))
        self.export_txt_button.clicked.connect(self.export_to_txt)
        layout_1.addWidget(self.export_txt_button)

        self.clear_button = QPushButton('Limpar Dados', self)
        clear_icon_path = os.path.join(icon_path, "clear.ico")
        self.clear_button.setIcon(QIcon(clear_icon_path))
        self.clear_button.clicked.connect(self.clear_data)
        layout_1.addWidget(self.clear_button)

        layout_2 = QVBoxLayout()
        
        self.directory_label = QLabel('Nenhum diretório selecionado', self)
        layout_2.addWidget(self.directory_label)

        self.db_content = QTableWidget(self)
        layout_2.addWidget(self.db_content)

        layout.addLayout(layout_1)
        layout.addLayout(layout_2)

        self.setLayout(layout)
        self.init_db()

    def init_db(self):
        self.conn = sqlite3.connect('directory_changes.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS changes (
                id INTEGER PRIMARY KEY,
                tipo TEXT,
                caminho TEXT,
                data_modificacao TEXT,
                tipo_arquivo TEXT
            )
        ''')
        self.conn.commit()

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Selecionar Diretório')
        if directory:
            self.current_directory = directory
            self.directory_label.setText(f'Diretório Selecionado: {directory}')
            self.previous_state = self.scan_directory(directory)

    def scan_directory(self, directory):
        state = {}
        for root, dirs, files in os.walk(directory):
            for name in dirs + files:
                path = os.path.join(root, name)
                state[path] = {
                    'mod_time': os.path.getmtime(path),
                    'file_type': 'Diretório' if os.path.isdir(path) else 'Arquivo'
                }
        return state

    def analyze_directory(self):
        if not self.current_directory:
            self.result_label.setText('Por favor, selecione um diretório primeiro.')
            return

        current_state = self.scan_directory(self.current_directory)
        renamed_dirs = self.detect_renamed_directories(self.previous_state, current_state)
        renamed_files = self.detect_renamed_files(self.previous_state, current_state)
        modified_items = self.detect_modified_items(self.previous_state, current_state)
        added_items = self.detect_added_items(self.previous_state, current_state)
        deleted_items = self.detect_deleted_items(self.previous_state, current_state)

        # Remover itens renomeados das listas de adicionados e excluídos
        renamed_paths = {old for old, new in renamed_dirs} | {new for old, new in renamed_dirs} | \
                        {old for old, new in renamed_files} | {new for old, new in renamed_files}
        added_items = [item for item in added_items if item not in renamed_paths]
        deleted_items = [item for item in deleted_items if item not in renamed_paths]

        self.save_to_db(renamed_dirs, renamed_files, modified_items, added_items, deleted_items, current_state, self.previous_state)
        self.previous_state = current_state
        self.load_db_content()

    def detect_renamed_directories(self, previous_state, current_state):
        renamed_dirs = []
        previous_dirs = {k: v for k, v in previous_state.items() if v['file_type'] == 'Diretório'}
        current_dirs = {k: v for k, v in current_state.items() if v['file_type'] == 'Diretório'}

        for prev_dir in previous_dirs:
            if prev_dir not in current_dirs:
                for curr_dir in current_dirs:
                    if previous_dirs[prev_dir]['mod_time'] == current_dirs[curr_dir]['mod_time']:
                        renamed_dirs.append((prev_dir, curr_dir))
                        break

        return renamed_dirs
    
    def detect_renamed_files(self, previous_state, current_state):
        renamed_files = []
        previous_files = {k: v for k, v in previous_state.items() if v['file_type'] == 'Arquivo'}
        current_files = {k: v for k, v in current_state.items() if v['file_type'] == 'Arquivo'}

        for prev_file in previous_files:
            if prev_file not in current_files:
                for curr_file in current_files:
                    if previous_files[prev_file]['mod_time'] == current_files[curr_file]['mod_time']:
                        renamed_files.append((prev_file, curr_file))
                        break

        return renamed_files

    def detect_added_items(self, previous_state, current_state):
        added_items = []
        for path in current_state:
            if path not in previous_state:
                added_items.append(path)
        return added_items

    def detect_deleted_items(self, previous_state, current_state):
        deleted_items = []
        for path in previous_state:
            if path not in current_state:
                deleted_items.append(path)
        return deleted_items

    def detect_modified_items(self, previous_state, current_state):
        modified_items = []
        for path in current_state:
            if path in previous_state and current_state[path]['mod_time'] != previous_state[path]['mod_time']:
                modified_items.append(path)
        return modified_items

    def save_to_db(self, renamed_dirs, renamed_files, modified_items, added_items, deleted_items, current_state, previous_state):
        for old_dir, new_dir in renamed_dirs:
            self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                                ('Renomeado', f'{old_dir} -> {new_dir}', self.format_time(previous_state.get(old_dir, {'mod_time': current_state[new_dir]['mod_time']})['mod_time']), 'Diretório'))

        for old_file, new_file in renamed_files:
            # Verificar se o arquivo não está dentro de um diretório renomeado
            if not any(old_file.startswith(old_dir) for old_dir, new_dir in renamed_dirs):
                self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                                    ('Renomeado', f'{old_file} -> {new_file}', self.format_time(previous_state.get(old_file, {'mod_time': current_state[new_file]['mod_time']})['mod_time']), 'Arquivo'))

        for item in modified_items:
            self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                                ('Modificado', item, self.format_time(current_state[item]['mod_time']), current_state[item]['file_type']))

        for item in added_items:
            self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                                ('Adicionado', item, self.format_time(current_state[item]['mod_time']), current_state[item]['file_type']))

        for item in deleted_items:
            if item in previous_state:
                self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                                    ('Excluído', item, self.format_time(previous_state[item]['mod_time']), previous_state[item]['file_type']))

        self.conn.commit()

    def load_db_content(self):
        self.cursor.execute('SELECT tipo, caminho, data_modificacao, tipo_arquivo FROM changes')
        rows = self.cursor.fetchall()
        self.db_content.setRowCount(len(rows))
        self.db_content.setColumnCount(4)
        self.db_content.setHorizontalHeaderLabels(['Tipo', 'Caminho', 'Data de modificação', 'Tipo de arquivo'])

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.db_content.setItem(i, j, QTableWidgetItem(str(value)))

    def export_to_excel(self):
        directory = QFileDialog.getExistingDirectory(self, 'Selecionar Diretório para Salvar')
        if directory:
            file_path = os.path.join(directory, 'directory_changes_export.xlsx')
            self.cursor.execute('SELECT tipo, caminho, data_modificacao, tipo_arquivo FROM changes')
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows, columns=['Tipo', 'Caminho', 'Data de modificação', 'Tipo de arquivo'])
            df.to_excel(file_path, index=False)

    def export_to_csv(self):
        directory = QFileDialog.getExistingDirectory(self, 'Selecionar Diretório para Salvar')
        if directory:
            file_path = os.path.join(directory, 'directory_changes_export.csv')
            self.cursor.execute('SELECT tipo, caminho, data_modificacao, tipo_arquivo FROM changes')
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows, columns=['Tipo', 'Caminho', 'Data de modificação', 'Tipo de arquivo'])
            df.to_csv(file_path, index=False)

    def export_to_txt(self):
        directory = QFileDialog.getExistingDirectory(self, 'Selecionar Diretório para Salvar')
        if directory:
            file_path = os.path.join(directory, 'directory_changes_export.txt')
            self.cursor.execute('SELECT tipo, caminho, data_modificacao, tipo_arquivo FROM changes')
            rows = self.cursor.fetchall()
            with open(file_path, 'w') as f:
                for row in rows:
                    f.write('\t'.join(map(str, row)) + '\n')

    def clear_data(self):
        # Limpar dados da tabela
        self.db_content.setRowCount(0)
        # Limpar dados do banco de dados
        self.cursor.execute('DELETE FROM changes')
        self.conn.commit()

    def format_time(self, timestamp):
        return pd.to_datetime(timestamp, unit='s').strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    analyzer = DirectoryAnalyzer()
    analyzer.show()
    sys.exit(app.exec())
