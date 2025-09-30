# Script para iniciar Chat FJ con acceso publico via ngrok
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  CHAT FJ - INICIO CON ACCESO PUBLICO" -ForegroundColor White
Write-Host "============================================================`n" -ForegroundColor Cyan

$ngrokPath = "$env:USERPROFILE\ngrok.exe"

# Verificar si ngrok esta configurado
if (-not (Test-Path $ngrokPath)) {
    Write-Host "ERROR: ngrok no esta instalado" -ForegroundColor Red
    Write-Host "Ejecuta primero: .\setup_ngrok.ps1`n" -ForegroundColor Yellow
    exit 1
}

# Verificar si ngrok esta configurado con authtoken
$configPath = "$env:USERPROFILE\.ngrok2\ngrok.yml"
if (-not (Test-Path $configPath)) {
    Write-Host "ERROR: ngrok no esta configurado" -ForegroundColor Red
    Write-Host "Ejecuta: .\ngrok.exe config add-authtoken TU_TOKEN`n" -ForegroundColor Yellow
    Write-Host "Obtén tu token en: https://dashboard.ngrok.com/get-started/your-authtoken`n" -ForegroundColor Cyan
    exit 1
}

Write-Host "1. Iniciando servidor Chat FJ..." -ForegroundColor Yellow
$serverProcess = Start-Process -FilePath "python" -ArgumentList "inicio.py" -PassThru -WindowStyle Normal

Write-Host "2. Esperando que el servidor este listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "3. Iniciando tunel ngrok..." -ForegroundColor Yellow
Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "  CHAT FJ ESTA PUBLICO!" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Green
Write-Host "`nBusca la URL en la ventana de ngrok que se abrio" -ForegroundColor Yellow
Write-Host "Algo como: https://abc123.ngrok-free.app`n" -ForegroundColor Cyan
Write-Host "Copia esa URL y usala en cualquier navegador/movil!`n" -ForegroundColor White
Write-Host "Presiona Ctrl+C para detener todo`n" -ForegroundColor Gray

# Iniciar ngrok en nueva ventana
Start-Process -FilePath $ngrokPath -ArgumentList "http 8501" -WindowStyle Normal

# Mantener el script corriendo
try {
    Wait-Process -Id $serverProcess.Id
} catch {
    Write-Host "`nDeteniendo servicios..." -ForegroundColor Yellow
}

# Limpiar procesos al salir
Stop-Process -Name "ngrok" -ErrorAction SilentlyContinue
Write-Host "`nServicios detenidos.`n" -ForegroundColor Green
