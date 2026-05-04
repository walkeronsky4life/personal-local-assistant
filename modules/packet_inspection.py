import logging
from scapy.all import sniff, IP, TCP, UDP

logging.basicConfig(filename='packet_inspection.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PacketInspection:
    def __init__(self):
        self.captured_packets = []
    
    def start_packet_capture(self, interface, packet_count=100):
        try:
            def packet_callback(packet):
                self.captured_packets.append(packet)
            
            sniff(iface=interface, prn=packet_callback, count=packet_count, store=True)
            logging.info("Captured %d packets", len(self.captured_packets))
            return self.captured_packets
        except Exception as e:
            logging.error("Error capturing packets: %s", e)
            return []
    
    def detect_suspicious_activity(self):
        suspicious = []
        for packet in self.captured_packets:
            if IP in packet and TCP in packet and packet[TCP].flags == 2:
                suspicious.append({'type': 'port_scan', 'src': packet[IP].src})
        return suspicious
    
    def export_pcap(self, filename):
        try:
            from scapy.all import wrpcap
            wrpcap(filename, self.captured_packets)
            return True
        except Exception as e:
            logging.error("Error exporting: %s", e)
            return False

packet_inspector = PacketInspection()
