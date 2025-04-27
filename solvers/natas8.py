import re
from .base_solver import NatasSolver
from utils.php_runner import run_php_script

class Natas8Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Run PHP script to decode the secret
            secret = run_php_script("payloads/natas8.php")
            if not secret:
                raise ValueError("Failed to decode secret from PHP")

            # Make POST request with decoded secret
            response = self.make_request(
                method="POST",
                data={
                    "secret": secret.strip(),
                    "submit": "submit"
                }
            )

            # Extract password using more precise regex pattern
            match = re.findall(r"Access granted. The password for natas9 is ([^<\s]+)", response.text)
            if not match:
                raise ValueError("Could not find password in response")
            
            return match[0].strip()

        except Exception as e:
            raise RuntimeError(f"Failed to solve natas8: {str(e)}")