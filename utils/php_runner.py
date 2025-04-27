import os
import subprocess
from typing import Optional

def run_php_script(script_path: str, *args) -> Optional[str]:
    """
    Run a PHP script and return its output
    
    Args:
        script_path: Path to PHP script
        *args: Additional arguments to pass to PHP script
    
    Returns:
        Output from PHP script or None if execution failed
    """
    try:
        cmd = ['php', script_path] + list(args)
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True, 
                              check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"PHP script execution failed: {e.stderr}")