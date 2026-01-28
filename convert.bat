@echo off
title LemonPyHub EXE Builder
color 0B

:: Set project path
set PROJECT_DIR=E:\LemonPy\LemonPyHubDebloat
set SCRIPT_NAME=LemonPyHubDebloat.py
set APP_NAME=LemonPyHub_Windows_Debloater_Privacy
set ICON_NAME=lemon.ico
set VERSION_FILE=file_version_info.txt

cd /d "%PROJECT_DIR%"

echo ====================================================
echo   BUILDING: %APP_NAME% WITH METADATA
echo ====================================================
echo.

:: Run PyInstaller
:: --version-file : Menyuntik maklumat Details (Version, Description, etc)
pyinstaller --noconsole --onefile --uac-admin ^
    --icon="%ICON_NAME%" ^
    --version-file="%VERSION_FILE%" ^
    --name "%APP_NAME%" ^
    "%SCRIPT_NAME%"

echo.
echo ====================================================
echo   BUILD COMPLETE!
echo   Sila semak tab 'Details' pada file Properties.
echo ====================================================
pause