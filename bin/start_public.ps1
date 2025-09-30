# Script para iniciar Chat FJ con acceso publico via ngrok
$ngrokPath = "$env:USERPROFILE\ngrok.exe"

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  CHAT FJ - INICIO CON ACCESO PUBLICO" -ForegroundColor White
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "1. Iniciando servidor Chat FJ..." -ForegroundColor Yellow
$serverProcess = Start-Process -FilePath "python" -ArgumentList "inicio.py" -PassThru -WindowStyle Normal

Write-Host "2. Esperando que el servidor este listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "3. Iniciando tunel ngrok...`n" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  CHAT FJ ESTA PUBLICO!" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Green
Write-Host "`nBusca la URL en la ventana de ngrok" -ForegroundColor Yellow
Write-Host "Ejemplo: https://abc123.ngrok-free.app`n" -ForegroundColor Cyan
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
