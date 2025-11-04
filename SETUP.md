# Setup Guide

## Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application

**Option A: Using run.py (Recommended)**
```bash
python run.py
```

**Option B: Using module**
```bash
python -m src.main
```

**Option C: Direct execution**
```bash
python src/main.py
```

## Project Structure

```
wifi-password-tester/
├── src/                    # Source code
│   ├── __init__.py        # Package initialization
│   ├── main.py            # Entry point and main logic
│   ├── scanner.py         # Network scanning
│   ├── connector.py       # Password testing
│   └── utils.py           # Helper functions
├── data/                   # Data files
│   ├── passwords.txt      # Your password list (gitignored)
│   └── passwords_sample.txt  # Sample password list
├── run.py                 # Quick run script
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── SETUP.md              # This file
└── .gitignore            # Git ignore rules
```

## Usage Examples

### Test with default password list
1. Run the application
2. Select a network
3. Choose option 1 (Use default test list)

### Test with custom password file
1. Create or edit `data/passwords.txt` with your passwords (one per line)
2. Run the application
3. Select a network
4. Choose option 2 (Load from file)
5. Enter path: `data/passwords.txt`

### Test single password
1. Run the application
2. Select a network
3. Choose option 3 (Enter single password)
4. Type your password

## Troubleshooting

### No WiFi interfaces found
- Ensure your WiFi adapter is enabled
- Run as administrator (Windows) or with sudo (Linux)

### Module import errors
- Make sure you're running from the project root directory
- Verify Python 3.7+ is installed: `python --version`

### Connection issues
- Some networks may have additional security measures
- Ensure the network is in range (check signal strength)
- Try increasing wait time in connector.py if needed

## Development

### Running from source
```bash
cd wifi-password-tester
python -m src.main
```

### Adding new features
- Scanner logic: Edit `src/scanner.py`
- Connection logic: Edit `src/connector.py`
- Utilities: Edit `src/utils.py`
- Main flow: Edit `src/main.py`
