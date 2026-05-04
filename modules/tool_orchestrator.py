import json
import logging
import subprocess
from datetime import datetime
from core.ai_assistant import ai_assistant

logging.basicConfig(filename='tool_orchestrator.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ToolOrchestrator:
    """Unified tool coordination and workflow automation"""
    
    def __init__(self):
        self.active_workflows = []
        self.tool_results = {}
    
    def create_htb_workflow(self, target_ip, challenge_type):
        """Create automated workflow for HTB challenges"""
        workflow = {
            'target': target_ip,
            'type': challenge_type,
            'steps': [],
            'timestamp': datetime.now().isoformat()
        }
        
        if challenge_type == 'web':
            workflow['steps'] = [
                {'order': 1, 'tool': 'nmap', 'action': 'port_scan', 'args': [target_ip]},
                {'order': 2, 'tool': 'burp', 'action': 'proxy_scan', 'args': [target_ip]},
                {'order': 3, 'tool': 'sqlmap', 'action': 'sql_injection_test', 'args': [target_ip]}
            ]
        elif challenge_type == 'network':
            workflow['steps'] = [
                {'order': 1, 'tool': 'nmap', 'action': 'network_scan', 'args': [target_ip]},
                {'order': 2, 'tool': 'wireshark', 'action': 'traffic_capture', 'args': [target_ip]},
                {'order': 3, 'tool': 'metasploit', 'action': 'exploit', 'args': [target_ip]}
            ]
        elif challenge_type == 'mobile':
            workflow['steps'] = [
                {'order': 1, 'tool': 'adb', 'action': 'list_devices', 'args': []},
                {'order': 2, 'tool': 'apktool', 'action': 'analyze_apk', 'args': [target_ip]},
                {'order': 3, 'tool': 'frida', 'action': 'dynamic_analysis', 'args': [target_ip]}
            ]
        
        self.active_workflows.append(workflow)
        logging.info("HTB workflow created: %s (%s)", target_ip, challenge_type)
        return workflow
    
    def execute_workflow(self, workflow):
        """Execute complete workflow with all tools"""
        results = {
            'workflow_id': workflow['target'],
            'steps_completed': [],
            'timestamp': datetime.now().isoformat()
        }
        
        for step in workflow['steps']:
            try:
                tool = step['tool']
                action = step['action']
                
                result = self.execute_tool_action(tool, action, step.get('args', []))
                
                results['steps_completed'].append({
                    'tool': tool,
                    'action': action,
                    'status': 'completed',
                    'result': result
                })
                
                logging.info("Step completed: %s - %s", tool, action)
            except Exception as e:
                logging.error("Step failed: %s", e)
        
        self.tool_results[workflow['target']] = results
        return results
    
    def execute_tool_action(self, tool, action, args):
        """Execute specific tool action"""
        try:
            if tool == 'nmap':
                cmd = ['nmap'] + args
            elif tool == 'hashcat':
                cmd = ['hashcat'] + args
            elif tool == 'airodump-ng':
                cmd = ['sudo', 'airodump-ng'] + args
            elif tool == 'metasploit':
                cmd = ['msfconsole', '-x', ' '.join(args)]
            else:
                cmd = [tool] + args
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.stdout
        except Exception as e:
            logging.error("Tool execution error: %s", e)
            return None
    
    def ai_suggest_next_step(self, current_results):
        """Use AI to suggest next step in workflow"""
        prompt = f"""Based on these penetration testing results:
        {json.dumps(current_results, indent=2)}
        
        What should be the next testing step? Be specific about tools and techniques."""
        
        response = ai_assistant.generate_response(prompt)
        logging.info("AI suggestion generated")
        return response
    
    def generate_unified_report(self, target, all_results):
        """Generate comprehensive report from all tools"""
        report = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'findings': all_results,
            'summary': self.ai_generate_summary(all_results)
        }
        
        logging.info("Unified report generated for %s", target)
        return report
    
    def ai_generate_summary(self, results):
        """Generate AI-powered summary"""
        prompt = f"""Summarize these security testing results:\n{json.dumps(results, indent=2)}"""
        return ai_assistant.generate_response(prompt)

tool_orchestrator = ToolOrchestrator()
