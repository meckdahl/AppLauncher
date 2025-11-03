#!/bin/bash
################################################################################
# Claude App Launcher - Easy Setup for Mac/Linux
################################################################################

# Change to script directory
cd "$(dirname "$0")"

# Check if already set up (marker file exists)
if [ -f ".launcher_ready" ]; then
    # Quick launch - already set up
    clear
    echo ""
    echo "============================================================================"
    echo "                   Claude App Launcher"
    echo "============================================================================"
    echo ""
    echo "Starting app..."
    echo ""
    
    # Determine Python command
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        echo "Error: Python 3 not found"
        read -p "Press Enter to close..."
        exit 1
    fi
    
    # Launch the app in background
    $PYTHON_CMD launcher.py &
    
    sleep 1
    echo "App window should open shortly..."
    echo ""
    echo "This terminal will close in 3 seconds..."
    sleep 3
    exit 0
fi

################################################################################
# FIRST TIME SETUP
################################################################################

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

clear
echo ""
echo "============================================================================"
echo "                   Claude App Launcher - First Time Setup"
echo "============================================================================"
echo ""
echo "Checking your system... Please wait..."
echo ""

################################################################################
# Detect OS
################################################################################
OS_TYPE="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="mac"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
fi

################################################################################
# STEP 1: Check Python
################################################################################
echo -e "${BLUE}[Step 1 of 3]${NC} Checking for Python..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}[OK]${NC} Python $PYTHON_VERSION found"
else
    echo ""
    echo -e "${RED}[X] Python 3 is NOT installed.${NC}"
    echo ""
    echo "============================================================================"
    echo "  ACTION REQUIRED: Install Python"
    echo "============================================================================"
    echo ""
    
    if [ "$OS_TYPE" = "mac" ]; then
        echo "For Mac:"
        echo "1. Go to: https://www.python.org/downloads/"
        echo "2. Download Python 3.8 or newer for macOS"
        echo "3. Install it"
        echo "4. Run this file again"
        echo ""
        echo "OR use Homebrew:"
        echo "  brew install python3"
    else
        echo "For Linux (Ubuntu/Debian):"
        echo "  sudo apt-get update"
        echo "  sudo apt-get install python3 python3-pip python3-tk"
        echo ""
        echo "For Linux (Fedora):"
        echo "  sudo dnf install python3 python3-pip python3-tkinter"
    fi
    
    echo ""
    echo "============================================================================"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

################################################################################
# STEP 2: Install UV
################################################################################
echo -e "${BLUE}[Step 2 of 3]${NC} Setting up fast package installer..."

$PYTHON_CMD -m pip install --upgrade pip --quiet 2>/dev/null

if command -v uv &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} UV ready"
else
    $PYTHON_CMD -m pip install uv --quiet 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK]${NC} UV installed"
    else
        echo -e "${GREEN}[OK]${NC} Using standard installer"
    fi
fi

################################################################################
# STEP 3: Check files and folders
################################################################################
echo -e "${BLUE}[Step 3 of 3]${NC} Checking files..."

if [ ! -f "launcher.py" ]; then
    echo ""
    echo -e "${RED}[X] ERROR: launcher.py is missing!${NC}"
    echo ""
    echo "============================================================================"
    echo "  The main app file is not in this folder."
    echo "============================================================================"
    echo ""
    echo "This probably means:"
    echo "- Incomplete download from GitHub"
    echo "- Files extracted to wrong location"
    echo "- File was accidentally deleted"
    echo ""
    echo "SOLUTION: Download the complete files from GitHub again"
    echo ""
    echo "============================================================================"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

if [ ! -d "projects" ]; then
    mkdir -p projects 2>/dev/null
fi

echo -e "${GREEN}[OK]${NC} All files present"
echo ""

# Create marker file to skip setup next time
echo "setup_complete" > .launcher_ready

echo "============================================================================"
echo "  Setup Complete!"
echo "============================================================================"
echo ""

################################################################################
# Launch the app
################################################################################
echo "Starting Claude App Launcher..."
echo ""

# Launch the app in background
$PYTHON_CMD launcher.py &

# Wait a moment
sleep 2

echo ""
echo "============================================================================"
echo "  App Started!"
echo "============================================================================"
echo ""
echo "App window should open shortly..."
echo ""
echo "This terminal will close in 3 seconds..."
sleep 3
