from __future__ import annotations
import argparse, json, time
from pathlib import Path
from fim import compare, scan

BASELINE = Path(".fim-baseline.json")

def load() -> dict[str, str]:
    return json.loads(BASELINE.read_text()) if BASELINE.exists() else {}

def save(data: dict[str, str]) -> None:
    BASELINE.write_text(json.dumps(data, indent=2))

def report(changes: dict[str, list[str]]) -> None:
    for kind in ("added", "removed", "changed"):
        for item in changes[kind]:
            print(f"{kind.upper():7} {item}")

def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("baseline", "check"):
        x = sub.add_parser(name); x.add_argument("--path", required=True)
    x = sub.add_parser("watch")
    x.add_argument("--path", required=True); x.add_argument("--interval", type=int, default=5)
    a = p.parse_args()
    root = Path(a.path)
    if not root.is_dir(): raise SystemExit(f"Not a directory: {root}")
    if a.cmd == "baseline":
        data = scan(root); save(data); print(f"Baseline saved for {len(data)} files.")
    elif a.cmd == "check":
        report(compare(load(), scan(root)))
    else:
        print("Watching. Ctrl+C to stop.")
        try:
            while True:
                report(compare(load(), scan(root)))
                time.sleep(a.interval)
        except KeyboardInterrupt:
            print("\nStopped.")

if __name__ == "__main__":
    main()
