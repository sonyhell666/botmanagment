param(
    [Parameter(Mandatory = $false)]
    [string]$ServerIp = "62.60.247.114",

    [string]$User = "root"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$RemoteDir = "/opt/botmanagment"

Write-Host "Подготовка директории на $User@${ServerIp}..."
ssh "${User}@${ServerIp}" "mkdir -p $RemoteDir/deploy"

Write-Host "Копирование файлов..."
scp "$ProjectRoot\main.py" `
    "$ProjectRoot\config.py" `
    "$ProjectRoot\handlers.py" `
    "$ProjectRoot\states.py" `
    "$ProjectRoot\keyboards.py" `
    "$ProjectRoot\requirements.txt" `
    "${User}@${ServerIp}:${RemoteDir}/"

scp "$ProjectRoot\deploy\install.sh" `
    "$ProjectRoot\deploy\bot.service" `
    "${User}@${ServerIp}:${RemoteDir}/deploy/"

Write-Host "Установка и запуск..."
ssh "${User}@${ServerIp}" "cd $RemoteDir && chmod +x deploy/install.sh && bash deploy/install.sh"

Write-Host "Готово. Проверка: ssh ${User}@${ServerIp} 'systemctl status botmanagment'"
