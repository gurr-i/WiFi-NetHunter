# WiFi NetHunter - Quick Start Guide

## 🚀 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the tool
python run.py
```

## 🎯 Basic Usage

### 1. Scan Networks
The tool automatically scans for WiFi networks when started.

### 2. Choose Your Mode
After scanning, you have 3 options:
- **[R]** Refresh - Rescan networks
- **[S]** Single - Attack one network
- **[A]** All - Attack all networks

### 3. Select Target
Choose a network by number (0-9)

### 4. Choose Attack Method

#### If WPS is Detected:
```
[1] ► WPS PIN Attack (Faster, ~11K PINs)
[2] ► Password Attack (Slower, uses wordlist)
[3] ► Show WPS Info
```

#### Password Attack Options:
```
[1] ► Use default wordlist (data/passwords.txt)
[2] ► Load custom wordlist
[3] ► Manual password entry
```

## 📊 Understanding Network Information

### Network Display Example:
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

### What Each Field Means:

| Field | Description |
|-------|-------------|
| **Signal** | Strength in dBm (higher = better) |
| **Signal %** | Quality percentage (0-100%) |
| **Distance** | Estimated distance from router |
| **Band** | 2.4 GHz or 5 GHz |
| **Channel** | WiFi channel number |
| **Security** | Encryption type (WPA2-PSK, etc.) |
| **Cipher** | Encryption cipher (CCMP/AES, TKIP) |
| **Rating** | Security strength (Strong/Medium/Weak) |
| **Difficulty** | Attack difficulty estimate |
| **Vendor** | Router manufacturer |
| **BSSID** | MAC address of router |
| **Stability** | How long network has been active |
| **WPS** | WPS status (Enabled/Locked) |
| **[✓ CRACKED]** | Previously cracked (password saved) |

## 🎨 Color Coding

- 🟢 **Green** - Success, strong signal, stable network
- 🟡 **Yellow** - Warning, medium signal, moderate stability
- 🔴 **Red** - Error, weak signal, failed attempts
- 🔵 **Cyan** - Information, data values
- 🟣 **Magenta** - User prompts, BSSID

## ⚡ Attack Methods

### WPS PIN Attack
**Best for**: Networks with WPS enabled  
**Speed**: Fast (~11,000 possible PINs)  
**Success Rate**: High if WPS enabled  
**Time**: Minutes

**Advantages:**
- Much faster than password cracking
- Only ~11K combinations vs billions
- Vendor-specific PIN prioritization

**Limitations:**
- Only works if WPS is enabled
- Some routers lock WPS after failures
- Simulation mode (needs reaver/bully for real attacks)

### Password Attack
**Best for**: Networks without WPS or when WPS fails  
**Speed**: Depends on wordlist size  
**Success Rate**: Depends on password strength  
**Time**: Minutes to hours

**Advantages:**
- Works on all networks
- Can use custom wordlists
- Real implementation (not simulation)

**Limitations:**
- Slower than WPS
- Requires good wordlist
- May take long time

### Mass Attack
**Best for**: Testing multiple networks  
**Speed**: Depends on number of networks  
**Success Rate**: Varies per network  
**Time**: Extended

**Advantages:**
- Automated testing of all networks
- Comprehensive coverage
- Saves all results to cracked.json

## 📁 Files Generated

### cracked.json
Stores all successfully cracked passwords:
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

### network_history.json
Tracks network stability and history:
```json
{
  "networks": {
    "NetworkName_AA:BB:CC:DD:EE:FF": {
      "ssid": "NetworkName",
      "bssid": "AA:BB:CC:DD:EE:FF",
      "first_seen": "2025-11-01 10:00:00",
      "last_seen": "2025-11-04 14:30:15",
      "seen_count": 12,
      "stability": "Stable",
      "days_active": 3
    }
  }
}
```

## 💡 Tips & Tricks

### 1. Signal Strength Matters
- **Strong (-50 to -60 dBm)**: Best for attacks
- **Medium (-60 to -70 dBm)**: Good success rate
- **Weak (-70+ dBm)**: May fail or take longer

### 2. WPS is Your Friend
- Always try WPS first if available
- Much faster than password cracking
- Check if network shows "WPS: ENABLED"

### 3. Use Good Wordlists
- Default list has common passwords
- Add custom passwords to data/passwords.txt
- One password per line

### 4. Check Cracked Networks
- Networks with [✓ CRACKED] already have saved passwords
- Password shown in network display
- Saved in cracked.json

### 5. Vendor Information
- Helps prioritize WPS PINs
- Shows router manufacturer
- Useful for vulnerability research

## 🔧 Troubleshooting

### No Networks Found
- Ensure WiFi is enabled
- Move closer to access points
- Try refreshing scan

### WPS Attack Not Working
- WPS might be locked
- Try password attack instead
- Wait 60+ minutes if locked

### Slow Connection Testing
- Normal - each test takes 5-10 seconds
- Be patient with large wordlists
- Consider using WPS if available

### Permission Errors (Linux)
```bash
sudo python3 run.py
```

## ⚖️ Legal Notice

**IMPORTANT**: Only test networks you own or have explicit permission to test!

✅ **Legal Uses:**
- Your own home network
- Networks with written authorization
- Authorized penetration testing

❌ **Illegal Uses:**
- Neighbor's networks
- Public WiFi
- Any unauthorized network

**Unauthorized access is a criminal offense!**

## 🆘 Need Help?

1. Check WPS_ATTACK_INFO.md for WPS details
2. Read README.md for full documentation
3. Review SETUP.md for installation help

---

**Author**: gurr-i 
**Tool**: WiFi NetHunter  
**Version**: 1.0

Happy (legal) hacking! 🎯
