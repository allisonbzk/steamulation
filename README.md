# Steam Emulator Station

A Python tool with a PyQt5 wizard GUI to add emulator ROMs as non-Steam games in Steam.

## Features
- Wizard UI: Select emulator .exe, ROMs folder, and platform name
- Scans ROMs folder for games
- Adds each ROM as a non-Steam game shortcut in Steam (shortcuts.vdf)
- Optionally fetches icons from SteamGridDB
- Can overwrite existing shortcuts for that platform

## Requirements
- Python 3.8+
- PyQt5
- vdf (Valve Data Format library)
- requests (for icon fetching)

## Setup
1. Install dependencies:
   pip install -r requirements.txt
2. Run the tool:
   python main.py

## Notes
- Make sure Steam is closed before running the tool (to avoid overwriting issues with shortcuts.vdf).
- The tool will guide you through the process step by step.
