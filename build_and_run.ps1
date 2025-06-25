# Script para compilar e executar o File Manager
# Use este script em vez de g++ diretamente

# Configurar o PATH para incluir as ferramentas Qt
$env:PATH = "C:\Qt\Tools\mingw1310_64\bin;C:\Qt\6.9.1\mingw_64\bin;$env:PATH"

# Navegar para o diretório do projeto
Set-Location "c:\Users\ferna\WORK\Projetos_CPP\File_Manager"

Write-Host "🔨 Compilando o projeto..." -ForegroundColor Green
cmake --build cmake-build-debug

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Compilação bem-sucedida!" -ForegroundColor Green
    Write-Host "🚀 Iniciando a aplicação..." -ForegroundColor Cyan
    .\cmake-build-debug\File_Manager.exe
} else {
    Write-Host "❌ Erro na compilação!" -ForegroundColor Red
}
