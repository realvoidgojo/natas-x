import re
from .base_solver import NatasSolver

class Natas5Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Set loggedin cookie
            response = self.make_request(
                cookies={"loggedin": "1"}
            )
            # Update regex to avoid capturing HTML tags
            match = re.findall(r"The password for natas6 is ([^<\s]+)", response.text)
            if not match:
                raise ValueError("Could not find password")
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas5: {str(e)}")