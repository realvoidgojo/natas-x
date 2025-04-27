import csv
import os
import re
from typing import Tuple, List

class CredentialManager:
    def __init__(self, csv_path: str = "credentials.csv"):
        self.csv_path = csv_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create credentials file with header if it doesn't exist"""
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['level', 'username', 'password'])

    def clean_password(self, password: str) -> str:
        """Clean password by removing HTML tags and extra whitespace"""
        # Remove HTML tags
        password = re.sub(r'<[^>]+>', '', password)
        # Remove extra whitespace
        password = password.strip()
        return password

    def read_credentials(self) -> List[List[str]]:
        """Read credentials from CSV file, handling malformed rows"""
        credentials = []
        if os.path.exists(self.csv_path):
            with open(self.csv_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 3:  # Only include valid rows
                        credentials.append(row)
        return credentials

    def save_credentials(self, level: int, password: str):
        """Save credentials to CSV file"""
        username = f"natas{level}"
        cleaned_password = self.clean_password(password)
        
        # Read existing credentials
        credentials = self.read_credentials()
        
        # Remove any existing entries for this level
        credentials = [row for row in credentials if len(row) >= 1 and row[0] != str(level)]
        
        # Add new credentials
        credentials.append([str(level), username, cleaned_password])
        
        # Sort credentials by level
        credentials.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0)
        
        # Write all credentials back to file
        with open(self.csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['level', 'username', 'password'])
            writer.writerows(credentials)

    def get_credentials(self, level: int) -> Tuple[str, str]:
        """Get credentials for a specific level"""
        credentials = self.read_credentials()
        for row in credentials:
            if len(row) >= 3 and row[0] == str(level):
                return row[1], row[2]
        return f"natas{level}", ""