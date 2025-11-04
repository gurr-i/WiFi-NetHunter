"""WiFi connection and password testing functionality."""

import pywifi
from pywifi import const
import time
from .utils import Colors


def try_password(iface, network, password):
    """Attempt to connect to a network with the given password."""
    try:
        profile = pywifi.Profile()
        profile.ssid = network.ssid

        # Handle auth - if it's a list, use the first element
        if isinstance(network.auth, list):
            profile.auth = (
                network.auth[0] if network.auth else const.AUTH_ALG_OPEN
            )
        else:
            profile.auth = network.auth

        # Handle AKM (authentication and key management)
        if hasattr(network, "akm") and network.akm:
            if isinstance(network.akm, list):
                profile.akm = network.akm
            else:
                profile.akm.append(network.akm)
        else:
            # Try common authentication methods
            profile.akm.append(const.AKM_TYPE_WPA2PSK)

        # Handle cipher - if it's a list, use it directly
        if hasattr(network, "cipher") and network.cipher:
            if isinstance(network.cipher, list):
                profile.cipher = (
                    network.cipher[0] if network.cipher else const.CIPHER_TYPE_CCMP
                )
            else:
                profile.cipher = network.cipher
        else:
            profile.cipher = const.CIPHER_TYPE_CCMP

        profile.key = password

        # Remove existing profiles and add new one
        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)

        # Attempt connection
        iface.connect(tmp_profile)

        # Wait and check connection status multiple times
        for _ in range(10):
            time.sleep(1)
            status = iface.status()
            if status == const.IFACE_CONNECTED:
                iface.disconnect()
                time.sleep(1)
                return True
            elif status == const.IFACE_DISCONNECTED:
                # Connection failed
                break

        # Ensure disconnection
        iface.disconnect()
        time.sleep(1)
        return False

    except Exception as e:
        print(f"{Colors.RED}[✗] Error testing password: {e}{Colors.RESET}")
        try:
            iface.disconnect()
        except:
            pass
        return False
