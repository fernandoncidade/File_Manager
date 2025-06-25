# Script para apenas compilar o File Manager
$env:PATH = "C:\Qt\Tools\mingw1310_64\bin;$env:PATH"
Set-Location "c:\Users\ferna\WORK\Projetos_CPP\File_Manager"

Write-Host "🔨 Compilando o projeto..." -ForegroundColor Green
cmake --build cmake-build-debug

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Compilação bem-sucedida!" -ForegroundColor Green
} else {
    Write-Host "❌ Erro na compilação!" -ForegroundColor Red
}
