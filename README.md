# File Integrity Monitor

A defensive file-integrity monitoring tool that uses SHA-256 hashes to detect files being added, removed, or changed.

It is useful for learning a basic security concept used by real defensive systems: establish a known-good baseline and compare the current state against it later.

## Features

- SHA-256 file hashing
- Recursive directory scanning
- Baseline creation
- Added-file detection
- Removed-file detection
- Changed-file detection
- Continuous watch mode
- Automated tests
- Never modifies monitored files

## Requirements

- Windows, Linux, or macOS
- Python **3.11 or newer**
- Git

## 1. Install Python

Download Python:

https://www.python.org/downloads/

On Windows, enable **Add Python to PATH** during installation.

Check:

```bash
python --version
```

## 2. Install Git

Download:

https://git-scm.com/downloads

Check:

```bash
git --version
```

## 3. Clone the repository

```bash
git clone https://github.com/tavishshukla/File-Integrity-Monitor.git
cd File-Integrity-Monitor
```

## 4. Create a virtual environment

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

## 5. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Pip normally comes with Python, so a separate pip download is not required.

## 6. Create a test folder

It is best to start with a folder specifically created for the experiment.

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

You can also use an existing folder that you own or are authorized to monitor.

## 7. Create the baseline

Run:

```bash
python main.py baseline --path ./sample_data
```

You should see something similar to:

```
Baseline saved for 1 files.
```

The baseline is stored in:

```
.fim-baseline.json
```

## 8. Check for changes

Run:

```bash
python main.py check --path ./sample_data
```

If nothing changed, there should be no change alerts.

Now edit `sample_data/example.txt` and run the check again.

You should see:

```
CHANGED sample_data/example.txt
```

## 9. Test added files

Create another file:

Windows:

```bat
echo New file > sample_data\\new.txt
```

Linux/macOS:

```bash
echo "New file" > sample_data/new.txt
```

Then:

```bash
python main.py check --path ./sample_data
```

You should see an `ADDED` result.

## 10. Test removed files

Delete a monitored file and run:

```bash
python main.py check --path ./sample_data
```

You should see a `REMOVED` result.

## 11. Use watch mode

Watch the directory continuously:

```bash
python main.py watch --path ./sample_data --interval 5
```

The program checks the directory every 5 seconds.

Stop it with:

```
Ctrl+C
```

## 12. Run the tests

```bash
python -m pytest
```

## How it works

1. The monitor recursively scans the selected directory.
2. Each file is read and hashed with SHA-256.
3. The resulting hashes are saved as the baseline.
4. Later scans are compared with the baseline.
5. Differences are reported as added, removed, or changed files.

A changed SHA-256 hash means the file's contents are different from the baseline.

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

## Important note

The baseline file is itself a file. Keep `.fim-baseline.json` outside the directory being monitored when building a more advanced version of the project.

Only monitor files and folders that you own or are authorized to inspect.
