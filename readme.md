# NatasX CTF Solver (Automation)

An automated solver for the OverTheWire Natas wargame challenges, featuring level-specific exploitation techniques and credential management.

## Features

- Automated solving for levels 0-34
- Session management and credential persistence
- Rich console output with progress indicators
- Modular solver architecture
- PHP payload generation and template handling
- Extensive error handling and logging

## Requirements

```
requests>=2.28.0
typing>=3.7.4
rich>=10.0.0
PHP CLI
```

## Project Structure

```text
├── config/
│   └── credentials.py       # Initial credentials config
├── payloads/
│   ├── natas*.php          # Level-specific PHP payloads
│   └── *.template          # PHP template files
├── solvers/
│   ├── base_solver.py      # Base solver class
│   └── natas*.py           # Level-specific solvers
├── utils/
│   ├── credentials.py      # Credential management
│   ├── http_client.py      # HTTP request handling
│   ├── php_template.py     # PHP template handling
│   └── php_runner.py       # PHP script execution
├── main.py                 # Main orchestrator
└── credentials.csv         # Credential storage
```

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure PHP CLI is installed:

```bash
php --version
```

3. Run the solver:

```bash
python main.py
```

<img src="/img/image.png" alt="Image Description" width="1500">

## Usage

To solve all levels, ensure that the `credentials.csv` file contains only the following content, removing any old credentials:

```
level,username,password
```

If the file already contains credentials, the solver will resume from the corresponding level.

## Level-Specific Features

Each level solver implements specific exploitation techniques:

- Level 0-10: Basic web exploitation
- Level 11-20: More advanced techniques (SQL injection, command injection)
- Level 21-30: Complex exploitation chains
- Level 31-34: Advanced PHP exploitation

## Key Components

- `NatasSolver`: Base class for all level solvers
- `NatasOrchestrator`: Main orchestration and progress tracking
- `CredentialManager`: Credential storage and retrieval
- `PHPTemplateHandler`: PHP payload template management

## Error Handling

Comprehensive error handling including:

- HTTP request failures
- PHP execution errors
- File operation errors
- Invalid credentials

## License

This project is for educational purposes only. Use only on systems you have permission to test.
