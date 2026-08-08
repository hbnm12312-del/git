#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch file management tool -- scan, find duplicates, organize.

Commands:
    scan    Report file stats (types, sizes, dates)
    dupes   Find duplicate files by content hash
    sort    Organize files into subdirectories by type or date

Usage:
    python file_organizer.py scan   C:/path/to/dir
    python file_organizer.py dupes  C:/path/to/dir
    python file_organizer.py sort   C:/path/to/dir --by type
    python file_organizer.py sort   C:/path/to/dir --by date --dry-run
"""
import argparse, collections, hashlib, json, os, shutil, sys, time
from datetime import datetime

# ---------------------------------------------------------------------------
# Core: walk a directory tree and collect file metadata
# ---------------------------------------------------------------------------
def walk_files(root_dir, include_hidden=False):
    """Yield (full_path, rel_path, size_bytes, mtime) for every file under root_dir."""
    root = os.path.abspath(root_dir)
    for dirpath, dirnames, filenames in os.walk(root):
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if not include_hidden and fn.startswith("."):
                continue
            fp = os.path.join(dirpath, fn)
            try:
                st = os.stat(fp)
            except OSError:
                continue
            yield fp, os.path.relpath(fp, root), st.st_size, st.st_mtime


def hash_file(fp, algo="md5", chunk_size=65536):
    """Compute hash of a file. Returns None on error."""
    h = hashlib.new(algo)
    try:
        with open(fp, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


# ---------------------------------------------------------------------------
# Command: scan
# ---------------------------------------------------------------------------
def cmd_scan(root_dir, top_n=20):
    """Report file statistics for a directory tree."""
    print(f"Scanning: {os.path.abspath(root_dir)}\n")

    by_ext = collections.Counter()
    by_ext_size = collections.Counter()
    total_size = 0
    total_files = 0
    records = []

    for fp, rp, size, mtime in walk_files(root_dir):
        total_files += 1
        total_size += size
        ext = os.path.splitext(fp)[1].lower() or "(no ext)"
        by_ext[ext] += 1
        by_ext_size[ext] += size
        records.append((size, mtime, rp))

    records.sort(key=lambda x: -x[0])
    largest = records[:top_n]
    records.sort(key=lambda x: -x[1])
    newest = records[:top_n]
    records.sort(key=lambda x: x[1])
    oldest = records[:top_n]

    print(f"{'Total files:':20s} {total_files:,}")
    print(f"{'Total size:':20s} {_fmt_size(total_size)}")
    print(f"{'Avg file size:':20s} {_fmt_size(total_size // max(total_files, 1))}")

    print(f"\n-- By extension --")
    print(f"{'Ext':12s} {'Count':>8s}  {'Size':>12s}")
    print("-" * 36)
    for ext, count in by_ext.most_common(10):
        sz = by_ext_size[ext]
        print(f"{ext:12s} {count:>8,}  {_fmt_size(sz):>12s}")

    print(f"\n-- Largest files --")
    for size, mtime, rp in largest:
        ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        print(f"  {_fmt_size(size):>10s}  {ts}  {rp}")

    print(f"\n-- Newest files --")
    for size, mtime, rp in newest:
        ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        print(f"  {ts}  {_fmt_size(size):>10s}  {rp}")

    print(f"\n-- Oldest files --")
    for size, mtime, rp in oldest:
        ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        print(f"  {ts}  {_fmt_size(size):>10s}  {rp}")


# ---------------------------------------------------------------------------
# Command: dupes
# ---------------------------------------------------------------------------
def cmd_dupes(root_dir, min_size=1):
    """Find duplicate files by content hash."""
    print(f"Finding duplicates in: {os.path.abspath(root_dir)}\n")

    by_size = collections.defaultdict(list)
    total = 0
    for fp, rp, size, mtime in walk_files(root_dir):
        if size < min_size:
            continue
        by_size[size].append((fp, rp))
        total += 1

    dupes = collections.defaultdict(list)
    checked = 0
    for size, files in by_size.items():
        if len(files) < 2:
            continue
        for fp, rp in files:
            h = hash_file(fp)
            if h:
                dupes[(size, h)].append(rp)
            checked += 1

    dupe_groups = [(size, h, paths) for (size, h), paths in dupes.items() if len(paths) > 1]
    dupe_groups.sort(key=lambda x: -x[0])

    wasted = 0
    for size, h, paths in dupe_groups:
        wasted += size * (len(paths) - 1)
        print(f"  [{_fmt_size(size)} x {len(paths)}]  hash={h[:12]}...")
        for p in paths:
            print(f"      {p}")
        print()

    if not dupe_groups:
        print("  No duplicates found.")
    else:
        total_dupes = sum(len(p) - 1 for _, _, p in dupe_groups)
        print(f"{'Duplicates found:':20s} {total_dupes}")
        print(f"{'Wasted space:':20s} {_fmt_size(wasted)}")

    print(f"\n  Files scanned: {total:,}  Hashed: {checked:,}")


# ---------------------------------------------------------------------------
# Command: sort
# ---------------------------------------------------------------------------
def cmd_sort(root_dir, by="type", dry_run=True):
    """Organize files into subdirectories by type (extension) or date (year-month)."""
    root = os.path.abspath(root_dir)
    action = "[DRY RUN] Would move" if dry_run else "Moving"
    print(f"{action} files in: {root}")
    print(f"Organize by: {by}\n")

    moves = []
    for fp, rp, size, mtime in walk_files(root):
        if by == "type":
            ext = os.path.splitext(fp)[1].lower().lstrip(".") or "no_ext"
            subdir = ext
        elif by == "date":
            dt = datetime.fromtimestamp(mtime)
            subdir = dt.strftime("%Y-%m")
        else:
            print(f"Unknown --by value: {by}")
            sys.exit(1)

        dest_dir = os.path.join(root, subdir)
        dest = os.path.join(dest_dir, os.path.basename(fp))

        if os.path.abspath(fp) == os.path.abspath(dest):
            continue

        moves.append((fp, dest, dest_dir, size))

    moves.sort(key=lambda x: (os.path.dirname(x[1]), os.path.basename(x[1])))

    if dry_run:
        by_dir = collections.defaultdict(list)
        for fp, dest, dest_dir, size in moves:
            by_dir[os.path.relpath(dest_dir, root)].append(
                (os.path.basename(fp), size)
            )
        for d in sorted(by_dir):
            total = sum(s for _, s in by_dir[d])
            print(f"  [{d}/]  {len(by_dir[d])} files, {_fmt_size(total)}")
        print(f"\n  Would move {len(moves)} files. Run with --no-dry-run to execute.")
    else:
        for fp, dest, dest_dir, size in moves:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(fp, dest)
            print(f"  {os.path.basename(fp)} -> {os.path.relpath(dest, root)}")
        print(f"\n  Moved {len(moves)} files.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _fmt_size(n):
    if n >= 1_073_741_824:
        return f"{n / 1_073_741_824:.1f} GB"
    if n >= 1_048_576:
        return f"{n / 1_048_576:.1f} MB"
    if n >= 1_024:
        return f"{n / 1_024:.1f} KB"
    return f"{n} B"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Batch file management -- scan, find duplicates, organize."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="Report file statistics")
    p_scan.add_argument("path", help="Directory to scan")
    p_scan.add_argument("--top", type=int, default=20, help="Top N largest/newest/oldest files (default: 20)")

    p_dupes = sub.add_parser("dupes", help="Find duplicate files by content hash")
    p_dupes.add_argument("path", help="Directory to scan")
    p_dupes.add_argument("--min-size", type=int, default=1, help="Skip files smaller than N bytes (default: 1)")

    p_sort = sub.add_parser("sort", help="Organize files into subdirectories")
    p_sort.add_argument("path", help="Directory to organize")
    p_sort.add_argument("--by", choices=["type", "date"], default="type",
                        help="Organize by 'type' (extension) or 'date' (year-month)")
    p_sort.add_argument("--dry-run", action="store_true", default=True,
                        help="Preview without moving (default: on)")
    p_sort.add_argument("--no-dry-run", action="store_false", dest="dry_run",
                        help="Actually move files")

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"ERROR: not a directory: {args.path}")
        sys.exit(1)

    if args.command == "scan":
        cmd_scan(args.path, top_n=args.top)
    elif args.command == "dupes":
        cmd_dupes(args.path, min_size=args.min_size)
    elif args.command == "sort":
        cmd_sort(args.path, by=args.by, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
