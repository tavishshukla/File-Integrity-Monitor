# File Integrity Monitor

A defensive file-integrity monitoring tool that uses SHA-256 hashes to detect files being added, removed, or changed.

## Features

- SHA-256 hashing
- Recursive scanning
- Baseline creation
- Added/removed/changed detection
- Continuous watch mode
- Custom baseline location
- Automated tests
- Read-only monitoring

## Requirements

- Windows, Linux, or macOS
- Python **3.11 or newer**
- Git

## Setup

Install Python from https://www.python.org/downloads/ and Git from https://git-scm.com/downloads/.

Verify:

```bash
python --version
git --version
```

Clone:

```bash
git clone https://github.com/tavishshukla/File-Integrity-Monitor.git
cd File-Integrity-Monitor
```

Create a virtual environment.

### Windows

```bat
python -m venv .venv
.venv\\Scripts\\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Create a test directory

Windows:

```bat
mkdir sample_data
echo Hello > sample_data\\example.txt
```

Linux/macOS:

```bash
mkdir -p sample_data
echo "Hello" > sample_data/example.txt
```

## Create a baseline

```bash
python main.py baseline --path ./sample_data
```

A SHA-256 hash is recorded for every file.

Use a custom baseline path if desired:

```bash
python main.py baseline --path ./sample_data --baseline ./data/baseline.json
```

## Check for changes

```bash
python main.py check --path ./sample_data
```

Edit a file and run the check again. You should receive a `CHANGED` result.

Create a new file for an `ADDED` result and remove a file for a `REMOVED` result.

## Watch continuously

```bash
python main.py watch --path ./sample_data --interval 5
```

Stop with `Ctrl+C`.

## How it works

1. Scan the selected directory recursively.
2. Calculate SHA-256 for each file.
3. Save the hashes as the known-good baseline.
4. Scan again later.
5. Compare current hashes with the baseline.
6. Report added, removed, and changed files.

The monitor never changes the files it is checking.

## Tests

```bash
python -m pytest
```

## Project structure

```
File-Integrity-Monitor/
├── main.py
├── fim.py
├── requirements.txt
├── README.md
└── tests/
    └── test_fim.py
```

## Security note

Only monitor directories you own or are authorized to inspect. For a production-style implementation, store the baseline outside the monitored directory and protect it from unauthorized modification.

## Recommended workflow

Create the baseline first with `python main.py baseline --path ./sample_data`, make an authorized test-file change, and then run `python main.py check --path ./sample_data`. The monitor reports differences without modifying monitored files.
