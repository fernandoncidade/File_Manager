@echo off
echo === COMPILACAO E EXECUCAO QT ===

REM Configurar PATH para Qt e MinGW
set PATH=C:\Qt\Tools\mingw1310_64\bin;C:\Qt\6.9.1\mingw_64\bin;%PATH%

REM Criar diretório output se não existir
if not exist output mkdir output

echo [1/3] Executando MOC...
C:\Qt\6.9.1\mingw_64\bin\moc.exe DirectoryAnalyzer.h -o moc_DirectoryAnalyzer.cpp
if not %ERRORLEVEL%==0 (
    echo ERRO: Falha no MOC!
    exit /b 1
)

echo [2/3] Compilando com g++...
g++.exe -std=c++20 -Wall -Wextra -g ^
    -IC:\Qt\6.9.1\mingw_64\include ^
    -IC:\Qt\6.9.1\mingw_64\include\QtCore ^
    -IC:\Qt\6.9.1\mingw_64\include\QtGui ^
    -IC:\Qt\6.9.1\mingw_64\include\QtWidgets ^
    -IC:\Qt\6.9.1\mingw_64\include\QtSql ^
    -DQT_CORE_LIB -DQT_GUI_LIB -DQT_WIDGETS_LIB -DQT_SQL_LIB ^
    File_Manager.cpp DirectoryAnalyzer.cpp moc_DirectoryAnalyzer.cpp ^
    -LC:\Qt\6.9.1\mingw_64\lib ^
    -lQt6Core -lQt6Gui -lQt6Widgets -lQt6Sql ^
    -o output\File_Manager.exe

if %ERRORLEVEL%==0 (
    echo [3/3] SUCESSO! Executando aplicacao...
    echo.
    output\File_Manager.exe
) else (
    echo ERRO: Falha na compilacao!
    if exist moc_DirectoryAnalyzer.cpp del moc_DirectoryAnalyzer.cpp
    exit /b 1
)
