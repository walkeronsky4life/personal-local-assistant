import subprocess
import json
import logging
from datetime import datetime

logging.basicConfig(filename='vuln_assessment.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VulnerabilityAssessment:
    def __init__(self):
        self.vulnerabilities = []
    
    def detect_service_vulnerabilities(self, target, ports):
        vulnerabilities = []
        service_vulns = {
            'ssh': ['CVE-2021-28041', 'CVE-2020-14144'],
            'http': ['CVE-2021-22911', 'CVE-2021-3129'],
            'ftp': ['CVE-2020-9484', 'CVE-2019-9193'],
            'mysql': ['CVE-2021-2109', 'CVE-2021-2372'],
        }
        
        for port_info in ports:
            service = port_info.get('service', '').lower()
            if service in service_vulns:
                for cve in service_vulns[service]:
                    vulnerabilities.append({
                        'service': service,
                        'port': port_info.get('port'),
                        'cve': cve,
                        'severity': 'HIGH'
                    })
        
        self.vulnerabilities = vulnerabilities
        return vulnerabilities
    
    def assess_risk_level(self, vulnerabilities):
        if not vulnerabilities:
            return "LOW"
        high_count = len([v for v in vulnerabilities if v.get('severity') == 'HIGH'])
        return "HIGH" if high_count >= 3 else "MEDIUM"

vuln_assessment = VulnerabilityAssessment()
