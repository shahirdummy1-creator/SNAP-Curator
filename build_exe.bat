@echo off
cd /d "%~dp0"
"C:/Users/User/.VIRTUALENVS/DJANGO_PROJECT-7L90E9FR/Scripts/pyinstaller.exe" --noconfirm --console --onefile --name SNAP-Curator run_app.py
pause
