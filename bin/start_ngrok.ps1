# Script para iniciar ngrok y exponer Chat FJ a internet
$ngrokPath = "$env:USERPROFILE\ngrok.exe"

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  INICIANDO TUNEL NGROK - CHAT FJ PUBLICO" -ForegroundColor White
Write-Host "============================================================`n" -ForegroundColor Cyan

# Verificar si el servidor esta corriendo
Write-Host "Verificando servidor..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8501" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
    Write-Host "OK - Servidor detectado en puerto 8501`n" -ForegroundColor Green
} catch {
    Write-Host "ADVERTENCIA: El servidor no parece estar corriendo" -ForegroundColor Yellow
    Write-Host "Ejecuta primero: python inicio.py`n" -ForegroundColor Yellow
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Iniciando tunel ngrok..." -ForegroundColor Yellow
Write-Host "Busca la URL publica en la ventana que se abre" -ForegroundColor Gray
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Gray
Write-Host "============================================================`n" -ForegroundColor Cyan

# Iniciar ngrok
& $ngrokPath http 8501
