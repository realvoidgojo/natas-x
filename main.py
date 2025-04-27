import importlib
import logging
import os
import sys
from typing import Dict, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from solvers.base_solver import NatasSolver
from utils.credentials import CredentialManager
from config.credentials import STARTING_PASSWORD

class NatasOrchestrator:
    def __init__(self, start_level: int = 0, start_password: str = STARTING_PASSWORD):
        self.current_level = start_level
        self.current_password = start_password
        self.console = Console()
        self.logger = self._setup_logging()
        self.solvers: Dict[int, NatasSolver] = {}
        self.cred_manager = CredentialManager()
        
        self._print_banner()
        self._initialize_environment()
        
    def _print_banner(self):
        """Print fancy banner with styling"""
        banner = Text()
        banner.append("\n╔══════════════════════════════════════════════════════════════════╗\n")
        banner.append("║", style="bold white")
        banner.append("                        Natas Level Solver                        ", style="bold cyan")
        banner.append("║\n")
        banner.append("║", style="bold white")
        banner.append("                    OverTheWire.org Challenge                     ", style="bold green")
        banner.append("║\n")
        banner.append("║                                                                  ║\n")
        banner.append("║               / | / /___ _/ /_____ ______                        ║\n", style="bold cyan")
        banner.append("║              /  |/ / __ `/ __/ __ `/ ___/                        ║\n", style="bold yellow")
        banner.append("║             / /|  / /_/ / /_/ /_/ (__  )                         ║\n", style="bold cyan")
        banner.append("║            /_/ |_/\__,_/\__/\__,_/____/                          ║\n", style="bold yellow")
        banner.append("╚══════════════════════════════════════════════════════════════════╝\n")
        
        self.console.print(banner)
        
    def _initialize_environment(self):
        """Initialize solver environment"""
        try:
            self.console.print("[cyan][*][/] Initializing environment...")
            
            # Load solvers
            self._load_solvers()
            
            # Setup credentials
            self._setup_credentials()
            
            # Print summary
            self.console.print(f"[bold green][+][/] Working directory: {os.getcwd()}")
            self.console.print(f"[green][+][/] Initialization complete!")
            
        except Exception as e:
            self.console.print(f"[bold red][!][/] Initialization failed: {str(e)}")
            sys.exit(1)
            
    def _print_level_header(self, level: int):
        """Print formatted level header with styling"""
        self.console.print("\n")
        self.console.rule(f"[bold cyan]Level {level:02d} Solver")

    def solve_next(self) -> Optional[str]:
        """Solve next level with progress indicators"""
        if self.current_level not in self.solvers:
            self.console.print(f"\n[yellow][!][/] Level {self.current_level} not implemented")
            self.console.print(f"[green][+][/] Last successful password: {self.current_password}")
            return None
            
        try:
            self._print_level_header(self.current_level)
            
            solver_class = self.solvers[self.current_level]
            clean_password = self.current_password.replace("</div>", "").strip()
            solver = solver_class(self.current_level, clean_password)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task(f"[cyan]Solving level {self.current_level}...", total=1)
                next_password = solver.solve()
                
                if next_password:
                    clean_next_password = next_password.replace("</div>", "").strip()
                    progress.update(task, description=f"[green]Level {self.current_level:02d} solved!")
                    self.console.print(f"[bold green][+][/] Password: {clean_next_password}")
                    self.cred_manager.save_credentials(self.current_level + 1, clean_next_password)
                    self.current_level += 1
                    self.current_password = clean_next_password
                    return clean_next_password
                
                progress.update(task, description=f"[red]Failed to solve level {self.current_level}")
                return None
                
        except Exception as e:
            self.console.print(f"[bold red][!][/] Error solving level {self.current_level}: {str(e)}")
            return None

    def solve_all(self) -> None:
        """Solve all implemented levels sequentially"""
        total_levels = max(self.solvers.keys())
        solved = 0
        
        while self.solve_next():
            solved += 1
            print(f"\n[*] Progress: {solved}/{total_levels} levels completed")
        
        print("\n" + "="*50)
        print(f"Solved {solved} out of {total_levels} levels")
        print(f"Final level reached: {self.current_level-1}")
        print(f"Last password: {self.current_password}")
        print("="*50 + "\n")

    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration"""
        logger = logging.getLogger('NatasSolver')
        logger.setLevel(logging.INFO)
        
        # Create formatters and handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # File handler
        file_handler = logging.FileHandler('natas_solver.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler with rich formatting
        class RichConsoleHandler(logging.Handler):
            def emit(self, record):
                try:
                    msg = self.format(record)
                    if record.levelno >= logging.ERROR:
                        self.console.print(f"[bold red]{msg}[/]")
                    elif record.levelno >= logging.WARNING:
                        self.console.print(f"[yellow]{msg}[/]")
                    else:
                        self.console.print(f"[cyan]{msg}[/]")
                except Exception:
                    self.handleError(record)
        
        console_handler = RichConsoleHandler()
        console_handler.console = self.console
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _load_solvers(self):
        """Dynamically load solver classes"""
        try:
            self.console.print("[cyan][*][/] Loading solver modules...")
            total_levels = 34
            loaded = 0
            
            # Import all solver modules dynamically
            for level in range(total_levels):
                try:
                    module = importlib.import_module(f"solvers.natas{level}")
                    solver_class = getattr(module, f"Natas{level}Solver")
                    self.solvers[level] = solver_class
                    loaded += 1
                except (ImportError, AttributeError):
                    continue
                    
            if not self.solvers:
                raise ValueError("No solver modules found")
            
            self.console.print(f"[green][+][/] Successfully loaded {loaded}/{total_levels} solvers")
            
        except Exception as e:
            self.console.print(f"[bold red][!][/] Failed to load solvers: {str(e)}")
            raise

    def _setup_credentials(self):
        """Set up credentials and resume state"""
        try:
            # Save initial credentials
            self.cred_manager.save_credentials(self.current_level, self.current_password)
            
            # Try to resume from last saved state
            last_creds = self.cred_manager.read_credentials()
            if last_creds:
                last_level = max(int(row[0]) for row in last_creds)
                _, last_password = self.cred_manager.get_credentials(last_level)
                if last_level > self.current_level:
                    self.current_level = last_level
                    self.current_password = last_password
                    self.console.print(f"[cyan][*][/] Resuming from level {last_level}")
                    
            self.console.print("[green][+][/] Credentials setup complete")
            
        except Exception as e:
            self.console.print(f"[bold red][!][/] Failed to setup credentials: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        orchestrator = NatasOrchestrator()
        orchestrator.solve_all()
    except KeyboardInterrupt:
        print("\n[!] Solver interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Fatal error: {str(e)}")
        sys.exit(1)