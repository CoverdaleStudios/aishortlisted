@echo off
REM Double-click to start the Bin Caddie Lead Engine. First run installs what it needs (1-2 minutes).
cd /d "%~dp0"
if exist "lead-engine\requirements.txt" cd lead-engine
where py >nul 2>nul && (set PY=py -3) || (set PY=python)
%PY% --version >nul 2>nul
if errorlevel 1 (
  echo Python 3 is not installed. Install it from https://www.python.org/downloads/
  echo IMPORTANT: tick "Add python.exe to PATH" on the first installer screen. Then double-click this file again.
  start "" https://www.python.org/downloads/
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo First-time setup: installing - this takes a minute or two...
  %PY% -m venv .venv || (echo Could not create the environment. & pause & exit /b 1)
  ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
  ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt || (echo Install failed - check your internet connection. & pause & exit /b 1)
)
".venv\Scripts\python.exe" -m leadengine.cli init >nul
echo Opening http://127.0.0.1:5050 in your browser. Keep this window open while you use it.
".venv\Scripts\python.exe" -m leadengine.cli serve --open
pause
