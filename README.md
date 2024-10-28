README.

# README (English)

---

# File_Manager

## Description

`File_Manager` is a Python application with a graphical user interface (GUI) built using PySide6. It allows users to monitor changes in a directory, including the addition, deletion, modification, and renaming of files and folders. The application displays this information and enables data export to Excel, CSV, and TXT files, as well as saving a change history in an SQLite database.

## Features

- **Directory Selection**: Choose a directory to monitor.
- **Directory Analysis**: Analyzes changes (added, modified, renamed, and deleted files).
- **Data Export**: Exports change information to Excel, CSV, or TXT files.
- **Data Clearing**: Clears the current change history.

## Technologies Used

- **Python 3.12.6**
- **PySide6**: GUI development.
- **Pandas**: Data manipulation and export to Excel and CSV.
- **SQLite3**: Built-in database for storing change history.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/fernandoncidade/File_Manager
    cd File_Manager
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:
    ```bash
    python File_Manager.py
    ```

2. **Select a directory** for monitoring and click "Analyze Directory" to check for changes.
3. **Export data** to Excel, CSV, or TXT using the appropriate buttons.
4. **Clear the analysis data** using the "Clear Data" button.

## Code Structure

The code consists of the `DirectoryAnalyzer` class, which creates the interface and defines all functionalities:

- **`initUI()`**: Initializes the interface with buttons and layouts.
- **`create_button()`**: Creates buttons with icons.
- **`init_db()`**: Initializes the SQLite database.
- **`select_directory()`**: Selects the directory for analysis.
- **`scan_directory()`**: Scans the current state of the directory.
- **`analyze_directory()`**: Compares the current state with the previous one to detect changes.
- **`detect_*` Functions**: Detect added, modified, renamed, and deleted files.
- **`export_to_*` Functions**: Export data to Excel, CSV, or TXT files.
- **`clear_data()`**: Clears the database.

## Code Example

```python
# Start the application
app = QApplication(sys.argv)
analyzer = DirectoryAnalyzer()
analyzer.show()
sys.exit(app.exec())
```

## Dependencies

- `pandas`
- `sqlite3`
- `PySide6`
---

# README (Portuguese)

# File_Manager

## Descrição

O `File_Manager` é uma aplicação em Python com interface gráfica (GUI) criada com PySide6, que permite ao usuário monitorar alterações em um diretório, como adição, exclusão, modificação e renomeação de arquivos e pastas. O aplicativo exibe essas informações e permite exportar os dados para arquivos Excel, CSV e TXT, além de armazenar um histórico das alterações em um banco de dados SQLite.

## Funcionalidades

- **Seleção de Diretório**: Escolha um diretório para monitoramento.
- **Análise de Diretório**: Analisa as mudanças (arquivos adicionados, modificados, renomeados e excluídos).
- **Exportação de Dados**: Exporta as informações de mudanças para arquivos Excel, CSV ou TXT.
- **Limpeza de Dados**: Limpa o histórico atual de mudanças.

## Tecnologias Utilizadas

- **Python 3.12.6**
- **PySide6**: Interface gráfica.
- **Pandas**: Manipulação de dados e exportação para Excel e CSV.
- **SQLite3**: Banco de dados embutido para armazenar histórico de mudanças.

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/fernandoncidade/File_Manager
    cd File_Manager
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. **Execute o aplicativo**:
    ```bash
    python File_Manager.py
    ```

2. **Selecione um diretório** para monitoramento e clique em "Analisar Diretório" para verificar mudanças.
3. **Exporte os dados** para Excel, CSV ou TXT usando os botões apropriados.
4. **Limpe os dados** da análise usando o botão "Limpar Dados".

## Estrutura do Código

O código consiste na classe `DirectoryAnalyzer`, que cria a interface e define todas as funcionalidades:

- **`initUI()`**: Inicializa a interface com botões e layouts.
- **`create_button()`**: Cria botões com ícones.
- **`init_db()`**: Inicializa o banco de dados SQLite.
- **`select_directory()`**: Seleciona o diretório para análise.
- **`scan_directory()`**: Analisa o estado atual do diretório.
- **`analyze_directory()`**: Compara o estado atual com o anterior e detecta mudanças.
- **Funções `detect_*`**: Detectam arquivos adicionados, modificados, renomeados e excluídos.
- **Funções `export_to_*`**: Exportam os dados para arquivos Excel, CSV ou TXT.
- **`clear_data()`**: Limpa o banco de dados.

## Exemplo de Código

```python
# Inicia a aplicação
app = QApplication(sys.argv)
analyzer = DirectoryAnalyzer()
analyzer.show()
sys.exit(app.exec())
```

## Dependências

- `pandas`
- `sqlite3`
- `PySide6`
