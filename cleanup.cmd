@echo off
chcp 65001 >nul
title Backdoor Cleanup - Rudeps

echo ================================
echo    Backdoor Cleanup Tool
echo        Rudeps Research
echo ================================
echo.

cd src

python cleanup-backdoor.py

pause