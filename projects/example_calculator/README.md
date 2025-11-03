# Example Calculator App

A simple GUI calculator demonstrating how to structure apps for the Claude App Launcher.

## Features

- Basic arithmetic operations (+, -, *, /)
- Clean GUI interface
- Clear and backspace functions
- Decimal support

## Running This App

### Using Claude App Launcher (Recommended)
1. This app is already in the `projects` folder
2. Open the Claude App Launcher
3. Select "example_calculator" from the list
4. Click "▶ Run Now"

### Using Generated Launcher Script
1. In Claude App Launcher, select this app
2. Click "📄 Create Launcher Script"
3. Double-click `run.sh` (Mac/Linux) or `run.bat` (Windows)

### Manual Run
```bash
cd projects/example_calculator
python main.py
```

## How It Works

This app demonstrates:
- ✅ Standard project structure (main.py as entry point)
- ✅ No external dependencies (uses tkinter - built into Python)
- ✅ Self-contained in its own folder
- ✅ Ready to run with the launcher

## File Structure

```
example_calculator/
├── main.py       # Main application file
└── README.md     # This file
```

## Usage

1. Click number buttons to input numbers
2. Click an operation button (+, -, *, /)
3. Enter the second number
4. Click "=" to see the result
5. Use "C" to clear
6. Use "←" to backspace

---

*This is an example app created to demonstrate the Claude App Launcher system*
