"""Clip Namer
Rename screen recording files with clean timestamps + optional prefix.

Usage:
  python clip_namer.py --dir "C:\\Users\\You\\Videos" --prefix "zoom" --ext .mp4
"""

import argparse
import os
import re
from datetime import datetime


def normalize(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_-]", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dir", required=True, help="Directory of recordings")
    p.add_argument("--prefix", default="recording", help="Filename prefix")
    p.add_argument("--ext", default=".mp4", help="Extension filter (e.g., .mp4)")
    args = p.parse_args()

    folder = os.path.abspath(args.dir)
    prefix = normalize(args.prefix)
    ext = args.ext.lower()

    if not os.path.isdir(folder):
        raise SystemExit(f"Not a directory: {folder}")

    files = [f for f in os.listdir(folder) if f.lower().endswith(ext)]
    files.sort()

    for f in files:
        old = os.path.join(folder, f)
        ts = datetime.fromtimestamp(os.path.getmtime(old)).strftime("%Y%m%d-%H%M%S")
        new_name = f"{prefix}-{ts}{ext}"
        new = os.path.join(folder, new_name)
        if old == new:
            continue
        if os.path.exists(new):
            continue
        os.rename(old, new)
        print(f"Renamed: {f} -> {new_name}")


if __name__ == "__main__":
    main()
