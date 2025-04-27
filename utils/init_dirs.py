import os

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        'payloads',
        'solvers',
        'utils',
        'config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)