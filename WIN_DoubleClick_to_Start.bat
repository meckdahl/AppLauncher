@echo off
REM ============================================================================
REM Claude App Launcher - Easy Setup for Windows
REM ============================================================================

cd /d "%~dp0"

REM Check if already set up (marker file exists)
if exist ".launcher_ready" goto :quick_launch

REM ============================================================================
REM FIRST TIME SETUP
REM ============================================================================
color 0A
cls
echo.
echo ============================================================================
echo                   Claude App Launcher - First Time Setup
echo ============================================================================
echo.
echo Checking your system... Please wait...
echo.

REM ============================================================================
REM STEP 1: Check Python
REM ============================================================================
echo [Step 1 of 3] Checking for Python...

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo [X] Python is NOT installed.
    echo.
    echo ============================================================================
    echo   ACTION REQUIRED: Install Python
    echo ============================================================================
    echo.
    echo Please install Python manually:
    echo.
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.8 or newer
    echo 3. Run the installer
    echo 4. IMPORTANT: Check the box "Add Python to PATH"
    echo 5. After installation, run this file again
    echo.
    echo ============================================================================
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM ============================================================================
REM STEP 2: Install UV (fast installer)
REM ============================================================================
echo [Step 2 of 3] Setting up fast package installer...

python -m pip install --upgrade pip --quiet >nul 2>&1

uv --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Installing UV...
    python -m pip install uv --quiet >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        echo [OK] UV installed
    ) else (
        echo [OK] Using standard installer
    )
) else (
    echo [OK] UV ready
)

REM ============================================================================
REM STEP 3: Check files and folders
REM ============================================================================
echo [Step 3 of 3] Checking files...

if not exist "launcher.py" (
    echo.
    echo [X] ERROR: launcher.py is missing!
    echo.
    echo ============================================================================
    echo   The main app file is not in this folder.
    echo ============================================================================
    echo.
    echo This probably means:
    echo - Incomplete download from GitHub
    echo - Files extracted to wrong location
    echo - File was accidentally deleted
    echo.
    echo SOLUTION: Download the complete files from GitHub again
    echo.
    echo ============================================================================
    echo.
    pause
    exit /b 1
)

if not exist "projects" mkdir projects >nul 2>&1

echo [OK] All files present
echo.

REM Create marker file to skip setup next time
echo setup_complete > .launcher_ready

echo ============================================================================
echo   Setup Complete!
echo ============================================================================
echo.
goto :run_app

:quick_launch
REM ============================================================================
REM QUICK LAUNCH (already set up)
REM ============================================================================
cls
echo.
echo ============================================================================
echo                   Claude App Launcher
echo ============================================================================
echo.

:run_app
echo Starting Claude App Launcher...
echo.

REM Launch in a new window so this one can close
start "Claude App Launcher" python launcher.py

REM Wait a moment
timeout /t 1 /nobreak >nul

echo App window should open shortly...
echo This window will close in 3 seconds...
timeout /t 3 /nobreak >nul

exit
