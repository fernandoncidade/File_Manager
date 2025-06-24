#ifndef DIRECTORYANALYZER_H
#define DIRECTORYANALYZER_H

#include <QWidget>
#include <QMap>
#include <QFileInfo>
#include <QSqlDatabase>
#include <QLabel>
#include <QTableWidget>
#include <QPushButton>

class DirectoryAnalyzer : public QWidget {
    Q_OBJECT

public:
    explicit DirectoryAnalyzer(QWidget *parent = nullptr);

private:
    QString current_directory;
    QMap<QString, QFileInfo> previous_state;
    QSqlDatabase db;

    QLabel *directory_label;
    QLabel *result_label;
    QTableWidget *db_content;

    void initUI();
    QPushButton* create_button(const QString &text);
    void init_db();
    void select_directory();
    QMap<QString, QFileInfo> scan_directory(const QString &directory);
    void analyze_directory();
    void load_db_content();
    //void export_to_xlsx();
    void export_to_csv();
    void export_to_txt();
    void clear_data();
    QString format_time(qint64 timestamp);
};

#endif // DIRECTORYANALYZER_H
