# Notificação diária do Claudinho (agendada no Agendador de Tarefas do Windows, dias úteis 8h30)
$ErrorActionPreference = 'SilentlyContinue'
$env:PYTHONIOENCODING = 'utf-8'
$painel = Join-Path $PSScriptRoot 'painel.py'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$texto = (& python $painel --texto) -join ' '
if (-not $texto) { $texto = 'Claudinho: abre o Claude pra ver o painel do dia' }
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$esc = [System.Security.SecurityElement]::Escape($texto)
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml("<toast duration='long'><visual><binding template='ToastGeneric'><text>ezeOS, painel do dia</text><text>$esc</text><text>Abre o Claude que eu te passo o que fazer.</text></binding></visual></toast>")
$app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show([Windows.UI.Notifications.ToastNotification]::new($xml))
