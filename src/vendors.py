"""MAC address vendor database (OUI - Organizationally Unique Identifier)."""

# Dictionary mapping MAC address prefixes (first 3 octets) to vendor names
# Source: IEEE OUI database and common router manufacturers
MAC_VENDORS = {
    # TP-Link
    "00:0C:42": "TP-Link",
    "00:27:22": "TP-Link",
    "50:C7:BF": "TP-Link",
    "A4:2B:B0": "TP-Link",
    "C0:25:E9": "TP-Link",
    "78:11:DC": "TP-Link",
    "F0:ED:B8": "TP-Link",
    "60:32:B1": "TP-Link",
    "F8:E4:E3": "TP-Link",
    "98:DA:C4": "TP-Link",
    "B0:4E:26": "TP-Link",
    "14:CC:20": "TP-Link",
    "1C:3B:F3": "TP-Link",
    "54:A7:03": "TP-Link",
    "74:DA:88": "TP-Link",
    "84:16:F9": "TP-Link",
    "90:9A:4A": "TP-Link",
    "A0:F3:C1": "TP-Link",
    "B0:95:75": "TP-Link",
    "C4:E9:84": "TP-Link",
    "D8:07:B6": "TP-Link",
    "E8:48:B8": "TP-Link",
    "EC:08:6B": "TP-Link",
    "F4:F2:6D": "TP-Link",
    
    # Netgear
    "00:1B:2F": "Netgear",
    "00:26:F2": "Netgear",
    "A0:63:91": "Netgear",
    "E0:91:F5": "Netgear",
    "00:0F:B5": "Netgear",
    "00:1F:33": "Netgear",
    
    # Linksys
    "00:18:E7": "Linksys",
    "00:1D:7E": "Linksys",
    "68:7F:74": "Linksys",
    
    # D-Link
    "00:24:01": "D-Link",
    "00:26:5A": "D-Link",
    "C8:D3:A3": "D-Link",
    "00:1F:1F": "D-Link",
    "14:D6:4D": "D-Link",
    "28:10:7B": "D-Link",
    "34:08:04": "D-Link",
    "5C:F4:AB": "D-Link",
    "90:94:E4": "D-Link",
    "B8:A3:86": "D-Link",
    "CC:B2:55": "D-Link",
    
    # Apple
    "00:1B:63": "Apple",
    "00:23:DF": "Apple",
    "00:25:00": "Apple",
    "00:26:BB": "Apple",
    "A8:5E:45": "Apple",
    
    # Cisco
    "00:1C:B3": "Cisco",
    "00:40:96": "Cisco",
    "00:0A:41": "Cisco",
    
    # Belkin
    "00:1E:13": "Belkin",
    "00:30:BD": "Belkin",
    "94:44:52": "Belkin",
    
    # Asus
    "00:11:50": "Asus",
    "00:1F:C6": "Asus",
    "04:D4:C4": "Asus",
    "00:22:15": "Asus",
    
    # Huawei
    "00:18:E2": "Huawei",
    "00:25:9E": "Huawei",
    "00:46:4B": "Huawei",
    "00:E0:FC": "Huawei",
    
    # Xiaomi
    "00:0D:B9": "Xiaomi",
    "34:CE:00": "Xiaomi",
    "64:09:80": "Xiaomi",
    
    # Google
    "00:1A:11": "Google",
    "00:1A:8A": "Google",
    "F4:F5:D8": "Google",
    
    # Intel
    "00:13:46": "Intel",
    "00:16:EA": "Intel",
    "00:1F:3C": "Intel",
    "00:21:6A": "Intel",
    "00:24:D7": "Intel",
    "00:02:B3": "Intel",
    "00:03:47": "Intel",
    "00:04:23": "Intel",
    "00:0E:35": "Intel",
    "00:12:F0": "Intel",
    "00:13:02": "Intel",
    "00:13:20": "Intel",
    "00:13:CE": "Intel",
    "00:15:00": "Intel",
    "00:16:76": "Intel",
    "00:19:D2": "Intel",
    "00:1B:77": "Intel",
    "00:1C:BF": "Intel",
    "00:1D:E0": "Intel",
    "00:1E:64": "Intel",
    "00:1E:65": "Intel",
    "00:1E:67": "Intel",
    "00:1F:3A": "Intel",
    "00:21:5C": "Intel",
    "00:21:5D": "Intel",
    "00:21:6B": "Intel",
    "00:22:FA": "Intel",
    "00:23:14": "Intel",
    "00:23:15": "Intel",
    "00:24:D6": "Intel",
    "00:26:C6": "Intel",
    "00:26:C7": "Intel",
    "00:27:10": "Intel",
    "00:27:0E": "Intel",
    "00:50:F1": "Intel",
    
    # Realtek
    "00:1E:58": "Realtek",
    "00:E0:4C": "Realtek",
    
    # MediaTek
    "00:0C:E7": "MediaTek",
    "00:0E:7F": "MediaTek",
    
    # Qualcomm
    "00:A0:C6": "Qualcomm",
    
    # Ralink
    "00:0C:43": "Ralink",
    "00:0E:2E": "Ralink",
    
    # Atheros
    "00:03:7F": "Atheros",
    
    # Microsoft
    "00:50:F2": "Microsoft",
    "00:15:5D": "Microsoft",
    
    # Taiyo Yuden
    "00:03:7A": "Taiyo Yuden",
    
    # OPPO
    "56:4E:85": "OPPO",
    
    # Jio (Reliance Jio)
    "F4:CA:E7": "Jio",
    "82:CA:E7": "Jio",
    "00:60:57": "Jio",
    
    # Airtel
    "24:DE:8A": "Airtel",
    "00:05:CD": "Airtel",
    "00:1A:2B": "Airtel",
    "00:21:91": "Airtel",
    "08:00:27": "Airtel",
    "10:BF:48": "Airtel",
    "18:28:61": "Airtel",
    "20:47:47": "Airtel",
    "28:28:5D": "Airtel",
    "30:D3:2D": "Airtel",
    "38:2C:4A": "Airtel",
    "40:4E:36": "Airtel",
    "48:5D:36": "Airtel",
    "50:39:55": "Airtel",
    "58:23:8C": "Airtel",
    "60:E3:27": "Airtel",
    "68:72:51": "Airtel",
    "70:4F:57": "Airtel",
    "78:44:76": "Airtel",
    "80:26:89": "Airtel",
    "88:36:6C": "Airtel",
    "90:61:AE": "Airtel",
    "98:FC:11": "Airtel",
    "A0:F4:59": "Airtel",
    "A8:9C:ED": "Airtel",
    "B0:C5:54": "Airtel",
    "B8:EE:0E": "Airtel",
    "C0:A0:BB": "Airtel",
    "C8:3A:35": "Airtel",
    "D0:17:C2": "Airtel",
    "D8:49:0B": "Airtel",
    "E0:05:C5": "Airtel",
    "E8:94:F6": "Airtel",
    "F0:79:59": "Airtel",
    "F8:C3:9E": "Airtel",
}


def get_vendor_from_mac(mac_address):
    """
    Identify vendor from MAC address using OUI lookup.
    
    Args:
        mac_address (str): MAC address in format "AA:BB:CC:DD:EE:FF"
    
    Returns:
        str: Vendor name or "Unknown" if not found
    """
    if not mac_address or mac_address == "Unknown":
        return "Unknown"
    
    # Clean up MAC address - remove trailing colons and whitespace
    mac_address = mac_address.strip().rstrip(':').upper()
    
    # Extract first 3 octets (OUI)
    mac_prefix = ':'.join(mac_address.split(':')[:3])
    
    return MAC_VENDORS.get(mac_prefix, "Unknown")


def add_custom_vendor(mac_prefix, vendor_name):
    """
    Add a custom vendor to the database.
    
    Args:
        mac_prefix (str): First 3 octets of MAC address (e.g., "AA:BB:CC")
        vendor_name (str): Name of the vendor
    """
    MAC_VENDORS[mac_prefix.upper()] = vendor_name


def get_all_vendors():
    """
    Get all vendors in the database.
    
    Returns:
        dict: Dictionary of MAC prefixes to vendor names
    """
    return MAC_VENDORS.copy()
