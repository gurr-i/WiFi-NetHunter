# WiFi Password Tester

A Python-based WiFi network scanner and password testing tool for educational and authorized testing purposes.

## Features

- **Network Discovery**: Scan and display available WiFi networks with detailed information
  - Signal strength (color-coded)
  - Authentication type
  - Security protocol (WPA/WPA2/WPA-PSK/WPA2-PSK)
  - Cipher type (TKIP/CCMP/WEP)
  - Refresh capability to update network list
  
- **Attack Modes**:
  - Single target attack
  - Mass attack (all networks sequentially)
  
- **Password Sources**:
  - Default wordlist (data/passwords.txt)
  - Custom wordlist file
  - Manual password entry
  
- **Results Logging**:
  - Automatic saving to cracked.json
  - Stores SSID, password, signal strength, security type, timestamp
  - Updates existing entries if network is cracked again
  
- **User Experience**:
  - Real-time connection status monitoring
  - Progress tracking with elapsed time
  - Secure password masking in output
  - Hacker-style terminal interface with colors
  - Comprehensive error handling

## Project Structure

```
wifi-password-tester/
├── src/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── scanner.py        # Network scanning functionality
│   ├── connector.py      # Password testing logic
│   └── utils.py          # Helper functions
├── data/
│   └── passwords.txt     # Sample password list
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── run.py               # Quick run script
```

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start
```bash
python run.py
```

### From Source
```bash
python -m src.main
```

### Attack Modes

After scanning, you can choose:
- **[R] Refresh** - Rescan networks to update the list
- **[S] Single Target** - Select and attack one specific network
- **[A] All Networks** - Attack all discovered networks sequentially

### Password Options

1. **Use default wordlist** - Loads passwords from data/passwords.txt
2. **Load custom wordlist** - Provide path to your password file (one per line)
3. **Manual password entry** - Test a specific password

### Results

All cracked passwords are automatically saved to `cracked.json` with:
- Network SSID
- Password
- Signal strength
- Security type
- Timestamp
- Time elapsed
- Number of attempts

## Requirements

- Python 3.7+
- pywifi library
- Windows/Linux/macOS with WiFi adapter

## Legal Notice

⚠️ **WARNING**: This tool is for educational and authorized testing purposes only.

- Only test on networks you own or have explicit permission to test
- Unauthorized access to computer networks is illegal
- Users are responsible for compliance with local laws and regulations

## License

For educational purposes only.
