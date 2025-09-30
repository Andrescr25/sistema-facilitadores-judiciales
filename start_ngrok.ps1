# Script para iniciar ngrok y exponer Chat FJ a internet
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  INICIANDO TUNEL NGROK - CHAT FJ PUBLICO" -ForegroundColor White
Write-Host "============================================================`n" -ForegroundColor Cyan

$ngrokPath = "$env:USERPROFILE\ngrok.exe"

# Verificar si ngrok esta instalado
if (-not (Test-Path $ngrokPath)) {
    Write-Host "ERROR: ngrok no esta instalado" -ForegroundColor Red
    Write-Host "Ejecuta: .\setup_ngrok.ps1`n" -ForegroundColor Yellow
    exit 1
}

# Verificar si el servidor esta corriendo
Write-Host "Verificando si el servidor esta corriendo..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8501" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
    Write-Host "OK - Servidor detectado en puerto 8501`n" -ForegroundColor Green
} catch {
    Write-Host "ADVERTENCIA: El servidor no parece estar corriendo" -ForegroundColor Yellow
    Write-Host "Asegurate de ejecutar: python inicio.py`n" -ForegroundColor Yellow
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Iniciando tunel ngrok..." -ForegroundColor Yellow
Write-Host "Presiona Ctrl+C para detener el tunel" -ForegroundColor Gray
Write-Host "============================================================`n" -ForegroundColor Cyan

# Iniciar ngrok
& $ngrokPath http 8501
