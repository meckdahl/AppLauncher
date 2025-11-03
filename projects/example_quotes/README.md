# Daily Quotes App

Inspirational quotes with automatic API fallback.

## Features

- 💭 Random quotes
- 📋 Copy to clipboard
- 🔄 Automatic fallback between sources
- 🎨 Clean interface

## APIs Used

1. **dummyjson.com** (primary) ✓ Working
2. **quotable.io** (backup)

App uses the working source automatically.

## Dependencies

- `requests>=2.31.0`

## Testing

```bash
python quick_test_api.py
```

From main folder, or:

```bash
cd projects/example_quotes
python test_api.py
```

## Usage

### With Launcher
1. Select "example_quotes"
2. Click "Run Now"
3. Click "New Quote"

### Standalone
```bash
pip install -r requirements.txt
python main.py
```

## Status

✓ **App is working** - dummyjson.com is responding correctly

## Files

```
example_quotes/
├── main.py            # App (uses dummyjson primarily)
├── test_api.py        # API test script
├── requirements.txt   # Dependencies
└── README.md          # This file
```
