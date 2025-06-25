@echo off
echo Compilando com g++ diretamente...

REM Configurar PATH
set PATH=C:\Qt\Tools\mingw1310_64\bin;C:\Qt\6.9.1\mingw_64\bin;%PATH%

REM Criar diretório de saída
if not exist output mkdir output

echo Executando MOC...
C:\Qt\6.9.1\mingw_64\bin\moc.exe DirectoryAnalyzer.h -o moc_DirectoryAnalyzer.cpp

if not %ERRORLEVEL%==0 (
    echo Erro no MOC!
    pause
    exit /b 1
)

echo Compilando com g++...
g++.exe -std=c++20 -Wall -Wextra -IC:\Qt\6.9.1\mingw_64\include -IC:\Qt\6.9.1\mingw_64\include\QtCore -IC:\Qt\6.9.1\mingw_64\include\QtGui -IC:\Qt\6.9.1\mingw_64\include\QtWidgets -IC:\Qt\6.9.1\mingw_64\include\QtSql -DQT_CORE_LIB -DQT_GUI_LIB -DQT_WIDGETS_LIB -DQT_SQL_LIB -DUNICODE -D_UNICODE File_Manager.cpp DirectoryAnalyzer.cpp moc_DirectoryAnalyzer.cpp -LC:\Qt\6.9.1\mingw_64\lib -lQt6Core -lQt6Gui -lQt6Widgets -lQt6Sql -o output\File_Manager.exe

if %ERRORLEVEL%==0 (
    echo Compilacao bem-sucedida!
    echo Executavel criado em: output\File_Manager.exe
    
    set /p run="Executar a aplicacao? (s/n): "
    if /i "%run%"=="s" (
        echo Iniciando a aplicacao...
        output\File_Manager.exe
    )
) else (
    echo Erro na compilacao!
    if exist moc_DirectoryAnalyzer.cpp del moc_DirectoryAnalyzer.cpp
)

pause
