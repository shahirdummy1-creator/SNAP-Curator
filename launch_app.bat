@echo off
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set PYTHON=".venv\Scripts\python.exe"
) else if exist "%USERPROFILE%\.virtualenvs\DJANGO_PROJECT-7L90E9FR\Scripts\python.exe" (
    set PYTHON="%USERPROFILE%\.virtualenvs\DJANGO_PROJECT-7L90E9FR\Scripts\python.exe"
) else (
    set PYTHON=py -3
)

start "" http://localhost:8512
%PYTHON% run_app.py
