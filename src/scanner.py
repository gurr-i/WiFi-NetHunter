"""Network scanning functionality."""

import pywifi
from pywifi import const
import time
import sys
import json
from pathlib import Path
from datetime import datetime
from .utils import Colors, check_if_cracked
from .vendors import get_vendor_from_mac
from .wps_attack import get_wps_info


def scan_networks_once(iface):
    """Perform a single network scan and return results."""
    try:
        # Disconnect from current network before scanning
        iface.disconnect()
        time.sleep(1)

        print(f"{Colors.YELLOW}[*] Initiating network scan...{Colors.RESET}")
        iface.scan()
        
        # Animated scanning
        for i in range(3):
            time.sleep(1)
            print(f"{Colors.CYAN}    Scanning{'.' * (i + 1)}{Colors.RESET}")
        
        results = iface.scan_results()

        if not results:
            print(f"{Colors.RED}[✗] No networks found.{Colors.RESET}")
            return []

        networks = []
        seen_ssids = set()

        for network in results:
            # Convert SSID to string if it's bytes
            try:
                if isinstance(network.ssid, bytes):
                    ssid_str = network.ssid.decode("utf-8", errors="ignore")
                else:
                    ssid_str = str(network.ssid)
            except:
                ssid_str = str(network.ssid)

            # Skip duplicate SSIDs and empty SSIDs
            if ssid_str in seen_ssids or not ssid_str:
                continue

            seen_ssids.add(ssid_str)
            networks.append(network)

        return networks

    except Exception as e:
        print(f"{Colors.RED}[✗] Error during network scan: {e}{Colors.RESET}")
        return []


def get_signal_quality(signal_dbm):
    """Convert signal strength from dBm to quality percentage."""
    if signal_dbm >= -50:
        return 100
    elif signal_dbm <= -100:
        return 0
    else:
        return 2 * (signal_dbm + 100)


def get_estimated_distance(signal_dbm):
    """Estimate distance based on signal strength (rough approximation)."""
    if signal_dbm >= -50:
        return "< 5m"
    elif signal_dbm >= -60:
        return "5-10m"
    elif signal_dbm >= -70:
        return "10-20m"
    elif signal_dbm >= -80:
        return "20-40m"
    elif signal_dbm >= -90:
        return "40-60m"
    else:
        return "> 60m"


def get_security_rating(akm, cipher):
    """Rate the security level of the network."""
    if "WPA2-PSK" in akm and "CCMP" in cipher:
        return "Strong"
    elif "WPA2" in akm:
        return "Medium"
    elif "WPA" in akm:
        return "Weak"
    elif "Open" in akm:
        return "None"
    else:
        return "Unknown"


def get_attack_difficulty(signal, security_rating):
    """Estimate attack difficulty based on signal and security."""
    if security_rating == "None":
        return "N/A (Open)"
    
    signal_factor = "Good" if signal > -70 else "Poor"
    
    if security_rating == "Strong" and signal > -70:
        return "Medium"
    elif security_rating == "Strong":
        return "Hard"
    elif security_rating == "Medium":
        return "Medium"
    elif security_rating == "Weak":
        return "Easy"
    else:
        return "Unknown"


def get_wifi_band(freq):
    """Determine WiFi band from frequency."""
    if freq is None or freq == 0:
        return "Unknown"
    
    # Convert kHz to MHz if needed
    if freq > 100000:
        freq = freq // 1000
    
    if 2400 <= freq <= 2500:
        return "2.4 GHz"
    elif 5000 <= freq <= 6000:
        return "5 GHz"
    elif 6000 <= freq <= 7125:
        return "6 GHz (WiFi 6E)"
    else:
        return "Unknown"


def get_channel_from_freq(freq):
    """Convert frequency to WiFi channel number."""
    if freq is None or freq == 0:
        return "Unknown"
    
    # Convert kHz to MHz if needed
    if freq > 100000:
        freq = freq // 1000
    
    # 2.4 GHz channels (1-14)
    if 2412 <= freq <= 2484:
        if freq == 2484:
            return 14
        else:
            return (freq - 2407) // 5
    
    # 5 GHz channels
    elif 5170 <= freq <= 5825:
        # Common 5GHz channels
        channel_map = {
            5180: 36, 5200: 40, 5220: 44, 5240: 48,
            5260: 52, 5280: 56, 5300: 60, 5320: 64,
            5500: 100, 5520: 104, 5540: 108, 5560: 112,
            5580: 116, 5600: 120, 5620: 124, 5640: 128,
            5660: 132, 5680: 136, 5700: 140, 5720: 144,
            5745: 149, 5765: 153, 5785: 157, 5805: 161, 5825: 165
        }
        return channel_map.get(freq, (freq - 5000) // 5)
    
    return "Unknown"


def track_network_stability(ssid, bssid):
    """Track network appearance history for stability analysis."""
    try:
        history_file = Path("network_history.json")
        
        # Load existing history
        if history_file.exists():
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = {"networks": {}}
        
        # Create unique key
        key = f"{ssid}_{bssid}"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if key in history["networks"]:
            # Update existing entry
            network = history["networks"][key]
            network["last_seen"] = current_time
            network["seen_count"] = network.get("seen_count", 1) + 1
            
            # Calculate stability
            first_seen = datetime.strptime(network["first_seen"], "%Y-%m-%d %H:%M:%S")
            last_seen = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
            days_active = (last_seen - first_seen).days
            
            if days_active > 7:
                stability = "Very Stable"
            elif days_active > 3:
                stability = "Stable"
            elif days_active > 1:
                stability = "Moderate"
            else:
                stability = "New/Transient"
            
            network["stability"] = stability
            network["days_active"] = days_active
        else:
            # New entry
            history["networks"][key] = {
                "ssid": ssid,
                "bssid": bssid,
                "first_seen": current_time,
                "last_seen": current_time,
                "seen_count": 1,
                "stability": "New",
                "days_active": 0
            }
        
        # Save history
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
        
        return history["networks"][key]
        
    except Exception as e:
        return {
            "stability": "Unknown",
            "days_active": 0,
            "seen_count": 1
        }


def get_network_details(network):
    """Extract detailed information about a network."""
    details = {}
    
    # SSID
    try:
        if isinstance(network.ssid, bytes):
            details['ssid'] = network.ssid.decode("utf-8", errors="ignore")
        else:
            details['ssid'] = str(network.ssid)
    except:
        details['ssid'] = str(network.ssid)
    
    # Signal strength
    details['signal'] = network.signal
    details['signal_quality'] = get_signal_quality(network.signal)
    details['distance'] = get_estimated_distance(network.signal)
    
    # BSSID (MAC Address)
    try:
        if hasattr(network, 'bssid'):
            details['bssid'] = network.bssid if network.bssid else "Unknown"
        else:
            details['bssid'] = "Unknown"
    except:
        details['bssid'] = "Unknown"
    
    # Vendor identification
    details['vendor'] = get_vendor_from_mac(details['bssid'])
    
    # Frequency and Channel
    try:
        if hasattr(network, 'freq') and network.freq:
            details['frequency'] = network.freq
            details['band'] = get_wifi_band(network.freq)
            details['channel'] = get_channel_from_freq(network.freq)
        else:
            details['frequency'] = 0
            details['band'] = "Unknown"
            details['channel'] = "Unknown"
    except:
        details['frequency'] = 0
        details['band'] = "Unknown"
        details['channel'] = "Unknown"
    
    # Network stability tracking
    stability_info = track_network_stability(details['ssid'], details['bssid'])
    details['stability'] = stability_info.get('stability', 'Unknown')
    details['days_active'] = stability_info.get('days_active', 0)
    details['seen_count'] = stability_info.get('seen_count', 1)
    
    # Authentication
    try:
        if isinstance(network.auth, list):
            auth_list = []
            for auth in network.auth:
                if auth == const.AUTH_ALG_OPEN:
                    auth_list.append("Open")
                elif auth == const.AUTH_ALG_SHARED:
                    auth_list.append("Shared")
                else:
                    auth_list.append(f"Auth:{auth}")
            details['auth'] = ', '.join(auth_list) if auth_list else "Open"
        else:
            auth_types = {
                const.AUTH_ALG_OPEN: "Open",
                const.AUTH_ALG_SHARED: "Shared",
            }
            details['auth'] = auth_types.get(network.auth, f"Auth:{network.auth}")
    except:
        details['auth'] = "Unknown"
    
    # AKM (Key Management)
    try:
        if hasattr(network, 'akm') and network.akm:
            if isinstance(network.akm, list):
                akm_types = []
                for akm in network.akm:
                    if akm == const.AKM_TYPE_NONE:
                        akm_types.append("Open")
                    elif akm == const.AKM_TYPE_WPA:
                        akm_types.append("WPA")
                    elif akm == const.AKM_TYPE_WPAPSK:
                        akm_types.append("WPA-PSK")
                    elif akm == const.AKM_TYPE_WPA2:
                        akm_types.append("WPA2")
                    elif akm == const.AKM_TYPE_WPA2PSK:
                        akm_types.append("WPA2-PSK")
                    else:
                        akm_types.append(f"AKM:{akm}")
                details['akm'] = ', '.join(akm_types)
            else:
                details['akm'] = str(network.akm)
        else:
            details['akm'] = "N/A"
    except:
        details['akm'] = "Unknown"
    
    # Cipher - with smart inference
    try:
        cipher_detected = None
        
        if hasattr(network, 'cipher') and network.cipher is not None:
            if isinstance(network.cipher, list) and len(network.cipher) > 0:
                cipher_types = []
                for cipher in network.cipher:
                    if cipher == const.CIPHER_TYPE_NONE:
                        continue  # Skip None, will infer from security
                    elif cipher == const.CIPHER_TYPE_WEP:
                        cipher_types.append("WEP")
                    elif cipher == const.CIPHER_TYPE_TKIP:
                        cipher_types.append("TKIP")
                    elif cipher == const.CIPHER_TYPE_CCMP:
                        cipher_types.append("CCMP")
                    else:
                        cipher_types.append(f"Cipher:{cipher}")
                
                if cipher_types:
                    cipher_detected = ', '.join(cipher_types)
                    
            elif isinstance(network.cipher, int):
                if network.cipher == const.CIPHER_TYPE_WEP:
                    cipher_detected = "WEP"
                elif network.cipher == const.CIPHER_TYPE_TKIP:
                    cipher_detected = "TKIP"
                elif network.cipher == const.CIPHER_TYPE_CCMP:
                    cipher_detected = "CCMP"
                elif network.cipher != const.CIPHER_TYPE_NONE:
                    cipher_detected = f"Cipher:{network.cipher}"
        
        # If no cipher detected or only None, infer from security type
        if not cipher_detected:
            if 'akm' in details and details['akm'] != "N/A":
                if "WPA2" in details['akm']:
                    cipher_detected = "CCMP (AES)"
                elif "WPA-PSK" in details['akm'] and "WPA2" not in details['akm']:
                    cipher_detected = "TKIP"
                elif "WPA" in details['akm']:
                    cipher_detected = "TKIP/CCMP"
                elif "Open" in details['akm']:
                    cipher_detected = "None"
        
        details['cipher'] = cipher_detected if cipher_detected else "Unknown"
        
    except Exception as e:
        # Fallback based on security type
        if 'akm' in details:
            if "WPA2" in details['akm']:
                details['cipher'] = "CCMP (AES)"
            elif "WPA" in details['akm']:
                details['cipher'] = "TKIP/CCMP"
            else:
                details['cipher'] = "Unknown"
        else:
            details['cipher'] = "Unknown"
    
    # Security rating and attack difficulty
    details['security_rating'] = get_security_rating(details['akm'], details['cipher'])
    details['attack_difficulty'] = get_attack_difficulty(details['signal'], details['security_rating'])
    
    # WPS information
    wps_info = get_wps_info(network)
    details['wps_enabled'] = wps_info['enabled']
    details['wps_locked'] = wps_info['locked']
    details['wps_version'] = wps_info['version']
    
    return details


def display_networks(networks, detailed=False):
    """Display the list of networks in a formatted table."""
    print(f"\n{Colors.CYAN}{'═' * 110}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}[*] AVAILABLE TARGETS: {Colors.CYAN}{len(networks)}{Colors.WHITE} networks found{Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 110}{Colors.RESET}")

    if detailed:
        # Detailed view with all information
        for idx, network in enumerate(networks):
            details = get_network_details(network)
            
            # Color code signal strength
            if details['signal'] > -50:
                signal_color = Colors.GREEN
                quality_color = Colors.GREEN
            elif details['signal'] > -70:
                signal_color = Colors.YELLOW
                quality_color = Colors.YELLOW
            else:
                signal_color = Colors.RED
                quality_color = Colors.RED
            
            # Color code security rating
            if details['security_rating'] == "Strong":
                security_color = Colors.GREEN
            elif details['security_rating'] == "Medium":
                security_color = Colors.YELLOW
            elif details['security_rating'] == "Weak":
                security_color = Colors.RED
            else:
                security_color = Colors.WHITE
            
            # Color code attack difficulty
            if details['attack_difficulty'] == "Easy":
                difficulty_color = Colors.GREEN
            elif details['attack_difficulty'] == "Medium":
                difficulty_color = Colors.YELLOW
            elif details['attack_difficulty'] == "Hard":
                difficulty_color = Colors.RED
            else:
                difficulty_color = Colors.WHITE
            
            # Check if already cracked
            cracked_info = check_if_cracked(details['ssid'])
            cracked_status = f" {Colors.GREEN}[✓ CRACKED]{Colors.RESET}" if cracked_info else ""
            
            # Color code stability
            if details['stability'] in ["Very Stable", "Stable"]:
                stability_color = Colors.GREEN
            elif details['stability'] == "Moderate":
                stability_color = Colors.YELLOW
            else:
                stability_color = Colors.WHITE
            
            print(f"{Colors.CYAN}[{idx}]{Colors.RESET} {Colors.BOLD}{Colors.WHITE}{details['ssid']}{Colors.RESET}{cracked_status}")
            print(f"    {Colors.WHITE}Signal:{Colors.RESET} {signal_color}{details['signal']} dBm{Colors.RESET} "
                  f"({quality_color}{details['signal_quality']}%{Colors.RESET}) │ "
                  f"{Colors.WHITE}Distance:{Colors.RESET} {Colors.CYAN}~{details['distance']}{Colors.RESET} │ "
                  f"{Colors.WHITE}Band:{Colors.RESET} {Colors.MAGENTA}{details['band']}{Colors.RESET}")
            print(f"    {Colors.WHITE}Channel:{Colors.RESET} {Colors.CYAN}{details['channel']}{Colors.RESET} │ "
                  f"{Colors.WHITE}Security:{Colors.RESET} {Colors.YELLOW}{details['akm']}{Colors.RESET} │ "
                  f"{Colors.WHITE}Cipher:{Colors.RESET} {Colors.CYAN}{details['cipher']}{Colors.RESET}")
            print(f"    {Colors.WHITE}Rating:{Colors.RESET} {security_color}{details['security_rating']}{Colors.RESET} │ "
                  f"{Colors.WHITE}Difficulty:{Colors.RESET} {difficulty_color}{details['attack_difficulty']}{Colors.RESET} │ "
                  f"{Colors.WHITE}Vendor:{Colors.RESET} {Colors.BLUE}{details['vendor']}{Colors.RESET}")
            print(f"    {Colors.WHITE}BSSID:{Colors.RESET} {Colors.MAGENTA}{details['bssid']}{Colors.RESET}")
            print(f"    {Colors.WHITE}Stability:{Colors.RESET} {stability_color}{details['stability']}{Colors.RESET} │ "
                  f"{Colors.WHITE}Active:{Colors.RESET} {Colors.CYAN}{details['days_active']} days{Colors.RESET} │ "
                  f"{Colors.WHITE}Seen:{Colors.RESET} {Colors.CYAN}{details['seen_count']}x{Colors.RESET}")
            
            # WPS status
            if details['wps_enabled']:
                wps_status = f"{Colors.RED}LOCKED{Colors.RESET}" if details['wps_locked'] else f"{Colors.GREEN}ENABLED{Colors.RESET}"
                print(f"    {Colors.WHITE}WPS:{Colors.RESET} {wps_status} │ "
                      f"{Colors.WHITE}Version:{Colors.RESET} {Colors.CYAN}{details['wps_version']}{Colors.RESET} "
                      f"{Colors.YELLOW}[⚡ WPS Attack Available]{Colors.RESET}")
            
            if cracked_info:
                print(f"    {Colors.GREEN}[✓] Password:{Colors.RESET} {Colors.WHITE}{cracked_info['password']}{Colors.RESET} │ "
                      f"{Colors.GREEN}Cracked:{Colors.RESET} {Colors.CYAN}{cracked_info['cracked_at']}{Colors.RESET}")
            
            print()
    else:
        # Compact view
        for idx, network in enumerate(networks):
            details = get_network_details(network)
            
            # Color code signal strength
            if details['signal'] > -50:
                signal_color = Colors.GREEN
            elif details['signal'] > -70:
                signal_color = Colors.YELLOW
            else:
                signal_color = Colors.RED
            
            print(f"{Colors.CYAN}[{idx}]{Colors.RESET} {Colors.WHITE}{details['ssid']:30}{Colors.RESET} │ "
                  f"{signal_color}{details['signal']:4} dBm{Colors.RESET} │ "
                  f"{Colors.MAGENTA}{details['auth']:10}{Colors.RESET} │ "
                  f"{Colors.YELLOW}{details['akm']}{Colors.RESET}")

    print(f"{Colors.CYAN}{'═' * 100}{Colors.RESET}")


def scan_networks():
    """Scan and return available WiFi networks with refresh option."""
    try:
        wifi = pywifi.PyWiFi()

        if not wifi.interfaces():
            print(f"{Colors.RED}[✗] Error: No WiFi interfaces found.{Colors.RESET}")
            sys.exit(1)

        iface = wifi.interfaces()[0]
        print(f"{Colors.GREEN}[✓] Interface:{Colors.RESET} {Colors.CYAN}{iface.name()}{Colors.RESET}")

        networks = []
        
        while True:
            # Perform scan
            networks = scan_networks_once(iface)
            
            if not networks:
                print(f"{Colors.YELLOW}[!] No networks found. Retrying...{Colors.RESET}")
                time.sleep(2)
                continue
            
            # Display networks
            display_networks(networks, detailed=True)
            
            # Ask user if they want to refresh or select
            print(f"\n{Colors.MAGENTA}[?] Options:{Colors.RESET}")
            print(f"{Colors.GREEN}[R]{Colors.RESET} {Colors.WHITE}► Refresh network list{Colors.RESET}")
            print(f"{Colors.GREEN}[S]{Colors.RESET} {Colors.WHITE}► Select single target{Colors.RESET}")
            print(f"{Colors.GREEN}[A]{Colors.RESET} {Colors.WHITE}► Attack all networks (mass attack){Colors.RESET}")
            
            choice = input(f"{Colors.MAGENTA}[?] Enter choice{Colors.RESET} {Colors.CYAN}[R/S/A]{Colors.RESET}: ").strip().upper()
            
            if choice == 'S':
                return networks, iface, 'single'
            elif choice == 'A':
                return networks, iface, 'all'
            elif choice == 'R':
                print(f"\n{Colors.YELLOW}[*] Refreshing network list...{Colors.RESET}")
                continue
            else:
                print(f"{Colors.RED}[✗] Invalid choice. Please enter R, S, or A.{Colors.RESET}")

    except IndexError:
        print(f"{Colors.RED}[✗] Error: No WiFi interface available.{Colors.RESET}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[✗] Scan cancelled by user.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[✗] Error during network scan: {e}{Colors.RESET}")
        sys.exit(1)


def select_network(networks):
    """Prompt user to select a network from the list."""
    while True:
        try:
            choice = input(
                f"\n{Colors.MAGENTA}[?] Select target{Colors.RESET} {Colors.CYAN}[0-{len(networks)-1}]{Colors.RESET}: "
            ).strip()

            if not choice:
                print(f"{Colors.RED}[✗] Please enter a number.{Colors.RESET}")
                continue

            choice = int(choice)

            if 0 <= choice < len(networks):
                print(f"{Colors.GREEN}[✓] Target locked{Colors.RESET}")
                time.sleep(0.3)
                return networks[choice]
            else:
                print(
                    f"{Colors.RED}[✗] Invalid choice. Enter a number between 0 and {len(networks)-1}.{Colors.RESET}"
                )
        except ValueError:
            print(f"{Colors.RED}[✗] Invalid input. Please enter a valid number.{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}[✗] Operation cancelled by user.{Colors.RESET}")
            sys.exit(0)
