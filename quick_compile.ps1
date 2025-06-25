# Compilação rápida com g++
$env:PATH = "C:\Qt\Tools\mingw1310_64\bin;C:\Qt\6.9.1\mingw_64\bin;$env:PATH"

# Executar MOC
C:\Qt\6.9.1\mingw_64\bin\moc.exe DirectoryAnalyzer.h -o moc_DirectoryAnalyzer.cpp

# Compilar
g++.exe -std=c++20 -IC:\Qt\6.9.1\mingw_64\include -IC:\Qt\6.9.1\mingw_64\include\QtCore -IC:\Qt\6.9.1\mingw_64\include\QtGui -IC:\Qt\6.9.1\mingw_64\include\QtWidgets -IC:\Qt\6.9.1\mingw_64\include\QtSql -DQT_CORE_LIB -DQT_GUI_LIB -DQT_WIDGETS_LIB -DQT_SQL_LIB File_Manager.cpp DirectoryAnalyzer.cpp moc_DirectoryAnalyzer.cpp -LC:\Qt\6.9.1\mingw_64\lib -lQt6Core -lQt6Gui -lQt6Widgets -lQt6Sql -o File_Manager.exe

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Sucesso! Executando..." -ForegroundColor Green
    .\File_Manager.exe
} else {
    Write-Host "❌ Erro na compilação!" -ForegroundColor Red
}
