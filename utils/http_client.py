import requests
from typing import Dict, Optional

class HTTPClient:
    def __init__(self):
        self.session = requests.Session()

    def request(self, 
                url: str,
                method: str = "GET",
                auth: tuple = None,
                cookies: Dict = None,
                data: Dict = None,
                files: Dict = None,
                headers: Dict = None,
                params: Dict = None,
                allow_redirects: bool = True) -> requests.Response:
        return self.session.request(
            method=method,
            url=url,
            auth=auth,
            cookies=cookies,
            data=data,
            files=files,
            headers=headers,
            params=params,
            allow_redirects=allow_redirects
        )