@echo off
chcp 65001 >nul
title Backdoor Builder - Rudeps

echo ================================
echo    Backdoor Builder - Rudeps
echo ================================
echo.

cd src

python build.py

pause