#!/usr/bin/env python3
"""
concatenate_repo.py  –  Dump all text files in the repo into one TXT file.

Usage:
    python concatenate_repo.py           # → writes repo_dump.txt
    python concatenate_repo.py -o all_code.txt
"""

from pathlib import Path
import argparse
import sys

def iter_repo_files(root: Path):
    """Yield every file under *root*, except those in .git/."""
    for path in root.rglob("*"):
        if (
            path.is_file()
            and ".git" not in path.parts     # skip Git internals
        ):
            yield path

def main(repo_root: Path, out_path: Path):
    with out_path.open("w", encoding="utf-8") as out_fp:
        for file_path in sorted(iter_repo_files(repo_root)):
            rel = file_path.relative_to(repo_root)
            try:
                text = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # Binary or non-UTF-8 file—skip it
                print(f"⚠️  Skipping non-text file: {rel}", file=sys.stderr)
                continue

            # Header plus a separator line
            out_fp.write(f"\n\n=== {rel} ===\n")
            out_fp.write(text)

    print(f"✅ Dump written to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concatenate repo files.")
    parser.add_argument("-o", "--out", default="concatenated_repo.txt",
                        help="output txt file (default: repo_dump.txt)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    out_file = Path(args.out).resolve()
    main(repo_root, out_file)
