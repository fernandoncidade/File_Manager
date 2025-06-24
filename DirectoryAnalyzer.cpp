#include "DirectoryAnalyzer.h"
#include <QApplication>
#include <QCoreApplication>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QFileDialog>
#include <QLabel>
#include <QSpacerItem>
#include <QSqlQuery>
#include <QSqlDatabase>
#include <QSqlError>
#include <QDateTime>
#include <QDir>
#include <QDebug>
#include <QIcon>
#include <QFile>
#include <QTextStream>
//#include "libxl.h"
//#include <string>


DirectoryAnalyzer::DirectoryAnalyzer(QWidget *parent) : QWidget(parent) {
    initUI();
    current_directory = "";
}

void DirectoryAnalyzer::initUI() {
        setWindowTitle("Analisador de Diretórios");
        setWindowIcon(QIcon("icones/manager_files1.png"));
        setGeometry(100, 100, 1000, 500);

        QHBoxLayout *layout = new QHBoxLayout(this);

        QVBoxLayout *layout_1 = new QVBoxLayout();
        layout_1->addSpacerItem(new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding));

        QHBoxLayout *layout_h_1 = new QHBoxLayout();
        QLabel *label_selecione = new QLabel("Selecionar Diretório:", this);
        layout_h_1->addWidget(label_selecione);

        QPushButton *select_button = create_button("");
        select_button->setIcon(QIcon("C:/Users/ferna/PROJETOS/Projetos_CPP/File-Folder-Manager/File_Manager/cmake-build-debug/icones/selecione.png"));
        connect(select_button, &QPushButton::clicked, this, &DirectoryAnalyzer::select_directory);
        layout_h_1->addWidget(select_button);
        layout_1->addLayout(layout_h_1);

        QHBoxLayout *layout_h_2 = new QHBoxLayout();
        QLabel *label_analyze = new QLabel("Analisar Diretório:", this);
        layout_h_2->addWidget(label_analyze);

        QPushButton *analyze_button = create_button("");
        analyze_button->setIcon(QIcon("C:/Users/ferna/PROJETOS/Projetos_CPP/File-Folder-Manager/File_Manager/cmake-build-debug/icones/analyze.png"));
        connect(analyze_button, &QPushButton::clicked, this, &DirectoryAnalyzer::analyze_directory);
        layout_h_2->addWidget(analyze_button);
        layout_1->addLayout(layout_h_2);
        /*
        QHBoxLayout *layout_h_3 = new QHBoxLayout();
        QLabel *label_export_excel = new QLabel("Exportar para Excel:", this);
        layout_h_3->addWidget(label_export_excel);

        QPushButton *export_excel_button = create_button("");
        export_excel_button->setIcon(QIcon("C:/Users/ferna/PROJETOS/Projetos_CPP/File-Folder-Manager/File_Manager/cmake-build-debug/icones/xlsx.png"));
        connect(export_excel_button, &QPushButton::clicked, this, &DirectoryAnalyzer::export_to_excel);
        layout_h_3->addWidget(export_excel_button);
        layout_1->addLayout(layout_h_3);
        */
        QHBoxLayout *layout_h_4 = new QHBoxLayout();
        QLabel *label_export_csv = new QLabel("Exportar para CSV:", this);
        layout_h_4->addWidget(label_export_csv);

        QPushButton *export_csv_button = create_button("");
        export_csv_button->setIcon(QIcon("C:/Users/ferna/PROJETOS/Projetos_CPP/File-Folder-Manager/File_Manager/cmake-build-debug/icones/csv.png"));
        connect(export_csv_button, &QPushButton::clicked, this, &DirectoryAnalyzer::export_to_csv);
        layout_h_4->addWidget(export_csv_button);
        layout_1->addLayout(layout_h_4);

        QHBoxLayout *layout_h_5 = new QHBoxLayout();
        QLabel *label_export_txt = new QLabel("Exportar para TXT:", this);
        layout_h_5->addWidget(label_export_txt);

        QPushButton *export_txt_button = create_button("");
        export_txt_button->setIcon(QIcon("C:/Users/ferna/PROJETOS/Projetos_CPP/File-Folder-Manager/File_Manager/cmake-build-debug/icones/txt.png"));
        connect(export_txt_button, &QPushButton::clicked, this, &DirectoryAnalyzer::export_to_txt);
        layout_h_5->addWidget(export_txt_button);
        layout_1->addLayout(layout_h_5);

        QHBoxLayout *layout_h_6 = new QHBoxLayout();
        QLabel *label_clear = new QLabel("Limpar Dados:", this);
        layout_h_6->addWidget(label_clear);

        QPushButton *clear_button = create_button("");
        clear_button->setIcon(QIcon("C:/Users/ferna/PROJETOS/Projetos_CPP/File-Folder-Manager/File_Manager/cmake-build-debug/icones/clear.png"));
        connect(clear_button, &QPushButton::clicked, this, &DirectoryAnalyzer::clear_data);
        layout_h_6->addWidget(clear_button);
        layout_1->addLayout(layout_h_6);

        QVBoxLayout *layout_2 = new QVBoxLayout();

        directory_label = new QLabel("Nenhum diretório selecionado:", this);  // Inicializa o label de diretório
        layout_2->addWidget(directory_label);

        result_label = new QLabel("", this);  // Inicializa o label de resultado
        layout_2->addWidget(result_label);

        db_content = new QTableWidget(this);  // Inicializa a tabela de conteúdo
        layout_2->addWidget(db_content);

        layout->addLayout(layout_1);
        layout->addLayout(layout_2);

        setLayout(layout);
        init_db();
    }

    QPushButton* DirectoryAnalyzer::create_button(const QString &text) {
        QPushButton *button = new QPushButton(text, this);
        button->setMinimumWidth(3 * button->fontMetrics().horizontalAdvance('m'));
        button->setMaximumWidth(3 * button->fontMetrics().horizontalAdvance('m'));
        button->setFont(QFont("Arial", 9));
        return button;
    }

    void DirectoryAnalyzer::init_db() {
        db = QSqlDatabase::addDatabase("QSQLITE");
        db.setDatabaseName("C:/Users/ferna/PROJETOS/Projetos_CPP/File-Folder-Manager/File_Manager/directory_changes.db");

        if (!db.open()) {
            qDebug() << "Error: connection with database failed";
        } else {
            qDebug() << "Database: connection ok";
        }

        QSqlQuery query;
        query.exec("CREATE TABLE IF NOT EXISTS changes ("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "tipo TEXT, "
                   "caminho TEXT, "
                   "data_modificacao TEXT, "
                   "tipo_arquivo TEXT)");
    }

    void DirectoryAnalyzer::select_directory() {
        QString directory = QFileDialog::getExistingDirectory(this, "Selecionar Diretório:");
        if (!directory.isEmpty()) {
            current_directory = directory;
            directory_label->setText("Diretório Selecionado: " + directory);
            previous_state = scan_directory(directory);
        }
    }

    QMap<QString, QFileInfo> DirectoryAnalyzer::scan_directory(const QString &directory) {
        QMap<QString, QFileInfo> state;
        QDir dir(directory);
        QFileInfoList list = dir.entryInfoList(QDir::Dirs | QDir::Files | QDir::NoDotAndDotDot, QDir::Name);

        foreach (QFileInfo fileInfo, list) {
            state[fileInfo.absoluteFilePath()] = fileInfo;
        }

        return state;
    }

    void DirectoryAnalyzer::analyze_directory() {
        if (current_directory.isEmpty()) {
            result_label->setText("Por favor, selecione um diretório primeiro.");
            return;
        }

        QMap<QString, QFileInfo> current_state = scan_directory(current_directory);
        QSqlQuery query;

        if (!db.isOpen()) {
            if (!db.open()) {
                qDebug() << "Error: connection with database failed";
                return;
            }
        }

        // Verificar arquivos novos ou modificados
        for (auto it = current_state.begin(); it != current_state.end(); ++it) {
            QString path = it.key();
            QFileInfo fileInfo = it.value();

            if (!previous_state.contains(path)) {
                // Arquivo novo
                query.prepare("INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)");
                query.addBindValue("Novo");
                query.addBindValue(path);
                query.addBindValue(fileInfo.lastModified().toString("yyyy-MM-dd HH:mm:ss"));
                query.addBindValue(fileInfo.isDir() ? "Diretório" : "Arquivo");
                if (!query.exec()) {
                    qDebug() << "Error inserting new file:" << query.lastError();
                }
            } else if (previous_state[path].lastModified() != fileInfo.lastModified()) {
                // Arquivo modificado
                query.prepare("INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)");
                query.addBindValue("Modificado");
                query.addBindValue(path);
                query.addBindValue(fileInfo.lastModified().toString("yyyy-MM-dd HH:mm:ss"));
                query.addBindValue(fileInfo.isDir() ? "Diretório" : "Arquivo");
                if (!query.exec()) {
                    qDebug() << "Error inserting modified file:" << query.lastError();
                }
            }
        }

        // Verificar arquivos deletados
        for (auto it = previous_state.begin(); it != previous_state.end(); ++it) {
            QString path = it.key();
            if (!current_state.contains(path)) {
                // Arquivo deletado
                query.prepare("INSERT INTO changes (tipo, caminho, data_modificacao, tipo_arquivo) VALUES (?, ?, ?, ?)");
                query.addBindValue("Deletado");
                query.addBindValue(path);
                query.addBindValue(QDateTime::currentDateTime().toString("yyyy-MM-dd HH:mm:ss"));
                query.addBindValue(it.value().isDir() ? "Diretório" : "Arquivo");
                if (!query.exec()) {
                    qDebug() << "Error inserting deleted file:" << query.lastError();
                }
            }
        }

        previous_state = current_state;
        load_db_content();
    }

    void DirectoryAnalyzer::load_db_content() {
        QSqlQuery query("SELECT tipo, caminho, data_modificacao, tipo_arquivo FROM changes");
        db_content->setRowCount(0); // Clear existing rows
        db_content->setColumnCount(4);
        db_content->setHorizontalHeaderLabels({"Tipo", "Caminho", "Data de modificação", "Tipo de arquivo"});

        int row = 0;
        while (query.next()) {
            db_content->insertRow(row);
            for (int col = 0; col < 4; ++col) {
                db_content->setItem(row, col, new QTableWidgetItem(query.value(col).toString()));
            }
            ++row;
        }
    }
    /*
    void DirectoryAnalyzer::export_to_xlsx() {
        QString directory = QFileDialog::getExistingDirectory(this, "Selecionar Diretório para Salvar");
        if (!directory.isEmpty()) {
            QString file_path = directory + "/directory_changes_export.xlsx";

            // Inicializa o livro de trabalho Excel
            libxl::Book* book = xlCreateBook();
            if (book) {
                // Cria a planilha
                libxl::Sheet* sheet = book->addSheet(L"Changes");
                if (sheet) {
                    // Define cabeçalhos
                    sheet->writeStr(0, 0, L"Tipo");
                    sheet->writeStr(0, 1, L"Caminho");
                    sheet->writeStr(0, 2, L"Data de Modificação");
                    sheet->writeStr(0, 3, L"Tipo de Arquivo");

                    // Carrega dados do banco e insere na planilha
                    QSqlQuery query("SELECT tipo, caminho, data_modificacao, tipo_arquivo FROM changes");
                    int row = 1;
                    while (query.next()) {
                        sheet->writeStr(row, 0, query.value(0).toString().toStdWString().c_str());
                        sheet->writeStr(row, 1, query.value(1).toString().toStdWString().c_str());
                        sheet->writeStr(row, 2, query.value(2).toString().toStdWString().c_str());
                        sheet->writeStr(row, 3, query.value(3).toString().toStdWString().c_str());
                        ++row;
                    }
                } else {
                    qDebug() << "Erro ao criar a planilha.";
                }
                // Salva o arquivo Excel no caminho especificado
                if (book->save(file_path.toStdWString().c_str())) {
                    qDebug() << "Arquivo Excel salvo com sucesso em:" << file_path;
                } else {
                    qDebug() << "Erro ao salvar arquivo Excel."; // Removido o método error()
                }
                book->release(); // Liberar o livro após salvar
            } else {
                qDebug() << "Erro ao criar o livro.";
            }
        }
    }
    */
    void DirectoryAnalyzer::export_to_csv() {
        QString directory = QFileDialog::getExistingDirectory(this, "Selecionar Diretório para Salvar");
        if (!directory.isEmpty()) {
            QString file_path = directory + "/directory_changes_export.csv";
            QFile file(file_path);
            if (file.open(QIODevice::WriteOnly)) {
                QTextStream stream(&file);
                stream << "Tipo,Caminho,Data de modificação,Tipo de arquivo\n";

                QSqlQuery query("SELECT tipo, caminho, data_modificacao, tipo_arquivo FROM changes");
                while (query.next()) {
                    stream << query.value(0).toString() << ","
                           << query.value(1).toString() << ","
                           << query.value(2).toString() << ","
                           << query.value(3).toString() << "\n";
                }
                file.close();
            }
        }
    }

    void DirectoryAnalyzer::export_to_txt() {
        QString directory = QFileDialog::getExistingDirectory(this, "Selecionar Diretório para Salvar");
        if (!directory.isEmpty()) {
            QString file_path = directory + "/directory_changes_export.txt";
            QFile file(file_path);
            if (file.open(QIODevice::WriteOnly)) {
                QTextStream stream(&file);
                stream << "Tipo\tCaminho\tData de modificação\tTipo de arquivo\n";

                QSqlQuery query("SELECT tipo, caminho, data_modificacao, tipo_arquivo FROM changes");
                while (query.next()) {
                    stream << query.value(0).toString() << "\t"
                           << query.value(1).toString() << "\t"
                           << query.value(2).toString() << "\t"
                           << query.value(3).toString() << "\n";
                }
                file.close();
            }
        }
    }

    void DirectoryAnalyzer::clear_data() {
        db_content->setRowCount(0);
        QSqlQuery query;
        query.exec("DELETE FROM changes");
    }

    QString format_time(qint64 timestamp) {
        return QDateTime::fromSecsSinceEpoch(timestamp).toString("yyyy-MM-dd HH:mm:ss");
    }
