@echo off
title TenderLatexPro Enhanced v3.0 - One-Click Setup and Run
color 0A

echo.
echo ================================================
echo   TenderLatexPro Enhanced v3.0 Setup Utility
echo ================================================
echo   An Initiative by Mrs. Premlata Jain
echo   Additional Administrative Officer, PWD, Udaipur
echo ================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Close any existing instances
echo [1/8] Closing existing instances...
taskkill /f /im "streamlit.exe" >nul 2>&1
taskkill /f /im "python.exe" /fi "windowtitle eq streamlit*" >nul 2>&1
timeout /t 2 >nul

REM Close browsers if running
echo [2/8] Closing browsers...
taskkill /f /im "firefox.exe" >nul 2>&1
taskkill /f /im "chrome.exe" >nul 2>&1
taskkill /f /im "msedge.exe" >nul 2>&1
timeout /t 2 >nul

REM Check Python installation
echo [3/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.9+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [4/8] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        echo Trying to install virtualenv...
        pip install virtualenv
        virtualenv venv
    )
) else (
    echo [4/8] Virtual environment already exists, skipping...
)

REM Activate virtual environment
echo [5/8] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Upgrade pip and install dependencies
echo [6/8] Installing/upgrading dependencies...
python -m pip install --upgrade pip setuptools wheel

REM Check for requirements file and install dependencies
if exist "pyproject.toml" (
    echo Installing from pyproject.toml...
    pip install -e .
) else if exist "requirements.txt" (
    echo Installing from requirements.txt...
    pip install -r requirements.txt
) else (
    echo Installing core dependencies...
    pip install streamlit pandas openpyxl plotly pymupdf psutil sqlalchemy pydantic jinja2 reportlab pillow python-docx
)

if errorlevel 1 (
    echo WARNING: Some dependencies may have failed to install.
    echo The application may still work with basic functionality.
    echo Check the output above for details.
    timeout /t 5
)

REM Initialize directories and database
echo [7/8] Initializing application...
if not exist "logs" mkdir logs
if not exist "outputs" mkdir outputs
if not exist "temp" mkdir temp
if not exist "cache" mkdir cache
if not exist "exports" mkdir exports
if not exist "backup" mkdir backup

REM Initialize database
echo Initializing database...
python -c "
try:
    from database_manager import DatabaseManager
    db = DatabaseManager()
    db.initialize_database()
    print('Database initialized successfully')
except ImportError:
    print('Database manager not found, will initialize on first run')
except Exception as e:
    print(f'Database initialization warning: {e}')
" 2>nul

REM Configure Git if available
echo Configuring Git...
git config user.email "crajkumarsingh@hotmail.com" 2>nul
git config user.name "RAJKUMAR SINGH CHAUHAN" 2>nul

echo [8/8] Starting TenderLatexPro Enhanced...
echo.
echo ================================================
echo Application is starting...
echo.
echo Once loaded, the application will open in your
echo default web browser at: http://localhost:8501
echo.
echo To stop the application, close this window or
echo press Ctrl+C in the terminal.
echo ================================================
echo.

REM Start the application with optimal settings
streamlit run app.py ^
    --server.port 8501 ^
    --server.headless false ^
    --server.runOnSave true ^
    --server.maxUploadSize 50 ^
    --server.enableCORS false ^
    --browser.gatherUsageStats false ^
    --theme.primaryColor "#4CAF50" ^
    --theme.backgroundColor "#FFFFFF" ^
    --theme.secondaryBackgroundColor "#F0F2F6"

REM If we reach here, the application has stopped
echo.
echo ================================================
echo TenderLatexPro Enhanced has been stopped.
echo Thank you for using our application!
echo.
echo An Initiative by Mrs. Premlata Jain
echo Additional Administrative Officer, PWD, Udaipur
echo ================================================
echo.
pause
