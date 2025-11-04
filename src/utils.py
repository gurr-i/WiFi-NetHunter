"""Utility functions for the WiFi password tester."""

import sys
from pathlib import Path
import time
import json
from datetime import datetime


# ANSI color codes
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def load_passwords_from_file(filepath):
    """Load passwords from a file, one per line."""
    try:
        path = Path(filepath)
        if not path.exists():
            print(f"{Colors.RED}❌ Error: Password file '{filepath}' not found.{Colors.RESET}")
            return None

        with open(path, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]

        print(f"{Colors.GREEN}✅ Loaded {Colors.CYAN}{len(passwords)}{Colors.GREEN} passwords from file.{Colors.RESET}")
        return passwords

    except Exception as e:
        print(f"{Colors.RED}❌ Error reading password file: {e}{Colors.RESET}")
        return None


def get_ssid_display(network):
    """Convert network SSID to displayable string."""
    if isinstance(network.ssid, bytes):
        return network.ssid.decode("utf-8", errors="ignore")
    return str(network.ssid)


def mask_password(password, visible_chars=3):
    """Mask password for display, showing only first few characters."""
    if len(password) > visible_chars:
        return password[:visible_chars] + "*" * (len(password) - visible_chars)
    return password


def check_if_cracked(ssid):
    """Check if network is already in cracked.json."""
    try:
        cracked_file = Path("cracked.json")
        if cracked_file.exists():
            with open(cracked_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for net in data.get("cracked_networks", []):
                if net["ssid"] == ssid:
                    return net
        return None
    except:
        return None


def save_cracked_password(ssid, password, signal, auth_type, elapsed_time, attempts):
    """Save cracked password to cracked.json file."""
    try:
        cracked_file = Path("cracked.json")
        
        # Load existing data
        if cracked_file.exists():
            with open(cracked_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"cracked_networks": []}
        
        # Create new entry
        entry = {
            "ssid": ssid,
            "password": password,
            "signal_strength": signal,
            "auth_type": auth_type,
            "cracked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "time_elapsed": f"{elapsed_time:.2f}s",
            "attempts": attempts
        }
        
        # Check if network already exists and update it
        existing = False
        for i, net in enumerate(data["cracked_networks"]):
            if net["ssid"] == ssid:
                data["cracked_networks"][i] = entry
                existing = True
                break
        
        if not existing:
            data["cracked_networks"].append(entry)
        
        # Save to file
        with open(cracked_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"{Colors.GREEN}✅ Results saved to cracked.json{Colors.RESET}")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error saving to cracked.json: {e}{Colors.RESET}")


def print_banner():
    """Print application banner with hacker aesthetic."""
    banner = f"""
{Colors.GREEN}{Colors.BOLD}
╦ ╦╦╔═╗╦  ╔╗╔╔═╗╔╦╗╦ ╦╦ ╦╔╗╔╔╦╗╔═╗╦═╗
║║║║╠╣ ║  ║║║║╣  ║ ╠═╣║ ║║║║ ║ ║╣ ╠╦╝
╚╩╝╩╚  ╩  ╝╚╝╚═╝ ╩ ╩ ╩╚═╝╝╚╝ ╩ ╚═╝╩╚═
{Colors.RESET}
{Colors.RED}[{Colors.YELLOW}!{Colors.RED}] {Colors.WHITE}WiFi Penetration Testing Tool v1.0{Colors.RESET}
{Colors.RED}[{Colors.YELLOW}!{Colors.RED}] {Colors.WHITE}Educational & Authorized Testing Only{Colors.RESET}
{Colors.RED}[{Colors.YELLOW}!{Colors.RED}] {Colors.WHITE}Author: {Colors.CYAN}gurr-i{Colors.RESET}
{Colors.RED}{'─' * 68}{Colors.RESET}

{Colors.YELLOW}⚠️  WARNING:{Colors.RESET} {Colors.WHITE}Unauthorized access is illegal!{Colors.RESET}
{Colors.CYAN}►  Only test networks you own or have permission to test{Colors.RESET}
"""
    print(banner)
    time.sleep(0.5)


def get_password_source():
    """Prompt user to select password source and return password list."""
    print(f"\n{Colors.CYAN}{'─' * 68}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}[*] SELECT ATTACK MODE:{Colors.RESET}")
    print(f"{Colors.CYAN}{'─' * 68}{Colors.RESET}")
    print(f"{Colors.GREEN}[1]{Colors.RESET} {Colors.WHITE}► Use default wordlist {Colors.YELLOW}(data/passwords.txt){Colors.RESET}")
    print(f"{Colors.GREEN}[2]{Colors.RESET} {Colors.WHITE}► Load custom wordlist{Colors.RESET}")
    print(f"{Colors.GREEN}[3]{Colors.RESET} {Colors.WHITE}► Manual password entry{Colors.RESET}")
    print(f"{Colors.CYAN}{'─' * 68}{Colors.RESET}")

    choice = input(f"{Colors.MAGENTA}[?] Enter choice{Colors.RESET} {Colors.CYAN}[1-3]{Colors.RESET}: ").strip()

    if choice == "1":
        # Try to load from data/passwords.txt
        default_path = Path("data/passwords.txt")
        print(f"\n{Colors.YELLOW}[*] Loading default wordlist...{Colors.RESET}")
        time.sleep(0.3)
        if default_path.exists():
            passwords = load_passwords_from_file(str(default_path))
            if passwords:
                return passwords
        
        # Fallback to hardcoded list if file doesn't exist
        print(f"{Colors.YELLOW}[!] Warning: data/passwords.txt not found, using built-in list{Colors.RESET}")
        passwords = [
            "1234567890",
            "123456789",
            "12345678",
            "987654321",
            "admin123",
            "password123",
            "guest1234",
            "9876543210",
            "00000000",
        ]
        print(f"{Colors.GREEN}✅ Loaded {Colors.CYAN}{len(passwords)}{Colors.GREEN} passwords from built-in list{Colors.RESET}")
        return passwords

    elif choice == "2":
        filepath = input(f"{Colors.MAGENTA}[?] Enter wordlist path:{Colors.RESET} ").strip()
        print(f"{Colors.YELLOW}[*] Loading custom wordlist...{Colors.RESET}")
        time.sleep(0.3)
        passwords = load_passwords_from_file(filepath)
        if passwords is None:
            sys.exit(1)
        return passwords

    elif choice == "3":
        pw = input(f"{Colors.MAGENTA}[?] Enter password:{Colors.RESET} ").strip()
        if pw:
            print(f"{Colors.GREEN}✅ Password loaded{Colors.RESET}")
            return [pw]
        else:
            print(f"{Colors.RED}❌ No password entered.{Colors.RESET}")
            sys.exit(1)

    else:
        print(f"{Colors.RED}❌ Invalid option.{Colors.RESET}")
        sys.exit(1)
