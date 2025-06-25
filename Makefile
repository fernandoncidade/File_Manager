# Makefile para compilar o File_Manager com g++ diretamente

# Variáveis
QT_PATH = C:/Qt/6.9.1/mingw_64
MINGW_PATH = C:/Qt/Tools/mingw1310_64
CXX = $(MINGW_PATH)/bin/g++.exe
MOC = $(QT_PATH)/bin/moc.exe

# Flags do compilador
CXXFLAGS = -std=c++20 -Wall -Wextra
INCLUDES = -I$(QT_PATH)/include \
           -I$(QT_PATH)/include/QtCore \
           -I$(QT_PATH)/include/QtGui \
           -I$(QT_PATH)/include/QtWidgets \
           -I$(QT_PATH)/include/QtSql

DEFINES = -DQT_CORE_LIB -DQT_GUI_LIB -DQT_WIDGETS_LIB -DQT_SQL_LIB -DUNICODE -D_UNICODE

LIBPATH = -L$(QT_PATH)/lib
LIBS = -lQt6Core -lQt6Gui -lQt6Widgets -lQt6Sql

# Arquivos fonte
SOURCES = File_Manager.cpp DirectoryAnalyzer.cpp
MOC_SOURCES = moc_DirectoryAnalyzer.cpp
HEADERS = DirectoryAnalyzer.h

# Arquivo de saída
TARGET = output/File_Manager.exe

# Regra padrão
all: $(TARGET)

# Criar diretório de saída
output:
	mkdir output

# Gerar arquivos MOC
moc_DirectoryAnalyzer.cpp: DirectoryAnalyzer.h
	$(MOC) DirectoryAnalyzer.h -o moc_DirectoryAnalyzer.cpp

# Compilar o executável
$(TARGET): $(SOURCES) $(MOC_SOURCES) | output
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(DEFINES) $(SOURCES) $(MOC_SOURCES) $(LIBPATH) $(LIBS) -o $(TARGET)

# Limpar arquivos gerados
clean:
	if exist moc_DirectoryAnalyzer.cpp del moc_DirectoryAnalyzer.cpp
	if exist output rmdir /s /q output

# Executar a aplicação
run: $(TARGET)
	$(TARGET)

# Recompilar tudo
rebuild: clean all

.PHONY: all clean run rebuild
