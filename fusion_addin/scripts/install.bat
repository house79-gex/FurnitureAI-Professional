@echo off
REM FurnitureAI Professional - Windows Installation Script

echo ======================================
echo FurnitureAI Professional v3.0 - Installer
echo ======================================
echo.

echo Detecting Fusion 360 installation...

set ADDINS_PATH=%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns

if not exist "%ADDINS_PATH%" (
    echo Warning: Fusion 360 AddIns directory not found
    echo Creating directory...
    mkdir "%ADDINS_PATH%"
)

echo AddIns path: %ADDINS_PATH%
echo.

set ADDON_SOURCE=%~dp0..
set ADDON_DEST=%ADDINS_PATH%\FurnitureAI

echo Installing addon...

REM Remove old installation
if exist "%ADDON_DEST%" (
    echo Removing old installation...
    rmdir /s /q "%ADDON_DEST%"
)

echo Copying files...
xcopy /E /I /Y "%ADDON_SOURCE%" "%ADDON_DEST%"

echo.
echo ======================================
echo Installation completed successfully!
echo ======================================
echo.
echo Next steps:
echo 1. Launch Fusion 360
echo 2. Go to TOOLS ^> ADD-INS ^> Scripts and Add-Ins
echo 3. Select 'FurnitureAI' and click 'Run'
echo.
echo For AI features, install:
echo - LM Studio (https://lmstudio.ai) for LLM
echo.
echo Documentation: %ADDON_DEST%\docs\
echo.
pause
