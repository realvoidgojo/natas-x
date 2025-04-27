import re
from .base_solver import NatasSolver

class Natas0Solver(NatasSolver):
    def solve(self) -> str:
        response = self.make_request()
        match = re.findall("<!--The password for natas1 is (.*) -->", response.text)
        if not match:
            raise ValueError("Could not find password")
        return match[0]