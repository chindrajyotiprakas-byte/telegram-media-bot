@echo off

cd /d "%~dp0"

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activate venv...
call venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Starting Bot...
python bot.py
pause
