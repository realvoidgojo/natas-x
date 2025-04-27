from abc import ABC, abstractmethod
import requests
from typing import Optional
from utils.http_client import HTTPClient

class NatasSolver(ABC):
    def __init__(self, level: int, password: str):
        self.level = level
        self.password = password
        self.username = f"natas{level}"
        self.base_url = f"http://{self.username}.natas.labs.overthewire.org"
        self.http_client = HTTPClient()

    @abstractmethod
    def solve(self) -> Optional[str]:
        """Solve the level and return password for next level"""
        pass

    def make_request(self, path: str = "", method: str = "GET", **kwargs) -> requests.Response:
        """Make authenticated HTTP request"""
        url = f"{self.base_url}/{path}".rstrip('/')
        auth = (self.username, self.password)
        return self.http_client.request(method=method, url=url, auth=auth, **kwargs)