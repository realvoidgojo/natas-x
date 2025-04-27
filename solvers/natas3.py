import re
from .base_solver import NatasSolver

class Natas3Solver(NatasSolver):
    def solve(self) -> str:
        # Access robots.txt hidden file
        response = self.make_request("s3cr3t/users.txt")
        match = re.findall(r"natas4:(.*)", response.text)
        if not match:
            raise ValueError("Could not find password")
        return match[0].strip()