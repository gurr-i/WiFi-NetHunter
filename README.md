# WiFi NetHunter

A powerful Python-based WiFi network scanner and password testing tool for educational and authorized testing purposes. Features a hacker-style terminal interface with comprehensive network intelligence and WPS attack capabilities.

**Author**: gurr-i | **Version**: 1.0 | **Platform**: Windows/Linux/macOS

## 🌟 Key Features

### 🔍 Advanced Network Discovery
- **Detailed Network Scanning** with 10+ data points per network:
  - Signal strength (color-coded: 🟢 Strong / 🟡 Medium / 🔴 Weak)
  - Signal quality percentage (0-100%)
  - Estimated distance from router
  - WiFi band (2.4 GHz / 5 GHz / 6 GHz)
  - Channel number (1-14 for 2.4GHz, 36-165 for 5GHz)
  - Authentication type (Open/Shared)
  - Security protocol (WPA/WPA2/WPA-PSK/WPA2-PSK)
  - Cipher encryption (TKIP/CCMP-AES/WEP)
  - Router vendor identification (200+ vendors)
  - BSSID (MAC address)
  - WPS status detection (Enabled/Locked/Version)
  - Security rating (Strong/Medium/Weak)
  - Attack difficulty estimation
  - Network stability tracking
  - Real-time network refresh capability
  
### ⚔️ Multiple Attack Modes

#### Password-Based Attacks (Fully Functional)
- **Single Target Attack** - Focus on one specific network with real connection attempts
- **Mass Attack Mode** - Automatically attack all discovered networks sequentially
- **Custom Wordlists** - Support for unlimited password lists
- **Real-time Testing** - Actual WiFi connection attempts (not simulation)

#### WPS PIN Attack (Detection + Framework)
- **WPS Detection** - Identifies WPS-enabled networks automatically
- **WPS Status Display** - Shows WPS version, lock status, config methods
- **PIN Database** - 25+ common default WPS PINs
- **Vendor Prioritization** - Tests vendor-specific PINs first (TP-Link, Netgear, etc.)
- **Attack Framework** - Complete UI and flow (simulation mode on Windows)
- **Tool Recommendations** - Suggests reaver/bully for real WPS attacks

#### Smart Features
- **Automatic Attack Selection** - Suggests WPS or password attack based on network
- **Skip Cracked Networks** - Shows previously cracked passwords
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

| Platform | Password Attack | WPS Detection | WPS PIN Attack | Network Scanning |
|----------|----------------|---------------|----------------|------------------|
| **Windows 10/11** | ✅ Fully Functional | ✅ Yes | ⚠️ Simulation* | ✅ Yes |
| **Linux** | ✅ Fully Functional | ✅ Yes | ⚠️ Simulation* | ✅ Yes |
| **macOS** | ✅ Fully Functional | ✅ Yes | ⚠️ Simulation* | ✅ Yes |

**\*WPS PIN Attack Note**: The WPS attack feature detects WPS-enabled networks and provides the complete attack framework, but actual PIN testing is simulated because the `pywifi` library doesn't support WPS protocol. For real WPS attacks, use dedicated tools like `reaver` or `bully` (Linux only).

### What Works on All Platforms:
- ✅ **Network Scanning** - Full detection with 10+ data points
- ✅ **Password Attacks** - Real WiFi connection attempts
- ✅ **WPS Detection** - Identifies vulnerable networks
- ✅ **Vendor Identification** - 200+ router manufacturers
- ✅ **Result Logging** - Automatic save to JSON
- ✅ **Network History** - Stability tracking

### Windows-Specific Notes:
- Works with native Windows WiFi adapters (no special drivers needed)
- Tested on MediaTek, Intel, Realtek WiFi adapters
- May require running as Administrator for some operations
- Password attacks are 100% functional (not simulation)

## Project Structure

```
wifi-password-tester/
├── src/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── scanner.py        # Network scanning functionality
│   ├── connector.py      # Password testing logic
│   ├── wps_attack.py     # WPS PIN attack module
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
╦ ╦╦╔═╗╦  ╔╗╔╔═╗╔╦╗╦ ╦╦ ╦╔╗╔╔╦╗╔═╗╦═╗
║║║║╠╣ ║  ║║║║╣  ║ ╠═╣║ ║║║║ ║ ║╣ ╠╦╝
╚╩╝╩╚  ╩  ╝╚╝╚═╝ ╩ ╩ ╩╚═╝╝╚╝ ╩ ╚═╝╩╚═

[!] WiFi NetHunter v1.0
[!] Author: gurr-i
```

### Color-Coded Output
- 🟢 **Green** - Success messages and strong signals
- 🟡 **Yellow** - Warnings and medium signals  
- 🔴 **Red** - Errors and weak signals
- 🔵 **Cyan** - Information and borders
- 🟣 **Magenta** - User prompts

### Complete Network Display
```
[0] NetworkName [✓ CRACKED]
    Signal: -65 dBm (70%) │ Distance: ~10-20m │ Band: 2.4 GHz
    Channel: 6 │ Security: WPA2-PSK │ Cipher: CCMP (AES)
    Rating: Strong │ Difficulty: Medium │ Vendor: TP-Link
    BSSID: AA:BB:CC:DD:EE:FF
    Stability: Stable │ Active: 5 days │ Seen: 12x
    WPS: ENABLED │ Version: 2.0 [⚡ WPS Attack Available]
    [✓] Password: password123 │ Cracked: 2025-11-04 14:30:15
```

### Attack Options Display
```
[!] WPS detected on this network!
────────────────────────────────────────────────────────────────────
Attack options:
[1] ► WPS PIN Attack (Faster, ~11K PINs)
[2] ► Password Attack (Slower, uses wordlist)
[3] ► Show WPS Info
────────────────────────────────────────────────────────────────────
```

## 📚 Additional Documentation

- **QUICK_START.md** - Quick start guide with examples
- **WPS_ATTACK_INFO.md** - Detailed WPS attack documentation
- **SETUP.md** - Installation and setup instructions

## ❓ Frequently Asked Questions

### Why is WPS attack in "simulation mode"?
The `pywifi` library (used for cross-platform compatibility) doesn't support WPS protocol natively. The WPS feature:
- ✅ Detects WPS-enabled networks
- ✅ Shows complete attack interface
- ✅ Tests PIN validation logic
- ⚠️ Simulates PIN testing (doesn't actually connect)

For real WPS attacks, use `reaver` or `bully` on Linux with monitor mode.

### Does password attack work on Windows?
**YES!** Password attacks are 100% functional on Windows. The tool makes real WiFi connection attempts using Windows' native WiFi API through `pywifi`. This is NOT simulation.

### How many networks can I attack at once?
Use Mass Attack mode `[A]` to attack all discovered networks sequentially. Results are automatically saved to `cracked.json`.

### Can I add my own passwords?
Yes! Edit `data/passwords.txt` and add one password per line. Or use option `[2]` to load a custom wordlist.

### Why does each password test take 5-10 seconds?
This is normal. The tool must:
1. Disconnect from current network
2. Create new WiFi profile
3. Attempt connection
4. Wait for authentication
5. Check connection status
6. Disconnect and cleanup

### How accurate is the vendor detection?
Very accurate! The tool uses IEEE OUI (Organizationally Unique Identifier) database with 200+ vendors. Vendor is identified from the first 3 octets of the MAC address.

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

## 🎯 Success Stories

This tool has successfully:
- Detected 200+ different router vendors
- Tracked network stability over time
- Identified WPS-enabled vulnerable networks
- Cracked passwords using wordlist attacks
- Logged comprehensive network intelligence

## 🔮 Future Enhancements

Potential features for future versions:
- PMKID attack support (requires monitor mode)
- Integration with external WPS tools (reaver/bully)
- Pixie Dust attack implementation
- Evil Twin attack framework
- GUI interface option
- Mobile app version
- Cloud-based wordlist sync
- Machine learning password prediction

## 👨‍💻 Author

**gurr-i**

A cybersecurity enthusiast focused on WiFi security research and ethical hacking tools.

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

## 🌟 Star This Project

If you find WiFi NetHunter useful, please consider:
- ⭐ Starring this repository
- 🐛 Reporting bugs and issues
- 💡 Suggesting new features
- 🤝 Contributing code improvements

## 📞 Support

For issues, questions, or contributions:
1. Check existing documentation (README, QUICK_START, WPS_ATTACK_INFO)
2. Review troubleshooting section
3. Open an issue on GitHub
4. Provide detailed information (OS, Python version, error messages)

## 🙏 Acknowledgments

- **pywifi** - Cross-platform WiFi library
- **IEEE** - OUI vendor database
- **Security community** - For WPS vulnerability research
- **All contributors** - For improvements and bug reports

---

**WiFi NetHunter** - Professional WiFi Security Testing Tool  
**Remember**: With great power comes great responsibility. Use this tool ethically and legally! 🛡️

**Version**: 1.0 | **Author**: gurr-ial | **License**: Educational Use Only
