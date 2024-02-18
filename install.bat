@echo off
echo Welcome to Jot-client Installation Wizard
echo.
echo This wizard will guide you through the installation process.
echo Press Enter to continue...
pause > nul

REM Step 1: Create Jot-client folder in the Documents directory and copy Jot-client.exe
set "DOCUMENTS_FOLDER=%USERPROFILE%\Documents"
set "JOT_CLIENT_FOLDER=%DOCUMENTS_FOLDER%\Jot-client"
set "EXECUTABLE_PATH=%~dp0\Jot-client.exe"

echo Creating Jot-client folder in the Documents directory...
if not exist "%JOT_CLIENT_FOLDER%" (
    mkdir "%JOT_CLIENT_FOLDER%"
)

echo Copying Jot-client.exe to the Jot-client folder...
copy "%EXECUTABLE_PATH%" "%JOT_CLIENT_FOLDER%" /Y > nul

echo.
echo Jot-client has been successfully installed in the Documents\Jot-client folder.
echo.

REM Step 2: Add Jot-client to startup programs in the registry
set "REG_KEY=HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
set "APP_NAME=Jot-client"

echo Adding Jot-client to startup programs...
reg add "%REG_KEY%" /v "%APP_NAME%" /t REG_SZ /d "\"%JOT_CLIENT_FOLDER%\Jot-client.exe\"" > nul

echo.
echo Jot-client has been added to startup programs.
echo.

REM Step 3: Execute Jot-client.exe
echo Starting Jot-client...
start "" "%JOT_CLIENT_FOLDER%\Jot-client.exe"

echo.
echo Installation is complete. Press any key to exit...
pause > nul
