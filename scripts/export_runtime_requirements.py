from __future__ import annotations

import argparse
import tomllib
from pathlib import Path


def build_runtime_requirements(lockfile_path: Path) -> str:
    lock_data = tomllib.loads(lockfile_path.read_text(encoding="utf-8"))
    packages = sorted(
        (
            package["name"].replace("_", "-"),
            package["version"],
        )
        for package in lock_data.get("package", [])
        if "main" in package.get("groups", [])
    )
    return "".join(f"{name}=={version}\n" for name, version in packages)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export pinned runtime requirements from poetry.lock.",
    )
    parser.add_argument(
        "--lockfile",
        default="poetry.lock",
        help="Path to poetry.lock.",
    )
    parser.add_argument(
        "--output",
        default="-",
        help="Output file path. Use '-' to write to stdout.",
    )
    args = parser.parse_args()

    requirements = build_runtime_requirements(Path(args.lockfile))

    if args.output == "-":
        print(requirements, end="")
        return 0

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(requirements, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
