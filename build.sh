#!/bin/bash
# Build script for local testing

echo "Building for current platform..."

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build using spec file
pyinstaller Steamulation.spec

echo "Build complete! Binary is in dist/ folder"
