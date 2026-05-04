import subprocess
import json
import logging
from datetime import datetime

logging.basicConfig(filename='predator_integration.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PredatorIntegration:
    """Orchestrate Predator Linux pentesting tools"""
    
    def __init__(self):
        self.tool_results = []
    
    def check_predator_tools(self):
        """Verify Predator tools are installed"""
        tools = ['aircrack-ng', 'hashcat', 'hcitool', 'bettercap', 'airodump-ng', 'airmon-ng']
        available = []
        
        for tool in tools:
            try:
                subprocess.run(['which', tool], capture_output=True, check=True)
                available.append(tool)
                logging.info("Tool available: %s", tool)
            except:
                logging.warning("Tool not found: %s", tool)
        
        return available
    
    def airmon_monitor_mode(self, interface):
        """Enable monitor mode with airmon-ng"""
        try:
            cmd = ['sudo', 'airmon-ng', 'start', interface]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            logging.info("Monitor mode enabled on %s", interface)
            return result.stdout
        except Exception as e:
            logging.error("Monitor mode error: %s", e)
            return None
    
    def airodump_scan(self, interface, output_file):
        """Scan WiFi networks with airodump-ng"""
        try:
            cmd = ['sudo', 'airodump-ng', interface, '-w', output_file, '-o', 'csv']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            logging.info("Airodump scan completed: %s", output_file)
            return result.stdout
        except Exception as e:
            logging.error("Airodump scan error: %s", e)
            return None
    
    def hashcat_crack(self, hash_file, wordlist, hash_type='1000'):
        """Crack hashes with hashcat"""
        try:
            cmd = ['hashcat', '-m', hash_type, hash_file, wordlist]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            
            result_entry = {
                'tool': 'hashcat',
                'hash_file': hash_file,
                'output': result.stdout,
                'timestamp': datetime.now().isoformat()
            }
            
            self.tool_results.append(result_entry)
            logging.info("Hashcat crack completed")
            return result.stdout
        except Exception as e:
            logging.error("Hashcat error: %s", e)
            return None
    
    def bettercap_session(self, target_ip):
        """Initialize bettercap session"""
        try:
            cmd = ['sudo', 'bettercap', '-iface', 'eth0', '-caplet', 'http-ui']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            logging.info("Bettercap session initialized for %s", target_ip)
            return result.stdout
        except Exception as e:
            logging.error("Bettercap error: %s", e)
            return None
    
    def execute_predator_command(self, command):
        """Execute arbitrary Predator command"""
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True, timeout=300)
            
            result_entry = {
                'command': command,
                'output': result.stdout,
                'errors': result.stderr,
                'timestamp': datetime.now().isoformat()
            }
            
            self.tool_results.append(result_entry)
            logging.info("Command executed: %s", command)
            return result.stdout
        except Exception as e:
            logging.error("Command execution error: %s", e)
            return None

predator = PredatorIntegration()
