@echo off
REM Setup script for SEN RAG Assistant on Windows

echo ========================================
echo SEN RAG Assistant - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 from https://www.python.org
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment created
echo.

REM Upgrade pip
echo Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
venv\Scripts\pip.exe install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.

REM Create .env file from template
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo ⚠ Important: Edit .env and add your OpenAI API key
    echo   OPENAI_API_KEY=sk-your_key_here
    echo.
)

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your OpenAI API key
echo 2. Run: streamlit run app.py
echo.
pause
