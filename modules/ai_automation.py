import json
import logging
from core.ai_assistant import ai_assistant

logging.basicConfig(filename='ai_automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AIAutomation:
    def __init__(self):
        self.workflows = []
    
    def analyze_recon_results(self, recon_data):
        prompt = f"Analyze these network results and suggest next steps: {json.dumps(recon_data)}"
        response = ai_assistant.generate_response(prompt)
        return response
    
    def suggest_exploitation_path(self, vulnerabilities):
        prompt = f"Suggest an exploitation priority order: {json.dumps(vulnerabilities)}"
        response = ai_assistant.generate_response(prompt)
        return response
    
    def automated_workflow(self, target, workflow_type='comprehensive'):
        workflow = {
            'target': target,
            'type': workflow_type,
            'steps': [
                {'step': 1, 'action': 'network_recon'},
                {'step': 2, 'action': 'port_scan'},
                {'step': 3, 'action': 'vuln_assessment'},
                {'step': 4, 'action': 'password_test'}
            ]
        }
        self.workflows.append(workflow)
        return workflow
    
    def generate_ai_report(self, findings):
        prompt = f"Generate professional pentest report: {json.dumps(findings)}"
        return ai_assistant.generate_response(prompt)

ai_automation = AIAutomation()
