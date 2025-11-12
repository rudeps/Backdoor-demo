@echo off
chcp 65001 >nul
title CMD File Selector

echo ========================================
echo        SELECTIVE CMD FILE RUNNER
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not installed or not in PATH!
    echo Install Python and try again.
    pause
    exit /b 1
)

python src\cmd-runner.py

echo.
echo Program finished.
pause