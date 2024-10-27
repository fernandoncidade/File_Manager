README.

---

# DirectoryAnalyzer

## Descrição

O `DirectoryAnalyzer` é uma aplicação em Python com interface gráfica (GUI) criada com PySide6, que permite ao usuário monitorar alterações em um diretório, como adição, exclusão, modificação e renomeação de arquivos e pastas. O aplicativo exibe essas informações e permite exportar os dados para arquivos Excel, CSV e TXT, além de armazenar um histórico das alterações em um banco de dados SQLite.

## Funcionalidades

- **Seleção de Diretório**: Escolha um diretório para monitoramento.
- **Análise de Diretório**: Analisa as mudanças (arquivos adicionados, modificados, renomeados e excluídos).
- **Exportação de Dados**: Exporta as informações de mudanças para arquivos Excel, CSV ou TXT.
- **Limpeza de Dados**: Limpa o histórico atual de mudanças.

## Tecnologias Utilizadas

- **Python 3**
- **PySide6**: Interface gráfica.
- **Pandas**: Manipulação de dados e exportação para Excel e CSV.
- **SQLite3**: Banco de dados embutido para armazenar histórico de mudanças.

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/username/DirectoryAnalyzer.git
    cd DirectoryAnalyzer
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. **Execute o aplicativo**:
    ```bash
    python main.py
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