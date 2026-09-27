$desktop = [Environment]::GetFolderPath('Desktop')
$target = Join-Path $PSScriptRoot 'launch_app.bat'
$icon = Join-Path $PSScriptRoot 'snap_icon.png'

$wsh = New-Object -ComObject WScript.Shell
$link = $wsh.CreateShortcut((Join-Path $desktop 'SNAP Curator.lnk'))
$link.TargetPath = $target
$link.WorkingDirectory = $PSScriptRoot
$link.IconLocation = "$icon, 0"
$link.Description = 'SNAP Curator desktop launcher'
$link.Save()

Write-Output "Created desktop shortcut: $desktop\SNAP Curator.lnk"
