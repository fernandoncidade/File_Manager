import os
import sqlite3
import pandas as pd
from PySide6.QtWidgets import QFileDialog, QTableWidgetItem
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue
from PySide6.QtCore import QTimer

def init_db(self):
    self.conn = sqlite3.connect('directory_changes.db')
    self.cursor = self.conn.cursor()
    self.cursor.execute('''CREATE TABLE IF NOT EXISTS changes (id INTEGER PRIMARY KEY, tipo TEXT, caminho TEXT, data_modificacao TEXT, tipo_arquivo TEXT)''')
    self.conn.commit()

def select_directory(self):
    directory = QFileDialog.getExistingDirectory(self, 'Selecionar Diretório:')
    if directory:
        self.current_directory = directory
        self.directory_label.setText(f'Diretório Selecionado: {directory}')
        self.previous_state = self.scan_directory(directory)
        self.start_observer()

def scan_directory(self, directory):
    state = {}
    for root, dirs, files in os.walk(directory):
        for name in dirs + files:
            path = os.path.join(root, name)
            try:
                file_type = 'Diretório' if os.path.isdir(path) else os.path.splitext(name)[1] or 'Arquivo'
                state[path] = {
                    'mod_time': os.path.getmtime(path),
                    'file_type': file_type
                }
            except FileNotFoundError:
                continue
    return state

def start_observer(self):
    self.event_queue = Queue()
    self.event_handler = DirectoryEventHandler(self.event_queue)
    self.observer = Observer()
    self.observer.schedule(self.event_handler, self.current_directory, recursive=True)
    self.observer.start()
    self.timer = QTimer()
    self.timer.timeout.connect(self.process_events)
    self.timer.start(1)

def stop_observer(self):
    if hasattr(self, 'observer'):
        self.observer.stop()
        self.observer.join()

def process_events(self):
    while not self.event_queue.empty():
        event = self.event_queue.get()
        self.analyze_directory()

class DirectoryEventHandler(FileSystemEventHandler):
    def __init__(self, event_queue):
        self.event_queue = event_queue

    def on_modified(self, event):
        self.event_queue.put(event)

    def on_created(self, event):
        self.event_queue.put(event)

    def on_deleted(self, event):
        self.event_queue.put(event)

    def on_moved(self, event):
        self.event_queue.put(event)

def toggle_analyze_directory(self):
    if hasattr(self, 'is_analyzing') and self.is_analyzing:
        self.stop_observer()
        self.result_label.setText("Análise Parada")
        self.is_analyzing = False
    else:
        if not self.current_directory:
            self.result_label.setText('Por favor, selecione um diretório primeiro.')
            return
        self.previous_state = self.scan_directory(self.current_directory)
        self.start_observer()
        self.result_label.setText("Análise Iniciada")
        self.is_analyzing = True

def analyze_directory(self):
    if not self.current_directory:
        self.result_label.setText('Por favor, selecione um diretório primeiro.')
        return

    self.current_state = current_state = self.scan_directory(self.current_directory)
    
    if self.detect_and_save_modifications(current_state):
        self.previous_state = current_state
        self.load_db_content()
        return
    
    if self.detect_and_save_renames(current_state):
        self.previous_state = current_state
        self.load_db_content()
        return
    
    if self.detect_and_save_moves(current_state):
        self.previous_state = current_state
        self.load_db_content()
        return
    
    if self.detect_and_save_additions(current_state):
        self.previous_state = current_state
        self.load_db_content()
        return
    
    if self.detect_and_save_deletions(current_state):
        self.previous_state = current_state
        self.load_db_content()
        return

    self.previous_state = current_state

def detect_and_save_moves(self, current_state):
    moved_items = self.detect_moved_items(self.previous_state, current_state)
    if moved_items:
        self.save_to_db(moved=moved_items)
        return True
    return False

def detect_and_save_renames(self, current_state):
    renamed_dirs = self.detect_renamed_directories(self.previous_state, current_state)
    renamed_files = self.detect_renamed_files(self.previous_state, current_state)
    if renamed_dirs or renamed_files:
        self.save_to_db(renamed_dirs=renamed_dirs, renamed_files=renamed_files)
        return True
    return False

def detect_and_save_additions(self, current_state):
    added_items = self.detect_added_items(self.previous_state, current_state)
    if added_items:
        self.save_to_db(added=added_items)
        return True
    return False

def detect_and_save_deletions(self, current_state):
    deleted_items = self.detect_deleted_items(self.previous_state, current_state)
    if deleted_items:
        self.save_to_db(deleted=deleted_items)
        return True
    return False

def detect_and_save_modifications(self, current_state):
    modified_items = self.detect_modified_items(self.previous_state, current_state)
    if modified_items:
        self.save_to_db(modified=modified_items)
        return True
    return False

def detect_moved_items(self, previous_state, current_state):
    moved_items = []
    previous_paths = set(previous_state.keys())
    current_paths = set(current_state.keys())
    
    renamed_dirs = self.detect_renamed_directories(previous_state, current_state)
    renamed_files = self.detect_renamed_files(previous_state, current_state)
    
    renamed_paths = {old: new for old, new in renamed_dirs}
    renamed_files_dict = {old: new for old, new in renamed_files}
    
    for prev_path in previous_paths:
        if prev_path not in current_paths:
            if prev_path in renamed_paths or prev_path in renamed_files_dict:
                continue
                
            is_in_renamed_dir = any(
                prev_path.startswith(old_dir + os.sep)
                for old_dir in renamed_paths.keys()
            )
            
            if is_in_renamed_dir:
                continue
                
            for curr_path in current_paths - previous_paths:
                if (previous_state[prev_path]['mod_time'] == current_state[curr_path]['mod_time'] and
                    previous_state[prev_path]['file_type'] == current_state[curr_path]['file_type'] and
                    curr_path not in [new_path for _, new_path in renamed_dirs + renamed_files]):
                    moved_items.append((prev_path, curr_path))
                    current_paths.remove(curr_path)
                    break

    return moved_items

def detect_renamed_directories(self, previous_state, current_state):
    renamed_dirs = []
    previous_dirs = {k: v for k, v in previous_state.items() if v['file_type'] == 'Diretório'}
    current_dirs = {k: v for k, v in current_state.items() if v['file_type'] == 'Diretório'}

    prev_dirs_sorted = sorted(previous_dirs.keys(), key=lambda x: x.count(os.sep))
    curr_dirs_sorted = sorted(current_dirs.keys(), key=lambda x: x.count(os.sep))

    for prev_dir in prev_dirs_sorted:
        if prev_dir not in current_dirs:
            if any(old_dir != prev_dir and prev_dir.startswith(old_dir + os.sep) 
                  for old_dir, _ in renamed_dirs):
                continue

            for curr_dir in curr_dirs_sorted:
                if (previous_dirs[prev_dir]['mod_time'] == current_dirs[curr_dir]['mod_time'] and
                    os.path.dirname(prev_dir) == os.path.dirname(curr_dir)):
                    renamed_dirs.append((prev_dir, curr_dir))
                    break

    return renamed_dirs

def detect_renamed_files(self, previous_state, current_state):
    renamed_files = []
    previous_files = {k: v for k, v in previous_state.items() if v['file_type'] != 'Diretório'}
    current_files = {k: v for k, v in current_state.items() if v['file_type'] != 'Diretório'}

    for prev_file in previous_files:
        if prev_file not in current_files:
            prev_dir = os.path.dirname(prev_file)
            prev_name = os.path.basename(prev_file)
            
            for curr_file in current_files:
                curr_dir = os.path.dirname(curr_file)
                curr_name = os.path.basename(curr_file)
                
                if (prev_dir == curr_dir and 
                    previous_files[prev_file]['mod_time'] == current_files[curr_file]['mod_time'] and
                    prev_name != curr_name and
                    curr_file not in [new_file for _, new_file in renamed_files]):
                    renamed_files.append((prev_file, curr_file))
                    break

    return renamed_files

def detect_added_items(self, previous_state, current_state):
    added_items = []
    
    previous_paths = set(previous_state.keys())
    current_paths = set(current_state.keys())
    
    new_items = current_paths - previous_paths
    
    for item in new_items:
        is_subitem = any(item != added and item.startswith(added + os.sep) for added in added_items)
        
        if not is_subitem:
            added_items.append(item)
    
    return added_items

def detect_deleted_items(self, previous_state, current_state):
    deleted_items = []
    previous_paths = set(previous_state.keys())
    current_paths = set(current_state.keys())
    
    removed_items = previous_paths - current_paths
    
    for item in sorted(removed_items, key=lambda x: x.count(os.sep), reverse=True):
        is_subitem = any(item != deleted and item.startswith(deleted + os.sep) for deleted in deleted_items)
        
        if not is_subitem:
            deleted_items.append(item)
    
    return deleted_items

def detect_modified_items(self, previous_state, current_state):
    modified_items = []
    
    for path in current_state:
        if (path in previous_state and 
            current_state[path]['file_type'] == 'Arquivo' and
            previous_state[path]['file_type'] == 'Arquivo' and
            current_state[path]['mod_time'] != previous_state[path]['mod_time']):
            modified_items.append(path)
    
    return modified_items

def save_to_db(self, moved=None, renamed_dirs=None, renamed_files=None, modified=None, added=None, deleted=None):
    if renamed_dirs or renamed_files:
        for old_dir, new_dir in (renamed_dirs or []):
            self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                                ('Renomeado', f'{new_dir}', self.format_time(self.previous_state[old_dir]['mod_time']), 'Diretório'))
        
        if renamed_files:
            for old_file, new_file in renamed_files:
                is_in_renamed_dir = any(old_file.startswith(old_dir + os.sep) for old_dir, _ in (renamed_dirs or []))

                if not is_in_renamed_dir:
                    self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                                        ('Renomeado', f'{new_file}', self.format_time(self.previous_state[old_file]['mod_time']), self.previous_state[old_file]['file_type']))
        
        self.conn.commit()
        return

    if moved:
        filtered_moved = []
        for old_path, new_path in moved:
            is_subitem_of_renamed_dir = any(
                old_path.startswith(renamed_old_dir + os.sep) for renamed_old_dir, _ in (renamed_dirs or []))
            
            if not is_subitem_of_renamed_dir:
                filtered_moved.append((old_path, new_path))

        for old_path, new_path in filtered_moved:
            self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                                ('Movido', f'{new_path}', self.format_time(self.previous_state[old_path]['mod_time']), self.previous_state[old_path]['file_type']))
        
        self.conn.commit()
        return

    if added:
        for item in added:
            self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                              ('Adicionado', item, self.format_time(os.path.getmtime(item)), 'Diretório' if os.path.isdir(item) else self.current_state[item]['file_type']))
        
        self.conn.commit()
        return

    if deleted:
        for item in deleted:
            self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                              ('Excluído', item, self.format_time(self.previous_state[item]['mod_time']), self.previous_state[item]['file_type']))
        
        self.conn.commit()
        return

    if modified:
        for item in modified:
            self.cursor.execute('INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)',
                              ('Modificado', item, self.format_time(self.current_state[item]['mod_time']), self.current_state[item]['file_type']))
        
        self.conn.commit()
        return

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
    self.db_content.setRowCount(0)
    self.cursor.execute('DELETE FROM changes')
    self.conn.commit()

# Formatação de tempo
def format_time(self, timestamp):
    return pd.to_datetime(timestamp, unit='s').strftime('%Y-%m-%d %H:%M:%S')
