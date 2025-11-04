# WiFi Password Tester

A powerful Python-based WiFi network scanner and password testing tool for educational and authorized testing purposes. Features a hacker-style terminal interface with comprehensive network intelligence.

## 🌟 Key Features

### 🔍 Advanced Network Discovery
- **Detailed Network Scanning** with comprehensive information:
  - Signal strength (color-coded: 🟢 Strong / 🟡 Medium / 🔴 Weak)
  - Authentication type (Open/Shared)
  - Security protocol (WPA/WPA2/WPA-PSK/WPA2-PSK)
  - Cipher encryption (TKIP/CCMP-AES/WEP)
  - Real-time network refresh capability
  
### ⚔️ Multiple Attack Modes
- **Single Target Attack** - Focus on one specific network
- **Mass Attack Mode** - Automatically attack all discovered networks sequentially
- **Smart Cipher Detection** - Automatically infers encryption type from security protocol

### 📝 Password Sources
- **Default Wordlist** - Automatically loads from `data/passwords.txt`
- **Custom Wordlist** - Load any external password file
- **Manual Entry** - Test a specific password instantly

### 💾 Intelligent Results Logging
- **Automatic JSON Logging** to `cracked.json`
- Stores comprehensive data:
  - Network SSID
  - Cracked password
  - Signal strength
  - Security type
  - Timestamp
  - Time elapsed
  - Number of attempts
- **Smart Updates** - Automatically updates if same network is cracked again

### 🎨 User Experience
- **Hacker-Style Interface** with ASCII art and color-coded output
- **Real-time Progress Tracking** with attempt counters
- **Password Masking** for security during testing
- **Animated Scanning** with visual feedback
- **Comprehensive Error Handling** with helpful messages
- **Keyboard Interrupt Support** (Ctrl+C to cancel anytime)

## 💻 Platform Support

✅ **Windows** (Tested on Windows 10/11)  
✅ **Linux** (Ubuntu, Debian, Kali, etc.)  
✅ **macOS** (with compatible WiFi adapter)

**Note**: This tool works on Windows with native WiFi adapters!

## Project Structure

```
wifi-password-tester/
├── src/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── scanner.py        # Network scanning functionality
│   ├── connector.py      # Password testing logic
│   ├── utils.py          # Helper functions
│   └── vendors.py        # MAC address vendor database (200+ vendors)
├── data/
│   └── passwords.txt     # Sample password list
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── run.py               # Quick run script
```

## 🚀 Installation

### Quick Install (All Platforms)

1. **Clone or download this repository**
```bash
git clone <repository-url>
cd wifi-password-tester
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

### Windows Installation
```powershell
# Install Python from python.org (if not installed)
# Then run:
pip install -r requirements.txt
```

### Linux Installation
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
```

### macOS Installation
```bash
brew install python3
pip3 install -r requirements.txt
```

## 🎯 Usage

### Quick Start

**Windows:**
```powershell
python run.py
```

**Linux/macOS:**
```bash
python3 run.py
# or with sudo if needed
sudo python3 run.py
```

### Alternative Methods
```bash
# Using module
python -m src.main

# Direct execution
python src/main.py
```

## 📖 How to Use

### 1. Network Discovery
- Script automatically scans for available WiFi networks
- Displays detailed information (signal, security, cipher)
- Networks are color-coded by signal strength

### 2. Choose Your Mode

After scanning, select an option:

| Option | Description |
|--------|-------------|
| **[R]** Refresh | Rescan networks to update the list |
| **[S]** Single Target | Select and attack one specific network |
| **[A]** Mass Attack | Attack all discovered networks sequentially |

### 3. Select Password Source

| Option | Description |
|--------|-------------|
| **[1]** Default Wordlist | Automatically loads `data/passwords.txt` |
| **[2]** Custom Wordlist | Provide path to your password file (one per line) |
| **[3]** Manual Entry | Test a specific password |

### 4. View Results

- **Real-time progress** with attempt counters
- **Success notification** with password and statistics
- **Automatic logging** to `cracked.json`

### 📊 Results File (cracked.json)

All cracked passwords are automatically saved with:
```json
{
  "cracked_networks": [
    {
      "ssid": "NetworkName",
      "password": "password123",
      "signal_strength": -65,
      "auth_type": "WPA2-PSK",
      "cracked_at": "2025-11-04 14:30:15",
      "time_elapsed": "45.23s",
      "attempts": 17
    }
  ]
}
```

## 📋 Requirements

- **Python 3.7+** (Python 3.8+ recommended)
- **pywifi library** (automatically installed via requirements.txt)
- **WiFi adapter** (built-in or external)
- **Operating System**: 
  - Windows 10/11 ✅
  - Linux (any distribution) ✅
  - macOS ✅

### Windows-Specific Notes
- Works with native Windows WiFi adapters (no special drivers needed)
- May require running as Administrator for some operations
- Tested on MediaTek, Intel, Realtek WiFi adapters

## 🎨 Features Showcase

### Hacker-Style Interface
```
╦ ╦╦╔═╗╦  ╔═╗╦═╗╔═╗╔═╗╦╔═╔═╗╦═╗
║║║║╠╣ ║  ║  ╠╦╝╠═╣║  ╠╩╗║╣ ╠╦╝
╚╩╝╩╚  ╩  ╚═╝╩╚═╩ ╩╚═╝╩ ╩╚═╝╩╚═

[!] WiFi Penetration Testing Tool v1.0
[!] Author: gurr-ial
```

### Color-Coded Output
- 🟢 **Green** - Success messages and strong signals
- 🟡 **Yellow** - Warnings and medium signals  
- 🔴 **Red** - Errors and weak signals
- 🔵 **Cyan** - Information and borders
- 🟣 **Magenta** - User prompts

### Network Display
```
[0] NetworkName                  │ -65 dBm    │ Auth:0
    Signal: -65 dBm │ Auth: 0
    Security: WPA2-PSK │ Cipher: CCMP (AES)
```

## 🛠️ Troubleshooting

### Windows Issues

**"No WiFi interfaces found"**
- Ensure WiFi adapter is enabled in Network Settings
- Try running as Administrator: `Right-click → Run as Administrator`

**"Module not found" error**
```powershell
pip install --upgrade pywifi
```

### Linux Issues

**Permission denied**
```bash
sudo python3 run.py
```

**WiFi adapter not detected**
```bash
# Check WiFi interface
ip link show
# or
iwconfig
```

### General Issues

**Slow connection testing**
- Normal behavior - each password test takes 5-10 seconds
- Reduce wait time in `src/connector.py` (less accurate)

**No networks found**
- Ensure WiFi is enabled
- Move closer to access points
- Try refreshing the scan

## 👨‍💻 Author

**gurr-ial**

## 📄 Legal Notice

⚠️ **WARNING**: This tool is for educational and authorized testing purposes only.

### Legal Requirements
- ✅ Only test on networks **you own**
- ✅ Only test with **explicit written permission**
- ❌ **Unauthorized access to computer networks is ILLEGAL**
- ❌ Violators may face criminal prosecution

### Disclaimer
- Users are **solely responsible** for compliance with local laws and regulations
- This tool is provided "as-is" for educational purposes
- The author assumes no liability for misuse

### Ethical Use
This tool is designed to help:
- Network administrators test their own security
- Security researchers in authorized environments
- Students learning about network security
- Penetration testers with proper authorization

## 📜 License

For educational and authorized testing purposes only.

---

**Remember**: With great power comes great responsibility. Use this tool ethically and legally! 🛡️
