from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from fim import compare, scan


def load(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def save(path: Path, data: dict[str, str]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def report(changes: dict[str, list[str]]) -> int:
    total = 0
    for kind in ("added", "removed", "changed"):
        for item in changes[kind]:
            print(f"{kind.upper():7} {item}")
            total += 1
    if total == 0:
        print("No integrity changes detected.")
    return total


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read-only SHA-256 file integrity monitor"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    for name in ("baseline", "check"):
        command = sub.add_parser(name)
        command.add_argument("--path", required=True)
        command.add_argument(
            "--baseline",
            default=".fim-baseline.json",
            help="Baseline JSON file",
        )
        if name == "check":
            command.add_argument(
                "--fail-on-change",
                action="store_true",
                help="Exit with status 2 when changes are detected",
            )

    watch = sub.add_parser("watch")
    watch.add_argument("--path", required=True)
    watch.add_argument("--interval", type=float, default=5)
    watch.add_argument("--baseline", default=".fim-baseline.json")

    args = parser.parse_args()
    root = Path(args.path).resolve()
    baseline_path = Path(args.baseline).resolve()

    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")
    if args.interval <= 0 if args.cmd == "watch" else False:
        raise SystemExit("--interval must be greater than 0")

    if args.cmd == "baseline":
        data = scan(root)
        save(baseline_path, data)
        print(f"Baseline saved to {baseline_path}")
        print(f"Files recorded: {len(data)}")
        return

    old = load(baseline_path)
    if not old:
        raise SystemExit(
            f"No baseline found at {baseline_path}. "
            f"Run the baseline command first."
        )

    if args.cmd == "check":
        changes = compare(old, scan(root))
        changed = report(changes)
        if args.fail_on_change and changed:
            raise SystemExit(2)
        return

    print("Watching. Ctrl+C to stop.")
    try:
        while True:
            report(compare(old, scan(root)))
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
