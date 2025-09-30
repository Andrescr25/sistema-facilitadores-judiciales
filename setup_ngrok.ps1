# Script para instalar y configurar ngrok
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  INSTALACION DE NGROK - ACCESO DESDE INTERNET" -ForegroundColor White
Write-Host "============================================================`n" -ForegroundColor Cyan

# Verificar si ngrok ya esta instalado
$ngrokPath = "$env:USERPROFILE\ngrok.exe"

if (Test-Path $ngrokPath) {
    Write-Host "OK - ngrok ya esta instalado`n" -ForegroundColor Green
} else {
    Write-Host "Descargando ngrok..." -ForegroundColor Yellow
    
    # Descargar ngrok
    $downloadUrl = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
    $zipPath = "$env:TEMP\ngrok.zip"
    
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath -UseBasicParsing
        Write-Host "OK - Descarga completada`n" -ForegroundColor Green
        
        # Extraer ngrok
        Write-Host "Extrayendo ngrok..." -ForegroundColor Yellow
        Expand-Archive -Path $zipPath -DestinationPath $env:USERPROFILE -Force
        Remove-Item $zipPath
        Write-Host "OK - ngrok instalado en: $ngrokPath`n" -ForegroundColor Green
    } catch {
        Write-Host "ERROR al descargar ngrok: $_" -ForegroundColor Red
        Write-Host "`nDescarga manual desde: https://ngrok.com/download`n" -ForegroundColor Yellow
        exit 1
    }
}

# Instrucciones para obtener authtoken
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "`nPASOS PARA CONFIGURAR NGROK:`n" -ForegroundColor Yellow

Write-Host "1. Registrate en ngrok (GRATIS):" -ForegroundColor White
Write-Host "   https://dashboard.ngrok.com/signup`n" -ForegroundColor Cyan

Write-Host "2. Inicia sesion y copia tu Authtoken:" -ForegroundColor White
Write-Host "   https://dashboard.ngrok.com/get-started/your-authtoken`n" -ForegroundColor Cyan

Write-Host "3. Ejecuta este comando con tu token:" -ForegroundColor White
Write-Host "   cd $env:USERPROFILE" -ForegroundColor Gray
Write-Host "   .\ngrok.exe config add-authtoken TU_TOKEN_AQUI`n" -ForegroundColor Green

Write-Host "4. Inicia el tunel:" -ForegroundColor White
Write-Host "   .\ngrok.exe http 8501`n" -ForegroundColor Green

Write-Host "============================================================`n" -ForegroundColor Cyan

# Abrir pagina de registro
Write-Host "Abriendo pagina de registro de ngrok..." -ForegroundColor Yellow
Start-Process "https://dashboard.ngrok.com/signup"

Write-Host "`nOK - Instalacion completada. Sigue los pasos de arriba.`n" -ForegroundColor Green