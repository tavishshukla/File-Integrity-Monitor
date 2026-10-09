# File Integrity Monitor

A defensive local file-integrity monitor using SHA-256.

## Features
- Create a file-hash baseline
- Detect added, removed, and changed files
- Recursive scanning
- Optional watch mode
- Never modifies monitored files

## Run
```bash
pip install -r requirements.txt
python main.py baseline --path ./sample_data
python main.py check --path ./sample_data
python main.py watch --path ./sample_data --interval 5
```

Only monitor folders you own or are authorized to monitor.
