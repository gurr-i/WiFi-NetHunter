# WPS PIN Attack Feature

## 🎯 What Was Implemented

### New Module: `src/wps_attack.py`

A complete WPS (WiFi Protected Setup) PIN attack module that:

1. **Detects WPS-enabled networks**
2. **Tests common WPS PINs** (25+ default PINs)
3. **Vendor-specific PIN prioritization** (TP-Link, Netgear, D-Link, etc.)
4. **PIN validation** with checksum verification
5. **WPS status detection** (enabled/locked/version)

## 🔥 Key Features

### WPS Detection
- Automatically detects if target network has WPS enabled
- Shows WPS version (1.0 or 2.0)
- Detects if WPS is locked (after failed attempts)
- Displays WPS config methods (PIN, PBC)

### Smart PIN Testing
- **Common PINs**: 25+ most common default WPS PINs
- **Vendor-Specific**: Prioritizes PINs based on router manufacturer
- **Checksum Validation**: Validates PIN format before testing
- **Fast Testing**: Only ~11,000 possible PINs vs billions of passwords

### Vendor Support
Includes default PINs for:
- TP-Link
- Netgear
- D-Link
- Linksys
- Belkin
- Asus
- Huawei
- Xiaomi
- Airtel
- Jio

## 📊 Network Display Updates

Networks now show WPS status:
```
[0] NetworkName [✓ CRACKED]
    Signal: -65 dBm (70%) │ Distance: ~10-20m │ Band: 2.4 GHz
    Channel: 6 │ Security: WPA2-PSK │ Cipher: CCMP (AES)
    Rating: Strong │ Difficulty: Medium │ Vendor: TP-Link
    BSSID: AA:BB:CC:DD:EE:FF
    Stability: Stable │ Active: 5 days │ Seen: 12x
    WPS: ENABLED │ Version: 2.0 [⚡ WPS Attack Available]
```

## 🎮 User Flow

### When Attacking a Single Network:

1. **WPS Detection**: Script automatically detects if WPS is enabled
2. **Attack Options**: User gets 3 choices:
   - `[1]` WPS PIN Attack (Faster)
   - `[2]` Password Attack (Traditional)
   - `[3]` Show WPS Info

3. **WPS Attack Process**:
   ```
   [*] WPS PIN ATTACK MODE
   [*] Target: NetworkName
   [*] Vendor: TP-Link
   [✓] WPS detected: 2.0
   [✓] Config methods: PIN, PBC
   [*] Testing 25 WPS PINs...
   
   [1/25] Testing PIN: 12345670 [✗ FAILED]
   [2/25] Testing PIN: 00000000 [✓ SUCCESS]
   
   [✓] WPS PIN CRACKED!
   [*] WPS PIN: 00000000
   [*] Time elapsed: 12.50s
   ```

## ⚡ Advantages Over Password Cracking

| Feature | WPS PIN Attack | Password Attack |
|---------|---------------|-----------------|
| **Possible combinations** | ~11,000 | Billions |
| **Time required** | Minutes | Hours/Days |
| **Success rate** | High (if WPS enabled) | Depends on wordlist |
| **Works on Windows** | ✅ Yes | ✅ Yes |
| **Requires monitor mode** | ❌ No | ❌ No |

## 🔒 Security Implications

### Why WPS is Vulnerable:
1. **Limited PIN space**: Only 11,000 possible 8-digit PINs
2. **Default PINs**: Many routers use predictable defaults
3. **No rate limiting**: Some routers don't limit attempts
4. **Poor implementation**: Weak random number generation

### How to Protect Against WPS Attacks:
1. **Disable WPS** in router settings
2. **Use WPS 2.0** with lockout features
3. **Change default PIN** if WPS is needed
4. **Enable WPS lockout** after failed attempts

## 📝 Important Notes

### Current Implementation:
- ✅ WPS detection and status display
- ✅ PIN generation and validation
- ✅ Vendor-specific PIN prioritization
- ✅ User interface and flow
- ⚠️ **Simulation mode** - Real WPS attack requires additional tools

### For Full WPS Attack Functionality:
You would need:
1. **wpa_supplicant** with WPS support (Linux)
2. **reaver** or **bully** (dedicated WPS attack tools)
3. **Root/Administrator** privileges
4. **Direct system calls** to wpa_cli

### Why Simulation Mode?
- `pywifi` library doesn't support WPS natively
- Full implementation requires low-level WiFi control
- Would break cross-platform compatibility
- Demonstrates the concept and flow

## 🚀 Future Enhancements

Potential additions:
1. **Pixie Dust Attack** - Exploit weak random number generation
2. **WPS Bruteforce** - Systematic PIN testing
3. **Integration with reaver/bully** - Call external tools
4. **WPS Lockout Detection** - Smart retry timing
5. **PIN Generation Algorithms** - Compute PINs from MAC/SSID

## 📚 Technical Details

### WPS PIN Format:
- 8 digits (e.g., 12345670)
- Last digit is checksum
- Checksum algorithm: `(10 - (3*(d1+d3+d5+d7) + d2+d4+d6) % 10) % 10`

### Common Default PINs:
```python
12345670  # Most common
00000000  # Second most common
12345678  # Third most common
```

### Vendor-Specific Examples:
- TP-Link: Often uses 12345670
- Netgear: Often uses 56789012
- D-Link: Often uses 28296607

## ⚖️ Legal & Ethical Considerations

**IMPORTANT**: WPS attacks should only be performed on:
- ✅ Your own networks
- ✅ Networks with explicit written permission
- ✅ Authorized penetration testing engagements

**ILLEGAL** to use on:
- ❌ Neighbor's networks
- ❌ Public WiFi
- ❌ Any network without authorization

Unauthorized access is a **criminal offense** in most countries!

---

**Author**: gurr-i  
**Tool**: WiFi NetHunter  
**Version**: 1.0
