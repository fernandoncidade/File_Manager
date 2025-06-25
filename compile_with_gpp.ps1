# Script para compilar com g++ diretamente (sem CMake)
# Este script configura todos os caminhos e bibliotecas necessárias para Qt

$QT_PATH = "C:\Qt\6.9.1\mingw_64"
$MINGW_PATH = "C:\Qt\Tools\mingw1310_64"

# Configurar PATH
$env:PATH = "$MINGW_PATH\bin;$QT_PATH\bin;$env:PATH"

# Parâmetros de compilação
$SOURCE_FILES = @(
    "File_Manager.cpp",
    "DirectoryAnalyzer.cpp"
)

$INCLUDE_PATHS = @(
    "-I$QT_PATH\include",
    "-I$QT_PATH\include\QtCore",
    "-I$QT_PATH\include\QtGui", 
    "-I$QT_PATH\include\QtWidgets",
    "-I$QT_PATH\include\QtSql"
)

$DEFINES = @(
    "-DQT_CORE_LIB",
    "-DQT_GUI_LIB",
    "-DQT_WIDGETS_LIB", 
    "-DQT_SQL_LIB",
    "-DUNICODE",
    "-D_UNICODE"
)

$LIBRARY_PATHS = @(
    "-L$QT_PATH\lib"
)

$LIBRARIES = @(
    "-lQt6Core",
    "-lQt6Gui",
    "-lQt6Widgets",
    "-lQt6Sql"
)

$CXX_FLAGS = @(
    "-Wall",
    "-Wextra", 
    "-std=c++20",
    "-fPIC"
)

$OUTPUT = "output\File_Manager.exe"

# Criar diretório de saída se não existir
if (!(Test-Path "output")) {
    New-Item -ItemType Directory -Path "output"
}

Write-Host "🔨 Compilando com g++ diretamente..." -ForegroundColor Green

# Primeiro passo: Executar MOC nos arquivos de cabeçalho
Write-Host "📝 Executando MOC..." -ForegroundColor Yellow
& "$QT_PATH\bin\moc.exe" DirectoryAnalyzer.h -o moc_DirectoryAnalyzer.cpp

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro no MOC!" -ForegroundColor Red
    exit 1
}

# Adicionar arquivo MOC gerado
$SOURCE_FILES += "moc_DirectoryAnalyzer.cpp"

# Construir comando de compilação
$COMMAND = @("$MINGW_PATH\bin\g++.exe") + $CXX_FLAGS + $INCLUDE_PATHS + $DEFINES + $SOURCE_FILES + $LIBRARY_PATHS + $LIBRARIES + @("-o", $OUTPUT)

Write-Host "📋 Comando: " -ForegroundColor Cyan
Write-Host ($COMMAND -join " ") -ForegroundColor Gray

# Executar compilação
Write-Host "▶️ Executando compilação..." -ForegroundColor Yellow
Start-Process -FilePath $COMMAND[0] -ArgumentList ($COMMAND[1..($COMMAND.Length-1)]) -Wait -NoNewWindow

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Compilação bem-sucedida!" -ForegroundColor Green
    Write-Host "📁 Executável criado em: $OUTPUT" -ForegroundColor Green
    
    # Perguntar se quer executar
    $run = Read-Host "🚀 Executar a aplicação? (s/n)"
    if ($run -eq "s" -or $run -eq "S") {
        Write-Host "🚀 Iniciando a aplicação..." -ForegroundColor Cyan
        Start-Process -FilePath ".\$OUTPUT" -Wait
    }
} else {
    Write-Host "❌ Erro na compilação!" -ForegroundColor Red
    
    # Limpar arquivo MOC em caso de erro
    if (Test-Path "moc_DirectoryAnalyzer.cpp") {
        Remove-Item "moc_DirectoryAnalyzer.cpp"
    }
}
