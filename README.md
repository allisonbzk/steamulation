# Steam Emulator Station

A Python tool with a PyQt5 wizard GUI to add emulator ROMs as non-Steam games in Steam, with full artwork support.

## Features
- **Wizard UI**: Step-by-step interface for emulator and ROM configuration
- **Automatic Platform Detection**: Recognizes popular emulators (Yuzu, PCSX2, RPCS3, etc.)
- **ROM Scanning**: Recursively scans folders for game files
- **Custom Launch Options**: Configure with `#rom` placeholder for ROM path
- **Full Artwork Suite**: Fetches 5 types from SteamGridDB:
  - Portrait grid (600x900)
  - Landscape grid (920x430)
  - Hero/background (1920x620)
  - Icon (library view)
  - Logo overlay
- **Collection Management**: Automatically adds games to platform collections
- **Multi-User Support**: Configure shortcuts for multiple Steam accounts

## Quick Start

### Download Binary (Recommended)
1. Download the latest release for your platform:
   - **Windows**: `SteamEmulatorStation.exe`
   - **Linux/Steam Deck**: `SteamEmulatorStation`
2. Run the executable
3. Follow the wizard

### Run from Source
```bash
pip install -r requirements.txt
python main.py
```

## Building from Source

### Local Build
**Windows:**
```cmd
build.bat
```

**Linux/Steam Deck:**
```bash
chmod +x build.sh
./build.sh
```

Binary will be in `dist/` folder.

### GitHub Actions
Push a tag to automatically build and release binaries for both platforms:
```bash
git tag v1.0.0
git push origin v1.0.0
```

Binaries will be attached to the GitHub release.

## Configuration

### SteamGridDB API Key
To enable artwork fetching:
1. Get a free API key: https://www.steamgriddb.com/profile/preferences/api
2. Enter it in the "Icon Options" page of the wizard
3. Check "Fetch game icons from SteamGridDB"

### Launch Options
Use `#rom` as a placeholder for the ROM file path. Examples:
- Default: `#rom`
- Yuzu: `-f -g #rom`
- PCSX2: `#rom --fullscreen`

## Requirements
- Python 3.8+
- PyQt5
- vdf (Valve Data Format library)
- requests (for SteamGridDB API)

## Notes
- **Close Steam** before running to avoid file conflicts
- Only base versions ([v0]) of ROMs are processed to avoid duplicates
- Icons appear in shortcuts.vdf and artwork in the grid folder
- Restart Steam after adding shortcuts to see changes

## Platform Support
Tested on:
- Windows 10/11
- Steam Deck (Linux)
