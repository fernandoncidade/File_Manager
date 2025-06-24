#include "DirectoryAnalyzer.h"
#include <QApplication>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    DirectoryAnalyzer analyzer;
    analyzer.show();
    return app.exec();
}
