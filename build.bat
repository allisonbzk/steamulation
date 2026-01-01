@echo off
REM Build script for local Windows testing

echo Building for Windows...

REM Install dependencies
pip install -r requirements.txt
pip install pyinstaller

REM Build using spec file
pyinstaller SteamEmulatorStation.spec

echo Build complete! Binary is in dist\ folder
pause
