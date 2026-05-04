import nmap
import subprocess
import logging

# Configure logging
logging.basicConfig(filename='network_recon.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def wifi_scan(interface):
    """Scan for WiFi networks using iwlist."""
    try:
        result = subprocess.check_output(['iwlist', interface, 'scanning']).decode()
        logging.info("WiFi Scan Results:\n%s", result)
        return result
    except subprocess.CalledProcessError as e:
        logging.error("Error during WiFi scan: %s", e)
        return None

def port_scan(target):
    """Scan for open ports on a target using nmap."""
    nm = nmap.PortScanner()
    try:
        nm.scan(target)
        logging.info("Port Scan Results for %s:\n%s", target, nm.all_udp() + nm.all_tcp())
        return nm.all_udp(), nm.all_tcp()
    except Exception as e:
        logging.error("Error during port scan for %s: %s", target, e)
        return None

def host_discovery(network):
    """Discover hosts in the given network."""
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=network, arguments='-sn')
        logging.info("Host Discovery Results:\n%s", nm.all_hosts())
        return nm.all_hosts()
    except Exception as e:
        logging.error("Error during host discovery on %s: %s", network, e)
        return None

def network_mapping(target):
    """Perform a full network mapping using nmap."""
    nm = nmap.PortScanner()
    try:
        nm.scan(target)
        logging.info("Network Mapping Results for %s:\n%s", target, nm.all_hosts())
        return nm.all_hosts()
    except Exception as e:
        logging.error("Error during network mapping for %s: %s", target, e)
        return None

# Example of how to use the functions
if __name__ == "__main__":
    print(wifi_scan('wlan0'))  # Replace 'wlan0' with your wireless interface
    print(port_scan('192.168.1.1'))  # Replace with your target IP
    print(host_discovery('192.168.1.0/24'))  # Replace with your subnet
    print(network_mapping('192.168.1.1'))  # Replace with your target IP
