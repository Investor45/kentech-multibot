@echo off
echo Starting Kentech Bot Pairing Application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Change to the application directory
cd /d "%~dp0"

REM Check if virtual environment exists and activate it
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    set PYTHON_CMD=python
) else if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    set PYTHON_CMD=python
) else (
    echo No virtual environment found, using system Python...
    set PYTHON_CMD=python
)

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing dependencies...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy ".env.example" ".env"
)

REM Create logs directory
if not exist "logs" (
    mkdir logs
)

echo.
echo Starting the application...
echo You can access the API at: http://localhost:8000
echo Health check: http://localhost:8000/health
echo API documentation: http://localhost:8000/docs
echo.

%PYTHON_CMD% run_app.py

pause
